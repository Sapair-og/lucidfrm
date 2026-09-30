"""LucidForm command line.

The CLI is also the evaluation driver: every pipeline stage is reachable in
isolation from here, so the validation gate can be exercised without a model, a
session, or a form (SPEC.md section 2, and requirement 3 of the project brief).

Only implemented commands are registered. A stub that prints "not yet" is worse
than a missing command -- it makes an unbuilt stage look built.
"""

from __future__ import annotations

import sys
from pathlib import Path

import typer

from lucidform.config import get_settings

# The Windows console defaults to a legacy code page, which turns Devanagari
# and even an em dash into replacement characters. This is not cosmetic: the
# Hindi prompts and glosses are the product, and a garbled read-back is
# indistinguishable to the user from a wrong one.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

app = typer.Typer(
    add_completion=False,
    help="Accessibility-first form assistant. The LLM never writes a form value.",
    no_args_is_help=True,
)
schema_app = typer.Typer(no_args_is_help=True, help="Inspect the form schema.")
persona_app = typer.Typer(no_args_is_help=True, help="Inspect the synthetic corpus.")
help_app = typer.Typer(no_args_is_help=True, help="The help agent: build, ask, evaluate.")
app.add_typer(schema_app, name="schema")
app.add_typer(persona_app, name="personas")
app.add_typer(help_app, name="help")


@help_app.command("build")
def help_build() -> None:
    """Chunk the official sources and embed them (a few minutes on the free tier)."""
    import time

    from lucidform.help import corpus
    from lucidform.help.answer import default_index_dir
    from lucidform.help.index import GeminiEmbedder, HelpIndex

    out = default_index_dir()
    chunks = corpus.load_chunks(out / "sources")
    typer.echo(f"{len(chunks)} chunks from {len(corpus.load_manifest(out / 'sources'))} sources")
    started = time.perf_counter()
    index = HelpIndex.build(chunks, GeminiEmbedder())
    index.save(out)
    typer.echo(f"embedded in {time.perf_counter() - started:.0f}s -> {out}")


@help_app.command("eval")
def help_eval(
    pause: float = typer.Option(1.0, help="Seconds between questions (free-tier pacing)."),
) -> None:
    """Run the help agent over the 30-question set + 6 controls (live)."""
    from lucidform.help import evaluate
    from lucidform.help.answer import default_index_dir, load_agent
    from lucidform.schema import loader

    settings = get_settings()
    agent = load_agent()
    if agent is None:
        typer.echo("no help index yet. Build it: lucidform help build")
        raise typer.Exit(2)
    items = evaluate.load_set(default_index_dir() / "eval_questions.yaml")
    rows = evaluate.run(agent, loader.load(), items, pause_s=pause)
    summary = evaluate.summarise(rows)
    meta = {"help_model": agent.client.model, "embedder": agent.index.embedder.name, "k": agent.k}
    rows_path, summary_path = evaluate.write(rows, summary, settings.results_dir, meta)

    for r in rows:
        flag = "hit " if r.hit else ("    " if r.kind == "control" else "MISS")
        typer.echo(f"{r.qid} {flag} {r.source:5s} {r.fallback_reason:24s} {r.question[:60]}")
    typer.echo("")
    for key in ("retrieval_hit_at_k", "answer_rate", "gold_citation_rate", "control_refusal_rate",
                "controls_scored", "errors", "latency_ms_p50", "latency_ms_p95"):
        typer.echo(f"  {key:22s} {summary[key]}")
    typer.echo(f"  fallbacks              {summary['fallbacks']}")
    typer.echo(f"\n  {rows_path}\n  {summary_path}")


