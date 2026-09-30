"""Normalization and single-field rules.

Pure functions over strings, with no model, no I/O, and no state. That is what
makes the accept/reject decision reproducible and exhaustively testable
(METHODOLOGY M0.2).

Two implementation notes that are easy to get wrong and expensive to get wrong:

  * `str.isdigit()` and `\\d` both match Devanagari digits. A code-mixing
    speaker's transcript can carry them, and a validator built on either would
    accept "३०२०१५" as a PIN code, then write characters into the form that no
    downstream system will read as a number. Every numeric rule here uses an
    explicit ASCII `[0-9]` range.
  * Normalization runs before validation, so `+91 98123 45607` and
    `9812345607` are one value. Normalization may reshape, never repair: it
    strips separators and case, and it does not guess at missing or wrong
    characters.
"""

from __future__ import annotations

import datetime as dt
import re
import unicodedata

from lucidform.models import FieldSpec, FieldType

# Characters that occupy space in a string but render as nothing. A value made
# only of these is empty to the user and non-empty to a length check -- so the
# user would confirm a blank field believing they had filled it.
INVISIBLE = dict.fromkeys(
    map(
        ord,
        "​‌‍⁠﻿"  # zero-width space / joiners / BOM
        "   "  # non-breaking spaces
        "‎‏‪‫‬‭‮",  # bidi controls
    )
)

# Separators a speaker or a transcriber inserts into an identifier.
_SEPARATORS = re.compile(r"[\s\-.()]+")

# Explicit ASCII ranges throughout. Never \d -- see the module docstring.
PATTERNS: dict[FieldType, re.Pattern[str]] = {
    FieldType.PAN: re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$"),
    # Issued Aadhaar numbers never begin 0 or 1.
    FieldType.AADHAAR: re.compile(r"^[2-9][0-9]{11}$"),
    FieldType.PIN: re.compile(r"^[1-9][0-9]{5}$"),
    FieldType.PHONE: re.compile(r"^[6-9][0-9]{9}$"),
    FieldType.EMAIL: re.compile(r"^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$"),
    # Latin names only. A genuine limitation, recorded rather than papered
    # over: a Devanagari-script name would be rejected here. The prototype's
    # form is an English document whose name field is filled in Latin script.
    FieldType.NAME: re.compile(r"^[A-Za-z][A-Za-z .'\-]*$"),
    FieldType.TEXT: re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ,.\-/#'()]*$"),
}

# Fields whose length is exact rather than bounded.
EXACT_LENGTH: dict[FieldType, int] = {
    FieldType.PAN: 10,
    FieldType.AADHAAR: 12,
    FieldType.PIN: 6,
    FieldType.PHONE: 10,
}

# Accepted date inputs, tried in order. Day-first is the Indian convention and
# is listed first so an ambiguous 03/04/1987 resolves the way the speaker meant
# it. Explicit formats rather than a fuzzy parser: a fuzzy parser will accept
# almost anything and silently pick an interpretation.
DATE_FORMATS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%d.%m.%Y",
    "%d %m %Y",
    "%d %B %Y",
    "%d %b %Y",
)

MIN_AGE_YEARS = 18


def strip_invisible(value: str) -> str:
    """Remove characters that render as nothing, then collapse whitespace."""
    if not value:
        return ""
    # NFKC folds full-width and compatibility forms onto their plain
    # equivalents, so a full-width digit does not slip past an ASCII range.
    value = unicodedata.normalize("NFKC", value)
    value = value.translate(INVISIBLE)
    return re.sub(r"\s+", " ", value).strip()


