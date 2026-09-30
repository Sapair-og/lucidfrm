"""Verhoeff checksum, and the synthetic-data generator built on it.

Aadhaar uses Verhoeff, not Luhn. The distinction is load-bearing: Luhn accepts
many numbers Verhoeff rejects, so a Luhn implementation would look correct on
happy-path tests while silently weakening the gate. The tests below pin the
behaviour that distinguishes them -- single-digit substitution and adjacent
transposition, the two error classes Verhoeff is designed to catch and the two
a user reading a card aloud actually produces.
"""

from __future__ import annotations

import random

import pytest

from lucidform.gate import checksums as ck


def test_generated_numbers_are_valid():
    rng = random.Random(1)
    for _ in range(200):
        assert ck.aadhaar_valid(ck.synthetic_aadhaar(rng))


def test_check_digit_completes_a_payload():
    payload = "74791098499"
    assert ck.verhoeff_check_digit(payload) == "2"
    assert ck.verhoeff_valid(payload + "2")


def test_every_single_digit_substitution_is_caught():
    """The realistic error: one digit misheard or mistyped.

    Exhaustive over all 12 positions and all 9 wrong digits, so this is a
    property, not a sample.
    """
    number = ck.synthetic_aadhaar(random.Random(7))
    for i in range(len(number)):
        for d in "0123456789":
            if d == number[i]:
                continue
            corrupted = number[:i] + d + number[i + 1 :]
            assert not ck.verhoeff_valid(corrupted), f"missed substitution at {i}: {d}"


def test_adjacent_transpositions_are_caught():
    """Two neighbouring digits swapped -- the classic dictation error.

    This is the case Luhn cannot catch for all digit pairs and Verhoeff can.
    """
    number = ck.synthetic_aadhaar(random.Random(11))
    checked = 0
    for i in range(len(number) - 1):
        if number[i] == number[i + 1]:
            continue  # swapping equal digits is not an error
        swapped = (
            number[:i] + number[i + 1] + number[i] + number[i + 2 :]
        )
        assert not ck.verhoeff_valid(swapped), f"missed transposition at {i}"
        checked += 1
    assert checked >= 8, "too few distinct pairs exercised to be meaningful"


def test_leading_zero_or_one_is_rejected():
    """Issued Aadhaar numbers never begin with 0 or 1.

    Treated as part of validity rather than as a separate format rule, because
    a number failing it is not a formatting problem -- it cannot exist.
    """
    valid = ck.synthetic_aadhaar(random.Random(3))
    for lead in "01":
        candidate = lead + valid[1:]
        assert not ck.aadhaar_valid(candidate)


def test_wrong_length_is_rejected():
    valid = ck.synthetic_aadhaar(random.Random(5))
    assert not ck.aadhaar_valid(valid[:-1])
    assert not ck.aadhaar_valid(valid + "0")


@pytest.mark.parametrize(
    "junk", ["", "   ", "abcdefghijkl", "7479 1098 4992", "74791098499X", "-47910984992"]
)
def test_non_digits_are_rejected_not_crashed(junk):
    """Whitespace-separated and letter-bearing input reaches this function in
    practice -- speech recognition emits both. It must return False, not raise.
    """
    assert not ck.aadhaar_valid(junk)
    assert not ck.verhoeff_valid(junk)


def test_corruption_helper_changes_exactly_one_digit():
    rng = random.Random(13)
    original = ck.synthetic_aadhaar(rng)
    for _ in range(50):
        bad = ck.corrupt_one_digit(original, rng)
        assert len(bad) == len(original)
        differing = sum(a != b for a, b in zip(original, bad))
        assert differing == 1
        assert not ck.verhoeff_valid(bad)


def test_check_digit_rejects_non_numeric_payload():
    with pytest.raises(ValueError):
        ck.verhoeff_check_digit("74791098499X")
