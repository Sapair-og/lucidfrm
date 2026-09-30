"""Does an identifier survive being spoken and heard?

METHODOLOGY M0.5 asserts that speech recognition degrades badly on alphanumeric
identifiers, and that this degradation is the empirical condition making
deterministic validation and explicit read-back load-bearing rather than
decorative. This module measures it instead of asserting it.

**The round trip.** For each identifier a synthetic persona holds, the probe
renders it the way the read-back renders it -- character by character, digits as
words -- synthesises that to audio, transcribes the audio, decodes the
transcript back to a value, and compares. The decode is the exact inverse of the
read-back's spelling, so the whole loop is deterministic and involves no
language model at all:

    value -> spelled -> audio -> transcript -> value' -> compare, then gate

Two figures come out of it. How often an identifier survives the round trip, and
-- for those that do not -- how often the validation gate rejects the corrupted
result. The second is the one that matters: a recogniser that mangles one PAN in
five is tolerable if every mangled PAN is rejected before the user is asked to
confirm it, and is not tolerable otherwise.

Prose fields are measured alongside as a control. If identifiers and prose
degrade equally then the claim in M0.5 is wrong and should be withdrawn, which
is why the control is here.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field as dc_field
from pathlib import Path
from typing import Sequence

from lucidform.channels.voice import SpeechRecognizer, SpeechSynthesizer, Transcript
from lucidform.eval.personas import Persona
from lucidform.gate.gate import ValidationGate
from lucidform.models import Candidate, FieldSpec, FieldType, Status
from lucidform.orchestrate import readback
from lucidform.schema.loader import FormSchema

# Field types whose value is spelled out in the read-back, and therefore
# decodable from a transcript without a model.
SPELLED = readback.SPELLED_OUT

WORD_TO_DIGIT = {word: digit for digit, word in readback.DIGIT_WORDS.items()}
# Recognisers frequently emit these instead of the digit words, so accepting
# them measures the recogniser's transcription rather than its spelling
# convention. A homophone is not an error the user made.
WORD_TO_DIGIT.update({"oh": "0", "o": "0", "for": "4", "to": "2", "too": "2", "won": "1", "ate": "8"})


def levenshtein(a: str, b: str) -> int:
    """Edit distance. Implemented rather than imported to avoid a dependency
    in a module that is already the heaviest thing in the project."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(
                min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (ca != cb))
            )
        previous = current
    return previous[-1]


def character_error_rate(reference: str, hypothesis: str) -> float:
    """Edit distance normalised by reference length, case- and space-insensitive."""
    ref = re.sub(r"\s+", " ", reference.casefold()).strip()
    hyp = re.sub(r"\s+", " ", hypothesis.casefold()).strip()
    if not ref:
        return 0.0 if not hyp else 1.0
    return round(levenshtein(ref, hyp) / len(ref), 4)


def decode_spelled(transcript: str, field: FieldSpec) -> str:
    """Turn a spelled-out transcript back into a value.

    The exact inverse of `readback.spell`. Tokens that are digit words become
    digits; single characters are taken as themselves; anything else is dropped,
    because a recogniser that inserted a word did not hear a character.
    """
    tokens = re.split(r"[\s.,\-]+", transcript.casefold())
    out: list[str] = []
    for token in tokens:
        if not token:
            continue
        if token in WORD_TO_DIGIT:
            out.append(WORD_TO_DIGIT[token])
        elif len(token) == 1 and token.isalnum():
            out.append(token)
        elif token.isdigit():
            # Some recognisers collapse spoken digits into a numeral run.
            out.append(token)
    value = "".join(out).upper()
    return value if field.type is not FieldType.PHONE else value.lstrip("+")


@dataclass
class ProbeResult:
    persona_id: str
    field_id: str
    category: str
    spoken_text: str
    truth: str
    transcript: str
    decoded: str = ""
    cer: float = 0.0
    survived: bool = False
    gate_status: str = ""
    gate_reason: str = ""
    asr_confidence: float | None = None
    model: str = ""

    @property
    def corrupted(self) -> bool:
        return bool(self.decoded) and not self.survived

    @property
    def caught_by_gate(self) -> bool:
        return self.corrupted and self.gate_status == "reject"


@dataclass
class ProbeSummary:
    results: list[ProbeResult] = dc_field(default_factory=list)

    def _of(self, category: str) -> list[ProbeResult]:
        return [r for r in self.results if r.category == category]

    def mean_cer(self, category: str | None = None) -> float | None:
        rows = self._of(category) if category else self.results
        return round(sum(r.cer for r in rows) / len(rows), 4) if rows else None

    def survival_rate(self, category: str = "identifier") -> float | None:
        rows = [r for r in self._of(category) if r.decoded or r.truth]
        return round(sum(r.survived for r in rows) / len(rows), 4) if rows else None

    @property
    def corrupted(self) -> list[ProbeResult]:
        return [r for r in self.results if r.corrupted]

    @property
    def caught(self) -> list[ProbeResult]:
        return [r for r in self.results if r.caught_by_gate]

    @property
    def escaped_the_gate(self) -> list[ProbeResult]:
        """Corrupted identifiers the gate accepted.

        The set that matters. Every one of these reaches a read-back carrying a
        wrong value that looked valid, and is caught only if the user notices.
        """
        return [r for r in self.corrupted if r.gate_status == "pass"]

    @property
    def gate_catch_rate(self) -> float | None:
        if not self.corrupted:
            return None
        return round(len(self.caught) / len(self.corrupted), 4)


