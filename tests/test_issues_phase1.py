"""Regression tests for docs/ISSUES.md LF-002, LF-007, LF-008.

Inputs are taken from the live session that surfaced them
(data/runs/bfcc50e1a3f9479e9a57b4907f401057.jsonl).
"""

from __future__ import annotations

import pytest

from lucidform.extract import grounding
from lucidform.extract.schema import Extraction, Intent
from lucidform.gate import rules
from lucidform.gate.gate import ValidationGate
from lucidform.models import Candidate, FieldType, Status
from lucidform.schema import loader
from tests.test_session import one_field, value


@pytest.fixture(scope="module")
def schema():
    return loader.load()


def _gate(schema, field_id, v, committed=None):
    cand = Candidate(field_id=field_id, value=v, raw_utterance=v, confidence=0.95)
    return ValidationGate(schema).check(cand, committed or {})


# -- LF-002: placeholder Aadhaar ---------------------------------------------


@pytest.mark.parametrize("number", ["999999999999", "222222222222", "234567890123", "987654321098"])
def test_placeholder_aadhaar_is_rejected(schema, number):
    report = _gate(schema, "aadhaar", number)
    assert report.status is Status.REJECT
    # Placeholders that fail Verhoeff are still rejected; the ones that pass it
    # (999999999999 does) are rejected by the placeholder rule.
    if rules.is_placeholder_number(number):
        assert report.reason.value in ("format", "checksum")


def test_999999999999_passes_verhoeff_but_not_the_gate(schema):
    from lucidform.gate.checksums import aadhaar_valid

    assert aadhaar_valid("999999999999")
    report = _gate(schema, "aadhaar", "999999999999")
    assert report.reason.value == "format"
    assert "placeholder" in report.detail


def test_real_looking_aadhaar_still_passes(schema):
    # control case: a valid synthetic number is not caught by the new rule
    assert _gate(schema, "aadhaar", "234123412346").status is Status.PASS


def test_repeated_digit_mobile_is_not_treated_as_placeholder(schema):
    # "fancy" numbers are really sold; rejecting them would be a false positive
    assert _gate(schema, "mobile", "9999999999").status is Status.PASS


# -- LF-007: the model changing digits ---------------------------------------


@pytest.mark.parametrize(
    "text,expected",
    [
        ("9 6 3 4", "9634"),
        ("nine six three four", "9634"),
        ("nau chhe teen char", "9634"),
        ("double nine triple four", "99444"),
        ("B F T P N aath do shunya chhe C", "8206"),
    ],
)
def test_spoken_digits(text, expected):
    assert grounding.spoken_digits(text, letters_possible=True) == expected


def test_compound_number_words_skip_the_check():
    assert grounding.spoken_digits("twenty two", letters_possible=False) is None


def test_oh_is_zero_only_where_letters_cannot_occur():
    assert grounding.spoken_digits("nine oh one", letters_possible=False) == "901"
    assert grounding.spoken_digits("A B O", letters_possible=True) == ""


def _extraction(v, quote):
    return Extraction(intent=Intent.VALUE, value=v, quote=quote, confidence=0.9)


def test_thirteen_nines_are_not_shortened_to_twelve():
    said = "9999999999999"
    g = grounding.check(_extraction("999999999999", said), said, FieldType.AADHAAR)
    assert g.replacement == said  # the user's 13 digits, for the gate to reject


def test_eleven_digit_mobile_is_not_shortened():
    said = "45555555555"
    g = grounding.check(_extraction("4555555555", said), said, FieldType.PHONE)
    assert g.replacement == said


def test_country_code_is_not_a_mismatch():
    said = "+91 98390 12457"
    g = grounding.check(_extraction("9839012457", said), said, FieldType.PHONE)
    assert g.grounded and g.replacement is None


def test_pan_digit_mismatch_is_ungrounded():
    said = "B F T P N aath do shunya chhe C"
    g = grounding.check(_extraction("BFTPN8006C", said), said, FieldType.PAN)
    assert not g.grounded


def test_pan_digit_match_is_grounded():
    said = "B F T P N aath do shunya chhe C"
    g = grounding.check(_extraction("BFTPN8206C", said), said, FieldType.PAN)
    assert g.grounded


def test_session_rejects_the_shortened_aadhaar(schema, tmp_path):
    result, state, channel, _ = one_field(
        schema,
        "aadhaar",
        [value(value="999999999999", quote="9999999999999", confidence=0.9)],
        ["9999999999999"],
        tmp_path,
    )
    assert "aadhaar" not in state.values
    assert any("got 13" in t for _, t in channel.said)


# -- LF-008: no PAN -> Form 60 -----------------------------------------------


def test_declining_pan_offers_form_60_and_commits_on_yes(schema, tmp_path):
    result, state, channel, _ = one_field(
        schema, "pan", [Extraction(intent=Intent.DECLINE)], ["i dont have", "yes"], tmp_path
    )
    assert state.values["pan"] == "Form 60"
    assert any("Form 60" in t for _, t in channel.said)
    assert channel.readbacks == [("pan", "Form 60")]


def test_form_60_is_not_committed_without_yes(schema, tmp_path):
    result, state, channel, _ = one_field(
        schema,
        "pan",
        [Extraction(intent=Intent.DECLINE), value(value="AKQPS3417M", quote="akqps3417m")],
        ["i dont have", "no", "akqps3417m", "yes"],
        tmp_path,
    )
    assert state.values["pan"] == "AKQPS3417M"


def test_form_60_skips_the_surname_check(schema):
    report = _gate(schema, "pan", "form 60", {"full_name": "Suresh Yadav"})
    assert report.status is Status.PASS
    assert report.normalized_value == "Form 60"


# -- LF-013: a quote that stops in the middle of a number ------------------------


def test_short_quote_inside_a_longer_number_is_widened():
    # live 2026-10-01: user typed 11 digits; model quoted and returned the first 10
    said = "98390124577"
    g = grounding.check(_extraction("9839012457", "9839012457"), said, FieldType.PHONE)
    assert g.replacement == said


def test_grouped_number_is_widened_across_spaces():
    said = "my number is 98390 12457 7"
    g = grounding.check(_extraction("9839012457", "98390 12457"), said, FieldType.PHONE)
    assert g.replacement == "98390124577"


def test_exact_quote_of_a_whole_number_is_unchanged():
    said = "my pin is 221001"
    g = grounding.check(_extraction("221001", "221001"), said, FieldType.PIN)
    assert g.grounded and g.replacement is None
