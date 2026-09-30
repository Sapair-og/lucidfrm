"""The conversation: one field at a time, through all five stages.

This module is the only place the stages meet, and it is deliberately thin. It
decides what to ask next and what to do with each stage's answer; it makes no
judgements of its own. In particular it never inspects a value to decide whether
it is acceptable -- that is the gate's verdict, and duplicating the reasoning
here would create a second, unaudited validator that could drift out of step
with the first.

The flow per field (implemented as a LangGraph graph in graph.py):

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

from lucidform.channels.base import InputChannel, Kind, OutputChannel
from lucidform.eval.events import Event, EventLog
from lucidform.extract.extractor import Extractor
from lucidform.formstate.state import FormState
from lucidform.gate.gate import ValidationGate
from lucidform.i18n import Strings
from lucidform.models import FieldSpec
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
    # True only when the user said an explicit yes to the final summary.
    approved: bool = False

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
        max_reviews: int = 5,
        helper=None,
    ) -> None:
        # Optional help agent (lucidform.help). Without one, a question is
        # answered with the field's human-authored gloss.
        self.helper = helper
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
        # Bounds the final summary loop, so "change X" cannot go on forever.
        self.max_reviews = max_reviews

    # -- the conversation ----------------------------------------------------

    def run(self) -> SessionResult:
        # The control flow lives in a LangGraph state machine (graph.py); this
        # class keeps the collaborators and the public API every caller uses.
        from lucidform.orchestrate.graph import SessionGraph

        return SessionGraph(self).run()

    def _explain(self, field: FieldSpec, said: str | None = None) -> None:
        if self.helper is not None and said:
            # The answer is spoken and logged -- it goes nowhere near the form.
            answer = self.helper.answer(field, said, self.lang)
            self.log.emit(
                Event.JARGON_EXPLAINED, field_id=field.id, payload=answer.to_payload()
            )
            self.output.say(answer.spoken, kind=Kind.EXPLANATION)
            return
        text = field.explain(self.lang) or field.name(self.lang)
        self.log.emit(
            Event.JARGON_EXPLAINED, field_id=field.id, payload={"text": text}
        )
        self.output.say(text, kind=Kind.EXPLANATION)

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
                "approved": result.approved,
                "blocked_writes": self.state.blocked_writes,
            }
        )
