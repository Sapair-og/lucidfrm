"""Regression tests for docs/ISSUES.md LF-012: "I have a PAN but can't find the number"."""

from __future__ import annotations

import pytest

from lucidform.extract.schema import Extraction, Intent
from lucidform.schema import loader
from tests.test_session import one_field, value


@pytest.fixture(scope="module")
def schema():
    return loader.load()


FIND = Extraction(intent=Intent.FIND)


def test_find_help_is_given_and_the_field_asked_again(schema, tmp_path):
    result, state, channel, _ = one_field(
        schema, "pan",
        [FIND, value(value="AKQPS3417M", quote="akqps3417m")],
        ["mere paas pan hai par number yaad nahi", "akqps3417m", "yes"],
        tmp_path,
    )
    said = " ".join(t for _, t in channel.said)
    assert "DigiLocker" in said and "incometax.gov.in" in said and "youtube.com" in said
    assert state.values["pan"] == "AKQPS3417M"
    assert result.fields[0].attempts == 0  # help is not a failed attempt
    assert result.fields[0].questions == 1


def test_cant_find_is_not_a_decline(schema, tmp_path):
    # having a PAN but not the number must never be offered Form 60
    _, state, channel, _ = one_field(schema, "pan", [FIND], ["i can't find it"], tmp_path)
    assert not any("Form 60" in t for _, t in channel.said)
    assert "pan" not in state.values


def test_aadhaar_find_help_uses_uidai(schema, tmp_path):
    _, _, channel, _ = one_field(schema, "aadhaar", [FIND], ["aadhaar number yaad nahi"], tmp_path)
    assert any("myaadhaar.uidai.gov.in" in t for _, t in channel.said)


def test_find_help_in_hindi(schema, tmp_path):
    _, _, channel, _ = one_field(schema, "pan", [FIND], ["pan number nahi mil raha"], tmp_path, lang="hi")
    assert any("डिजीलॉकर" in t for _, t in channel.said)


def test_field_without_find_help_falls_back_to_the_explanation(schema, tmp_path):
    _, _, channel, _ = one_field(schema, "city", [FIND], ["pata nahi"], tmp_path)
    assert any(k == "explanation" for k, _ in channel.said)


def test_official_form_inherits_pan_find_help():
    assert "DigiLocker" in loader.load_official().by_id("pan").find_help["en"]


def test_repeated_find_requests_are_bounded(schema, tmp_path):
    result, _, _, _ = one_field(schema, "pan", [FIND] * 6, ["?"] * 6, tmp_path, max_questions=2)
    assert result.fields[0].questions <= 2 * 2  # per visit, one end-of-form revisit
