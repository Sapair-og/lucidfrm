"""Model clients for the extraction layer.

The extractor talks to a small protocol rather than to the SDK directly, so the
same code path runs against the real model, against recorded responses, and
against hand-written ones. That matters for more than convenience: the offline
suite must be able to exercise every branch of the pipeline without credentials
and without network variance, or the evaluation numbers stop being reproducible.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from lucidform.extract.schema import Extraction


@dataclass(frozen=True)
class ModelReply:
    """One model response, plus what it cost."""

    extraction: Extraction
    model: str
    usage: dict[str, int] = field(default_factory=dict)


class ExtractionClient(Protocol):
    """Anything that can turn a prompt into an `Extraction`."""

    def complete(self, system: str, user: str) -> ModelReply: ...


class AnthropicExtractionClient:
    """The real client.

    Uses the SDK's structured-output helper, so the response is parsed and
    validated against the schema before it reaches us. A reply that does not fit
    the schema is an SDK error rather than something the pipeline has to
    interpret -- there is no free-text branch to fall back to, by design.
    """

    def __init__(self, model: str | None = None, max_tokens: int = 4096) -> None:
        import anthropic  # imported here so the package is optional offline

        from lucidform.config import get_settings

        settings = get_settings()
        self.model = model or settings.extraction_model
        self.max_tokens = max_tokens
        self._client = anthropic.Anthropic(
            **({"api_key": settings.anthropic_api_key} if settings.anthropic_api_key else {})
        )

    def complete(self, system: str, user: str) -> ModelReply:
        # `effort` is deliberately not set here. It belongs in `output_config`,
        # which is also where the structured-output helper puts the response
        # format -- so passing our own risks clobbering it. Worth revisiting
        # once there are credentials to verify the combination against; until
        # then the default is the safe choice.
        response = self._client.messages.parse(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
            output_format=Extraction,
        )
        usage = getattr(response, "usage", None)
        return ModelReply(
            extraction=response.parsed_output,
            model=getattr(response, "model", self.model),
            usage={
                "input_tokens": getattr(usage, "input_tokens", 0),
                "output_tokens": getattr(usage, "output_tokens", 0),
            }
            if usage
            else {},
        )


class GeminiExtractionClient:
    """The Gemini client, held to the same contract as the Anthropic one.

    The reply is constrained by the `Extraction` JSON schema and then validated
    by Pydantic here as well: the schema is enforced server-side on a best-effort
    basis, and a reply that slips past it (a confidence of 7, a missing intent)
    must raise rather than be coerced. As with the Anthropic client there is no
    free-text branch to fall back to.

    Rate limits and transient server errors are retried with exponential
    backoff; everything else is raised at once. A retry re-sends the identical
    request, so it cannot change what the user is asked to confirm.
    """

    def __init__(
        self,
        model: str | None = None,
        *,
        sdk=None,
        max_retries: int = 5,
        base_delay: float = 2.0,
        sleep=None,
    ) -> None:
        from lucidform.config import get_settings

        settings = get_settings()
        self.model = model or settings.gemini_model
        self.max_retries = max_retries
        self.base_delay = base_delay
        self._sleep = sleep  # None -> with_retries uses time.sleep
        if sdk is None:
            from lucidform.llm import make_genai_client

            sdk = make_genai_client()
        self._sdk = sdk

    def complete(self, system: str, user: str) -> ModelReply:
        from lucidform.llm import json_config, with_retries

        config = json_config(system, Extraction.model_json_schema())
        response = with_retries(
            lambda: self._sdk.models.generate_content(
                model=self.model, contents=user, config=config
            ),
            max_retries=self.max_retries,
            base_delay=self.base_delay,
            sleep=self._sleep,
        )
        extraction = Extraction.model_validate_json(response.text or "")
        usage = getattr(response, "usage_metadata", None)
        return ModelReply(
            extraction=extraction,
            model=getattr(response, "model_version", None) or self.model,
            usage={
                "input_tokens": getattr(usage, "prompt_token_count", 0) or 0,
                "output_tokens": getattr(usage, "candidates_token_count", 0) or 0,
            }
            if usage
            else {},
        )


class UnknownProvider(ValueError):
    """An extraction provider was named that this build has no client for."""


PROVIDERS = ("gemini", "anthropic")


def make_client(provider: str | None = None) -> ExtractionClient:
    """The live extraction client for `provider`, or for the configured one."""
    from lucidform.config import get_settings

    provider = (provider or get_settings().extraction_provider).casefold()
    if provider == "gemini":
        return GeminiExtractionClient()
    if provider == "anthropic":
        return AnthropicExtractionClient()
    raise UnknownProvider(f"unknown extraction provider {provider!r}; expected one of {PROVIDERS}")


class ScriptedClient:
    """Returns extractions handed to it. For tests that need one exact reply."""

    def __init__(self, replies: list[Extraction], model: str = "scripted") -> None:
        self._replies = list(replies)
        self.model = model
        self.calls: list[tuple[str, str]] = []

    def complete(self, system: str, user: str) -> ModelReply:
        self.calls.append((system, user))
        if not self._replies:
            raise AssertionError("ScriptedClient ran out of replies")
        return ModelReply(extraction=self._replies.pop(0), model=self.model)


class ReplayClient:
    """Replays recorded model responses from disk, keyed by field and utterance.

    Lets the offline suite exercise the real prompt-to-candidate path against
    responses an actual model produced, without a network call. Recorded
    fixtures are checked in, so a change in extraction behaviour shows up as a
    diff rather than as a number that quietly moved.
    """

    def __init__(self, fixtures: Path) -> None:
        self.path = Path(fixtures)
        with self.path.open(encoding="utf-8") as fh:
            raw = json.load(fh)
        self.model = raw.get("model", "replay")
        self._by_key = {
            f"{entry['field_id']}\x1f{entry['utterance']}": entry["extraction"]
            for entry in raw["recordings"]
        }
        self.misses: list[str] = []

    def complete(self, system: str, user: str) -> ModelReply:  # pragma: no cover
        raise NotImplementedError(
            "ReplayClient is keyed by field and utterance; use "
            "Extractor.extract, which calls `lookup` instead."
        )

    def lookup(self, field_id: str, utterance: str) -> ModelReply:
        key = f"{field_id}\x1f{utterance}"
        if key not in self._by_key:
            self.misses.append(key)
            raise KeyError(
                f"no recorded response for {field_id}={utterance!r}. Record one "
                "with: lucidform extract --record"
            )
        return ModelReply(
            extraction=Extraction.model_validate(self._by_key[key]),
            model=self.model,
        )
