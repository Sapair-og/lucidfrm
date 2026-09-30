"""Reduce session event logs to analysable tables.

Reads the append-only JSONL logs and writes CSV. Nothing here re-runs a session,
so the analysis can be revised, corrected, and re-run against logs already
collected -- which is the reason instrumentation and analysis were separated in
the first place (METHODOLOGY M0.7).

**Which measures need ground truth, and which do not.** Accuracy, gate recall,
and the gate's false-positive rate all require knowing what the correct answer
was, so they are computable only for synthetic-persona sessions. Latency,
turns-per-field, the rejection-reason distribution, and the read-back correction
rate need no ground truth and are computable for any session, including a real
user's. Sessions without a persona contribute to the second group and are
excluded from the first rather than being scored against an assumed answer.

**The layered result.** A wrong value can be stopped in three places, and the
interesting number is how the work divides between them:

    proposed wrong  ->  caught by the gate
                    ->  caught by the read-back   (gate could not: value is valid)
                    ->  committed wrong           (must be zero)

The third row is a correctness invariant, not a finding. The second row is the
evidence that the read-back earns its place: those are values no deterministic
check could have rejected, because nothing about them is malformed.
"""

from __future__ import annotations

import csv
import statistics
import textwrap
from dataclasses import asdict, dataclass, field as dc_field
from pathlib import Path
from typing import Any, Iterable, Sequence

from lucidform.eval.events import Event, read_log
from lucidform.eval.personas import Persona, load_all
from lucidform.gate import rules
from lucidform.schema.loader import FormSchema


def percentile(values: Sequence[float], p: float) -> float | None:
    """Nearest-rank percentile.

    Deliberately not interpolated: with the sample sizes a prototype produces,
    an interpolated percentile reports a latency no request actually had.
    """
    if not values:
        return None
    ordered = sorted(values)
    rank = max(1, min(len(ordered), int(round(p / 100 * len(ordered) + 0.5))))
    return round(ordered[rank - 1], 3)


@dataclass
class Turn:
    """One ask -> answer cycle for one field."""

    session_id: str
    persona_id: str
    field_id: str
    turn: int
    intent: str = ""
    extracted_value: str = ""
    reported_confidence: float | None = None
    confidence: float | None = None
    grounded: bool | None = None
    ambiguous: bool | None = None
    validation_status: str = ""
    validation_reason: str = ""
    normalized_value: str = ""
    readback_value: str = ""
    confirmed: bool | None = None
    confirmation_basis: str = ""
    committed: bool = False
    committed_value: str = ""
    extraction_ms: float | None = None
    # Ground-truth-dependent. None where the session has no persona.
    proposal_correct: bool | None = None

    @property
    def proposed_a_value(self) -> bool:
        return self.intent == "value" and bool(self.extracted_value)


@dataclass
class FieldOutcome:
    session_id: str
    persona_id: str
    field_id: str
    turns: int = 0
    questions: int = 0
    rejections: list[str] = dc_field(default_factory=list)
    corrections: int = 0
    committed_value: str = ""
    ground_truth: str = ""
    resolution: str = "abandoned"  # committed | declined | abandoned
    correct: bool | None = None


@dataclass
class SessionMetrics:
    session_id: str
    persona_id: str
    lang: str
    model: str
    client: str
    turns: list[Turn] = dc_field(default_factory=list)
    fields: list[FieldOutcome] = dc_field(default_factory=list)
    blocked_writes: int = 0

    @property
    def has_ground_truth(self) -> bool:
        return bool(self.persona_id)


def _personas() -> dict[str, Persona]:
    return {p.persona_id: p for p in load_all()}


def _truth(persona: Persona | None, field_id: str) -> str:
    return persona.truth(field_id) if persona else ""


