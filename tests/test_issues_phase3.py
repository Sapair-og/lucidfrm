"""Regression tests for docs/ISSUES.md LF-004 (email), LF-005 (income), LF-009 (near misses).

Inputs are from the live session: "uhauihiuah@hhd.com", "1 lakh", "45 lakh",
"kerela", "housewife".
"""

from __future__ import annotations

import pytest

from lucidform.gate import suggest
from lucidform.gate.gate import ValidationGate
from lucidform.models import Candidate, Status
from lucidform.schema import loader
from tests.test_session import one_field, value


@pytest.fixture(scope="module")
def schema():
    return loader.load()


def _gate(schema, field_id, v, **kw):
    cand = Candidate(field_id=field_id, value=v, raw_utterance=v, confidence=0.95)
    return ValidationGate(schema, **kw).check(cand, {})


# -- LF-005: amount -> band ----------------------------------------------------


@pytest.mark.parametrize(
    "said,band",
    [
        ("45 lakh", "Above 25 Lakh"),
        ("1 lakh", "1-5 Lakh"),
        ("4.5 lakh", "1-5 Lakh"),
        ("4,50,000", "1-5 Lakh"),
        ("paanch lakh", "1-5 Lakh"),
        ("teen lakh", "1-5 Lakh"),
        ("80000", "Below 1 Lakh"),
        ("30 hazaar mahina", "1-5 Lakh"),  # 3.6 lakh a year
        ("2 crore", "Above 25 Lakh"),
        ("25 lakh", "10-25 Lakh"),
        ("ten lakh", "5-10 Lakh"),
    ],
)
def test_amount_band(schema, said, band):
    assert suggest.amount_band(said, schema.by_id("income_band").enum_values) == band


@pytest.mark.parametrize("said", ["i do not know", "5 or 6 lakh", "45", "bahut kam"])
def test_no_clear_amount_no_band(schema, said):
    assert suggest.amount_band(said, schema.by_id("income_band").enum_values) is None


def test_income_rejected_but_band_offered(schema):
    report = _gate(schema, "income_band", "45 lakh")
    assert report.status is Status.REJECT and report.suggestion == "Above 25 Lakh"


def test_offered_band_needs_a_yes(schema, tmp_path):
    result, state, channel, _ = one_field(
        schema, "income_band", [value(value="45 lakh", quote="45 lakh")], ["45 lakh", "yes"], tmp_path
    )
    assert state.values["income_band"] == "Above 25 Lakh"
    assert ("income_band", "Above 25 Lakh") in channel.readbacks


def test_offered_band_denied_is_not_saved(schema, tmp_path):
    result, state, _, _ = one_field(
        schema, "income_band", [value(value="45 lakh", quote="45 lakh")], ["45 lakh", "no"], tmp_path
    )
    assert "income_band" not in state.values


# -- LF-009: near misses --------------------------------------------------------


@pytest.mark.parametrize(
    "field_id,said,meant",
    [
        ("state", "kerela", "Kerala"),
        ("state", "maharastra", "Maharashtra"),
        ("occupation", "housewife", "Homemaker"),
        ("occupation", "kheti karta hoon", "Agriculture"),
        ("occupation", "hoemmeaker", "Homemaker"),
        ("occupation", "I work at an IT company", "Salaried"),
    ],
)
def test_near_miss_is_suggested(schema, field_id, said, meant):
    report = _gate(schema, field_id, said)
    assert report.status is Status.REJECT
    assert report.suggestion == meant


def test_unrelated_answer_gets_no_suggestion(schema):
    assert _gate(schema, "state", "banana").suggestion is None


def test_only_one_suggestion_per_utterance(schema, tmp_path):
    # the offered value is denied; the user is asked again, not offered another
    result, state, channel, _ = one_field(
        schema, "state", [value(value="kerela", quote="kerela")], ["kerela", "no"], tmp_path, max_attempts=1
    )
    assert sum("I think you meant" in t for _, t in channel.said) == 1
    assert "state" not in state.values


# -- LF-004: email ---------------------------------------------------------------


def test_provider_typo_is_rejected_with_suggestion(schema):
    report = _gate(schema, "email", "ramesh@gmial.com")
    assert report.status is Status.REJECT
    assert report.suggestion == "ramesh@gmail.com"


def test_domain_without_mail_is_rejected(schema):
    report = _gate(schema, "email", "uhauihiuah@hhd.com", domain_check=lambda d: False)
    assert report.status is Status.REJECT and "does not receive email" in report.detail


def test_lookup_failure_never_rejects(schema):
    assert _gate(schema, "email", "a@hhd.com", domain_check=lambda d: None).status is Status.PASS


def test_offline_gate_skips_the_domain_check(schema):
    report = _gate(schema, "email", "a@example.invalid")
    assert report.status is Status.PASS
    assert any(c.name == "email_domain" and "not checked" in c.detail for c in report.checks)


def test_a_suggestion_never_rides_on_a_pass(schema):
    with pytest.raises(ValueError):
        from lucidform.models import ValidationReport

        ValidationReport(status=Status.PASS, candidate_id="x", field_id="state", suggestion="Kerala")