@help_app.command("ask")
def help_ask(
    field: str = typer.Option(..., "--field", "-f", help="Field id, e.g. pan."),
    question: str = typer.Option(..., "--question", "-q", help="What the user asked."),
    lang: str = typer.Option("en", help="Answer language."),
) -> None:
    """Ask the help agent one question, showing what it retrieved and cited."""
    from lucidform.help.answer import load_agent
    from lucidform.schema import loader

    schema = loader.load()
    if field not in schema.ids:
        typer.echo(f"unknown field {field!r}. Known: {', '.join(schema.ids)}")
        raise typer.Exit(2)
    agent = load_agent()
    if agent is None:
        typer.echo("no help index yet. Build it: lucidform help build")
        raise typer.Exit(2)
    spec = schema.by_id(field)
    answer = agent.answer(spec, question, lang)
    typer.echo("  retrieved")
    for cid in answer.retrieved_ids:
        mark = "*" if cid in answer.cited_ids else " "
        typer.echo(f"   {mark} {agent.index.get(cid).label}")
    typer.echo(f"\n  source   {answer.source}" + (f" ({answer.fallback_reason})" if answer.fallback_reason else ""))
    typer.echo(f"  says     {answer.spoken}")


@app.command("make-form")
def make_form_cmd(
    out: Path = typer.Option(None, help="Output path; defaults to data/forms/."),
) -> None:
    """Generate the target fillable PDF from the schema overlay."""
    from lucidform.schema import make_form

    path = make_form.build(out=out)
    typer.echo(f"wrote {path}")