def parse_session(
    path: Path,
    schema: FormSchema,
    personas: dict[str, Persona] | None = None,
) -> SessionMetrics:
    """Turn one log file into per-turn and per-field records.

    Turns are delimited by the ask, not by the logged turn index: an
    explanation request does not advance that index, so grouping on it would
    merge a question and the answer that followed into one record.
    """
    personas = personas if personas is not None else _personas()
    records = read_log(path)
    start = next(r for r in records if r["event"] == Event.SESSION_START.value)
    meta = start.get("payload") or {}
    persona_id = meta.get("persona_id", "")
    persona = personas.get(persona_id)

    session = SessionMetrics(
        session_id=start["session_id"],
        persona_id=persona_id,
        lang=meta.get("lang", ""),
        model=meta.get("model", ""),
        client=meta.get("client", ""),
    )

    turn: Turn | None = None
    per_field: dict[str, FieldOutcome] = {}
    counters: dict[str, int] = {}

    def outcome(field_id: str) -> FieldOutcome:
        if field_id not in per_field:
            per_field[field_id] = FieldOutcome(
                session_id=session.session_id,
                persona_id=persona_id,
                field_id=field_id,
                ground_truth=_truth(persona, field_id),
            )
        return per_field[field_id]

    def close_turn() -> None:
        nonlocal turn
        if turn is not None:
            session.turns.append(turn)
            turn = None

    for record in records:
        event = record["event"]
        field_id = record.get("field_id") or ""
        payload = record.get("payload") or {}

        if event == Event.FIELD_ASKED.value:
            close_turn()
            index = counters.get(field_id, 0)
            counters[field_id] = index + 1
            turn = Turn(
                session_id=session.session_id,
                persona_id=persona_id,
                field_id=field_id,
                turn=index,
            )
            outcome(field_id).turns += 1

        elif turn is None:
            continue

        elif event == Event.EXTRACTION.value:
            turn.intent = payload.get("intent", "")
            turn.extracted_value = payload.get("value", "")
            turn.reported_confidence = payload.get("reported_confidence")
            turn.confidence = payload.get("confidence")
            turn.grounded = payload.get("grounded")
            turn.ambiguous = payload.get("ambiguous")
            turn.extraction_ms = record.get("latency_ms")
            if turn.intent == "question":
                outcome(field_id).questions += 1
            if persona and turn.proposed_a_value:
                turn.proposal_correct = _is_correct(
                    turn.extracted_value, field_id, persona, schema
                )

        elif event == Event.VALIDATION.value:
            turn.validation_status = payload.get("status", "")
            turn.validation_reason = payload.get("reason") or ""
            turn.normalized_value = payload.get("normalized_value", "")
            if turn.validation_status == "reject":
                outcome(field_id).rejections.append(turn.validation_reason)

        elif event == Event.READBACK.value:
            turn.readback_value = payload.get("value", "")

        elif event == Event.CONFIRMATION.value:
            turn.confirmed = payload.get("explicit")
            turn.confirmation_basis = payload.get("basis", "")

        elif event == Event.CORRECTION.value and "value_rejected" in payload:
            outcome(field_id).corrections += 1

        elif event == Event.COMMIT.value:
            turn.committed = True
            turn.committed_value = payload.get("value", "")
            entry = outcome(field_id)
            entry.committed_value = payload.get("value", "")
            entry.resolution = "committed"

        elif event == Event.SESSION_END.value:
            close_turn()
            session.blocked_writes = payload.get("blocked_writes", 0)
            for declined in payload.get("declined", []):
                outcome(declined).resolution = "declined"
            for abandoned in payload.get("abandoned", []):
                outcome(abandoned).resolution = "abandoned"

    close_turn()

    for entry in per_field.values():
        if persona and entry.resolution == "committed":
            entry.correct = entry.committed_value == entry.ground_truth
        elif persona and entry.resolution == "declined":
            entry.correct = entry.ground_truth == ""
    session.fields = [per_field[f.id] for f in schema if f.id in per_field]
    return session


def _is_correct(
    value: str, field_id: str, persona: Persona, schema: FormSchema
) -> bool:
    """Is this proposed value the right answer?

    Compared after normalisation, using the same rules the gate applies, so
    "+91 98123 45607" and "9812345607" count as the same answer. Judging a
    proposal on its punctuation would overstate the error rate.
    """
    try:
        spec = schema.by_id(field_id)
    except KeyError:
        return False
    return rules.normalize(value, spec) == rules.normalize(
        persona.truth(field_id), spec
    )


