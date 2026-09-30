"""Checksum primitives for the validation gate.

Pure functions over strings. No I/O, no model, no state -- so they can be
exhaustively tested and reused to *generate* synthetic test data that genuinely
exercises the checksum path (METHODOLOGY M0.8).

Aadhaar uses the Verhoeff scheme, not Luhn. This matters: Luhn accepts many
numbers Verhoeff rejects, so a Luhn implementation would silently weaken the
gate while appearing to work.
"""

from __future__ import annotations

import random

# Verhoeff dihedral group D5 multiplication table.
_D = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
)

# Permutation table, applied cyclically by digit position.
_P = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8),
)

# Multiplicative inverse in D5.
_INV = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)


def verhoeff_valid(digits: str) -> bool:
    """True if `digits` (including its trailing check digit) satisfies Verhoeff."""
    if not digits.isdigit():
        return False
    c = 0
    for i, ch in enumerate(reversed(digits)):
        c = _D[c][_P[i % 8][int(ch)]]
    return c == 0


def verhoeff_check_digit(payload: str) -> str:
    """Check digit for a payload that does not yet carry one."""
    if not payload.isdigit():
        raise ValueError("payload must be digits only")
    c = 0
    for i, ch in enumerate(reversed(payload)):
        c = _D[c][_P[(i + 1) % 8][int(ch)]]
    return str(_INV[c])


def aadhaar_valid(number: str) -> bool:
    """Structural + checksum validity of a 12-digit Aadhaar number.

    The first digit is never 0 or 1 in issued numbers, so that rule is part of
    validity rather than a separate format check.
    """
    if len(number) != 12 or not number.isdigit():
        return False
    if number[0] in "01":
        return False
    return verhoeff_valid(number)


def synthetic_aadhaar(rng: random.Random | None = None) -> str:
    """Generate a checksum-valid but entirely fabricated Aadhaar number.

    Used only to build the synthetic corpus. These numbers are structurally
    indistinguishable from issued ones by design -- that is what makes them
    useful for exercising the checksum path -- and are generated, never sourced.
    """
    rng = rng or random.Random()
    payload = str(rng.randint(2, 9)) + "".join(
        str(rng.randint(0, 9)) for _ in range(10)
    )
    return payload + verhoeff_check_digit(payload)


def corrupt_one_digit(number: str, rng: random.Random | None = None) -> str:
    """Change exactly one digit, producing a checksum-invalid variant.

    The single-digit transposition/substitution error is the realistic failure
    mode -- both for a user misreading a card and for speech recognition -- and
    is precisely what Verhoeff is designed to catch.
    """
    rng = rng or random.Random()
    i = rng.randrange(len(number))
    replacement = rng.choice([d for d in "0123456789" if d != number[i]])
    return number[:i] + replacement + number[i + 1 :]
