"""Stage 3: an utterance becomes a candidate.

A candidate is a *proposal*. Nothing here writes, and nothing here decides
whether a value is acceptable -- that is the gate's job, downstream, without a
model. The extractor's whole contribution is turning speech into a typed
proposal and being honest about how sure it is.

Three things happen to the model's reply before it becomes a candidate, all of
them deterministic:

  1. **Intent is separated from value.** A question or a decline never becomes a
     candidate, so "what is a PAN?" cannot be written into the PAN field.
  2. **The quote is grounded** against the utterance. A value the model did not
     take from something the user said is not trusted.
  3. **Confidence is clamped**, never raised. Where a deterministic check
     disagrees with the model's self-report, the check wins.

The result is frozen. Revising a value means minting a new candidate with a new
id, because a receipt is bound to a candidate -- mutating one would silently
decouple it from an authorisation already issued for it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from lucidform.eval.events import Event, EventLog
from lucidform.extract import grounding as ground
from lucidform.extract.client import ExtractionClient, ModelReply
from lucidform.extract.prompt import build
from lucidform.extract.schema import Extraction, Intent
from lucidform.models import Candidate, FieldSpec
from lucidform.schema.loader import FormSchema


@dataclass(frozen=True)
class ExtractionOutcome:
    """Everything stage 3 produced, including the parts that did not become a value."""

    field_id: str
    utterance: str
    intent: Intent
    extraction: Extraction
    grounding: ground.Grounding
    confidence: float
    model: str
    candidate: Candidate | None = None
    usage: Mapping[str, int] | None = None
    # Set when the model call itself failed; the turn is then UNCLEAR.
    error: str | None = None

    @property
    def has_candidate(self) -> bool:
        return self.candidate is not None

    @property
    def asked_a_question(self) -> bool:
        return self.intent is Intent.QUESTION

    @property
    def declined(self) -> bool:
        return self.intent is Intent.DECLINE


class Extractor:
    def __init__(
        self,
        client: ExtractionClient,
        schema: FormSchema,
        lang: str = "en",
        log: EventLog | None = None,
    ) -> None:
        self.client = client
        self.schema = schema
        self.lang = lang
        self._log = log

    def _reply(self, field: FieldSpec, utterance: str) -> ModelReply:
        # The replay client is keyed by field and utterance rather than by
        # prompt text, so that editing the prompt does not invalidate every
        # recorded fixture at once.
        lookup = getattr(self.client, "lookup", None)
        if lookup is not None:
            return lookup(field.id, utterance)
        system, user = build(field, utterance, self.lang)
        return self.client.complete(system, user)

    def extract(self, field_id: str, utterance: str) -> ExtractionOutcome:
        field = self.schema.by_id(field_id)

        if self._log is not None:
            with self._log.timed(Event.EXTRACTION, field_id=field_id) as box:
                outcome = self._extract(field, utterance)
                box.update(
                    {
                        "intent": outcome.intent.value,
                        "value": outcome.extraction.value,
                        "reported_confidence": outcome.extraction.confidence,
                        "confidence": outcome.confidence,
                        "grounded": outcome.grounding.grounded,
                        "grounding_detail": outcome.grounding.detail,
                        "ambiguous": outcome.extraction.ambiguous,
                        "alternatives": outcome.extraction.alternatives,
                        "model": outcome.model,
                        "usage": dict(outcome.usage or {}),
                        "error": outcome.error,
                    }
                )
            return outcome
        return self._extract(field, utterance)

    def _extract(self, field: FieldSpec, utterance: str) -> ExtractionOutcome:
        try:
            reply = self._reply(field, utterance)
        except (KeyError, AssertionError):
            # A replay-corpus miss is a broken fixture and an AssertionError is
            # a test double's over-call check; neither is a model failure, and
            # both must stay loud.
            raise
        except Exception as exc:  # noqa: BLE001 - a failed call costs one attempt, not the session
            # An empty or safety-blocked reply, an off-schema reply, exhausted
            # retries or a dead network all mean the same thing to the user:
            # nothing usable was heard. UNCLEAR routes to "please say that
            # again" and spends one attempt; no candidate can exist.
            failed = Extraction(intent=Intent.UNCLEAR)
            return ExtractionOutcome(
                field_id=field.id,
                utterance=utterance,
                intent=Intent.UNCLEAR,
                extraction=failed,
                grounding=ground.check(failed, utterance),
                confidence=0.0,
                model=getattr(self.client, "model", ""),
                error=f"{type(exc).__name__}: {exc}"[:300],
            )
        extraction = reply.extraction

        grounded = ground.check(extraction, utterance, field.type)
        confidence = ground.clamp_confidence(extraction, grounded)

        candidate: Candidate | None = None
        if extraction.is_value:
            candidate = Candidate(
                field_id=field.id,
                # LF-007: where the model changed the digits the user said, the
                # user's digits are what the gate judges and the user hears.
                value=grounded.replacement or extraction.value,
                raw_utterance=utterance,
                confidence=confidence,
                span=grounded.span,
                # An ungrounded value is treated as ambiguous as well as
                # zero-confidence, so it is rejected by the gate's ambiguity
                # check even if a future threshold change would have let a
                # zero-confidence value through.
                ambiguous=extraction.ambiguous or not grounded.grounded,
            )

        return ExtractionOutcome(
            field_id=field.id,
            utterance=utterance,
            intent=extraction.intent,
            extraction=extraction,
            grounding=grounded,
            confidence=confidence,
            model=reply.model,
            candidate=candidate,
            usage=reply.usage,
        )
