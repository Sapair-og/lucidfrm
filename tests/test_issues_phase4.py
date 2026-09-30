"""Regression tests for docs/ISSUES.md LF-006: revisit missing fields, final review."""

from __future__ import annotations

import pytest

from lucidform.eval.events import EventLog
from lucidform.extract.client import ScriptedClient
from lucidform.extract.extractor import Extractor
from lucidform.formstate.state import FormState
from lucidform.gate.gate import ValidationGate
from lucidform.orchestrate.graph import field_named
from lucidform.orchestrate.session import Session
from lucidform.schema import loader
from tests.test_session import Puppet, value


@pytest.fixture(scope="module")
def schema():
    return loader.load()


def two_fields(schema, extractions, replies, tmp_path, ids=("city", "state")):
    sub = type(schema)(
        form_id=schema.form_id,
        version=schema.version,
        title=schema.title,
        fields=tuple(schema.by_id(i) for i in ids),
    )
    log = EventLog(tmp_path, session_id="p4")
    channel = Puppet(replies)
    state = FormState(log=log)
    session = Session(
        schema=sub,
        extractor=Extractor(ScriptedClient(extractions), sub, log=log),
        gate=ValidationGate(sub),
        state=state,
        input_channel=channel,
        output_channel=channel,
        log=log,
        max_attempts=1,
    )
    return session.run(), state, channel


CITY = value(value="Jaipur", quote="jaipur")
STATE = value(value="Rajasthan", quote="rajasthan")


def test_a_missing_field_is_asked_again_before_the_end(schema, tmp_path):
    # city fails its single attempt, state succeeds, then city is revisited
    result, state, channel = two_fields(
        schema,
        [value(value="x@", quote="x@"), STATE, CITY],
        ["x@", "rajasthan", "yes", "jaipur", "yes", "yes"],
        tmp_path,
    )
    assert state.values == {"city": "Jaipur", "state": "Rajasthan"}
    assert any("still missing" in t for _, t in channel.said)
    assert result.complete and result.approved


def test_nothing_is_approved_without_a_final_yes(schema, tmp_path):
    result, state, channel = two_fields(
        schema, [CITY, STATE], ["jaipur", "yes", "rajasthan", "yes"], tmp_path
    )
    assert result.complete and not result.approved
    assert any("Here is everything" in t for _, t in channel.said)


def test_change_a_field_at_the_review(schema, tmp_path):
    result, state, channel = two_fields(
        schema,
        [CITY, STATE, value(value="Kota", quote="kota")],
        ["jaipur", "yes", "rajasthan", "yes", "change city", "kota", "yes", "yes"],
        tmp_path,
    )
    assert state.values["city"] == "Kota"
    assert result.approved
    assert [r.field_id for r in result.fields].count("city") == 1


def test_changing_then_giving_nothing_keeps_the_confirmed_value(schema, tmp_path):
    result, state, _ = two_fields(
        schema,
        [CITY, STATE],
        ["jaipur", "yes", "rajasthan", "yes", "change city"],
        tmp_path,
    )
    assert state.values["city"] == "Jaipur"
    assert next(r for r in result.fields if r.field_id == "city").committed


def test_an_unclear_review_reply_asks_again(schema, tmp_path):
    result, _, channel = two_fields(
        schema,
        [CITY, STATE],
        ["jaipur", "yes", "rajasthan", "yes", "hmm", "yes"],
        tmp_path,
    )
    assert result.approved
    assert any("did not understand" in t for _, t in channel.said)


def test_a_hedged_yes_does_not_approve(schema, tmp_path):
    result, _, _ = two_fields(
        schema,
        [CITY, STATE],
        ["jaipur", "yes", "rajasthan", "yes", "yes I think so"],
        tmp_path,
    )
    assert not result.approved


@pytest.mark.parametrize(
    "said,field_id",
    [
        ("change city", "city"),
        ("father's name is wrong", "father_name"),
        ("the pan number", "pan"),
        ("mobile number galat hai", "mobile"),
        ("change my name", "full_name"),
        ("aadhar", "aadhaar"),
    ],
)
def test_field_named(schema, said, field_id):
    fields = list(schema)
    assert fields[field_named(said, fields)].id == field_id


def test_field_named_does_not_guess(schema):
    assert field_named("something else entirely", list(schema)) is None


def test_export_stamps_an_unfinished_form(schema, tmp_path):
    from pypdf import PdfReader

    from lucidform.formstate.writer import export

    out = export(FormState(), schema, tmp_path / "f.pdf", stamp="INCOMPLETE")
    assert "INCOMPLETE" in PdfReader(str(out)).pages[0].extract_text()
    clean = export(FormState(), schema, tmp_path / "g.pdf")
    assert "INCOMPLETE" not in PdfReader(str(clean)).pages[0].extract_text()
