"""Shared plumbing for Gemini calls: the client, retries, schema-constrained JSON.

Kept out of both the extractor and the help agent so neither has its own copy
of the credential lookup or the retry policy. Nothing under gate/ or formstate/
may import this module.
"""

from __future__ import annotations

import re

RETRYABLE = frozenset({429, 500, 502, 503, 504})
# A server's own retry hint is honoured, but never beyond this: a user is
# waiting on the other end of every call.
MAX_DELAY_S = 60.0


def make_genai_client():
    """The one place credentials for Gemini are resolved."""
    from google import genai

    from lucidform.config import get_settings

    key = get_settings().gemini_api_key
    return genai.Client(**({"api_key": key} if key else {}))


def _hinted_delay(exc) -> float | None:
    """Seconds from a google.rpc.RetryInfo detail on a 429, if the server sent one."""
    details = getattr(exc, "details", None) or {}
    for d in (details.get("error", {}) or {}).get("details", []) or []:
        if str(d.get("@type", "")).endswith("RetryInfo"):
            m = re.match(r"^\s*([0-9.]+)s\s*$", str(d.get("retryDelay", "")))
            if m:
                return float(m.group(1))
    return None


def with_retries(call, *, max_retries: int = 5, base_delay: float = 2.0, sleep=None):
    """Run `call`, retrying rate limits, transient server errors and transport failures.

    Backoff is exponential, or the server's RetryInfo hint when it gives one,
    capped at MAX_DELAY_S. A retry re-sends the identical request, so it cannot
    change what the user is later asked to confirm. Anything else is raised.
    """
    import httpx
    from google.genai import errors

    if sleep is None:
        import time

        sleep = time.sleep
    attempt = 0
    while True:
        try:
            return call()
        except errors.APIError as exc:
            if exc.code not in RETRYABLE or attempt >= max_retries:
                raise
            delay = _hinted_delay(exc) or base_delay * (2**attempt)
        except httpx.TransportError:
            # Timeouts, refused or dropped connections: the request may never
            # have arrived, so sending it again is safe.
            if attempt >= max_retries:
                raise
            delay = base_delay * (2**attempt)
        sleep(min(delay, MAX_DELAY_S))
        attempt += 1


def json_config(system: str, schema: dict):
    from google.genai import types

    return types.GenerateContentConfig(
        system_instruction=system,
        response_mime_type="application/json",
        response_json_schema=schema,
        # No tools are declared anywhere; leaving AFC on only buys an SDK
        # warning and a code path that could call something.
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )
