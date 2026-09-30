"""Cross-field checks, and the discipline around when they may run.

The rules themselves are simple. The part worth testing hard is the guard: a
check whose dependency has not been confirmed must be *skipped*, not passed,
and skipping must not reject the value either. Getting that wrong in either
direction is a real defect -- silently passing inflates the gate's apparent
accuracy, silently rejecting blocks users on a check that never ran.
"""

from __future__ import annotations

import pytest

from lucidform.gate import crossfield
from lucidform.gate.gate import ValidationGate
from lucidform.models import Candidate, Reason, Status
from lucidform.schema import loader


@pytest.fixture(scope="module")
def gate():
    return ValidationGate(loader.load())


def _check(gate, field_id, value, committed):
    return gate.check(
        Candidate(
            field_id=field_id, value=value, raw_utterance=value, confidence=0.95
        ),
        committed,
    )


# -- PAN against surname -----------------------------------------------------


def test_pan_fifth_character_matching_the_surname_passes():
    result = crossfield.pan_matches_surname(
        "AKQPS3417M", {"full_name": "Ramesh Kumar Sharma"}
    )
    assert result.ran and result.passed


def test_pan_fifth_character_disagreeing_with_the_surname_fails():
    result = crossfield.pan_matches_surname(
        "AKQPB3417M", {"full_name": "Ramesh Kumar Sharma"}
    )
    assert result.failed
    assert "Sharma" in result.detail and "'S'" in result.detail


def test_surname_matching_is_case_insensitive():
    assert crossfield.pan_matches_surname(
        "AKQPS3417M", {"full_name": "ramesh kumar sharma"}
    ).passed


def test_single_word_names_use_that_word_as_the_surname():
    """Mononyms are common and must not crash or be waved through."""
    assert crossfield.pan_matches_surname("AKQPS3417M", {"full_name": "Sharma"}).passed
    assert crossfield.pan_matches_surname("AKQPB3417M", {"full_name": "Sharma"}).failed


# -- PIN against state -------------------------------------------------------


def test_pin_in_the_right_postal_region_passes():
    assert crossfield.pin_matches_confirmed_state(
        "302015", {"state": "Rajasthan"}
    ).passed


def test_pin_in_the_wrong_postal_region_fails():
    result = crossfield.pin_matches_confirmed_state("560001", {"state": "Rajasthan"})
    assert result.failed
    assert "Rajasthan" in result.detail


def test_a_state_with_no_region_data_is_not_checked():
    """Declining is the honest outcome. Inventing a pass would let an
    unverifiable pairing through while appearing to have been checked."""
    result = crossfield.pin_matches_confirmed_state("790001", {"state": "Nagaland"})
    assert not result.ran
    assert not result.passed
    assert "no postal region data" in result.detail


# -- the dependency guard ----------------------------------------------------


def test_a_check_with_an_unconfirmed_dependency_is_skipped_not_passed():
    result = crossfield.pan_matches_surname("AKQPB3417M", {})
    assert not result.ran
    assert not result.passed
    assert not result.failed, "a skipped check must not reject the value"
    assert "has not been confirmed" in result.detail


def test_skipping_lets_the_value_through_but_records_the_skip(gate):
    """The value passes -- there is nothing to contradict yet -- but the log
    must show the check did not run, so the results can distinguish
    'checked and consistent' from 'never checked'."""
    report = _check(gate, "pan", "AKQPB3417M", {})
    assert report.status is Status.PASS

    entry = next(c for c in report.checks if c.name == "pan_matches_surname")
    assert not entry.passed
    assert "has not been confirmed" in entry.detail


def test_the_same_value_is_rejected_once_the_dependency_is_confirmed(gate):
    """The dependency guard defers a check; it does not waive it."""
    committed = {"full_name": "Ramesh Kumar Sharma"}
    assert _check(gate, "pan", "AKQPB3417M", committed).reason is Reason.CROSS_FIELD


def test_an_empty_dependency_counts_as_unconfirmed(gate):
    """A field the user declined is not a confirmed value to check against."""
    report = _check(gate, "pan", "AKQPB3417M", {"full_name": "   "})
    assert report.status is Status.PASS


def test_cross_field_checks_read_only_committed_values(gate):
    """Never another pending candidate.

    Validating a candidate against an unconfirmed value would let an
    unreviewed value influence what the gate accepts -- a second, indirect
    path by which something the user never confirmed shapes the form.
    """
    committed = {"full_name": "Ramesh Kumar Sharma"}
    assert _check(gate, "pan", "AKQPS3417M", committed).status is Status.PASS
    # The signature takes committed values only; there is no parameter through
    # which a pending candidate could be supplied.
    assert crossfield.check("pan", "AKQPS3417M", committed) is not None


def test_fields_without_a_cross_field_rule_return_nothing():
    assert crossfield.check("city", "Jaipur", {"state": "Rajasthan"}) is None


# -- ordering ----------------------------------------------------------------


def test_structural_failures_are_reported_before_cross_field_ones(gate):
    """A malformed PAN is malformed regardless of the surname.

    Reporting it as a cross-field mismatch would tell the user to check their
    name when the real problem is the number they just read out.
    """
    report = _check(
        gate, "pan", "AKQPS34I7M", {"full_name": "Ramesh Kumar Sharma"}
    )
    assert report.reason is Reason.FORMAT
