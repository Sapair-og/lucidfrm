"""The shape the model is allowed to reply in.

This schema is a safety boundary, not a convenience. Because the response is
constrained to it, the model has no channel through which to emit an
instruction, a status claim, or a request to write -- the only things it can
say are a proposed value, how confident it is, where in the utterance it found
it, and what kind of thing the user was doing. A schema-constrained extractor
cannot ask for a commit because there is no field in which to ask.

Two fields carry more weight than they look like they do:

  * `quote` must be copied verbatim from the utterance. It is checked
    deterministically afterwards (see `grounding.py`), which catches a value the
    model produced from nowhere.
  * `intent` separates "the user gave a value" from "the user asked a question"
    and "the user declined". Collapsing those into a value field is how
    "pan kya hota hai" -- what is a PAN? -- ends up written into the PAN field.
"""

from __future__ import annotations

import enum

from pydantic import BaseModel, Field


class Intent(str, enum.Enum):
    """What the user was doing, not what they said."""

    VALUE = "value"
    # A request for the field to be explained. Answering it with a value would
    # write the user's question into the form.
    QUESTION = "question"
    # An explicit refusal to answer -- meaningful only for optional fields, and
    # recorded as a decision rather than as an empty value.
    DECLINE = "decline"
    # Speech was heard but no value could be recovered from it.
    UNCLEAR = "unclear"
    # The user has the document but does not know or cannot find the number
    # (ISSUES.md LF-012). Not a decline: "I have a PAN but don't remember it"
    # must not be offered Form 60. Answered with how to look the number up.
    FIND = "find"


class Extraction(BaseModel):
    """The model's entire permitted output."""

    intent: Intent = Field(
        description=(
            "What the user was doing. 'value' only if they stated a value for "
            "this field. 'question' if they asked what the field means or how "
            "to answer it. 'find' if they have one but do not know, remember "
            "or cannot find the number, or ask how to find or download it. "
            "'decline' if they said they do not have one or do not wish to "
            "give it. 'unclear' if you cannot tell."
        )
    )
    value: str = Field(
        default="",
        description=(
            "The value for this field, normalised to how it would be written "
            "on the form. Empty string unless intent is 'value'. Do not guess: "
            "if the user did not state it, leave this empty and set intent to "
            "'unclear'."
        ),
    )
    quote: str = Field(
        default="",
        description=(
            "The exact words from the user's message that the value came from, "
            "copied character for character. This is checked against the "
            "original message, so it must appear in it verbatim. Empty if "
            "intent is not 'value'."
        ),
    )
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description=(
            "How certain you are that this is the value the user intended. Be "
            "honest and use the low end: a value you inferred rather than "
            "heard should score below 0.5. Under-confidence costs the user one "
            "repeated question; over-confidence puts a wrong value on a legal "
            "document."
        ),
    )
    ambiguous: bool = Field(
        default=False,
        description=(
            "True if the message has more than one plausible reading for this "
            "field. Set this rather than picking one."
        ),
    )
    alternatives: list[str] = Field(
        default_factory=list,
        description=(
            "Other readings you considered, if ambiguous. At most three. These "
            "are recorded for analysis; they are never written to the form."
        ),
    )

    @property
    def is_value(self) -> bool:
        return self.intent is Intent.VALUE and bool(self.value)
