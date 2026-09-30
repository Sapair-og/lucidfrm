"""Answering a user's question about a field, grounded in retrieved passages.

The same pattern as extraction: the model's reply is bounded by a schema, and
a deterministic check runs on it afterwards instead of trusting it. Here the
check is on citations -- every passage the model cites must be one it was
actually shown, and an answer must cite at least one. Anything else (a cited
passage that was never retrieved, no citation, "not answerable", an API error)
falls back to the field's human-authored gloss, with an honest "I'm not sure".

The help agent explains. It has no channel to the form: its output is spoken
to the user and logged, and that is all. A question like "what should I write
here?" still gets an explanation, never a value.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from typing import Protocol

from pydantic import BaseModel, Field

from lucidform.help.index import Hit, HelpIndex
from lucidform.i18n import Strings
from lucidform.models import FieldSpec

LANGUAGE_NAMES = {"en": "simple English", "hi": "simple Hindi (Devanagari script)"}

SYSTEM = """You help people who may have low literacy, or who cannot see the form,
understand a field on an Indian KYC (Know Your Customer) form.

Rules:
- Answer ONLY from the numbered passages you are given. Do not use outside knowledge.
- Cite every passage you relied on by its id in cited_ids.
- If the passages do not answer the question, set answerable to false and leave answer empty.
- Write at most three short sentences, in {language}, in plain everyday words. Explain any
  official term you use.
- Never state, guess, or suggest the person's own value for the field, and never tell them
  what to write. You explain; the person answers.
"""


class HelpReply(BaseModel):
    """The model's entire permitted output."""

    answer: str = Field(default="", description="The explanation, or empty if not answerable.")
    cited_ids: list[str] = Field(
        default_factory=list, description="Ids of the passages the answer is based on."
    )
    answerable: bool = Field(
        description="False if the passages do not contain the answer to the question."
    )


class AnswerClient(Protocol):
    model: str

    def reply(self, system: str, user: str) -> HelpReply: ...


class GeminiAnswerClient:
    def __init__(self, model: str | None = None, sdk=None, sleep=None) -> None:
        from lucidform.config import get_settings

        settings = get_settings()
        self.model = model or settings.help_model
        if sdk is None:
            from lucidform.llm import make_genai_client

            sdk = make_genai_client()
        self._sdk = sdk
        self._sleep = sleep

    def reply(self, system: str, user: str) -> HelpReply:
        from lucidform.llm import json_config, with_retries

        config = json_config(system, HelpReply.model_json_schema())
        response = with_retries(
            lambda: self._sdk.models.generate_content(model=self.model, contents=user, config=config),
            sleep=self._sleep,
        )
        return HelpReply.model_validate_json(response.text or "")


class ScriptedAnswerClient:
    """Returns the replies handed to it; an Exception in the list is raised."""

    model = "scripted"

    def __init__(self, replies: list) -> None:
        self._replies = list(replies)
        self.calls: list[tuple[str, str]] = []

    def reply(self, system: str, user: str) -> HelpReply:
        self.calls.append((system, user))
        item = self._replies.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


@dataclass
class HelpAnswer:
    spoken: str
    source: str  # "rag" or "gloss"
    retrieved_ids: list[str] = dc_field(default_factory=list)
    cited_ids: list[str] = dc_field(default_factory=list)
    cited_labels: list[str] = dc_field(default_factory=list)
    fallback_reason: str | None = None
    model: str = ""

    def to_payload(self) -> dict:
        return {
            "text": self.spoken,
            "source": self.source,
            "retrieved": self.retrieved_ids,
            "cited": self.cited_ids,
            "cited_labels": self.cited_labels,
            "fallback_reason": self.fallback_reason,
            "model": self.model,
        }


def _passages(hits: list[Hit]) -> str:
    return "\n\n".join(f"[{h.chunk_id}] {h.label}\n{h.text}" for h in hits)


class HelpAgent:
    def __init__(self, index: HelpIndex, client: AnswerClient, k: int = 4) -> None:
        self.index = index
        self.client = client
        self.k = k

    def answer(self, field: FieldSpec, question: str, lang: str = "en") -> HelpAnswer:
        strings = Strings(lang)
        # The field's own name anchors a terse question ("ye kya hai?") to the
        # right topic without rewriting what the user asked.
        try:
            hits = self.index.search(f"{question}\n{field.label}", k=self.k)
        except Exception as exc:  # noqa: BLE001 - retrieval is a live API call too
            return self._fallback(field, lang, strings, [], f"error:{type(exc).__name__}")
        retrieved = [h.chunk_id for h in hits]
        user = (
            f"Form field: {field.name(lang)} ({field.label})\n"
            f"What this field is for: {field.explain('en') or field.label}\n"
            f"The person asked: {question}\n\n"
            f"Passages:\n{_passages(hits)}"
        )
        system = SYSTEM.format(language=LANGUAGE_NAMES.get(lang, LANGUAGE_NAMES["en"]))

        try:
            reply = self.client.reply(system, user)
        except Exception as exc:  # noqa: BLE001 - a help failure must not end the session
            return self._fallback(field, lang, strings, retrieved, f"error:{type(exc).__name__}")

        if not reply.answerable or not reply.answer.strip():
            return self._fallback(field, lang, strings, retrieved, "not_answerable")
        if not reply.cited_ids:
            return self._fallback(field, lang, strings, retrieved, "no_citation")
        if not set(reply.cited_ids) <= set(retrieved):
            return self._fallback(field, lang, strings, retrieved, "citation_not_retrieved")

        by_id = {h.chunk_id: h for h in hits}
        cited = list(dict.fromkeys(reply.cited_ids))
        labels = list(dict.fromkeys(by_id[c].label for c in cited))
        spoken = f"{reply.answer.strip()} {strings.say('help_source', sources='; '.join(labels))}"
        return HelpAnswer(
            spoken=spoken,
            source="rag",
            retrieved_ids=retrieved,
            cited_ids=cited,
            cited_labels=labels,
            model=getattr(self.client, "model", ""),
        )

    def _fallback(self, field, lang, strings, retrieved, reason) -> HelpAnswer:
        gloss = field.explain(lang) or field.name(lang)
        return HelpAnswer(
            spoken=f"{strings.get('help_uncertain')} {gloss}",
            source="gloss",
            retrieved_ids=retrieved,
            fallback_reason=reason,
            model=getattr(self.client, "model", ""),
        )


def default_index_dir():
    from lucidform.config import get_settings

    return get_settings().data_dir / "help"


def load_agent(index_dir=None) -> HelpAgent | None:
    """The live help agent, or None if no index has been built yet."""
    from lucidform.help.index import GeminiEmbedder

    index_dir = index_dir or default_index_dir()
    if not (index_dir / "index.npz").exists():
        return None
    index = HelpIndex.load(index_dir, GeminiEmbedder())
    return HelpAgent(index, GeminiAnswerClient())