@app.command("replay")
def replay_cmd(
    personas: list[str] = typer.Option(
        None, "--persona", "-p", help="Persona id. Repeatable. Default: all."
    ),
    replay: bool = typer.Option(
        True,
        "--replay/--live",
        help="Offline corpus (default) or the real model.",
    ),
    lang: str = typer.Option(None, help="Conversation language."),
    repeat: int = typer.Option(1, help="Run each persona this many times."),
    fresh: bool = typer.Option(
        False, "--fresh", help="Delete existing run logs first."
    ),
    extended: bool = typer.Option(
        False, "--extended", help="Also run the live-only extended personas (needs --live)."
    ),
    runs_dir: Path = typer.Option(
        None, "--runs-dir", help="Where to write session logs (keep live and offline apart)."
    ),
) -> None:
    """Run personas through the whole pipeline and record the sessions.

    Offline this verifies pipeline behaviour deterministically. With --live it
    also measures extraction accuracy, which the offline corpus cannot -- see
    METHODOLOGY M4.4.
    """
    from lucidform.eval.personas import load_all
    from lucidform.eval.replay import run_persona
    from lucidform.schema import loader

    settings = get_settings()
    if extended and replay:
        # The extended set has no offline fixtures on purpose: its value is in
        # what a real model does with it.
        typer.echo("--extended personas have no offline corpus; add --live")
        raise typer.Exit(2)
    schema = loader.load()
    client = _extraction_client(replay)
    helper = _help_agent(replay)

    pool = load_all() + (load_all(settings.extended_personas_dir) if extended else [])
    everyone = {p.persona_id: p for p in pool}
    chosen = list(personas) if personas else list(everyone)
    unknown = [p for p in chosen if p not in everyone]
    if unknown:
        typer.echo(f"unknown persona(s): {unknown}. Known: {list(everyone)}")
        raise typer.Exit(2)

    out_dir = Path(runs_dir or settings.runs_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if fresh:
        removed = 0
        for old in out_dir.glob("*.jsonl"):
            old.unlink()
            removed += 1
        typer.echo(f"removed {removed} existing run log(s)")

    escaped_total = 0
    for _ in range(repeat):
        for persona_id in chosen:
            run = run_persona(
                everyone[persona_id], schema, client, runs_dir=out_dir, lang=lang,
                echo=False, helper=helper,
            )
            result = run.result
            escaped = run.escaped_errors
            escaped_total += len(escaped)
            flag = (
                typer.style("  ESCAPED", fg=typer.colors.RED, bold=True)
                if escaped
                else ""
            )
            typer.echo(
                f"{persona_id}  committed {len(result.committed):2d}  "
                f"declined {len(result.declined)}  "
                f"abandoned {len(result.abandoned)}  "
                f"readback-denials {len(run.channel.denials)}{flag}"
            )
            for field_id, truth, got in escaped:
                typer.echo(f"    {field_id}: expected {truth!r}, committed {got!r}")

    typer.echo(f"\nlogs in {out_dir}")
    # --out keeps a live run's tables out of the offline results the paper cites.
    results = settings.results_dir / out_dir.name if runs_dir else settings.results_dir
    typer.echo(f"reduce them with: lucidform metrics --runs {out_dir} --out {results}")
    raise typer.Exit(1 if escaped_total else 0)


@app.command("asr-probe")
def asr_probe_cmd(
    real: bool = typer.Option(
        False,
        "--real",
        help="Use faster-whisper and Piper. Without this, errors are simulated.",
    ),
    voice: Path = typer.Option(None, help="Piper voice model (.onnx). Requires --real."),
    model_size: str = typer.Option("small", help="Whisper model size."),
    error_every: int = typer.Option(
        7, help="Simulator only: corrupt one token in this many."
    ),
    lang: str = typer.Option(None, help="Language to speak and recognise."),
    audio_dir: Path = typer.Option(None, help="Where to write the audio."),
    out: Path = typer.Option(None, help="Write per-utterance rows to this CSV."),
) -> None:
    """Measure whether an identifier survives being spoken and heard.

    Renders each persona's values the way the read-back does, synthesises them,
    transcribes them back, and reports how often the value survives -- and, when
    it does not, whether the gate rejects the result before the user is asked to
    confirm it.

    This is the experiment behind METHODOLOGY M0.5. Without --real the errors are
    simulated and the numbers are not measurements; the report says so.
    """
    import csv as _csv
    import tempfile

    from lucidform.channels.voice import (
        CorruptingRecognizer,
        SilentSynthesizer,
        VoiceBackendMissing,
    )
    from lucidform.eval import asr_probe
    from lucidform.eval.personas import load_all
    from lucidform.gate.gate import ValidationGate
    from lucidform.schema import loader

    settings = get_settings()
    schema = loader.load()
    lang = lang or settings.lang

    if real:
        from lucidform.channels.voice import FasterWhisperRecognizer, PiperSynthesizer

        if voice is None:
            typer.echo("--real needs --voice pointing at a Piper .onnx voice model.")
            typer.echo("See requirements-voice.txt.")
            raise typer.Exit(2)
        try:
            recognizer = FasterWhisperRecognizer(model_size=model_size)
            synthesizer = PiperSynthesizer(voice=voice)
        except VoiceBackendMissing as exc:
            typer.echo(str(exc))
            raise typer.Exit(2)
    else:
        recognizer = CorruptingRecognizer(error_every=error_every)
        synthesizer = SilentSynthesizer()

    audio_dir = Path(audio_dir or tempfile.mkdtemp(prefix="lucidform-probe-"))
    summary = asr_probe.probe(
        load_all(),
        schema,
        recognizer,
        synthesizer,
        audio_dir,
        gate=ValidationGate(schema, min_confidence=settings.min_confidence),
        lang=lang,
    )

    typer.echo("")
    typer.echo(asr_probe.report(summary))
    typer.echo(f"\n  audio in {audio_dir}")

    if out:
        rows = asr_probe.rows(summary)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8", newline="") as fh:
            writer = _csv.DictWriter(fh, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        typer.echo(f"  rows written to {out}")

    # A corrupted identifier the gate accepted reaches a read-back looking
    # valid, and is caught only if the user notices. Worth a non-zero exit.
    raise typer.Exit(1 if summary.escaped_the_gate else 0)


@app.command("metrics")
def metrics_cmd(
    runs: Path = typer.Option(None, help="Directory of session logs."),
    out: Path = typer.Option(None, help="Directory to write CSV tables to."),
    csv_only: bool = typer.Option(False, "--csv-only", help="Suppress the report."),
) -> None:
    """Reduce session logs to CSV tables and print the headline figures."""
    from lucidform.eval import metrics
    from lucidform.schema import loader

    settings = get_settings()
    runs = Path(runs or settings.runs_dir)
    out = Path(out or settings.results_dir)

    sessions = metrics.load_sessions(runs, loader.load())
    if not sessions:
        typer.echo(f"no session logs in {runs}. Record some with: lucidform replay")
        raise typer.Exit(2)

    written = metrics.write_tables(sessions, out)
    agg = metrics.aggregate(sessions)

    if not csv_only:
        typer.echo("")
        typer.echo(metrics.report(agg))
        typer.echo("")
    for name, path in written.items():
        typer.echo(f"  {name:12} {path}")

    # A committed value differing from ground truth is a defect, not a result,
    # so the command fails rather than reporting it as a number.
    raise typer.Exit(1 if agg.escaped_errors else 0)


@app.command("run")
def run_cmd(
    persona: str = typer.Option(
        None,
        "--persona",
        "-p",
        help="Run a synthetic persona instead of prompting. Id or file path.",
    ),
    replay: bool = typer.Option(
        False, "--replay", help="Use the offline fixture corpus instead of the model."
    ),
    lang: str = typer.Option(None, help="Conversation language."),
    export_to: Path = typer.Option(
        None, "--export", help="Write the completed form to this PDF."
    ),
    quiet: bool = typer.Option(False, help="Suppress the transcript (persona runs)."),
    form: str = typer.Option(
        "template",
        "--form",
        help="template: the 14-field research form. official: the real CKYC form (LF-001).",
    ),
) -> None:
    """Fill in the form by conversation.

    With no --persona, prompts you at the terminal. With one, runs a simulated
    user through the whole pipeline headlessly -- the same components either
    way, only the person is different.

        run --persona p02 --replay
    """
    from lucidform.channels.text import ConsoleChannel
    from lucidform.eval.events import EventLog
    from lucidform.extract.extractor import Extractor
    from lucidform.formstate.state import FormState
    from lucidform.gate.gate import ValidationGate
    from lucidform.orchestrate.session import Session
    from lucidform.schema import loader

    settings = get_settings()
    if form not in ("template", "official"):
        typer.echo("--form must be 'template' or 'official'")
        raise typer.Exit(2)
    if form == "official" and persona:
        # Personas and their ground truth are written for the template's fields.
        typer.echo("personas run on the template form only")
        raise typer.Exit(2)
    schema = loader.load_official() if form == "official" else loader.load()
    client = _extraction_client(replay)
    helper = _help_agent(replay)

    if persona:
        from lucidform.eval.personas import load_all, load_persona
        from lucidform.eval.replay import run_persona

        path = Path(persona)
        if path.exists():
            who = load_persona(path)
        else:
            matches = [p for p in load_all() if p.persona_id == persona]
            if not matches:
                available = ", ".join(p.persona_id for p in load_all())
                typer.echo(f"no persona {persona!r}. Available: {available}")
                raise typer.Exit(2)
            who = matches[0]

        run = run_persona(who, schema, client, lang=lang, echo=not quiet, helper=helper)
        state, result = run.state, run.result
        typer.echo(f"\nlog: {run.log_path}")
    else:
        from lucidform.netcheck import email_domain_ok

        log = EventLog(settings.runs_dir, meta={"lang": lang or settings.lang})
        channel = ConsoleChannel()
        state = FormState(log=log)
        session = Session(
            schema=schema,
            extractor=Extractor(client, schema, lang=lang or settings.lang, log=log),
            gate=ValidationGate(
                schema,
                min_confidence=settings.min_confidence,
                # A live user: check that the email domain receives mail
                # (LF-004). Persona replays keep their synthetic domains.
                domain_check=None if replay else email_domain_ok,
            ),
            state=state,
            input_channel=channel,
            output_channel=channel,
            log=log,
            lang=lang or settings.lang,
            helper=helper,
        )
        result = session.run()
        typer.echo(f"\nlog: {log.path}")

    typer.echo(
        f"committed {len(result.committed)} | declined {len(result.declined)} "
        f"| abandoned {len(result.abandoned)} | approved {'yes' if result.approved else 'no'} "
        f"| blocked writes {state.blocked_writes}"
    )

    if persona:
        escaped = run.escaped_errors
        if escaped:
            # A correctness invariant, not a finding. See SPEC.md section 3.
            typer.echo(
                typer.style(
                    f"\nESCAPED ERRORS: {len(escaped)} committed value(s) differ "
                    "from ground truth. This is a defect, not a result.",
                    fg=typer.colors.RED,
                    bold=True,
                )
            )
            for field_id, truth, got in escaped:
                typer.echo(f"  {field_id}: expected {truth!r}, committed {got!r}")
        if run.channel.denials:
            typer.echo("\nread-back caught (nothing downstream could have):")
            for field_id, truth, got in run.channel.denials:
                typer.echo(f"  {field_id}: read back {got!r}, user wanted {truth!r}")

    if export_to:
        from lucidform.formstate.official_writer import export_official
        from lucidform.formstate.writer import export

        # LF-006: an unfinished or unapproved form says so on its face.
        if not result.complete:
            stamp = "INCOMPLETE"
        elif not result.approved:
            stamp = "NOT CONFIRMED BY APPLICANT"
        else:
            stamp = None
        if form == "official":
            written = export_official(state, schema, export_to, stamp=stamp)
        else:
            written = export(state, schema, export_to, stamp=stamp)
        typer.echo(f"\nwrote {written}" + (f"  [stamped {stamp}]" if stamp else ""))

    raise typer.Exit(0 if result.complete else 1)


def _help_agent(replay: bool):
    """The live help agent for question turns, or None to answer from the gloss.

    Offline runs always use the gloss, so replayed sessions stay deterministic
    and the golden transcripts remain comparable across runs.
    """
    if replay:
        return None
    from lucidform.help.answer import load_agent

    try:
        agent = load_agent()
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"help agent unavailable ({exc}); questions will get the field's gloss")
        return None
    if agent is None:
        typer.echo("no help index yet (lucidform help build); questions will get the field's gloss")
    return agent


def _extraction_client(replay: bool):
    """The extraction client, or a clear message about why there isn't one."""
    if replay:
        from lucidform.extract.client import ReplayClient

        fixtures = (
            Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "extractions.json"
        )
        if not fixtures.exists():
            typer.echo("no fixture corpus. Build it: python -m lucidform.eval.fixtures")
            raise typer.Exit(2)
        return ReplayClient(fixtures)

    from lucidform.extract.client import make_client

    try:
        return make_client()
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"could not construct a model client: {exc}")
        typer.echo("Try --replay to run against the offline fixture corpus.")
        raise typer.Exit(2)


