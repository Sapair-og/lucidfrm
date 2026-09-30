"""The synthetic corpus must be internally consistent.

Accuracy is measured against persona ground truth, so a persona carrying an
invalid PAN or a PIN that disagrees with its state would be scored against a
wrong answer -- silently corrupting every figure derived from it, in the
direction that makes the gate look worse than it is.

These tests also double as a guard on the data-generation story in
METHODOLOGY M0.8: they confirm the Aadhaar numbers really do satisfy Verhoeff,
so the checksum path in the gate is genuinely exercised rather than nominally
present.
"""

from __future__ import annotations

import datetime as dt
import re

import pytest

from lucidform.eval.personas import load_all
from lucidform.gate import checksums as ck
from lucidform.gate.regions import pin_matches_state
from lucidform.schema import loader

PAN_RE = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
MOBILE_RE = re.compile(r"^[6-9][0-9]{9}$")
PIN_RE = re.compile(r"^[1-9][0-9]{5}$")


@pytest.fixture(scope="module")
def personas():
    found = load_all()
    assert found, "no personas found -- the eval corpus is empty"
    return found


@pytest.fixture(scope="module")
def schema():
    return loader.load()


def test_persona_ids_are_unique(personas):
    ids = [p.persona_id for p in personas]
    assert len(set(ids)) == len(ids)


def test_ground_truth_covers_every_required_field(personas, schema):
    """A persona that cannot answer a required field would abandon it mid-run,
    which reads as a pipeline failure rather than a corpus gap."""
    for p in personas:
        for field in schema:
            if not field.required:
                continue
            assert p.truth(field.id), f"{p.persona_id}: no ground truth for {field.id}"


def test_ground_truth_declares_no_unknown_fields(personas, schema):
    known = set(schema.ids)
    for p in personas:
        unknown = set(p.ground_truth) - known
        assert not unknown, f"{p.persona_id}: unknown field(s) {sorted(unknown)}"


def test_aadhaar_numbers_satisfy_verhoeff(personas):
    """If these were invalid, the checksum branch of the gate would never be
    reached on a happy-path run and its recall would be untested."""
    for p in personas:
        aadhaar = p.truth("aadhaar")
        assert ck.aadhaar_valid(aadhaar), f"{p.persona_id}: {aadhaar} fails Verhoeff"


def test_pan_is_well_formed_and_agrees_with_the_surname(personas):
    """PAN's fifth character is the surname's first letter.

    This is the cross-field check the gate performs, so the corpus has to
    satisfy it -- otherwise every persona would be rejected on a correct answer
    and the false-positive rate would read 100%.
    """
    for p in personas:
        pan = p.truth("pan")
        assert PAN_RE.match(pan), f"{p.persona_id}: malformed PAN {pan}"
        surname = p.truth("full_name").split()[-1]
        assert pan[4] == surname[0].upper(), (
            f"{p.persona_id}: PAN 5th char {pan[4]!r} does not match "
            f"surname {surname!r}"
        )


def test_pin_agrees_with_state(personas):
    for p in personas:
        assert pin_matches_state(p.truth("pin"), p.truth("state")) is True, (
            f"{p.persona_id}: PIN {p.truth('pin')} is not in the postal region "
            f"for {p.truth('state')}"
        )
        assert PIN_RE.match(p.truth("pin"))


def test_mobile_numbers_are_well_formed(personas):
    for p in personas:
        assert MOBILE_RE.match(p.truth("mobile")), f"{p.persona_id}: bad mobile"


def test_everyone_is_an_adult(personas):
    """The form states an 18-year minimum, and the gate enforces it."""
    today = dt.date.today()
    for p in personas:
        dob = dt.date.fromisoformat(p.truth("dob"))
        age = (today - dob).days // 365
        assert age >= 18, f"{p.persona_id}: age {age}"


def test_enum_values_are_in_the_permitted_set(personas, schema):
    for p in personas:
        for field in schema:
            if not field.enum_values:
                continue
            value = p.truth(field.id)
            if not value:
                continue
            assert value in field.enum_values, (
                f"{p.persona_id}: {field.id}={value!r} not in {field.enum_values}"
            )


def test_optional_fields_may_be_declined_but_must_still_be_answerable(personas):
    """A persona who has no email still has to say so out loud.

    An empty ground truth means "declines this field", which the pipeline must
    record as a skip. It does not mean the field is never asked.
    """
    for p in personas:
        for field_id, value in p.ground_truth.items():
            if value == "":
                assert p.utterances(field_id), (
                    f"{p.persona_id}: declines {field_id} but says nothing"
                )


def test_email_addresses_use_a_reserved_domain(personas):
    """.invalid is reserved by RFC 2606 and can never resolve.

    A synthetic corpus that used a real-looking domain could send mail to a
    real person if anything ever acted on these values.
    """
    for p in personas:
        email = p.truth("email")
        if email:
            assert email.endswith(".invalid"), f"{p.persona_id}: {email}"


def test_every_persona_declares_a_synthetic_header(personas):
    """The data provenance claim in METHODOLOGY M0.8 is only true if the files
    actually say so -- this keeps the claim and the corpus in step."""
    for p in personas:
        head = p.source.read_text(encoding="utf-8")[:600].upper()
        assert "SYNTHETIC" in head, f"{p.source.name}: no SYNTHETIC header"
        assert "NOT REAL PII" in head, f"{p.source.name}: no PII disclaimer"


def test_a_persona_with_no_utterances_is_rejected(tmp_path):
    """The loader must refuse a persona the replay driver could not run."""
    from lucidform.eval.personas import PersonaError, load_persona

    path = tmp_path / "broken.yaml"
    path.write_text(
        "persona_id: bad\nground_truth:\n  pan: AKQPS3417M\nturns: {}\n",
        encoding="utf-8",
    )
    with pytest.raises(PersonaError, match="no utterances"):
        load_persona(path)
