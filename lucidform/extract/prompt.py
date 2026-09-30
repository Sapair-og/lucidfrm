"""The extraction prompt.

Built per field, from the schema the form parser produced. Two things it must
do, and one it must not.

Must: tell the model what shape the field takes, so it can transcribe spoken
digits and letters into the written form; and make clear that reporting
uncertainty is the preferred outcome when the utterance is unclear, because the
cost of a low confidence score is one repeated question while the cost of a
confident wrong value is a wrong entry on a legal document.

Must not: ask the model to validate, decide, or confirm anything. Validation is
the gate's job and confirmation is the user's. A prompt that says "only return
valid values" moves the accept/reject decision into the model, which is exactly
the architecture this project exists to avoid -- and it would do so invisibly,
since a model that silently drops an invalid value looks identical to a user who
never said one.
"""

from __future__ import annotations

from lucidform.models import FieldSpec, FieldType

# Shape hints per field type. Descriptive, not prescriptive: they tell the model
# how the value is written down so it can transcribe speech into it. They do not
# ask the model to reject anything that fails to match -- a malformed value must
# reach the gate, be rejected with a reason, and be read back to the user as a
# problem. Silently dropping it would leave the user repeating themselves with
# no idea why.
SHAPE_HINTS: dict[FieldType, str] = {
    FieldType.PAN: (
        "A PAN is written as ten characters with no spaces: five letters, then "
        "four digits, then one letter. Speakers usually read it out one "
        "character at a time."
    ),
    FieldType.AADHAAR: (
        "An Aadhaar number is twelve digits with no spaces. Speakers usually "
        "read it out digit by digit, sometimes in groups of four."
    ),
    FieldType.PIN: "A PIN code is six digits with no spaces.",
    FieldType.PHONE: (
        "An Indian mobile number is ten digits. Drop any country code or "
        "leading zero."
    ),
    FieldType.DATE: (
        "Write the date as YYYY-MM-DD. Speakers give dates day first, so "
        "'third of April 1987' is 1987-04-03."
    ),
    FieldType.EMAIL: (
        "Speakers say 'at' for @ and 'dot' for a full stop. Write the address "
        "in its normal written form."
    ),
    FieldType.NAME: (
        "Write the name in the normal written form, capitalised. Do not expand "
        "initials or correct the spelling."
    ),
}

SYSTEM = """\
You extract a single field value from what a person said while filling in a \
government form. Many of these people cannot read the form, and some cannot see \
it at all. They are speaking, so what you receive is a transcript: it may be \
hesitant, it may mix Hindi and English, and identifiers are usually read out one \
character at a time.

Your only job is to report what the person said. You are not filling in the \
form and nothing you return is written to it directly. A separate component \
checks every value you produce, and the person is then read the value back and \
asked to confirm it before anything is stored.

Because of that, the useful thing you can do is be accurate about your own \
uncertainty:

- If the person clearly stated a value, return it with a high confidence score.
- If you had to infer or repair it, say so with a low confidence score. A low \
score costs one repeated question. A confident wrong value goes to someone who \
cannot check it.
- If they asked what the field means, that is a question, not a value.
- If they said they do not have one, that is a decline, not an empty value.
- If two readings are possible, mark it ambiguous instead of choosing one.

Do not validate. Do not correct a value you think is wrong -- report what you \
heard and let the checker find the problem. Do not fill in anything the person \
did not say.

The `quote` you return is checked against the transcript character by \
character, so copy it exactly from their words.\
"""


def build_user_message(field: FieldSpec, utterance: str, lang: str = "en") -> str:
    hint = SHAPE_HINTS.get(field.type, "")
    lines = [
        f"Field being asked for: {field.label}",
        f"The person was asked: {field.ask(lang)}",
    ]
    if hint:
        lines.append(f"How this value is written: {hint}")
    if field.enum_values:
        lines.append(
            "This field accepts only these exact options: "
            + ", ".join(field.enum_values)
            + ". If what they said is not one of these, report what they said "
            "as the value and set confidence low -- do not substitute the "
            "closest option."
        )
    if not field.required:
        lines.append("This field is optional; the person may decline it.")
    lines.append("")
    lines.append("What the person said:")
    lines.append(utterance)
    return "\n".join(lines)


def build(field: FieldSpec, utterance: str, lang: str = "en") -> tuple[str, str]:
    """Return (system, user) for one extraction."""
    return SYSTEM, build_user_message(field, utterance, lang)
