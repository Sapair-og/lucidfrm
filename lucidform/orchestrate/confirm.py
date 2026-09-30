"""Read-back confirmation: deciding whether the user actually said yes.

This module is the sole issuer of confirmation receipts, and therefore the only
place in the system from which a write can be authorised.

The interesting problem here is narrower than it looks. The naive
implementation asks whether the utterance *contains* an affirmative token, and
that implementation commits a value on "yes, I know that's wrong" and on
"yesterday I gave you the wrong number". Both are things a real user says. The
first is a silent write in the most literal sense: the user has just told the
system the value is incorrect, and the system stores it.

So the parser is a whitelist, not a search. An utterance confirms only if the
whole of it -- after normalisation and removal of politeness -- is a recognised
affirmation. Anything else is treated as not-a-confirmation and the system asks
again.

**The costs are asymmetric, and the design reflects that.** A false negative
means re-asking a user who did confirm: a few seconds of friction, and the
correct value still reaches the form. A false positive means writing a value
into a legal document that the user did not agree to, in a system whose users
are specifically those least able to detect it afterwards. Those are not
comparable, so the threshold is not set halfway between them. The false-negative
rate is measured and reported (METHODOLOGY M3.3) rather than assumed to be zero.
"""

from __future__ import annotations

import re

from lucidform.formstate.receipt import ConfirmationReceipt
from lucidform.models import Affirmation, Candidate, ValidationReport, fingerprint

# Any of these anywhere in the utterance defeats confirmation outright, before
# the whitelist is consulted. "yes but the last digit is wrong" must not
# confirm, and neither must "haan lekin galat hai".
NEGATION = re.compile(
    r"\b("
    r"no|not|nope|never|wrong|incorrect|mistake|error|change|fix|again|"
    r"but|except|however|actually|wait|hold|stop|"
    r"nahi|nahin|galat|rukiye|ruko|badal|theek nahi"
    r")\b"
)

# Uncertainty. A confirmation that is hedged is not a confirmation; the system
# should read the value back again rather than resolve the doubt on the user's
# behalf.
HEDGE = re.compile(
    r"\b("
    r"maybe|perhaps|probably|possibly|think|guess|suppose|almost|nearly|"
    r"roughly|about|around|sure\?|unsure|if|unless|shayad|lagta|shayad hai"
    r")\b"
)

# Politeness and address, removed before matching so that "yes please" and
# "haan ji" reduce to their affirmative core. These carry no propositional
# content, so removing them cannot change whether the user agreed.
FILLER = re.compile(
    r"\b(please|kindly|sir|madam|thank you|thanks|shukriya|dhanyavaad|to|so)\b"
)

# The whitelist. An utterance confirms only if it matches one of these in full.
# Deliberately small: every entry is a phrase whose only reading is agreement.
AFFIRMATIONS = tuple(
    re.compile(p)
    for p in (
        r"^yes$",
        r"^yes yes$",
        r"^yeah$",
        r"^yep$",
        r"^yup$",
        r"^correct$",
        r"^right$",
        r"^confirm$",
        r"^confirmed$",
        r"^agreed$",
        r"^yes correct$",
        r"^yes right$",
        r"^yes confirm(ed)?$",
        r"^(yes )?(that|thats|that is|this|this is|it|it is|its) (is )?(correct|right)$",
        r"^(that|thats|it) ?s (correct|right)$",
        # Hindi / Hinglish, in the romanised form a transcriber produces.
        r"^haan$",
        r"^haan haan$",
        r"^ha$",
        r"^haan ji$",
        r"^ji haan$",
        r"^ji$",
        r"^bilkul$",
        r"^bilkul sahi$",
        r"^sahi$",
        r"^sahi hai$",
        r"^haan sahi hai$",
        r"^ji haan sahi hai$",
        r"^theek hai$",
        r"^thik hai$",
        r"^haan theek hai$",
    )
)

# Tokens deliberately NOT treated as confirmation, recorded here because their
# absence is a design decision rather than an oversight. "ok" and "acha"
# overwhelmingly acknowledge that the user *heard* the read-back, not that they
# agree with it; accepting them would convert every "mm-hm, go on" into a
# committed value.
NOT_CONFIRMATION = ("ok", "okay", "acha", "achha", "hmm", "mhm", "aage", "next")


def normalize_utterance(utterance: str) -> str:
    """Lowercase, strip punctuation and filler, collapse whitespace.

    Apostrophes become spaces so that "that's" and "thats" reduce to the same
    form without the whitelist having to enumerate both.
    """
    text = (utterance or "").casefold()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = FILLER.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_affirmation(utterance: str) -> Affirmation:
    """Decide whether an utterance is an explicit confirmation.

    Returns an `Affirmation` carrying the verdict, the original words, and the
    rule that decided -- the basis is written to the event log so a reviewer can
    see why a given utterance was or was not treated as consent.
    """
    raw = utterance or ""
    text = normalize_utterance(raw)

    if not text:
        return Affirmation(False, raw, basis="nothing was said")

    if NEGATION.search(text):
        return Affirmation(
            False, raw, basis="contains a negation or correction cue"
        )

    if HEDGE.search(text):
        return Affirmation(False, raw, basis="the confirmation was hedged")

    for pattern in AFFIRMATIONS:
        if pattern.match(text):
            return Affirmation(
                True, raw, basis=f"whole utterance matched {pattern.pattern!r}"
            )

    if text in NOT_CONFIRMATION:
        return Affirmation(
            False,
            raw,
            basis=(
                f"{text!r} acknowledges the read-back but does not agree with it"
            ),
        )

    return Affirmation(
        False, raw, basis="not a recognised affirmation in full"
    )


def confirm(
    candidate: Candidate,
    validation: ValidationReport,
    utterance: str,
) -> tuple[Affirmation, ConfirmationReceipt | None]:
    """Parse the user's response and, if it is a yes, issue a receipt.

    This is the only function in the system that produces a receipt. It returns
    the affirmation regardless, so the caller can log a denial and re-ask, and a
    receipt only when a write is genuinely authorised.
    """
    affirmation = parse_affirmation(utterance)

    if not affirmation.explicit or not validation.passed:
        return affirmation, None

    # Guarded above; re-stated here because this is the last point before a
    # write becomes possible, and a stale report reaching this line would pair
    # one candidate's verdict with another's confirmation.
    if validation.candidate_id != candidate.candidate_id:
        return affirmation, None

    receipt = ConfirmationReceipt(
        field_id=candidate.field_id,
        candidate_id=candidate.candidate_id,
        candidate_fingerprint=fingerprint(
            candidate.field_id,
            validation.normalized_value,
            candidate.candidate_id,
        ),
        validation=validation,
        affirmation=affirmation,
    )
    return affirmation, receipt
