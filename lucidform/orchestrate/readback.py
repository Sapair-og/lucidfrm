"""Rendering a validated value so a person can check it by ear.

This is the last thing the user hears before a value is committed, and for a
user who cannot see the form it is the *only* representation of that value they
will ever receive. If the read-back is not checkable by ear, the confirmation
step is theatre: the user says yes to something they could not actually verify.

So identifiers are spelled out rather than spoken as words. "AKQPS3417M" read
aloud is an unpronounceable noise that no listener can compare against the card
in their hand; the same value delivered character by character is checkable one
symbol at a time, which is how a bank clerk reads an identifier back across a
counter. Digits are rendered as words for the same reason -- a synthesiser
reading "3417" as "three thousand four hundred and seventeen" has silently
regrouped the number, and the listener cannot tell whether the system holds the
digits they gave.

Dates are the mirror image: `1987-03-14` is the stored form and an unreadable
one, so the read-back says "14 March 1987". In every case the *stored* value is
unchanged -- only its presentation differs, and the value being confirmed is
always exactly the value that will be written.
"""

from __future__ import annotations

import datetime as dt

from lucidform.models import FieldSpec, FieldType

DIGIT_WORDS = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
}

# Field types whose value is an identifier rather than a word: meaningless as
# speech, checkable only symbol by symbol.
SPELLED_OUT = {
    FieldType.PAN,
    FieldType.AADHAAR,
    FieldType.PIN,
    FieldType.PHONE,
}

# Read in groups, with a pause between them, so the listener can hold each
# group in memory long enough to compare it. Ungrouped, a twelve-digit number
# is not checkable by ear.
GROUP_SIZE = {
    FieldType.AADHAAR: 4,
    FieldType.PHONE: 5,
    FieldType.PIN: 3,
    FieldType.PAN: 5,
}

GROUP_SEPARATOR = " ... "
CHAR_SEPARATOR = " "


def spell(value: str, group_size: int | None = None) -> str:
    """Render a value character by character, digits as words.

    Letters are upper-cased so a synthesiser pronounces them as letter names
    rather than attempting a word.
    """
    symbols = [DIGIT_WORDS.get(ch, ch.upper()) for ch in value if not ch.isspace()]
    if not group_size or group_size <= 0:
        return CHAR_SEPARATOR.join(symbols)

    groups = [
        CHAR_SEPARATOR.join(symbols[i : i + group_size])
        for i in range(0, len(symbols), group_size)
    ]
    return GROUP_SEPARATOR.join(groups)


# Punctuation a listener cannot hear as a character. Spoken as words, or the
# read-back contains symbols that a synthesiser either skips silently or
# pronounces inconsistently -- and a listener cannot confirm what they did not
# hear.
PUNCTUATION_WORDS = {
    ".": "dot",
    "_": "underscore",
    "-": "dash",
    "+": "plus",
}


def spell_email(value: str) -> str:
    """Emails are spoken with 'at' and 'dot', and the local part spelled out.

    The domain is left as words: a listener can check "example dot invalid"
    without hearing it letter by letter, whereas the local part is frequently a
    name abbreviation that cannot be guessed from its sound.
    """
    local, _, domain = value.partition("@")
    spelled_local = " ".join(
        PUNCTUATION_WORDS.get(ch, DIGIT_WORDS.get(ch, ch.upper()))
        for ch in local
        if not ch.isspace()
    )
    domain_spoken = " dot ".join(part for part in domain.split("."))
    return f"{spelled_local} at {domain_spoken}".strip()


def render_value(value: str, field: FieldSpec, lang: str = "en") -> str:
    """The value, as it should be heard."""
    if field.decline_value and value == field.decline_value:
        return value
    if field.type is FieldType.DATE:
        try:
            parsed = dt.date.fromisoformat(value)
        except ValueError:
            return value
        # No leading zero on the day: "4 March", not "04 March".
        return f"{parsed.day} {parsed.strftime('%B')} {parsed.year}"

    if field.type is FieldType.EMAIL:
        return spell_email(value)

    if field.type in SPELLED_OUT:
        return spell(value, GROUP_SIZE.get(field.type))

    return value


def render(value: str, field: FieldSpec, template: str, lang: str = "en") -> str:
    """The full read-back sentence.

    `template` comes from the string table so the phrasing is translatable
    without touching this module.
    """
    return template.format(
        label=field.name(lang), value=render_value(value, field, lang)
    )