def _category(field: FieldSpec) -> str:
    if field.type in SPELLED:
        return "identifier"
    if field.type is FieldType.DATE:
        return "date"
    if field.type is FieldType.NAME:
        return "name"
    return "prose"


def probe(
    personas: Sequence[Persona],
    schema: FormSchema,
    recognizer: SpeechRecognizer,
    synthesizer: SpeechSynthesizer,
    audio_dir: Path,
    gate: ValidationGate | None = None,
    lang: str = "en",
) -> ProbeSummary:
    """Run the synthesise-recognise round trip over every persona's values."""
    gate = gate or ValidationGate(schema)
    audio_dir = Path(audio_dir)
    audio_dir.mkdir(parents=True, exist_ok=True)
    summary = ProbeSummary()

    for persona in personas:
        for field in schema:
            truth = persona.truth(field.id)
            if not truth:
                continue

            spoken = readback.render_value(truth, field, lang)
            wav = audio_dir / f"{persona.persona_id}_{field.id}.wav"
            synthesizer.synthesize(spoken, wav, lang)
            heard: Transcript = recognizer.transcribe(wav, lang)

            result = ProbeResult(
                persona_id=persona.persona_id,
                field_id=field.id,
                category=_category(field),
                spoken_text=spoken,
                truth=truth,
                transcript=heard.text,
                cer=character_error_rate(spoken, heard.text),
                asr_confidence=heard.confidence,
                model=heard.model,
            )

            if result.category == "identifier":
                result.decoded = decode_spelled(heard.text, field)
                result.survived = result.decoded == truth
                if not result.survived and result.decoded:
                    # Would the gate stop this before the user is asked to
                    # confirm it? Confidence is set high deliberately: the
                    # question is whether the *value* is rejected on its own
                    # merits, not whether a low score would have masked it.
                    report = gate.check(
                        Candidate(
                            field_id=field.id,
                            value=result.decoded,
                            raw_utterance=heard.text,
                            confidence=0.95,
                        ),
                        persona.ground_truth,
                    )
                    result.gate_status = report.status.value
                    result.gate_reason = report.reason.value if report.reason else ""
                elif result.survived:
                    result.gate_status = "pass"
            else:
                result.survived = result.cer == 0.0

            summary.results.append(result)

    return summary


SIMULATED_PREFIXES = ("simulated/", "echo")


def is_simulated(summary: ProbeSummary) -> bool:
    models = {r.model for r in summary.results}
    return bool(models) and all(
        m.startswith(SIMULATED_PREFIXES) for m in models
    )


def report(summary: ProbeSummary) -> str:
    lines = [
        "speech round trip: value -> spelled -> audio -> transcript -> value",
        "",
        f"  utterances            {len(summary.results)}",
    ]
    if summary.results:
        lines.insert(1, f"  recogniser            {sorted({r.model for r in summary.results})[0]}")
    for category in ("identifier", "date", "name", "prose"):
        cer = summary.mean_cer(category)
        if cer is None:
            continue
        rows = [r for r in summary.results if r.category == category]
        exact = sum(r.survived for r in rows)
        lines.append(
            f"  {category:20} CER {cer:.3f}   survived {exact}/{len(rows)}"
        )

    lines += ["", "identifiers specifically"]
    survival = summary.survival_rate("identifier")
    lines.append(
        f"  survived the round trip   "
        + ("n/a" if survival is None else f"{survival * 100:.1f}%")
    )
    lines.append(f"  corrupted                 {len(summary.corrupted)}")
    lines.append(
        f"  of those, gate rejected   {len(summary.caught)}"
        + (
            f"  ({summary.gate_catch_rate * 100:.1f}%)"
            if summary.gate_catch_rate is not None
            else ""
        )
    )
    escaped = summary.escaped_the_gate
    lines.append(
        f"  reached the read-back     {len(escaped)}"
        "   (wrong, but valid -- only the user can catch these)"
    )
    for row in escaped:
        lines.append(f"      {row.persona_id} {row.field_id}: {row.truth} -> {row.decoded}")

    if summary.results:
        prose = summary.mean_cer("prose")
        ident = summary.mean_cer("identifier")
        if prose is not None and ident is not None:
            lines += [
                "",
                "the claim in METHODOLOGY M0.5",
                f"  identifiers degrade {ident:.3f} CER against prose {prose:.3f}",
                "  "
                + (
                    "identifiers are worse, as predicted"
                    if ident > prose
                    else "identifiers are NOT worse -- M0.5 overstates the case "
                    "and should be revised"
                ),
            ]

    if is_simulated(summary):
        lines += [
            "",
            "read this before quoting any of the above",
            "  - THESE ARE NOT MEASUREMENTS. No speech was synthesised and none",
            "    was recognised. The errors were chosen from documented error",
            "    classes and applied on a fixed schedule, so the figures describe",
            "    the simulator and nothing else. The claim in M0.5 is neither",
            "    supported nor refuted by this run.",
            "  - For real figures, install the voice extras and re-run:",
            "        pip install -r requirements-voice.txt",
            "        lucidform asr-probe --real --voice <piper-voice.onnx>",
        ]
    return "\n".join(lines)


def rows(summary: ProbeSummary) -> list[dict]:
    return [asdict(r) for r in summary.results]