@app.command("extract")
def extract_cmd(
    field: str = typer.Option(..., "--field", "-f", help="Field id, e.g. pan."),
    utterance: str = typer.Option(..., "--utterance", "-u", help="What the user said."),
    replay: bool = typer.Option(
        False,
        "--replay",
        help="Use the offline fixture corpus instead of calling the model.",
    ),
    lang: str = typer.Option(None, help="Language of the conversation."),
    gate: bool = typer.Option(
        True, help="Also run the candidate through the validation gate."
    ),
    committed: list[str] = typer.Option(
        None, "--committed", "-c", help="Confirmed value as id=value. Repeatable."
    ),
) -> None:
    """Run the extraction layer on one utterance.

    Shows what the model proposed, what the deterministic checks made of it, and
    what the gate then decided -- the three separately, because the whole point
    of the design is that they are three separate judgements.

        extract -f pan -u "pan kya hota hai" --replay
    """
    from lucidform.extract.extractor import Extractor
    from lucidform.extract.schema import Intent
    from lucidform.schema import loader

    settings = get_settings()
    schema = loader.load()
    if field not in schema.ids:
        typer.echo(f"unknown field {field!r}. Known: {', '.join(schema.ids)}")
        raise typer.Exit(2)

    client = _extraction_client(replay)
    extractor = Extractor(client, schema, lang=lang or settings.lang)
    try:
        outcome = extractor.extract(field, utterance)
    except KeyError as exc:
        typer.echo(f"{exc}")
        raise typer.Exit(2)
    except Exception as exc:  # noqa: BLE001
        # Credentials are resolved at request time, not at construction, so an
        # unauthenticated run gets this far before failing. Say what to do about
        # it rather than surfacing the SDK's message alone.
        message = str(exc)
        lowered = message.casefold()
        if "authentication" in lowered or "api_key" in lowered or "api key" in lowered:
            typer.echo(
                f"no credentials for provider {settings.extraction_provider!r}. Set "
                "GEMINI_API_KEY or ANTHROPIC_API_KEY in .env (and "
                "LUCIDFORM_EXTRACTION_PROVIDER to match), or use --replay to run "
                "against the offline fixture corpus."
            )
        else:
            typer.echo(f"extraction failed: {type(exc).__name__}: {message}")
        raise typer.Exit(2)

    ex = outcome.extraction
    typer.echo(f"\nutterance   {utterance!r}")
    typer.echo(f"model       {outcome.model}")
    typer.echo("\n  what the model proposed")
    typer.echo(f"    intent      {ex.intent.value}")
    typer.echo(f"    value       {ex.value!r}")
    typer.echo(f"    quote       {ex.quote!r}")
    typer.echo(f"    confidence  {ex.confidence:.2f}")
    if ex.ambiguous:
        typer.echo(f"    ambiguous   yes  {ex.alternatives}")

    typer.echo("\n  what the deterministic checks made of it")
    mark = "grounded" if outcome.grounding.grounded else "NOT GROUNDED"
    typer.echo(f"    {mark}{('  ' + outcome.grounding.detail) if outcome.grounding.detail else ''}")
    if outcome.confidence != ex.confidence:
        typer.echo(
            f"    confidence clamped {ex.confidence:.2f} -> {outcome.confidence:.2f}"
        )

    if not outcome.has_candidate:
        reason = {
            Intent.QUESTION: "the user asked what the field means; explain it and ask again",
            Intent.DECLINE: "the user declined this field",
            Intent.FIND: "the user has one but cannot find the number; say how to look it up",
            Intent.UNCLEAR: "nothing usable was heard; ask again",
        }.get(ex.intent, "no value was proposed")
        typer.echo(f"\n  no candidate -- {reason}\n")
        raise typer.Exit(0)

    typer.echo(f"\n  candidate   {outcome.candidate.value!r}  (id {outcome.candidate.candidate_id[:8]})")

    if not gate:
        typer.echo("")
        raise typer.Exit(0)

    from lucidform.gate.gate import ValidationGate
    from lucidform.models import Status

    context: dict[str, str] = {}
    for pair in committed or []:
        key, _, val = pair.partition("=")
        context[key.strip()] = val.strip()

    report = ValidationGate(schema, min_confidence=settings.min_confidence).check(
        outcome.candidate, context
    )
    passed = report.status is Status.PASS
    verdict = typer.style(
        "PASS" if passed else f"REJECT  ({report.reason.value})",
        fg=typer.colors.GREEN if passed else typer.colors.RED,
        bold=True,
    )
    typer.echo(f"\n  what the gate decided\n    {verdict}")
    if report.detail:
        typer.echo(f"    {report.detail}")
    if passed:
        typer.echo(f"    would read back: {report.normalized_value!r}")
    typer.echo("")
    raise typer.Exit(0 if passed else 1)


