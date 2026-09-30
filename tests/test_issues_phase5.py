"""Regression tests for docs/ISSUES.md LF-001: filling the official CKYC form."""

from __future__ import annotations

import datetime as dt

import pytest
from pypdf import PdfReader

from lucidform.eval.events import EventLog
from lucidform.extract.client import ScriptedClient
from lucidform.extract.extractor import Extractor
from lucidform.formstate.official_writer import export_official, split_name, wrap
from lucidform.formstate.state import FormState
from lucidform.gate import regions
from lucidform.gate.gate import ValidationGate
from lucidform.models import Candidate, Status
from lucidform.orchestrate.session import Session
from lucidform.schema import loader
from tests.test_session import Puppet, value


@pytest.fixture(scope="module")
def official():
    return loader.load_official()


def _gate(schema, field_id, v, committed=None, today=None):
    cand = Candidate(field_id=field_id, value=v, raw_utterance=v, confidence=0.95)
    return ValidationGate(schema, today=today).check(cand, committed or {})


# -- schema --------------------------------------------------------------------


def test_official_schema_inherits_from_the_template(official):
    template = loader.load()
    assert official.by_id("pan").prompt == template.by_id("pan").prompt
    assert official.by_id("pan").decline_value == "Form 60"
    assert official.by_id("cur_pin").prompt["en"].startswith("What is the six-digit PIN code of your current")
    assert official.by_id("address_line").max_length == 128


def test_conditional_fields(official):
    number = official.by_id("poi_number")
    assert number.applies({"poi_type": "Passport"})
    assert not number.applies({"poi_type": "Aadhaar"})
    assert not number.applies({})
    assert official.by_id("cur_pin").applies({"same_address": "No"})
    assert not official.by_id("cur_pin").applies({"same_address": "Yes"})


# -- gate rules for the new fields --------------------------------------------


def test_expired_document_is_rejected(official):
    today = dt.date(2026, 9, 30)
    assert _gate(official, "poi_expiry", "2025-01-01", today=today).status is Status.REJECT
    assert _gate(official, "poi_expiry", "2031-05-20", today=today).status is Status.PASS


@pytest.mark.parametrize(
    "doc,number,ok",
    [
        ("Passport", "K1234567", True),
        ("Passport", "K12345", False),
        ("Voter ID", "ABC1234567", True),
        ("Voter ID", "AB12345678", False),
        ("Driving Licence", "RJ14 20110012345", True),  # state formats vary: length only
    ],
)
def test_document_number_shape(official, doc, number, ok):
    report = _gate(official, "poi_number", number, {"poi_type": doc})
    assert (report.status is Status.PASS) is ok


def test_current_address_is_checked_against_its_own_pin(official):
    committed = {"pin": "221001", "state": "Uttar Pradesh", "cur_pin": "466114"}
    assert _gate(official, "cur_state", "Uttar Pradesh", committed).status is Status.REJECT
    assert _gate(official, "cur_state", "Madhya Pradesh", committed).status is Status.PASS


def test_proposals():
    assert regions.propose("district", {"pin": "466114"})[0] == "Sehore"
    assert regions.propose("cur_state", {"cur_pin": "226001"})[0] == "Uttar Pradesh"
    assert regions.propose("place", {"city": "Varanasi"})[0] == "Varanasi"
    assert regions.propose("district", {}) is None


# -- conversation --------------------------------------------------------------


def _session(schema, ids, extractions, replies, tmp_path):
    sub = type(schema)(
        form_id=schema.form_id, version=schema.version, title=schema.title,
        fields=tuple(schema.by_id(i) for i in ids),
    )
    log = EventLog(tmp_path, session_id="official")
    channel = Puppet(replies)
    state = FormState(log=log)
    result = Session(
        schema=sub,
        extractor=Extractor(ScriptedClient(extractions), sub, log=log),
        gate=ValidationGate(sub), state=state,
        input_channel=channel, output_channel=channel, log=log,
    ).run()
    return result, state, channel


def test_a_field_that_does_not_apply_is_not_asked(official, tmp_path):
    result, state, channel = _session(
        official,
        ("poi_type", "poi_number", "poi_expiry"),
        [value(value="Aadhaar", quote="aadhaar")],
        ["aadhaar", "yes", "yes"],
        tmp_path,
    )
    assert state.values == {"poi_type": "Aadhaar"}
    assert result.complete and result.approved
    assert not any("number printed on that document" in t for _, t in channel.said)


def test_passport_asks_number_and_expiry(official, tmp_path):
    result, state, _ = _session(
        official,
        ("poi_type", "poi_number", "poi_expiry"),
        [
            value(value="Passport", quote="passport"),
            value(value="K1234567", quote="K1234567"),
            value(value="2031-05-20", quote="20 may 2031"),
        ],
        ["passport", "yes", "K1234567", "yes", "20 may 2031", "yes", "yes"],
        tmp_path,
    )
    assert state.values["poi_number"] == "K1234567"
    assert state.values["poi_expiry"] == "2031-05-20"


