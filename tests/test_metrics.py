"""The measures, and the guards on how they may be read.

Every number reported in the results section comes out of this module, so the
tests are as much about what it refuses to claim as about what it computes. Two
in particular: a session with no ground truth must be excluded from accuracy
rather than scored against an assumption, and figures produced offline must
carry the warning that they are not measurements.
"""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path

import pytest

from lucidform.eval import metrics
from lucidform.eval.events import Event, EventLog
from lucidform.eval.personas import load_all
from lucidform.eval.replay import run_persona
from lucidform.extract.client import ReplayClient
from lucidform.schema import loader

FIXTURES = Path(__file__).parent / "fixtures" / "extractions.json"


@pytest.fixture(scope="module")
def schema():
    return loader.load()


@pytest.fixture(scope="module")
def runs(schema):
    """Three real sessions, recorded into a scratch directory."""
    tmp = Path(tempfile.mkdtemp())
    client = ReplayClient(FIXTURES)
    for persona in load_all():
        run_persona(persona, schema, client, runs_dir=tmp)
    return tmp


@pytest.fixture(scope="module")
def sessions(runs, schema):
    return metrics.load_sessions(runs, schema)


@pytest.fixture(scope="module")
def agg(sessions):
    return metrics.aggregate(sessions)


# -- parsing -----------------------------------------------------------------


def test_every_session_is_parsed(sessions):
    assert len(sessions) == 3
    assert {s.persona_id for s in sessions} == {"p01", "p02", "p03"}


def test_a_question_and_the_answer_after_it_are_separate_turns(sessions):
    """A turn is delimited by the ask, not by the logged turn index.

    An explanation request does not advance that index, so grouping on it would
    merge the question and the answer into one record and hide the question
    entirely.
    """
    p03 = next(s for s in sessions if s.persona_id == "p03")
    pan_turns = [t for t in p03.turns if t.field_id == "pan"]
    assert len(pan_turns) == 2
    assert pan_turns[0].intent == "question"
    assert pan_turns[1].intent == "value"


def test_field_outcomes_record_how_each_field_ended(sessions):
    p03 = next(s for s in sessions if s.persona_id == "p03")
    by_id = {f.field_id: f for f in p03.fields}
    assert by_id["email"].resolution == "declined"
    assert by_id["pan"].resolution == "committed"
    assert by_id["pan"].questions == 1


def test_turn_records_carry_both_confidence_figures(sessions):
    """The gap between reported and clamped confidence is itself a measure."""
    turns = [t for s in sessions for t in s.turns if t.intent == "value"]
    assert turns
    assert all(t.reported_confidence is not None for t in turns)
    assert all(t.confidence is not None for t in turns)


# -- correctness of the classification ---------------------------------------


def test_normalisation_is_applied_before_judging_a_proposal(schema):
    """"+91 98123 45607" and "9812345607" are the same answer.

    Judging a proposal on its punctuation would overstate the error rate.
    """
    persona = next(p for p in load_all() if p.persona_id == "p01")
    assert metrics._is_correct("+91 98123 45607", "mobile", persona, schema)
    assert metrics._is_correct("9812345607", "mobile", persona, schema)
    assert not metrics._is_correct("9812345600", "mobile", persona, schema)


def test_the_wrong_values_in_the_corpus_are_identified(agg):
    """Six deliberate errors are planted across the three personas."""
    assert agg.proposals_wrong == 6
    assert agg.proposals_correct == agg.proposals - 6


# -- the layered result ------------------------------------------------------


def test_the_layers_account_for_every_wrong_value(agg):
    """The headline table must balance.

    A wrong value is stopped by the gate, stopped by the read-back, or
    committed. If these do not sum, something is being counted twice or not at
    all -- and the missing case would be a value nobody stopped.
    """
    accounted = (
        agg.gate_rejected_wrong + agg.readback_caught_wrong + agg.escaped_errors
    )
    assert accounted == agg.proposals_wrong, (
        f"{agg.proposals_wrong} wrong proposals but {accounted} accounted for"
    )


def test_nothing_wrong_was_committed(agg):
    """The correctness invariant. A defect, not a finding."""
    assert agg.escaped_errors == 0


def test_the_read_back_caught_what_the_gate_could_not(agg):
    """The evidence that the read-back is a stage rather than a courtesy.

    These are values the gate accepted because nothing about them is malformed
    -- they are simply not what the user said.
    """
    assert agg.readback_caught_wrong >= 1
    assert agg.gate_passed_wrong == agg.readback_caught_wrong, (
        "every wrong value the gate let through should have been denied at "
        "read-back; one that was not would be an escaped error"
    )


def test_the_gate_rejected_no_correct_value(agg):
    """A false positive is a real user told their correct answer is wrong."""
    assert agg.gate_rejected_correct == 0
    assert agg.gate_false_positive_rate == 0.0


def test_recall_and_false_positive_rate_are_both_reported(agg):
    """Recall alone is not a result: a gate that rejects everything scores 100%."""
    assert agg.gate_recall is not None
    assert agg.gate_false_positive_rate is not None
    row = agg.as_row()
    assert "gate_recall" in row and "gate_false_positive_rate" in row


def test_no_write_was_blocked(agg):
    assert agg.blocked_writes == 0


# -- what the measures refuse to claim ---------------------------------------


