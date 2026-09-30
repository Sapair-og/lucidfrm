"""Regression tests for docs/ISSUES.md LF-003: PIN / city / state consistency.

The failing case is from the live session: city Kota, state Goa, PIN 466114.
"""

from __future__ import annotations

import pytest

from lucidform.extract.schema import Extraction, Intent
from lucidform.gate import crossfield, regions
from lucidform.gate.gate import ValidationGate
from lucidform.models import Candidate, Status
from lucidform.schema import loader
from tests.test_session import one_field, value


@pytest.fixture(scope="module")
def schema():
    return loader.load()


def _gate(schema, field_id, v, committed):
    cand = Candidate(field_id=field_id, value=v, raw_utterance=v, confidence=0.95)
    return ValidationGate(schema).check(cand, committed)


def test_directory_lookup():
    assert regions.pin_place("466114") == ("Madhya Pradesh", "Sehore")
    assert regions.pin_place("000000") is None


def test_same_region_wrong_state_is_now_caught(schema):
    # region 4 contains both MP and Goa; the old first-digit check passed this
    report = _gate(schema, "pin", "466114", {"state": "Goa"})
    assert report.status is Status.REJECT and report.reason.value == "cross_field"
    assert "Madhya Pradesh" in report.detail


def test_state_against_confirmed_pin(schema):
    assert _gate(schema, "state", "Goa", {"pin": "466114"}).status is Status.REJECT
    assert _gate(schema, "state", "Madhya Pradesh", {"pin": "466114"}).status is Status.PASS


def test_known_city_in_another_state_is_caught(schema):
    report = _gate(schema, "city", "Kota", {"pin": "466114"})
    assert report.status is Status.REJECT
    assert "Rajasthan" in report.detail and "Madhya Pradesh" in report.detail
    assert _gate(schema, "state", "Goa", {"city": "Kota"}).status is Status.REJECT


def test_unknown_city_is_never_rejected(schema):
    # a locality the directory does not list must not be a false positive
    assert _gate(schema, "city", "Rawatbhata", {"pin": "323307"}).status is Status.PASS


@pytest.mark.parametrize(
    "city,pin",
    [("Jaipur", "302015"), ("Kochi", "682016"), ("Bengaluru", "560001"), ("Varanasi", "221001")],
)
def test_correct_pairs_pass(schema, city, pin):
    assert _gate(schema, "city", city, {"pin": pin}).status is Status.PASS


def test_pin_missing_from_directory_falls_back_to_region(schema):
    # not in the directory, but a valid region-3 PIN for Rajasthan: not rejected
    assert regions.pin_place("399999") is None
    assert _gate(schema, "pin", "399999", {"state": "Rajasthan"}).status is Status.PASS


def test_state_is_proposed_from_the_pin_and_needs_a_yes(schema, tmp_path):
    single = type(schema)(
        form_id=schema.form_id, version=schema.version, title=schema.title,
        fields=(schema.by_id("pin"), schema.by_id("state")),
    )
    from lucidform.eval.events import EventLog
    from lucidform.extract.client import ScriptedClient
    from lucidform.extract.extractor import Extractor
    from lucidform.formstate.state import FormState
    from lucidform.orchestrate.session import Session
    from tests.test_session import Puppet

    log = EventLog(tmp_path, session_id="prop")
    channel = Puppet(["466114", "yes", "yes"])
    state = FormState(log=log)
    Session(
        schema=single,
        extractor=Extractor(ScriptedClient([value(value="466114", quote="466114")]), single, log=log),
        gate=ValidationGate(single), state=state,
        input_channel=channel, output_channel=channel, log=log,
    ).run()
    assert state.values == {"pin": "466114", "state": "Madhya Pradesh"}
    assert any("466114 is in Madhya Pradesh" in t for _, t in channel.said)
    assert ("state", "Madhya Pradesh") in channel.readbacks
