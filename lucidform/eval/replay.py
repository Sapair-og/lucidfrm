"""Run a persona through the whole pipeline, headlessly.

This is the driver every reported number comes from. It assembles the real
components -- the real extractor, the real gate, the real confirmation step, the
real write path -- and drives them with a simulated user. Nothing is stubbed
except the person and, offline, the model.

The same driver takes either client. Offline it replays the expected-response
corpus and verifies pipeline behaviour deterministically; with credentials it
calls the model and the extraction figures become measurements. The distinction
matters and is set out in METHODOLOGY M4.4: offline accuracy against the corpus
is perfect by construction and is not a result.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from lucidform.channels.text import PersonaChannel
from lucidform.config import get_settings
from lucidform.eval.events import EventLog
from lucidform.eval.personas import Persona
from lucidform.extract.client import ExtractionClient
from lucidform.extract.extractor import Extractor
from lucidform.formstate.state import FormState
from lucidform.gate.gate import ValidationGate
from lucidform.orchestrate.session import Session, SessionResult
from lucidform.schema.loader import FormSchema


@dataclass
class ReplayRun:
    persona_id: str
    result: SessionResult
    state: FormState
    channel: PersonaChannel
    log_path: Path

    @property
    def escaped_errors(self) -> list[tuple[str, str, str]]:
        """Committed values that differ from ground truth.

        The correctness invariant, not a reported finding: any entry here means
        a value the user did not agree to reached the form, and is a defect to
        be fixed before results are collected (SPEC.md section 3).
        """
        persona = self.channel.persona
        return [
            (field_id, persona.truth(field_id), value)
            for field_id, value in self.state.values.items()
            if value != persona.truth(field_id)
        ]


def run_persona(
    persona: Persona,
    schema: FormSchema,
    client: ExtractionClient,
    runs_dir: Path | None = None,
    lang: str | None = None,
    echo: bool = False,
    max_attempts: int = 3,
    helper=None,
) -> ReplayRun:
    settings = get_settings()
    lang = lang or persona.lang or settings.lang
    runs_dir = Path(runs_dir or settings.runs_dir)

    log = EventLog(
        runs_dir,
        meta={
            "persona_id": persona.persona_id,
            "lang": lang,
            "form_id": schema.form_id,
            "form_version": schema.version,
            "model": getattr(client, "model", "unknown"),
            "min_confidence": settings.min_confidence,
            # Recorded so a results table can never conflate a corpus replay
            # with a live run.
            "client": type(client).__name__,
            "help": "rag" if helper is not None else "gloss",
        },
    )

    channel = PersonaChannel(persona, echo=echo)
    state = FormState(log=log)
    session = Session(
        schema=schema,
        extractor=Extractor(client, schema, lang=lang, log=log),
        gate=ValidationGate(schema, min_confidence=settings.min_confidence),
        state=state,
        input_channel=channel,
        output_channel=channel,
        log=log,
        lang=lang,
        max_attempts=max_attempts,
        helper=helper,
    )

    result = session.run()
    return ReplayRun(
        persona_id=persona.persona_id,
        result=result,
        state=state,
        channel=channel,
        log_path=log.path,
    )
