"""Shared plumbing for Gemini calls: retries, and schema-constrained JSON replies.

Kept out of both the extractor and the help agent so neither has its own copy
of the retry policy. Nothing under gate/ or formstate/ may import this module.
"""

from __future__ import annotations

RETRYABLE = frozenset({429, 500, 502, 503, 504})


def with_retries(call, *, max_retries: int = 5, base_delay: float = 2.0, sleep=None):
    """Run `call`, retrying rate limits and transient server errors with backoff.

    A retry re-sends the identical request, so it cannot change what the user
    is later asked to confirm. Anything else is raised at once.
    """
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
            sleep(base_delay * (2**attempt))
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
