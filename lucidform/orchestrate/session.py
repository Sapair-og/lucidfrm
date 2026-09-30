"""The conversation: one field at a time, through all five stages.

This module is the only place the stages meet, and it is deliberately thin. It
decides what to ask next and what to do with each stage's answer; it makes no
judgements of its own. In particular it never inspects a value to decide whether
it is acceptable -- that is the gate's verdict, and duplicating the reasoning
here would create a second, unaudited validator that could drift out of step
with the first.

The loop per field:

    ask -> listen -> extract -> [question? explain and ask again]
                             -> [decline? record it, or say it is required]
                             -> validate -> [rejected? say why, ask again]
                             -> read back -> listen
                             -> [not confirmed? say so, ask again]
                             -> commit

Two limits keep a session finite. `max_attempts` bounds the number of times a
field is re-asked, so a user stuck on one field is moved on rather than trapped;
the field is recorded as abandoned, never as empty. `max_questions` separately
bounds explanation requests, which do not count as attempts -- asking what a
field means is the system working as intended, not a failure to answer, and
charging it against the retry budget would penalise exactly the users the
project exists for.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field

from lucidform.channels.base import InputChannel, Kind, OutputChannel, Purpose
from lucidform.eval.events import Event, EventLog
from lucidform.extract.extractor import Extractor
from lucidform.formstate.state import FormState
from lucidform.gate.gate import ValidationGate
from lucidform.i18n import Strings
from lucidform.models import FieldSpec, Status
from lucidform.orchestrate import readback
from lucidform.orchestrate.confirm import confirm
from lucidform.schema.loader import FormSchema


@dataclass
class FieldResult:
    field_id: str
    committed: bool = False
    declined: bool = False
    abandoned: bool = False
    attempts: int = 0
    questions: int = 0
    rejections: list[str] = dc_field(default_factory=list)
    corrections: int = 0

    @property
    def resolved(self) -> bool:
        return self.committed or self.declined


@dataclass
class SessionResult:
    session_id: str
    fields: list[FieldResult] = dc_field(default_factory=list)

    @property
    def committed(self) -> list[FieldResult]:
        return [f for f in self.fields if f.committed]

    @property
    def declined(self) -> list[FieldResult]:
        return [f for f in self.fields if f.declined]

    @property
    def abandoned(self) -> list[FieldResult]:
        return [f for f in self.fields if f.abandoned]

    @property
    def complete(self) -> bool:
        return not self.abandoned


class Session:
    def __init__(
        self,
        schema: FormSchema,
        extractor: Extractor,
        gate: ValidationGate,
        state: FormState,
        input_channel: InputChannel,
        output_channel: OutputChannel,
        log: EventLog,
        lang: str = "en",
        max_attempts: int = 3,
        max_questions: int = 2,
    ) -> None:
        self.schema = schema
        self.extractor = extractor
        self.gate = gate
        self.state = state
        self.input = input_channel
        self.output = output_channel
        self.log = log
        self.lang = lang
        self.strings = Strings(lang)
        self.max_attempts = max_attempts
        self.max_questions = max_questions

    # -- the loop ----------------------------------------------------------

    def run(self) -> SessionResult:
        result = SessionResult(session_id=self.log.session_id)
        self.output.say(self.strings.get("greeting"), kind=Kind.PROGRESS)

        for index, field in enumerate(self.schema):
            if self.state.is_resolved(field.id):
                continue
            result.fields.append(self._field(field, index))

        self._close(result)
        return result

    def _field(self, field: FieldSpec, index: int) -> FieldResult:
        outcome = FieldResult(field_id=field.id)

        while outcome.attempts < self.max_attempts and not outcome.resolved:
            self.log.emit(
                Event.FIELD_ASKED,
                field_id=field.id,
                turn_idx=outcome.attempts,
                payload={"attempt": outcome.attempts},
            )
            self.output.say(field.ask(self.lang), kind=Kind.PROMPT)

            said = self.input.listen(field.id, Purpose.VALUE)
            if said is None:
                outcome.abandoned = True
                break
            self.log.emit(
                Event.USER_UTTERANCE,
                field_id=field.id,
                turn_idx=outcome.attempts,
                payload={"text": said, "purpose": Purpose.VALUE.value},
            )

            extraction = self.extractor.extract(field.id, said)

            if extraction.asked_a_question:
                if outcome.questions >= self.max_questions:
                    # Explaining again is not helping. Treat it as an attempt
                    # so the session can move on rather than looping.
                    outcome.attempts += 1
                    continue
                outcome.questions += 1
                self._explain(field)
                continue

            if extraction.declined:
                if field.required:
                    self.output.say(self.strings.get("required"), kind=Kind.PROBLEM)
                    outcome.attempts += 1
                    continue
                self.state.decline(field.id, said=said)
                self.output.say(self.strings.get("declined"), kind=Kind.PROGRESS)
                outcome.declined = True
                break

            if not extraction.has_candidate:
                self.output.say(self.strings.get("not_understood"), kind=Kind.PROBLEM)
                outcome.attempts += 1
                continue

            candidate = extraction.candidate
            report = self.gate.check(candidate, self.state.values)
            self.log.emit(
                Event.VALIDATION,
                field_id=field.id,
                turn_idx=outcome.attempts,
                payload=report,
            )

            if report.status is not Status.PASS:
                outcome.rejections.append(report.reason.value)
                # The gate's own wording reaches the user. It is written to be
                # said aloud, and re-phrasing it here would put a second,
                # untested explanation in front of the person who needs it most.
                self.output.say(
                    self.strings.say("problem", detail=report.detail),
                    kind=Kind.PROBLEM,
                )
                outcome.attempts += 1
                continue

            if self._read_back_and_confirm(field, candidate, report, outcome):
                outcome.committed = True
                break
            outcome.attempts += 1

        if not outcome.resolved and not outcome.abandoned:
            outcome.abandoned = True
            self.output.say(
                self.strings.say("out_of_attempts", label=field.name(self.lang)),
                kind=Kind.PROGRESS,
            )

        return outcome

    def _explain(self, field: FieldSpec) -> None:
        text = field.explain(self.lang) or field.name(self.lang)
        self.log.emit(
            Event.JARGON_EXPLAINED, field_id=field.id, payload={"text": text}
        )
        self.output.say(text, kind=Kind.EXPLANATION)

    def _read_back_and_confirm(self, field, candidate, report, outcome) -> bool:
        value = report.normalized_value
        text = readback.render(value, field, self.strings.get("readback"), self.lang)

        self.log.emit(
            Event.READBACK,
            field_id=field.id,
            turn_idx=outcome.attempts,
            payload={"value": value, "spoken": text},
        )
        self.output.read_back(field.id, value, text)

        said = self.input.listen(field.id, Purpose.CONFIRMATION)
        if said is None:
            outcome.abandoned = True
            return False

        # Logged with the same event type as any other thing the user said, so
        # the metrics can count turns and measure latency without special-casing
        # the confirmation reply. `purpose` is what distinguishes them.
        self.log.emit(
            Event.USER_UTTERANCE,
            field_id=field.id,
            turn_idx=outcome.attempts,
            payload={"text": said, "purpose": Purpose.CONFIRMATION.value},
        )

        affirmation, receipt = confirm(candidate, report, said)
        self.log.emit(
            Event.CONFIRMATION,
            field_id=field.id,
            turn_idx=outcome.attempts,
            payload=affirmation,
        )

        if receipt is None:
            outcome.corrections += 1
            self.log.emit(
                Event.CORRECTION,
                field_id=field.id,
                turn_idx=outcome.attempts,
                payload={"value_rejected": value, "said": said},
            )
            self.output.say(self.strings.get("denied"), kind=Kind.PROBLEM)
            return False

        # The only write in the whole system.
        self.state.commit(candidate, receipt)
        self.output.say(self.strings.get("confirmed"), kind=Kind.PROGRESS)
        return True

    def _close(self, result: SessionResult) -> None:
        declined = len(result.declined)
        note = (
            self.strings.say("declined_note_some", count=declined) if declined else ""
        )
        self.output.say(
            self.strings.say(
                "closing", committed=len(result.committed), declined_note=note
            ),
            kind=Kind.CLOSING,
        )
        if result.abandoned:
            labels = ", ".join(
                self.schema.by_id(f.field_id).name(self.lang) for f in result.abandoned
            )
            self.output.say(
                self.strings.say(
                    "incomplete", count=len(result.abandoned), fields=labels
                ),
                kind=Kind.CLOSING,
            )
        self.log.close(
            {
                "committed": [f.field_id for f in result.committed],
                "declined": [f.field_id for f in result.declined],
                "abandoned": [f.field_id for f in result.abandoned],
                "blocked_writes": self.state.blocked_writes,
            }
        )
