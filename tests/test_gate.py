"""Gate-level invariants: the contract the rest of the pipeline relies on.

Phase 2 builds the write path on top of these guarantees -- in particular that
a rejected candidate carries nothing committable, and that a verdict does not
depend on what the gate was asked previously.
"""

from __future__ import annotations

import datetime as dt

import pytest

from lucidform.gate.gate import CHECK_ORDER, ValidationGate
from lucidform.models import Candidate, Reason, Status, ValidationReport
from lucidform.schema import loader


@pytest.fixture(scope="module")
def schema():
    return loader.load()


@pytest.fixture(scope="module")
def gate(schema):
    return ValidationGate(schema, min_confidence=0.55)


def candidate(field_id, value, **kw):
    return Candidate(
        field_id=field_id,
        value=value,
        raw_utterance=kw.pop("utterance", value),
        confidence=kw.pop("confidence", 0.95),
        **kw,
    )


# -- the report contract -----------------------------------------------------


def test_a_rejection_carries_nothing_committable(gate):
    """The write path reads `normalized_value`. A rejected report must leave it
    empty so that a caller which ignored `status` still cannot commit anything.
    """
    report = gate.check(candidate("aadhaar", "747910984993"))
    assert report.status is Status.REJECT
    assert report.normalized_value == ""


def test_a_pass_carries_the_exact_value_that_will_be_written(gate):
    report = gate.check(candidate("mobile", "+91 98123 45607"))
    assert report.status is Status.PASS
    assert report.normalized_value == "9812345607"


def test_a_rejection_must_carry_a_reason():
    with pytest.raises(ValueError, match="must carry a reason"):
        ValidationReport(
            status=Status.REJECT, candidate_id="c1", field_id="pan"
        )


def test_a_pass_must_not_carry_a_reason():
    with pytest.raises(ValueError, match="must not carry a reason"):
        ValidationReport(
            status=Status.PASS,
            candidate_id="c1",
            field_id="pan",
            reason=Reason.FORMAT,
        )


def test_every_report_records_the_candidate_it_judged(gate):
    """So a receipt can be bound to one exact candidate in Phase 2."""
    cand = candidate("pan", "AKQPS3417M")
    report = gate.check(cand)
    assert report.candidate_id == cand.candidate_id
    assert report.field_id == "pan"


def test_every_report_records_the_checks_it_ran(gate):
    report = gate.check(candidate("aadhaar", "747910984992"))
    names = [c.name for c in report.checks]
    assert "verhoeff" in names
    assert "length" in names
    # Passed checks are recorded too -- the log should show what was
    # exercised, not only what tripped.
    assert all(c.passed for c in report.checks)


# -- determinism -------------------------------------------------------------


def test_the_same_input_always_gets_the_same_verdict(gate):
    """The point of a non-model validator.

    Reproducibility is what lets the adversarial suite stand as evidence: a
    verdict that varied between runs could not be cited at all.
    """
    verdicts = set()
    for _ in range(50):
        report = gate.check(
            candidate("pan", "AKQPS34I7M"), {"full_name": "Ramesh Kumar Sharma"}
        )
        verdicts.add((report.status, report.reason, report.detail))
    assert len(verdicts) == 1


def test_the_gate_keeps_no_state_between_candidates(gate):
    """A rejection must not colour the next verdict.

    The gate is used in a loop over fields; a leaked flag would make a value's
    acceptability depend on what the user said a minute earlier.
    """
    good = candidate("aadhaar", "747910984992")
    bad = candidate("aadhaar", "747910984993")

    first = gate.check(good).status
    gate.check(bad)
    gate.check(bad)
    assert gate.check(good).status is first is Status.PASS


def test_two_gates_agree(schema):
    """Construction order and instance identity must not matter."""
    a = ValidationGate(schema, min_confidence=0.55)
    b = ValidationGate(schema, min_confidence=0.55)
    cand = candidate("dob", "14/03/1987")
    assert a.check(cand).normalized_value == b.check(cand).normalized_value


# -- check order -------------------------------------------------------------


def test_check_order_covers_the_whole_taxonomy():
    """An unreachable reason code would be a column in the results table that
    always reads zero for reasons unrelated to the data."""
    assert set(CHECK_ORDER) == set(Reason)


def test_check_order_has_no_duplicates():
    assert len(CHECK_ORDER) == len(set(CHECK_ORDER))


def test_check_order_is_the_documented_sequence():
    """Pinned deliberately. The reported reason distribution shifts if this
    changes, so a reordering must be a conscious edit to this test as well."""
    assert CHECK_ORDER == (
        Reason.EMPTY,
        Reason.TYPE_MISMATCH,
        Reason.FORMAT,
        Reason.ENUM,
        Reason.CHECKSUM,
        Reason.RANGE,
        Reason.CROSS_FIELD,
        Reason.AMBIGUOUS_EXTRACTION,
        Reason.LOW_CONFIDENCE,
    )


def test_the_first_failing_check_wins(gate):
    """A value failing several checks reports the earliest one.

    Deterministic attribution is what makes the reason distribution
    interpretable -- otherwise the same defect could be reported differently
    on different runs.
    """
    # Empty, and also far too short, and also badly formatted.
    assert gate.check(candidate("aadhaar", "   ")).reason is Reason.EMPTY


def test_structural_failure_outranks_low_confidence(gate):
    """Otherwise a malformed value would be reported as a confidence problem,
    hiding the real defect behind a weaker one."""
    report = gate.check(candidate("pan", "AKQPS34I7M", confidence=0.1))
    assert report.reason is Reason.FORMAT


# -- configuration -----------------------------------------------------------


def test_the_confidence_threshold_is_configurable(schema):
    """It is tuned against the false-positive rate, not fixed by fiat."""
    cand = candidate("pan", "AKQPS3417M", confidence=0.4)
    assert ValidationGate(schema, min_confidence=0.55).check(cand).status is Status.REJECT
    assert ValidationGate(schema, min_confidence=0.3).check(cand).status is Status.PASS


def test_the_clock_is_injectable(schema):
    """Date rules must be testable without freezing the global clock, and a
    replayed session must be re-scorable against the date it actually ran on.
    """
    cand = candidate("dob", "2008-09-06")
    assert (
        ValidationGate(schema, today=dt.date(2026, 9, 6)).check(cand).status
        is Status.PASS
    )
    assert (
        ValidationGate(schema, today=dt.date(2020, 1, 1)).check(cand).status
        is Status.REJECT
    )


def test_an_unknown_field_is_an_error_not_a_pass(gate):
    """Silently accepting a value for a field that does not exist would write
    it nowhere while reporting success."""
    with pytest.raises(KeyError):
        gate.check(candidate("not_a_field", "anything"))


# -- optional fields ---------------------------------------------------------


def test_an_optional_field_still_rejects_an_empty_value(gate):
    """Declining a field is a decision the orchestrator records, not a value
    the gate validates. An empty string reaching the gate is a defect.
    """
    assert gate.check(candidate("email", "")).reason is Reason.EMPTY
