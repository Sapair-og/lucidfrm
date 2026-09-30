"""Deterministic checks on the model's output, performed without the model.

The extraction layer is the one place a model's judgement enters the pipeline.
These checks constrain what that judgement is allowed to look like, using
arithmetic and string comparison rather than a second model call -- so they are
reproducible and testable in the same way the validation gate is.

The main one is **grounding**: the model must quote, verbatim, the part of the
user's message the value came from. If that quote does not appear in the
message, the model produced it from somewhere other than the utterance, and the
extraction is not trustworthy regardless of how confident the model claims to
be.

What grounding does and does not establish is worth stating precisely, because
it is easy to overclaim. It proves the extraction is *anchored* to a region of
what the user actually said. It does not prove the value is a correct reading of
that region: a model can quote "seven four seven" honestly and still transcribe
it wrongly. Catching that is the validation gate's job, and then the read-back's.
Grounding closes one specific hole -- a value with no basis in the utterance at
all -- and is not claimed to close more.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from lucidform.extract.schema import Extraction

# Comparison is whitespace- and case-insensitive. A model that reflows spacing
# or changes case is still quoting; one that supplies words the user never said
# is not, and that is the distinction worth enforcing.
_WS = re.compile(r"\s+")


def _loose(text: str) -> str:
    return _WS.sub(" ", (text or "").casefold()).strip()


@dataclass(frozen=True)
class Grounding:
    grounded: bool
    span: tuple[int, int] | None
    detail: str = ""


def locate(quote: str, utterance: str) -> Grounding:
    """Find the quote in the utterance and return its span.

    Spans are reported against the original string so the event log can point
    at the exact characters, which is what an error analysis needs.
    """
    if not quote.strip():
        return Grounding(False, None, "the extractor quoted nothing")

    # Exact match first, so the common case reports an exact span.
    index = utterance.find(quote)
    if index >= 0:
        return Grounding(True, (index, index + len(quote)), "")

    loose_quote = _loose(quote)
    loose_utterance = _loose(utterance)
    if loose_quote and loose_quote in loose_utterance:
        # Whitespace or case differ. Grounded, but the span cannot be mapped
        # back to exact offsets without re-tokenising, so it is reported as
        # unavailable rather than approximated -- a wrong span in the log is
        # worse than none.
        return Grounding(True, None, "quote matched after normalising whitespace")

    return Grounding(
        False,
        None,
        f"the extractor quoted {quote!r}, which does not appear in what the "
        "user said",
    )


def check(extraction: Extraction, utterance: str) -> Grounding:
    """Ground an extraction against the utterance it claims to come from.

    Only value-bearing extractions are grounded. A question or a decline has no
    value and therefore nothing to anchor.
    """
    if not extraction.is_value:
        return Grounding(True, None, "no value to ground")
    return locate(extraction.quote, utterance)


def clamp_confidence(extraction: Extraction, grounding: Grounding) -> float:
    """Confidence the pipeline will actually use.

    The model reports its own confidence, and a model has no privileged access
    to whether it is wrong. Where a deterministic check contradicts it, the
    check wins: an ungrounded extraction is forced to zero regardless of how
    certain the model claims to be, and an extraction the model itself flagged
    as ambiguous is capped below any sensible acceptance threshold.

    This only ever lowers the value. Nothing here can talk confidence up.
    """
    reported = max(0.0, min(1.0, extraction.confidence))
    if not grounding.grounded:
        return 0.0
    if extraction.ambiguous:
        return min(reported, 0.4)
    return reported
