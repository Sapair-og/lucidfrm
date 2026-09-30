"""Provider selection and the Gemini extraction client, offline.

The Gemini client is exercised against a fake SDK object, so these tests pin the
contract -- what is sent, how the reply is parsed, what happens on a rate limit
or a malformed reply -- without a network call. Whether the live model actually
honours the schema is `test_extraction_live.py`'s job.
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from lucidform.config import Settings
from lucidform.extract.client import (
    GeminiExtractionClient,
    ModelReply,
    UnknownProvider,
    make_client,
)
from lucidform.extract.schema import Extraction, Intent

REPLY = {
    "intent": "value",
    "value": "AKQPS3417M",
    "quote": "A K Q P S three four one seven M",
    "confidence": 0.91,
    "ambiguous": False,
    "alternatives": [],
}


class FakeModels:
    def __init__(self, outcomes):
        # Each outcome is either a reply text or an exception to raise.
        self._outcomes = list(outcomes)
        self.calls = []

    def generate_content(self, *, model, contents, config):
        self.calls.append({"model": model, "contents": contents, "config": config})
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return SimpleNamespace(
            text=outcome,
            model_version=model,
            usage_metadata=SimpleNamespace(prompt_token_count=120, candidates_token_count=30),
        )


def fake_sdk(*outcomes):
    return SimpleNamespace(models=FakeModels(outcomes))


def rate_limited():
    from google.genai import errors

    return errors.ClientError(429, {"error": {"code": 429, "message": "quota", "status": "RESOURCE_EXHAUSTED"}})


def client_with(*outcomes, **kw):
    sleeps = []
    client = GeminiExtractionClient(
        model="gemini-test", sdk=fake_sdk(*outcomes), sleep=sleeps.append, **kw
    )
    return client, sleeps


# -- settings ------------------------------------------------------------------


def test_sdk_key_variables_are_read_without_the_project_prefix(monkeypatch):
    # They are the SDKs' own variable names; requiring LUCIDFORM_GEMINI_API_KEY
    # would silently ignore a key the user did set.
    monkeypatch.setenv("GEMINI_API_KEY", "g-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "a-key")
    s = Settings(_env_file=None)
    assert s.gemini_api_key == "g-key"
    assert s.anthropic_api_key == "a-key"


def test_the_default_provider_is_gemini_and_the_model_is_config(monkeypatch):
    monkeypatch.delenv("LUCIDFORM_EXTRACTION_PROVIDER", raising=False)
    monkeypatch.setenv("LUCIDFORM_GEMINI_MODEL", "gemini-other")
    s = Settings(_env_file=None)
    assert s.extraction_provider == "gemini"
    assert s.gemini_model == "gemini-other"


# -- the Gemini client -----------------------------------------------------------


def test_a_reply_is_parsed_into_the_schema():
    client, _ = client_with(json.dumps(REPLY))
    reply = client.complete("system prompt", "user message")

    assert isinstance(reply, ModelReply)
    assert reply.extraction == Extraction.model_validate(REPLY)
    assert reply.extraction.intent is Intent.VALUE
    assert reply.model == "gemini-test"
    assert reply.usage == {"input_tokens": 120, "output_tokens": 30}


def test_the_request_is_schema_constrained_with_the_system_prompt_separate():
    client, _ = client_with(json.dumps(REPLY))
    client.complete("system prompt", "user message")

    call = client._sdk.models.calls[0]
    assert call["model"] == "gemini-test"
    assert call["contents"] == "user message"
    config = call["config"]
    assert config.system_instruction == "system prompt"
    assert config.response_mime_type == "application/json"
    assert config.response_json_schema == Extraction.model_json_schema()


def test_a_rate_limit_is_retried_with_backoff():
    client, sleeps = client_with(rate_limited(), rate_limited(), json.dumps(REPLY))
    reply = client.complete("s", "u")

    assert reply.extraction.value == "AKQPS3417M"
    assert len(client._sdk.models.calls) == 3
    assert sleeps == sorted(sleeps) and len(sleeps) == 2


def test_retries_are_bounded():
    client, _ = client_with(*[rate_limited() for _ in range(10)], max_retries=3)
    with pytest.raises(Exception):
        client.complete("s", "u")
    assert len(client._sdk.models.calls) == 4  # the first try plus three retries


def test_a_non_retryable_error_is_raised_immediately():
    from google.genai import errors

    bad = errors.ClientError(400, {"error": {"code": 400, "message": "bad", "status": "INVALID_ARGUMENT"}})
    client, sleeps = client_with(bad)
    with pytest.raises(errors.ClientError):
        client.complete("s", "u")
    assert sleeps == []


def test_a_reply_outside_the_schema_is_an_error_not_a_fallback():
    # There is no free-text branch: a malformed reply must never be coerced into
    # something that looks like a value.
    for text in ["not json at all", json.dumps({**REPLY, "confidence": 7.0}), json.dumps({"value": "X"})]:
        client, _ = client_with(text)
        with pytest.raises(Exception):
            client.complete("s", "u")


# -- the factory -------------------------------------------------------------------


def test_the_factory_picks_the_configured_provider(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "g-key")
    client = make_client("gemini")
    assert isinstance(client, GeminiExtractionClient)


def test_an_unknown_provider_is_refused():
    with pytest.raises(UnknownProvider):
        make_client("gpt-something")


# -- the shared retry policy -------------------------------------------------------


def test_transport_errors_are_retried():
    import httpx

    from lucidform.llm import with_retries

    calls, sleeps = [], []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise httpx.ReadTimeout("slow")
        return "ok"

    assert with_retries(flaky, sleep=sleeps.append) == "ok"
    assert len(calls) == 3 and len(sleeps) == 2


def test_a_rate_limit_retry_delay_hint_is_honoured():
    from google.genai import errors

    from lucidform.llm import with_retries

    hinted = errors.ClientError(
        429,
        {"error": {"code": 429, "message": "q", "status": "RESOURCE_EXHAUSTED",
                   "details": [{"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "37s"}]}},
    )
    outcomes = [hinted, "ok"]
    sleeps = []

    def call():
        o = outcomes.pop(0)
        if isinstance(o, Exception):
            raise o
        return o

    assert with_retries(call, base_delay=2.0, sleep=sleeps.append) == "ok"
    assert sleeps == [37.0]


def test_a_huge_retry_hint_is_capped():
    from google.genai import errors

    from lucidform.llm import MAX_DELAY_S, with_retries

    hinted = errors.ClientError(
        429, {"error": {"code": 429, "details": [{"@type": "x.RetryInfo", "retryDelay": "3600s"}]}}
    )
    outcomes, sleeps = [hinted, "ok"], []

    def call():
        o = outcomes.pop(0)
        if isinstance(o, Exception):
            raise o
        return o

    with_retries(call, sleep=sleeps.append)
    assert sleeps == [MAX_DELAY_S]