def test_offline_sessions_are_flagged_as_not_measuring_accuracy(agg):
    """The circularity warning must travel with the number."""
    assert agg.offline_only
    caveats = " ".join(agg.caveats())
    assert "Extraction accuracy is NOT a result" in caveats
    assert "Latency is NOT a result" in caveats


def test_the_caveat_survives_into_the_csv(agg):
    """A row lifted out of the CSV into a paper still carries the warning."""
    row = agg.as_row()
    assert row["offline_only"] is True
    assert row["clients"] == "ReplayClient"


def test_a_small_sample_is_flagged_rather_than_quoted_as_a_rate(agg):
    assert any("Too few to quote as a rate" in c for c in agg.caveats())


def test_a_session_without_ground_truth_is_excluded_from_accuracy(schema, tmp_path):
    """A real user's session has no correct answer to score against.

    It must contribute latency and rejection reasons without being scored
    against an assumed answer.
    """
    log = EventLog(tmp_path, session_id="anonymous", meta={"lang": "en"})
    log.emit(Event.FIELD_ASKED, field_id="city")
    log.emit(
        Event.EXTRACTION,
        field_id="city",
        payload={"intent": "value", "value": "Jaipur", "confidence": 0.9},
    )
    log.close({"committed": ["city"], "declined": [], "abandoned": []})

    session = metrics.parse_session(log.path, schema)
    assert not session.has_ground_truth

    agg = metrics.aggregate([session])
    assert agg.scored_sessions == 0
    assert agg.proposals == 0, "an unscored proposal must not enter the accuracy base"
    assert agg.extraction_accuracy is None
    assert agg.gate_recall is None
    assert any("no persona" in c for c in agg.caveats())


def test_unscored_sessions_still_contribute_the_measures_that_need_no_truth(
    sessions, schema, tmp_path
):
    log = EventLog(tmp_path, session_id="mixed", meta={"lang": "en"})
    log.emit(Event.FIELD_ASKED, field_id="pin")
    log.emit(
        Event.VALIDATION,
        field_id="pin",
        payload={"status": "reject", "reason": "format", "normalized_value": ""},
    )
    log.close({"committed": [], "declined": [], "abandoned": ["pin"]})

    combined = metrics.aggregate(sessions + [metrics.parse_session(log.path, schema)])
    assert combined.sessions == 4
    assert combined.scored_sessions == 3
    assert combined.rejection_reasons["format"] >= 2


# -- percentiles -------------------------------------------------------------


def test_percentiles_are_values_that_actually_occurred():
    """Not interpolated. At prototype sample sizes an interpolated percentile
    reports a latency no request ever had."""
    values = [1.0, 2.0, 3.0, 4.0, 100.0]
    assert metrics.percentile(values, 50) in values
    assert metrics.percentile(values, 95) in values
    assert metrics.percentile(values, 100) == 100.0


def test_percentile_of_nothing_is_none_not_zero():
    """Zero would read as an instantaneous stage rather than an unmeasured one."""
    assert metrics.percentile([], 50) is None


# -- CSV output --------------------------------------------------------------


def test_all_tables_are_written(sessions, tmp_path):
    written = metrics.write_tables(sessions, tmp_path)
    assert set(written) == {"turns", "fields", "sessions", "summary", "rejections"}
    for path in written.values():
        assert path.exists() and path.stat().st_size > 0


def test_the_turns_table_has_one_row_per_turn(sessions, tmp_path):
    written = metrics.write_tables(sessions, tmp_path)
    with written["turns"].open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == sum(len(s.turns) for s in sessions)
    assert {"field_id", "validation_reason", "proposal_correct"} <= set(rows[0])


def test_the_fields_table_records_ground_truth_beside_what_was_committed(
    sessions, tmp_path
):
    """So a reader can audit the accuracy figure rather than trusting it."""
    written = metrics.write_tables(sessions, tmp_path)
    with written["fields"].open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    committed = [r for r in rows if r["resolution"] == "committed"]
    assert committed
    for row in committed:
        assert row["committed_value"] == row["ground_truth"]


def test_the_summary_is_a_single_row(sessions, tmp_path):
    written = metrics.write_tables(sessions, tmp_path)
    with written["summary"].open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 1
    assert rows[0]["escaped_errors"] == "0"


def test_the_report_names_the_invariant(agg):
    text = metrics.report(agg)
    assert "committed wrong" in text
    assert "invariant" in text
    assert "false positives" in text


def test_the_logs_are_internally_consistent(agg):
    """Every commit agrees with the validation verdict in the same turn.

    Unreachable through the pipeline, since the write path derives the value
    from the report. Checked anyway: the entire result rests on the logs being
    a faithful record, and that is an assumption worth testing rather than
    stating.
    """
    assert agg.log_inconsistencies == 0


def test_a_tampered_log_is_detected(runs, schema, tmp_path):
    """Guard on the guard above.

    A consistency check that has never been seen to fire is not evidence of
    consistency.
    """
    import json
    import shutil

    source = sorted(runs.glob("*.jsonl"))[0]
    target = tmp_path / source.name
    rows = [json.loads(line) for line in source.open(encoding="utf-8")]
    for row in rows:
        if row["event"] == "commit":
            row["payload"]["value"] = "Tampered"
            break
    with target.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    tampered = metrics.aggregate(metrics.load_sessions(tmp_path, schema))
    assert tampered.log_inconsistencies >= 1
    assert any("altered" in c for c in tampered.caveats())
