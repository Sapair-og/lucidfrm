"""The event log is the evaluation substrate, so its guarantees are tested.

Everything reported in the results section is derived from these files. If the
log can lose a record, reorder one, or be rewritten after the fact, then every
number downstream is unverifiable.
"""

from __future__ import annotations

import json

import pytest

from lucidform.eval.events import Event, EventLog, read_log
from lucidform.models import Candidate, Reason, Status, ValidationReport


@pytest.fixture
def log(tmp_path):
    return EventLog(tmp_path, session_id="testsession", meta={"persona": "p01"})


def test_session_start_is_written_on_construction(log):
    records = read_log(log.path)
    assert len(records) == 1
    assert records[0]["event"] == Event.SESSION_START.value
    assert records[0]["payload"]["persona"] == "p01"


def test_records_are_appended_never_overwritten(log):
    for i in range(5):
        log.emit(Event.FIELD_ASKED, field_id=f"f{i}", turn_idx=i)

    records = read_log(log.path)
    assert len(records) == 6  # session_start + 5
    # Sequence numbers are monotonic and gap-free, so a dropped write is
    # detectable in the analysis rather than invisible.
    assert [r["seq"] for r in records] == list(range(1, 7))


def test_a_second_log_on_the_same_session_appends(tmp_path):
    """Reopening a session must not truncate what is already there.

    A crash-and-resume that silently discarded the first half of a run would
    produce a plausible-looking but incomplete log.
    """
    first = EventLog(tmp_path, session_id="resume")
    first.emit(Event.FIELD_ASKED, field_id="pan")
    second = EventLog(tmp_path, session_id="resume")
    second.emit(Event.FIELD_ASKED, field_id="aadhaar")

    events = [r["event"] for r in read_log(second.path)]
    assert events.count(Event.SESSION_START.value) == 2
    assert len(events) == 4


def test_dataclass_payloads_are_serialised(log):
    candidate = Candidate(
        field_id="pan", value="AKQPS3417M", raw_utterance="my pan is...", confidence=0.9
    )
    log.emit(Event.EXTRACTION, field_id="pan", payload=candidate)

    payload = read_log(log.path)[-1]["payload"]
    assert payload["value"] == "AKQPS3417M"
    assert payload["candidate_id"] == candidate.candidate_id


def test_enums_inside_payloads_become_their_values(log):
    report = ValidationReport(
        status=Status.REJECT,
        candidate_id="c1",
        field_id="aadhaar",
        reason=Reason.CHECKSUM,
        detail="verhoeff failed",
    )
    log.emit(Event.VALIDATION, field_id="aadhaar", payload=report)

    payload = read_log(log.path)[-1]["payload"]
    assert payload["status"] == "reject"
    assert payload["reason"] == "checksum"
    # Must be plain JSON -- the analysis step reads these files without
    # importing the package.
    json.dumps(payload)


def test_timed_records_latency_and_a_payload_set_inside_the_block(log):
    with log.timed(Event.EXTRACTION, field_id="pan") as box:
        box["model"] = "claude-opus-5-5"

    record = read_log(log.path)[-1]
    assert record["latency_ms"] is not None
    assert record["latency_ms"] >= 0
    assert record["payload"]["model"] == "claude-opus-5-5"


def test_timed_still_emits_when_the_block_raises(log):
    """A stage that throws is exactly the stage worth having a record of."""
    with pytest.raises(RuntimeError):
        with log.timed(Event.EXTRACTION, field_id="pan") as box:
            box["note"] = "about to fail"
            raise RuntimeError("boom")

    record = read_log(log.path)[-1]
    assert record["event"] == Event.EXTRACTION.value
    assert record["payload"]["note"] == "about to fail"
    assert record["latency_ms"] is not None


def test_latency_is_null_when_unmeasured_not_zero(log):
    """Null means "not applicable"; zero would mean "instantaneous".

    Conflating them would drag every latency percentile toward zero.
    """
    log.emit(Event.FIELD_ASKED, field_id="pan")
    assert read_log(log.path)[-1]["latency_ms"] is None


def test_the_log_exposes_no_way_to_update_or_delete():
    """Append-only is enforced by the absence of an API, not by convention."""
    for forbidden in ("update", "delete", "remove", "rewrite", "truncate", "clear"):
        assert not hasattr(EventLog, forbidden), f"EventLog exposes {forbidden}()"


def test_unicode_survives_the_round_trip(log):
    """Hindi utterances must not be mangled into escapes.

    The logs are read by a human during error analysis; \\u0928\\u093e\\u092e is
    not reviewable.
    """
    log.emit(Event.USER_UTTERANCE, payload={"text": "मेरा नाम अब्दुल है"})
    raw = log.path.read_text(encoding="utf-8")
    assert "मेरा नाम" in raw
    assert read_log(log.path)[-1]["payload"]["text"] == "मेरा नाम अब्दुल है"


def test_session_end_closes_the_record(log):
    log.close({"completed": True})
    assert read_log(log.path)[-1]["event"] == Event.SESSION_END.value


def test_silent_write_blocked_is_a_first_class_event():
    """Not a swallowed error -- a logged finding (SPEC.md section 2)."""
    assert Event.SILENT_WRITE_BLOCKED.value == "silent_write_blocked"


def test_voice_events_exist_before_the_voice_channel_does():
    """Declared in Phase 0 so the log schema does not change in Phase 7.

    A schema change mid-project would make early and late runs non-comparable.
    """
    assert Event.ASR_RESULT and Event.TTS_EMIT