# -- aggregation -------------------------------------------------------------


@dataclass
class Aggregate:
    sessions: int = 0
    scored_sessions: int = 0
    fields_committed: int = 0
    fields_declined: int = 0
    fields_abandoned: int = 0

    proposals: int = 0
    proposals_correct: int = 0
    proposals_wrong: int = 0

    gate_rejected_wrong: int = 0
    gate_rejected_correct: int = 0
    gate_passed_wrong: int = 0
    gate_passed_correct: int = 0

    readbacks: int = 0
    readbacks_denied: int = 0
    readback_caught_wrong: int = 0

    escaped_errors: int = 0
    blocked_writes: int = 0
    # Commits whose value disagrees with the validation verdict in the same
    # turn. Unreachable through the pipeline -- the write path derives the
    # value from the report -- so a non-zero count means the log was altered
    # after the fact or the write path has a defect. Either way every figure
    # below it is untrustworthy, which is why it is checked rather than assumed.
    log_inconsistencies: int = 0

    turns_to_commit: list[int] = dc_field(default_factory=list)
    extraction_latencies: list[float] = dc_field(default_factory=list)
    rejection_reasons: dict[str, int] = dc_field(default_factory=dict)

    # Which client produced these sessions. Decides which figures are results
    # and which are only checks -- see `caveats`.
    clients: dict[str, int] = dc_field(default_factory=dict)

    @property
    def offline_only(self) -> bool:
        """True if no session called a real model."""
        return bool(self.clients) and set(self.clients) <= {"ReplayClient", "ScriptedClient"}

    def caveats(self) -> list[str]:
        """Figures that must not be read as results, given how they were produced.

        Printed with the table rather than left to a footnote, because a number
        detached from its provenance is exactly how a circular result ends up in
        a paper.
        """
        notes: list[str] = []
        if self.log_inconsistencies:
            notes.append(
                f"{self.log_inconsistencies} commit(s) disagree with the "
                "validation verdict recorded in the same turn. This cannot "
                "happen through the pipeline, so the logs have been altered or "
                "the write path is defective. Do not quote anything above."
            )
        if self.offline_only:
            notes.append(
                "Extraction accuracy is NOT a result here. These sessions "
                "replayed the offline corpus, whose expected values were "
                "derived from the same ground truth the accuracy is scored "
                "against, so the figure is an artefact of construction. Re-run "
                "with --live to measure it (METHODOLOGY M4.4)."
            )
            notes.append(
                "Latency is NOT a result here. No model was called, so these "
                "are dictionary-lookup times, not inference times."
            )
        if self.scored_sessions < self.sessions:
            notes.append(
                f"{self.sessions - self.scored_sessions} session(s) had no "
                "persona and are excluded from accuracy, recall, and "
                "false-positive figures; they still contribute latency, turns, "
                "and rejection reasons."
            )
        if self.proposals_wrong and self.proposals_wrong < 10:
            notes.append(
                f"Gate recall is computed over only {self.proposals_wrong} "
                "wrong proposals. Too few to quote as a rate -- report the "
                "counts."
            )
        return notes

    # -- derived ------------------------------------------------------------

    @property
    def extraction_accuracy(self) -> float | None:
        if not self.proposals:
            return None
        return round(self.proposals_correct / self.proposals, 4)

    @property
    def gate_recall(self) -> float | None:
        """Of the wrong values proposed, how many did the gate reject?"""
        total = self.gate_rejected_wrong + self.gate_passed_wrong
        return round(self.gate_rejected_wrong / total, 4) if total else None

    @property
    def gate_false_positive_rate(self) -> float | None:
        """Of the correct values proposed, how many did the gate wrongly reject?

        The measure that separates a discriminating gate from an obstructive
        one, and the one most often omitted. Reporting recall without it is not
        a result: a gate that rejects everything scores perfect recall.
        """
        total = self.gate_rejected_correct + self.gate_passed_correct
        return round(self.gate_rejected_correct / total, 4) if total else None

    @property
    def gate_precision(self) -> float | None:
        total = self.gate_rejected_wrong + self.gate_rejected_correct
        return round(self.gate_rejected_wrong / total, 4) if total else None

    @property
    def readback_correction_rate(self) -> float | None:
        if not self.readbacks:
            return None
        return round(self.readbacks_denied / self.readbacks, 4)

    @property
    def mean_turns_to_commit(self) -> float | None:
        if not self.turns_to_commit:
            return None
        return round(statistics.mean(self.turns_to_commit), 3)

    def as_row(self) -> dict[str, Any]:
        return {
            "sessions": self.sessions,
            "scored_sessions": self.scored_sessions,
            "fields_committed": self.fields_committed,
            "fields_declined": self.fields_declined,
            "fields_abandoned": self.fields_abandoned,
            "proposals": self.proposals,
            "extraction_accuracy": self.extraction_accuracy,
            "gate_recall": self.gate_recall,
            "gate_false_positive_rate": self.gate_false_positive_rate,
            "gate_precision": self.gate_precision,
            "readback_correction_rate": self.readback_correction_rate,
            "readback_caught_wrong": self.readback_caught_wrong,
            "escaped_errors": self.escaped_errors,
            "blocked_writes": self.blocked_writes,
            "log_inconsistencies": self.log_inconsistencies,
            "mean_turns_to_commit": self.mean_turns_to_commit,
            "extraction_ms_p50": percentile(self.extraction_latencies, 50),
            "extraction_ms_p95": percentile(self.extraction_latencies, 95),
            "clients": "|".join(sorted(self.clients)),
            # So a row lifted out of the CSV into a paper still carries the
            # warning that two of its columns are not measurements.
            "offline_only": self.offline_only,
        }