# -- writer --------------------------------------------------------------------


class _Values:
    def __init__(self, values):
        self.values = values


SAMPLE = {
    "prefix": "Mr", "full_name": "Suresh Prasad Yadav", "father_name": "Ram Prasad Yadav",
    "dob": "1958-03-14", "gender": "Male", "pan": "AFRPY4521K", "marital_status": "Married",
    "citizenship": "Indian", "residential_status": "Resident Individual",
    "poi_type": "Passport", "poi_number": "K1234567", "poi_expiry": "2031-05-20",
    "address_line": "Sarai Mohana, Rajghat", "pin": "221001", "district": "Varanasi",
    "city": "Varanasi", "state": "Uttar Pradesh", "same_address": "Yes",
    "mobile": "9839012457", "email": "suresh@gmail.com", "place": "Varanasi",
}


def _text(path, page=0):
    return PdfReader(str(path)).pages[page].extract_text()


def _drawn(path, page=0):
    """(text, x, y_from_top) for every string drawn on the page, via pypdf."""
    pg = PdfReader(str(path)).pages[page]
    height = float(pg.mediabox.height)
    out = []

    def visit(text, cm, tm, font, size):
        if text.strip():
            out.append((text.strip(), tm[4] * cm[0] + cm[4], height - (tm[5] * cm[3] + cm[5])))

    pg.extract_text(visitor_text=visit)
    return out


def _row(path, top, bottom, x0, x1, page=0):
    """Characters drawn inside one row of boxes, left to right."""
    hits = sorted(
        (x, t) for t, x, y in _drawn(path, page) if top <= y <= bottom + 1 and x0 - 6 <= x <= x1
    )
    return "".join(t for _, t in hits)


def test_writer_puts_values_in_their_boxes(official, tmp_path):
    out = export_official(_Values(SAMPLE), official, tmp_path / "f.pdf", today=dt.date(2026, 9, 30))
    assert len(PdfReader(str(out)).pages) == 4  # the whole official document
    assert _row(out, 209, 219.2, 172.1, 291.1) == "SURESH"  # first name
    assert _row(out, 209, 219.2, 442.8, 561.9) == "YADAV"  # last name
    assert _row(out, 292, 302.2, 130.7, 229.9) == "AFRPY4521K"  # PAN
    assert _row(out, 379, 389.7, 123.3, 202.7) == "K1234567"  # passport number
    assert _row(out, 548, 558.8, 263.1, 322.6) == "221001"  # PIN
    assert _row(out, 548, 558.8, 408.2, 428.0) == "UP"  # state code
    assert _row(out, 80, 90.8, 63.5, 390.9, page=1) == "suresh@gmail.com"  # case kept


def test_writer_skips_values_that_no_longer_apply(official, tmp_path):
    stale = {**SAMPLE, "poi_type": "Aadhaar"}  # a passport number is still stored
    out = export_official(_Values(stale), official, tmp_path / "g.pdf", today=dt.date(2026, 9, 30))
    assert _row(out, 379, 389.7, 123.3, 202.7) == ""


def test_form_60_ticks_the_box_instead_of_writing(official, tmp_path):
    out = export_official(_Values({**SAMPLE, "pan": "Form 60"}), official, tmp_path / "h.pdf")
    assert _row(out, 292, 302.2, 130.7, 229.9) == ""  # PAN boxes left empty
    assert _row(out, 290, 304, 296.0, 310.0) == "X"  # FORM 60 furnished ticked


def test_name_and_address_helpers():
    assert split_name("Suresh Prasad Yadav") == ("Suresh", "Prasad", "Yadav")
    assert split_name("Lakshmi") == ("Lakshmi", "", "")
    assert split_name("A B C D") == ("A", "B C", "D")
    lines = wrap("House 12, Sarai Mohana, Near Rajghat Bridge, Adampura Ward", [20, 20, 10])
    assert all(len(line) <= 20 for line in lines[:2])
    assert " ".join(lines).split() == "House 12, Sarai Mohana, Near Rajghat Bridge, Adampura Ward".split()


def test_stamp_on_an_unfinished_official_form(official, tmp_path):
    out = export_official(_Values(SAMPLE), official, tmp_path / "s.pdf", stamp="INCOMPLETE")
    assert "INCOMPLETE" in _text(out)


def test_a_valid_option_the_model_was_unsure_of_is_offered(official):
    # live run: "voter card" -> model value "voter card", ambiguous, conf 0.4
    cand = Candidate(field_id="poi_type", value="voter card", raw_utterance="voter card",
                     confidence=0.4, ambiguous=True)
    report = ValidationGate(official).check(cand, {})
    assert report.status is Status.REJECT and report.suggestion == "Voter ID"


def test_an_ambiguous_date_is_still_not_offered(official):
    cand = Candidate(field_id="dob", value="1987-01-05", raw_utterance="5/1/87",
                     confidence=0.4, ambiguous=True)
    assert ValidationGate(official).check(cand, {}).suggestion is None
