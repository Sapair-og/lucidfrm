"""Suggestions for a rejected value (ISSUES.md LF-005, LF-009, LF-004).

A suggestion is never a value. The gate still rejects; the suggestion is then
offered to the user as a fresh candidate that goes through the gate, the
read-back and the explicit yes like anything else. That keeps the rule from
CLAUDE.md intact -- normalization reshapes and never repairs -- because nothing
here changes what is written without the user saying yes to it.

All of it is deterministic: amount arithmetic, a human-written list of
synonyms, and edit distance. No model.
"""

from __future__ import annotations

import difflib
import re

from lucidform.models import FieldSpec, FieldType

# Close enough to be a misspelling (kerela -> Kerala is 0.83), far enough that
# two different options are not confused.
_CUTOFF = 0.8

EMAIL_PROVIDERS = (
    "gmail.com",
    "yahoo.com",
    "yahoo.co.in",
    "outlook.com",
    "hotmail.com",
    "rediffmail.com",
    "icloud.com",
    "live.com",
    "protonmail.com",
)


def suggest(value: str, field: FieldSpec) -> str | None:
    text = (value or "").strip()
    if not text:
        return None
    if field.type is FieldType.EMAIL:
        return _email(text)
    if field.type is not FieldType.ENUM or not field.enum_values:
        return None
    if field.amount_bands:
        band = amount_band(text, field.enum_values)
        if band:
            return band
    folded = " ".join(text.casefold().split())
    for option, names in field.suggest_names.items():
        if any(folded == n.casefold() or f" {n.casefold()} " in f" {folded} " for n in names):
            return option
    by_fold = {o.casefold(): o for o in field.enum_values}
    close = difflib.get_close_matches(folded, list(by_fold), n=2, cutoff=_CUTOFF)
    if len(close) == 1 or (
        len(close) == 2
        and difflib.SequenceMatcher(None, folded, close[0]).ratio()
        > difflib.SequenceMatcher(None, folded, close[1]).ratio()
    ):
        return by_fold[close[0]]
    return None


def email_typo(domain: str) -> str | None:
    """The provider a domain is a near-miss of, or None."""
    domain = domain.casefold()
    if domain in EMAIL_PROVIDERS:
        return None
    close = difflib.get_close_matches(domain, EMAIL_PROVIDERS, n=1, cutoff=0.85)
    return close[0] if close else None


def _email(value: str) -> str | None:
    local, at, domain = value.partition("@")
    fixed = email_typo(domain) if at else None
    return f"{local}@{fixed}" if fixed else None


# -- amounts -> income band ----------------------------------------------------

_NUM_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "fifteen": 15, "twenty": 20, "twenty five": 25, "thirty": 30, "forty": 40,
    "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
    "ek": 1, "do": 2, "teen": 3, "char": 4, "chaar": 4, "paanch": 5, "panch": 5,
    "chhe": 6, "saat": 7, "aath": 8, "nau": 9, "das": 10, "barah": 12,
    "pandrah": 15, "bees": 20, "pachchees": 25, "pachees": 25, "tees": 30,
    "chalees": 40, "pachaas": 50, "pachas": 50, "saath": 60, "sattar": 70,
    "assi": 80, "nabbe": 90, "dedh": 1.5, "dhai": 2.5, "half": 0.5, "aadha": 0.5,
}
_SCALE = {
    "hundred": 100, "sau": 100,
    "thousand": 1_000, "hazaar": 1_000, "hazar": 1_000, "k": 1_000,
    "lakh": 100_000, "lakhs": 100_000, "lac": 100_000, "lacs": 100_000, "l": 100_000,
    "crore": 10_000_000, "crores": 10_000_000, "cr": 10_000_000,
}
_MONTHLY = re.compile(r"\b(per month|a month|monthly|mahina|mahine|mahinay|month)\b")
_TOKEN = re.compile(r"[0-9][0-9,]*(?:\.[0-9]+)?|[a-z]+")


def parse_amount(text: str) -> float | None:
    """Rupees per year stated in `text`, or None if it holds no clear amount.

    "45 lakh" -> 4,500,000; "4,50,000" -> 450,000; "paanch lakh" -> 500,000;
    "30 hazaar mahina" -> 360,000. Two separate numbers ("5 or 6 lakh") are
    not an amount; the caller then offers nothing.
    """
    folded = text.casefold().replace("rs.", " ").replace("₹", " ")
    monthly = bool(_MONTHLY.search(folded))
    folded = folded.replace("twenty five", "twenty-five").replace("twenty-five", " 25 ")
    # (value, stands on its own). A bare number word ("do" in "I do not know")
    # or a small bare figure ("45") is not an amount until a scale follows it.
    numbers: list[tuple[float, bool]] = []
    current: list | None = None
    for token in _TOKEN.findall(folded):
        if token[0].isdigit():
            if current is not None:
                numbers.append(tuple(current))
            figure = float(token.replace(",", ""))
            current = [figure, figure >= 1_000]
        elif token in _NUM_WORDS:
            if current is not None:
                numbers.append(tuple(current))
            current = [float(_NUM_WORDS[token]), False]
        elif token in _SCALE and current is not None:
            current = [current[0] * _SCALE[token], True]
    if current is not None:
        numbers.append(tuple(current))
    amounts = [v for v, real in numbers if real]
    if len(amounts) != 1 or len(numbers) != 1:
        return None
    return amounts[0] * 12 if monthly else amounts[0]


_BAND = re.compile(r"(below|under|above|over)?\s*([0-9.]+)(?:\s*-\s*([0-9.]+))?\s*lakh", re.I)


def amount_band(text: str, options) -> str | None:
    """The option whose range contains the stated amount (upper bound inclusive)."""
    amount = parse_amount(text)
    if amount is None or amount < 0:
        return None
    lakhs = amount / 100_000
    for option in options:
        m = _BAND.fullmatch(option.strip())
        if not m:
            continue
        word, lo, hi = m.group(1), float(m.group(2)), m.group(3)
        word = (word or "").casefold()
        if word in ("below", "under") and lakhs < lo:
            return option
        if word in ("above", "over") and lakhs > lo:
            return option
        if hi is not None and lo <= lakhs <= float(hi):
            # 1 lakh exactly is "1-5 Lakh", not "Below 1 Lakh"; 5 lakh is "1-5".
            return option
    return None