def aggregate(sessions: Iterable[SessionMetrics]) -> Aggregate:
    agg = Aggregate()

    for session in sessions:
        agg.sessions += 1
        agg.blocked_writes += session.blocked_writes
        client = session.client or "unknown"
        agg.clients[client] = agg.clients.get(client, 0) + 1
        scored = session.has_ground_truth
        if scored:
            agg.scored_sessions += 1

        for turn in session.turns:
            if turn.extraction_ms is not None:
                agg.extraction_latencies.append(turn.extraction_ms)
            if turn.validation_reason:
                agg.rejection_reasons[turn.validation_reason] = (
                    agg.rejection_reasons.get(turn.validation_reason, 0) + 1
                )
            if turn.readback_value:
                agg.readbacks += 1
                if turn.confirmed is False:
                    agg.readbacks_denied += 1
            # The write path derives the committed value from the validation
            # report, so these must agree. If they do not, the record is not a
            # faithful account of what happened.
            if turn.committed and turn.committed_value != turn.normalized_value:
                agg.log_inconsistencies += 1

            if not (scored and turn.proposed_a_value):
                continue

            agg.proposals += 1
            correct = bool(turn.proposal_correct)
            agg.proposals_correct += correct
            agg.proposals_wrong += not correct

            rejected = turn.validation_status == "reject"
            if correct and rejected:
                agg.gate_rejected_correct += 1
            elif correct:
                agg.gate_passed_correct += 1
            elif rejected:
                agg.gate_rejected_wrong += 1
            else:
                agg.gate_passed_wrong += 1
                # A wrong value the gate could not reject. If the read-back
                # denied it, that is the read-back doing work nothing else
                # could have done.
                if turn.confirmed is False:
                    agg.readback_caught_wrong += 1

        for entry in session.fields:
            if entry.resolution == "committed":
                agg.fields_committed += 1
                agg.turns_to_commit.append(entry.turns)
                if scored and entry.correct is False:
                    agg.escaped_errors += 1
            elif entry.resolution == "declined":
                agg.fields_declined += 1
            else:
                agg.fields_abandoned += 1

    return agg


# -- output ------------------------------------------------------------------