@app.command("graph")
def graph_cmd(
    out: Path = typer.Option(None, "--out", "-o", help="Write the Mermaid source here."),
) -> None:
    """Print the orchestrator's LangGraph as Mermaid -- the paper's pipeline figure."""
    from lucidform.orchestrate.graph import mermaid

    text = mermaid()
    if out:
        out.write_text(text, encoding="utf-8")
        typer.echo(f"wrote {out}")
    else:
        typer.echo(text)


@app.command("gate-check")
def gate_check(
    field: str = typer.Option(..., "--field", "-f", help="Field id, e.g. pan."),
    value: str = typer.Option(..., "--value", "-v", help="The candidate value."),
    confidence: float = typer.Option(0.95, help="Simulated extraction confidence."),
    ambiguous: bool = typer.Option(False, help="Simulate an ambiguous extraction."),
    committed: list[str] = typer.Option(
        None,
        "--committed",
        "-c",
        help="Already-confirmed value as id=value, for cross-field checks. Repeatable.",
    ),
) -> None:
    """Run the validation gate on a hand-written candidate.

    No model, no session, no form -- the gate is exercised in isolation, which
    is how the safety claim is meant to be inspected (project brief,
    requirement 3).

        gate-check -f pan -v AKQPB3417M -c full_name="Ramesh Kumar Sharma"
    """
    from lucidform.gate.gate import ValidationGate
    from lucidform.models import Candidate, Status
    from lucidform.schema import loader

    settings = get_settings()
    schema = loader.load()
    if field not in schema.ids:
        typer.echo(f"unknown field {field!r}. Known: {', '.join(schema.ids)}")
        raise typer.Exit(2)

    context: dict[str, str] = {}
    for pair in committed or []:
        if "=" not in pair:
            typer.echo(f"--committed expects id=value, got {pair!r}")
            raise typer.Exit(2)
        key, _, val = pair.partition("=")
        context[key.strip()] = val.strip()

    gate = ValidationGate(schema, min_confidence=settings.min_confidence)
    report = gate.check(
        Candidate(
            field_id=field,
            value=value,
            raw_utterance=value,
            confidence=confidence,
            ambiguous=ambiguous,
        ),
        context,
    )

    passed = report.status is Status.PASS
    headline = typer.style(
        "PASS" if passed else f"REJECT  ({report.reason.value})",
        fg=typer.colors.GREEN if passed else typer.colors.RED,
        bold=True,
    )
    typer.echo(f"\n{field} = {value!r}")
    typer.echo(f"  {headline}")
    if report.detail:
        typer.echo(f"  {report.detail}")
    if passed:
        # What would actually be written, which is also what the read-back
        # states -- so the user confirms the stored value, not their phrasing.
        typer.echo(f"  would commit: {report.normalized_value!r}")

    typer.echo("\n  checks run")
    for entry in report.checks:
        mark = "ok  " if entry.passed else "FAIL"
        typer.echo(f"    {mark}  {entry.name:22} {entry.detail}")
    typer.echo("")

    raise typer.Exit(0 if passed else 1)


