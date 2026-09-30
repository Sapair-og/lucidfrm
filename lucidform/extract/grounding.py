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
from lucidform.models import FieldType

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
    # Set when the model's value disagreed with the digits the user said, for a
    # field made only of digits: the pipeline uses the user's digits instead,
    # so the gate judges what was said rather than what the model wrote.
    replacement: str | None = None


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


# -- digit consistency (ISSUES.md LF-007) -----------------------------------
#
# A quote can be honest while the value is not: the user said thirteen nines,
# the model quoted all thirteen, and returned twelve. For identifier fields the
# digits are the whole value, so the digits in the value must be exactly the
# digits in the quote. Number words are read one digit per word; anything that
# is not a single-digit word ("twenty", "hundred") makes the quote unreadable
# as a digit string, and the check declines to run rather than guess.

_DIGIT_WORDS = {
    "zero": "0", "shunya": "0", "shoonya": "0", "sunya": "0", "sifar": "0",
    "one": "1", "ek": "1",
    "two": "2", "do": "2", "doh": "2",
    "three": "3", "teen": "3", "tin": "3",
    "four": "4", "char": "4", "chaar": "4",
    "five": "5", "paanch": "5", "panch": "5", "pach": "5",
    "six": "6", "chhe": "6", "chhah": "6", "chah": "6", "che": "6", "chheh": "6", "cheh": "6",
    "seven": "7", "saat": "7", "sat": "7",
    "eight": "8", "aath": "8", "ath": "8", "aat": "8",
    "nine": "9", "nau": "9", "nao": "9",
}
# "oh" is a zero only where letters cannot occur; in a PAN it may be the letter O.
_ZERO_LETTER_WORDS = {"oh": "0", "o": "0"}
_REPEAT = {"double": 2, "triple": 3}
# Words that denote a multi-digit number. A quote containing one cannot be read
# digit by digit, so the check is skipped rather than risk a false reject.
_COMPOUND = re.compile(
    r"^(ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|"
    r"nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"
    r"thousand|lakh|lac|crore|das|bees|sau|hazaar|hazar)$"
)
_TOKEN = re.compile(r"[0-9]+|[a-z]+")

DIGIT_FIELDS = {FieldType.AADHAAR, FieldType.PHONE, FieldType.PIN, FieldType.PAN}
_PHONE_PREFIXES = ("0091", "91", "0")


def spoken_digits(text: str, *, letters_possible: bool) -> str | None:
    """The digit string a quote spells out, or None if it cannot be read that way."""
    words = dict(_DIGIT_WORDS)
    if not letters_possible:
        words.update(_ZERO_LETTER_WORDS)
    out: list[str] = []
    repeat = 1
    for token in _TOKEN.findall((text or "").casefold()):
        if token.isdigit():
            out.append(token[0] * repeat + token[1:])
            repeat = 1
        elif token in _REPEAT:
            repeat = _REPEAT[token]
        elif token in words:
            out.append(words[token] * repeat)
            repeat = 1
        elif _COMPOUND.match(token):
            return None
        else:
            repeat = 1  # a letter or filler word
    return "".join(out)


def _strip_phone_prefix(digits: str) -> str:
    for prefix in _PHONE_PREFIXES:
        if digits.startswith(prefix) and len(digits) - len(prefix) == 10:
            return digits[len(prefix):]
    return digits


def digits_agree(value: str, quote: str, field_type: FieldType) -> Grounding | None:
    """None when consistent or not checkable; a failed Grounding otherwise."""
    if field_type not in DIGIT_FIELDS:
        return None
    heard = spoken_digits(quote, letters_possible=field_type is FieldType.PAN)
    if heard is None:
        return None
    written = "".join(re.findall(r"[0-9]", value or ""))
    if field_type is FieldType.PHONE:
        heard, written = _strip_phone_prefix(heard), _strip_phone_prefix(written)
    if heard == written:
        return None
    if field_type is not FieldType.PAN:
        return Grounding(
            True,
            None,
            f"the model wrote digits {written!r} but the user said {heard!r}; "
            "using what the user said",
            replacement=heard,
        )
    return Grounding(
        False,
        None,
        f"the value has digits {written!r} but the user said {heard!r} "
        f"({len(heard)} digits); the model changed the number",
    )


def check(
    extraction: Extraction, utterance: str, field_type: FieldType | None = None
) -> Grounding:
    """Ground an extraction against the utterance it claims to come from.

    Only value-bearing extractions are grounded. A question or a decline has no
    value and therefore nothing to anchor. For identifier fields the value's
    digits must also match the quote's (LF-007).
    """
    if not extraction.is_value:
        return Grounding(True, None, "no value to ground")
    located = locate(extraction.quote, utterance)
    if located.grounded and field_type is not None:
        mismatch = digits_agree(extraction.value, extraction.quote, field_type)
        if mismatch is not None:
            if mismatch.replacement is not None:
                return Grounding(True, located.span, mismatch.detail, mismatch.replacement)
            return mismatch
    return located


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