def _write_csv(path: Path, rows: Sequence[dict[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_tables(
    sessions: Sequence[SessionMetrics], out_dir: Path
) -> dict[str, Path]:
    out_dir = Path(out_dir)
    turns = [asdict(t) for s in sessions for t in s.turns]
    fields = [
        {**asdict(f), "rejections": "|".join(f.rejections)}
        for s in sessions
        for f in s.fields
    ]
    per_session = [
        {
            "session_id": s.session_id,
            "persona_id": s.persona_id,
            "lang": s.lang,
            "model": s.model,
            "client": s.client,
            "turns": len(s.turns),
            "committed": sum(f.resolution == "committed" for f in s.fields),
            "declined": sum(f.resolution == "declined" for f in s.fields),
            "abandoned": sum(f.resolution == "abandoned" for f in s.fields),
            "escaped_errors": sum(f.correct is False for f in s.fields),
            "blocked_writes": s.blocked_writes,
        }
        for s in sessions
    ]
    agg = aggregate(sessions)
    reasons = [
        {"reason": reason, "count": count}
        for reason, count in sorted(
            agg.rejection_reasons.items(), key=lambda kv: -kv[1]
        )
    ]

    return {
        "turns": _write_csv(out_dir / "turns.csv", turns),
        "fields": _write_csv(out_dir / "fields.csv", fields),
        "sessions": _write_csv(out_dir / "sessions.csv", per_session),
        "summary": _write_csv(out_dir / "summary.csv", [agg.as_row()]),
        "rejections": _write_csv(out_dir / "rejection_reasons.csv", reasons),
    }


def load_sessions(
    runs_dir: Path, schema: FormSchema
) -> list[SessionMetrics]:
    personas = _personas()
    return [
        parse_session(path, schema, personas)
        for path in sorted(Path(runs_dir).glob("*.jsonl"))
    ]


def _pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:.1f}%"


def report(agg: Aggregate) -> str:
    """The headline table, formatted for a terminal."""
    lines = [
        f"sessions              {agg.sessions}"
        + (f"  ({agg.scored_sessions} with ground truth)" if agg.sessions else ""),
        f"fields                {agg.fields_committed} committed, "
        f"{agg.fields_declined} declined, {agg.fields_abandoned} abandoned",
        "",
        "where wrong values were stopped",
    ]
    if agg.proposals_wrong:
        lines += [
            f"  proposed wrong      {agg.proposals_wrong}",
            f"  caught by the gate  {agg.gate_rejected_wrong}",
            f"  caught by read-back {agg.readback_caught_wrong}"
            "   (gate could not: the value was valid)",
            f"  committed wrong     {agg.escaped_errors}"
            + ("   <-- INVARIANT VIOLATED" if agg.escaped_errors else "   (invariant: must be 0)"),
        ]
    else:
        lines.append("  no wrong values were proposed in these sessions")

    lines += [
        "",
        "validation gate",
        f"  recall              {_pct(agg.gate_recall)}"
        "   of wrong values, how many it rejected",
        f"  false positives     {_pct(agg.gate_false_positive_rate)}"
        "   of correct values, how many it wrongly rejected",
        f"  precision           {_pct(agg.gate_precision)}",
        "",
        "read-back",
        f"  correction rate     {_pct(agg.readback_correction_rate)}"
        f"   ({agg.readbacks_denied} of {agg.readbacks} read-backs denied)",
        "",
        "extraction",
        f"  accuracy            {_pct(agg.extraction_accuracy)}"
        f"   over {agg.proposals} proposals",
        f"  latency p50 / p95   {percentile(agg.extraction_latencies, 50)} ms"
        f" / {percentile(agg.extraction_latencies, 95)} ms",
        "",
        "effort",
        f"  turns per committed field   {agg.mean_turns_to_commit}",
        f"  blocked writes              {agg.blocked_writes}"
        "   (a defect upstream if non-zero)",
        f"  log inconsistencies         {agg.log_inconsistencies}"
        "   (must be 0 or nothing above is trustworthy)",
    ]

    if agg.rejection_reasons:
        lines += ["", "rejections by reason"]
        for reason, count in sorted(agg.rejection_reasons.items(), key=lambda kv: -kv[1]):
            lines.append(f"  {reason:22} {count}")

    caveats = agg.caveats()
    if caveats:
        lines += ["", "read this before quoting any of the above"]
        for note in caveats:
            lines.append(
                textwrap.fill(
                    note, width=74, initial_indent="  - ", subsequent_indent="    "
                )
            )
    return "\n".join(lines)