def parse_date(value: str) -> dt.date | None:
    """Parse an accepted date input. Returns None if it is not a real date.

    Rejects rather than repairs: `1987-13-45` has no valid reading, so it
    returns None instead of clamping to a nearby date.
    """
    text = strip_invisible(value)
    for fmt in DATE_FORMATS:
        try:
            return dt.datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def normalize(value: str, field: FieldSpec) -> str:
    """Canonical form of a value: what gets read back, and what gets committed.

    The read-back states the normalized value precisely so the user confirms
    what will actually be written, rather than confirming their own phrasing
    and having something else stored.
    """
    text = strip_invisible(value)
    if not text:
        return ""

    ftype = field.type

    if ftype in (FieldType.PAN, FieldType.AADHAAR, FieldType.PIN):
        return _SEPARATORS.sub("", text).upper()

    if ftype is FieldType.PHONE:
        digits = _SEPARATORS.sub("", text)
        # Drop an Indian country code or trunk prefix. This is reshaping, not
        # repair: the subscriber number is unchanged.
        for prefix in ("+91", "0091", "91", "0"):
            if digits.startswith(prefix) and len(digits) - len(prefix) == 10:
                return digits[len(prefix) :]
        return digits

    if ftype is FieldType.EMAIL:
        return text.lower()

    if ftype is FieldType.DATE:
        parsed = parse_date(text)
        # An unparseable date is returned unchanged so the format check can
        # reject it and report what the user actually said.
        return parsed.isoformat() if parsed else text

    if ftype is FieldType.ENUM:
        # Case and spacing are resolved against the option list; anything else
        # is left alone for the enum check to reject. Choosing the "nearest"
        # option would be the system deciding on the user's behalf.
        folded = text.casefold()
        for option in field.enum_values:
            if option.casefold() == folded:
                return option
            # A declared name of the option in the user's language is the
            # option, not a guess at it: exact match only, and only names a
            # human wrote into the overlay for this field.
            # The name gets the same cleaning as the value, or a precomposed
            # character in the overlay could never match its NFKC form.
            names = field.enum_names.get(option, ())
            if any(strip_invisible(name).casefold() == folded for name in names):
                return option
        return text

    return text  # NAME, TEXT: whitespace already collapsed


def length_error(value: str, field: FieldSpec) -> str | None:
    """Wrong size. Returns a human-readable detail, or None if the size is fine."""
    exact = EXACT_LENGTH.get(field.type)
    if exact is not None and len(value) != exact:
        return f"expected exactly {exact} characters, got {len(value)}"
    if field.max_length is not None and len(value) > field.max_length:
        return f"exceeds the field's {field.max_length}-character limit"
    return None


def format_error(value: str, field: FieldSpec) -> str | None:
    """Right size, wrong shape. Returns a detail, or None if the shape is fine."""
    if field.type is FieldType.DATE:
        # A date's shape is "is it a real calendar date", not a regex.
        return None if parse_date(value) else "not a recognisable date"

    pattern = PATTERNS.get(field.type)
    if pattern is None or pattern.match(value):
        return None

    return {
        FieldType.PAN: "a PAN is five letters, four digits, then one letter",
        FieldType.AADHAAR: "an Aadhaar number is twelve digits and cannot start with 0 or 1",
        FieldType.PIN: "a PIN code is six digits and cannot start with 0",
        FieldType.PHONE: "an Indian mobile number is ten digits starting 6, 7, 8 or 9",
        FieldType.EMAIL: "not a valid email address",
        FieldType.NAME: "a name may contain only letters, spaces, apostrophes and hyphens",
        FieldType.TEXT: "contains characters that are not allowed in this field",
    }.get(field.type, "does not match the expected format")


def enum_error(value: str, field: FieldSpec) -> str | None:
    if not field.enum_values or value in field.enum_values:
        return None
    return f"must be one of: {', '.join(field.enum_values)}"


def range_error(value: str, field: FieldSpec, *, today: dt.date | None = None) -> str | None:
    """Well-formed, but outside the permitted domain."""
    if field.type is not FieldType.DATE:
        return None

    parsed = parse_date(value)
    if parsed is None:
        return None  # already reported as a format error

    today = today or dt.date.today()
    if parsed > today:
        return "that date is in the future"

    if field.id == "dob":
        age = (
            today.year
            - parsed.year
            - ((today.month, today.day) < (parsed.month, parsed.day))
        )
        if age < MIN_AGE_YEARS:
            return (
                f"the applicant must be at least {MIN_AGE_YEARS}; "
                f"that date gives an age of {age}"
            )
    return None