@schema_app.command("show")
def schema_show(
    lang: str = typer.Option(None, help="Show prompts and glosses in this language."),
) -> None:
    """List every parsed field, its constraints, and its plain-language prompt."""
    from lucidform.schema import loader

    settings = get_settings()
    lang = lang or settings.lang
    schema = loader.load()

    typer.echo(f"{schema.title}  ({schema.form_id} v{schema.version})")
    typer.echo(f"{len(schema)} fields, language: {lang}\n")

    for field in schema:
        flag = "" if field.required else "  (optional)"
        typer.echo(typer.style(f"{field.id}{flag}", bold=True))
        typer.echo(f"  type       {field.type.value}")
        if field.max_length:
            typer.echo(f"  max length {field.max_length}   (from the PDF)")
        if field.enum_values:
            typer.echo(f"  options    {', '.join(field.enum_values)}")
        if field.depends_on:
            typer.echo(f"  validated against  {', '.join(field.depends_on)}")
        typer.echo(f"  asks       {field.ask(lang)}")
        gloss = field.explain(lang)
        if gloss:
            typer.echo(f"  explains   {gloss}")
        typer.echo("")


@persona_app.command("list")
def personas_list() -> None:
    """List the synthetic personas used by the evaluation harness."""
    from lucidform.eval.personas import load_all

    personas = load_all()
    if not personas:
        typer.echo("no personas found")
        raise typer.Exit(1)

    typer.echo("All personas are fabricated. No real personal data is used.\n")
    for p in personas:
        typer.echo(typer.style(f"{p.persona_id}  {p.name}", bold=True))
        typer.echo(f"  language    {p.lang}")
        for key, value in p.profile.items():
            if key != "notes":
                typer.echo(f"  {key:12} {value}")
        typer.echo(f"  fields      {len(p.ground_truth)}")
        typer.echo("")


@persona_app.command("show")
def personas_show(persona_id: str) -> None:
    """Print one persona's ground truth and the utterances it will produce."""
    from lucidform.eval.personas import load_all

    match = [p for p in load_all() if p.persona_id == persona_id]
    if not match:
        typer.echo(f"no persona {persona_id!r}")
        raise typer.Exit(1)
    p = match[0]

    typer.echo(typer.style(f"{p.persona_id}  {p.name}  (synthetic)", bold=True))
    typer.echo(f"\n{p.profile.get('notes', '').strip()}\n")
    for field_id, truth in p.ground_truth.items():
        shown = truth if truth else "(declines this field)"
        typer.echo(typer.style(f"{field_id}", bold=True) + f"  ->  {shown}")
        for i, utterance in enumerate(p.utterances(field_id)):
            label = "says" if i == 0 else "retry"
            typer.echo(f"    {label:5}  {utterance}")
    typer.echo(f"\n  affirms with  {p.affirm}\n  denies with   {p.deny}")


if __name__ == "__main__":  # pragma: no cover
    app()
