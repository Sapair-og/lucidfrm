"""Regression tests for docs/ISSUES.md LF-015: help for document numbers.

The first test replays the user's session from 2026-10-01 (screenshot):
Voter ID chosen, then "how to get the number of voter id", "how to get it",
"how to get that document".
"""

from __future__ import annotations

import pytest

from lucidform.eval.events import EventLog
from lucidform.extract.client import ScriptedClient
from lucidform.extract.extractor import Extractor
from lucidform.extract.schema import Extraction, Intent
from lucidform.formstate.state import FormState
from lucidform.gate.gate import ValidationGate
from lucidform.orchestrate.session import Session
from lucidform.schema import loader
from tests.test_session import Puppet, value


@pytest.fixture(scope="module")
def official():
    return loader.load_official()


def run(schema, ids, extractions, replies, tmp_path, **kw):
    sub = type(schema)(
        form_id=schema.form_id, version=1, title="t",
        fields=tuple(schema.by_id(i) for i in ids),
    )
    log = EventLog(tmp_path, session_id="docs")
    channel = Puppet(replies)
    state = FormState(log=log)
    result = Session(
        schema=sub, extractor=Extractor(ScriptedClient(extractions), sub, log=log),
        gate=ValidationGate(sub), state=state,
        input_channel=channel, output_channel=channel, log=log, **kw,
    ).run()
    return result, state, channel


VOTER = value(value="Voter ID", quote="voter id")
FIND = Extraction(intent=Intent.FIND)
QUESTION = Extraction(intent=Intent.QUESTION)
DECLINE = Extraction(intent=Intent.DECLINE)


def test_the_screenshot_session(official, tmp_path):
    _, _, channel = run(
        official, ("poi_type", "poi_number"),
        [VOTER, FIND, FIND, QUESTION],
        ["voter id", "yes", "how to get the number of voter id", "how to get it", "how to get that document"],
        tmp_path,
    )
    said = [t for _, t in channel.said]
    helps = [t for t in said if "electoralsearch.eci.gov.in" in t]
    assert len(helps) == 2  # both lookup requests answered for Voter ID
    assert not any("I am not certain" in t for t in said)
    # the third request, over the budget, is told so rather than met with silence
    assert any("explained all I can" in t for t in said)


def test_how_to_get_the_document_question_gets_lookup_help(official, tmp_path):
    _, _, channel = run(
        official, ("poi_type", "poi_number"),
        [VOTER, QUESTION], ["voter id", "yes", "how to get that document"], tmp_path,
    )
    assert any("Form 6" in t for _, t in channel.said)


@pytest.mark.parametrize("doc,marker", [
    ("Passport", "passportindia.gov.in"),
    ("Driving Licence", "mParivahan"),
    ("NREGA Job Card", "nrega.nic.in"),
    ("NPR Letter", "National Population Register"),
])
def test_help_matches_the_chosen_document(official, tmp_path, doc, marker):
    _, _, channel = run(
        official, ("poi_type", "poi_number"),
        [value(value=doc, quote=doc.casefold()), FIND], [doc.casefold(), "yes", "?"], tmp_path,
    )
    assert any(marker in t for _, t in channel.said)


def test_no_document_reopens_the_choice(official, tmp_path):
    # no voter ID -> back to proof of identity -> Aadhaar -> no number needed
    result, state, channel = run(
        official, ("poi_type", "poi_number", "address_line"),
        [VOTER, DECLINE, value(value="Aadhaar", quote="aadhaar"), value(value="12 MG Road", quote="12 mg road")],
        ["voter id", "yes", "i dont have voter id", "aadhaar", "yes", "12 mg road", "yes", "yes"],
        tmp_path,
    )
    assert state.values == {"poi_type": "Aadhaar", "address_line": "12 MG Road"}
    assert any("choose a different" in t for _, t in channel.said)
    assert result.complete and result.approved
    assert "poi_number" not in {r.field_id for r in result.fields}


def test_reopen_to_another_document_asks_its_number(official, tmp_path):
    result, state, _ = run(
        official, ("poi_type", "poi_number"),
        [VOTER, DECLINE, value(value="Passport", quote="passport"), value(value="K1234567", quote="K1234567")],
        ["voter id", "yes", "i dont have it", "passport", "yes", "K1234567", "yes", "yes"],
        tmp_path,
    )
    assert state.values == {"poi_type": "Passport", "poi_number": "K1234567"}
    assert result.complete


def test_current_address_document_has_the_same_help(official):
    f = official.by_id("cur_poa_number")
    assert f.decline_reopens == "cur_poa_type"
    assert "electoralsearch" in f.find_text("en", {"cur_poa_type": "Voter ID"})
