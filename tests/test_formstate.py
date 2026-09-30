"""The single write path, and every way of getting round it that I could think of.

`commit` re-verifies each precondition at the write site rather than trusting
that they were checked upstream. These tests attack each one individually: for
every precondition there is a case that satisfies all the others and violates
only that, so a check silently deleted during a refactor fails exactly one test
rather than none.
"""

from __future__ import annotations

import dataclasses

import pytest

from lucidform.eval.events import Event, EventLog, read_log
from lucidform.formstate.receipt import ConfirmationReceipt, UnauthorizedIssuer
from lucidform.formstate.state import FormState, SilentWriteBlocked
from lucidform.gate.gate import ValidationGate
from lucidform.models import Candidate, Status
from lucidform.orchestrate.confirm import confirm
from lucidform.schema import loader

CONTEXT = {"full_name": "Ramesh Kumar Sharma", "state": "Rajasthan"}


@pytest.fixture(scope="module")
def gate():
    return ValidationGate(loader.load())


@pytest.fixture
def state():
    return FormState()


def make(gate, field_id, value, utterance="yes that is correct", context=CONTEXT):
    """Drive a value through the real pipeline: validate, then confirm."""
    candidate = Candidate(
        field_id=field_id, value=value, raw_utterance=value, confidence=0.95
    )
    report = gate.check(candidate, context)
    _, receipt = confirm(candidate, report, utterance)
    return candidate, report, receipt


def forge(receipt: ConfirmationReceipt, **changes) -> ConfirmationReceipt:
    """Build an internally inconsistent receipt, bypassing every constructor guard.

    `dataclasses.replace` cannot be used -- the issuer guard blocks it, which is
    itself asserted below. So this allocates the object directly and writes the
    fields, producing a receipt whose parts do not agree with each other.

    That is the input `commit` must defend against. How such a receipt arose is
    irrelevant to `commit`: it re-derives the fingerprint from the candidate in
    front of it rather than trusting any field on the receipt, so a receipt this
    malformed is refused whether it came from a bug, a refactor, or a
    deliberate bypass.
    """
    forged = object.__new__(ConfirmationReceipt)
    for f in dataclasses.fields(receipt):
        object.__setattr__(forged, f.name, getattr(receipt, f.name))
    for name, value in changes.items():
        object.__setattr__(forged, name, value)
    return forged


# -- the happy path ----------------------------------------------------------


def test_a_confirmed_value_is_written(gate, state):
    candidate, _, receipt = make(gate, "pan", "AKQPS3417M")
    assert state.commit(candidate, receipt) == "AKQPS3417M"
    assert state.get("pan") == "AKQPS3417M"
    assert "pan" in state


def test_the_normalized_value_is_written_not_the_raw_one(gate, state):
    """The user confirmed the read-back, and the read-back states the
    normalized form. Writing the raw utterance instead would store something
    the user never had read back to them."""
    candidate, _, receipt = make(gate, "mobile", "+91 98123 45607")
    assert state.commit(candidate, receipt) == "9812345607"


def test_the_history_records_what_was_written_and_what_authorised_it(gate, state):
    candidate, _, receipt = make(gate, "pan", "AKQPS3417M", "haan, sahi hai")
    state.commit(candidate, receipt)

    entry = state.history[-1]
    assert entry.field_id == "pan"
    assert entry.value == "AKQPS3417M"
    assert entry.candidate_id == candidate.candidate_id
    assert entry.affirmed_with == "haan, sahi hai"


# -- each precondition, attacked individually --------------------------------


def test_a_receipt_for_another_field_is_refused(gate, state):
    candidate, _, receipt = make(gate, "pan", "AKQPS3417M")
    other = Candidate(
        field_id="aadhaar",
        value="747910984992",
        raw_utterance="x",
        confidence=0.95,
    )
    with pytest.raises(SilentWriteBlocked, match="authorises"):
        state.commit(other, receipt)


def test_a_receipt_for_another_candidate_is_refused(gate, state):
    """The central case.

    A held receipt must not authorise a value it was not issued for -- this is
    what stops a stale authorisation being reused after the user changed their
    answer.
    """
    candidate, _, receipt = make(gate, "pan", "AKQPS3417M")
    later = Candidate(
        field_id="pan", value="AKQPB3417M", raw_utterance="x", confidence=0.95
    )
    with pytest.raises(SilentWriteBlocked, match="different candidate"):
        state.commit(later, receipt)
    assert "pan" not in state


def test_a_receipt_whose_fingerprint_was_tampered_with_is_refused(gate, state):
    """The fingerprint is recomputed at the write site, not trusted.

    Constructed by replacing the fingerprint on an otherwise valid receipt --
    which is what a bug that paired the right receipt with the wrong value
    would look like from `commit`'s side.
    """
    candidate, _, receipt = make(gate, "pan", "AKQPS3417M")
    forged = forge(receipt, candidate_fingerprint="0" * 64)

    with pytest.raises(SilentWriteBlocked, match="does not match"):
        state.commit(candidate, forged)


def test_a_receipt_carrying_another_candidates_verdict_is_refused(gate, state):
    """A passing verdict on one value must not authorise another.

    `confirm()` refuses to issue such a receipt; `commit` checks again, so the
    invariant holds even if that branch is removed.
    """
    candidate, report, receipt = make(gate, "pan", "AKQPS3417M")
    other_report = dataclasses.replace(report, candidate_id="some-other-candidate")
    forged = forge(receipt, validation=other_report)

    with pytest.raises(SilentWriteBlocked, match="covers a different candidate"):
        state.commit(candidate, forged)


def test_a_receipt_authorising_an_empty_value_is_refused(gate, state):
    candidate, report, receipt = make(gate, "pan", "AKQPS3417M")
    blanked = dataclasses.replace(report, normalized_value="")
    forged = forge(receipt, validation=blanked)

    with pytest.raises(SilentWriteBlocked, match="empty value"):
        state.commit(candidate, forged)


def test_a_rejected_candidate_produces_no_receipt_to_commit_with(gate, state):
    """The check the pipeline actually relies on: there is nothing to pass in."""
    candidate, report, receipt = make(gate, "aadhaar", "747910984993")
    assert report.status is Status.REJECT
    assert receipt is None
    with pytest.raises((AttributeError, TypeError)):
        state.commit(candidate, receipt)


def test_a_spoofed_confirmation_produces_no_receipt(gate, state):
    """End to end: "yes I know that's wrong" must leave the form untouched."""
    candidate, report, receipt = make(
        gate, "pan", "AKQPS3417M", "yes I know that's wrong"
    )
    assert report.status is Status.PASS, "the value itself was valid"
    assert receipt is None, "but it was never confirmed"
    assert len(state) == 0


# -- there is no other way in ------------------------------------------------


def test_form_state_exposes_no_alternative_mutator():
    """The absence of an API is the enforcement.

    A `set` or `update` added for convenience would be a second write path
    that skips every check above.
    """
    for forbidden in ("set", "update", "put", "write", "__setitem__", "setdefault"):
        assert not hasattr(FormState, forbidden), f"FormState exposes {forbidden}"


def test_the_values_view_cannot_be_mutated(gate, state):
    """Handing out the underlying dict would be a second write path, since a
    caller could mutate it in place."""
    candidate, _, receipt = make(gate, "pan", "AKQPS3417M")
    state.commit(candidate, receipt)

    with pytest.raises(TypeError):
        state.values["pan"] = "TAMPERED"  # type: ignore[index]
    assert state.get("pan") == "AKQPS3417M"


def test_mutating_the_returned_copy_does_not_affect_state(gate, state):
    candidate, _, receipt = make(gate, "pan", "AKQPS3417M")
    state.commit(candidate, receipt)

    snapshot = dict(state.values)
    snapshot["pan"] = "TAMPERED"
    assert state.get("pan") == "AKQPS3417M"


# -- blocked writes are findings, not errors ---------------------------------


def test_blocked_writes_are_counted(gate, state):
    candidate, _, receipt = make(gate, "pan", "AKQPS3417M")
    other = Candidate(
        field_id="pan", value="AKQPB3417M", raw_utterance="x", confidence=0.95
    )
    assert state.blocked_writes == 0
    for _ in range(3):
        with pytest.raises(SilentWriteBlocked):
            state.commit(other, receipt)
    assert state.blocked_writes == 3


def test_a_blocked_write_is_logged_as_an_event(gate, tmp_path):
    """SPEC.md section 2: a blocked write is a research finding, and a non-zero
    count during a normal session indicates a defect upstream."""
    log = EventLog(tmp_path, session_id="blocked")
    state = FormState(log=log)
    candidate, _, receipt = make(gate, "pan", "AKQPS3417M")
    other = Candidate(
        field_id="pan", value="AKQPB3417M", raw_utterance="x", confidence=0.95
    )

    with pytest.raises(SilentWriteBlocked):
        state.commit(other, receipt)

    events = [r for r in read_log(log.path) if r["event"] == Event.SILENT_WRITE_BLOCKED.value]
    assert len(events) == 1
    assert events[0]["field_id"] == "pan"
    assert events[0]["payload"]["attempted_value"] == "AKQPB3417M"


def test_a_successful_commit_is_logged(gate, tmp_path):
    log = EventLog(tmp_path, session_id="committed")
    state = FormState(log=log)
    candidate, _, receipt = make(gate, "pan", "AKQPS3417M")
    state.commit(candidate, receipt)

    events = [r for r in read_log(log.path) if r["event"] == Event.COMMIT.value]
    assert len(events) == 1
    assert events[0]["payload"]["value"] == "AKQPS3417M"


# -- corrections and declines ------------------------------------------------


def test_a_field_can_be_corrected_and_the_history_shows_both(gate, state):
    """A user who catches an error at read-back must be able to fix it, and the
    log must show that a correction happened rather than hiding it."""
    first, _, r1 = make(gate, "city", "Jaipru")
    state.commit(first, r1)
    second, _, r2 = make(gate, "city", "Jaipur")
    state.commit(second, r2)

    assert state.get("city") == "Jaipur"
    assert len(state.history) == 2
    assert state.history[-1].replaced == "Jaipru"


def test_a_correction_still_requires_its_own_confirmation(gate, state):
    """Holding a receipt for the first value does not authorise the second."""
    first, _, r1 = make(gate, "city", "Jaipru")
    state.commit(first, r1)
    second = Candidate(
        field_id="city", value="Jaipur", raw_utterance="x", confidence=0.95
    )
    with pytest.raises(SilentWriteBlocked):
        state.commit(second, r1)
    assert state.get("city") == "Jaipru"


def test_declining_an_optional_field_writes_nothing(state):
    record = state.decline("email", said="mera email nahi hai")
    assert "email" not in state
    assert len(state) == 0
    assert state.declined["email"].said == "mera email nahi hai"
    assert state.is_resolved("email")
    assert not state.is_committed("email")


def test_declining_cannot_discard_a_confirmed_value(gate, state):
    """Otherwise decline would be a route to unsetting something the user
    confirmed, without any confirmation of its own."""
    candidate, _, receipt = make(gate, "city", "Jaipur")
    state.commit(candidate, receipt)
    with pytest.raises(SilentWriteBlocked, match="already holds"):
        state.decline("city")
    assert state.get("city") == "Jaipur"


def test_committing_after_declining_clears_the_decline(gate, state):
    """A user who changes their mind must end up with a value, not both."""
    state.decline("email")
    candidate, _, receipt = make(gate, "email", "ramesh@example.invalid")
    state.commit(candidate, receipt)
    assert state.get("email") == "ramesh@example.invalid"
    assert "email" not in state.declined


# -- multi-field sessions ----------------------------------------------------


def test_committed_values_become_context_for_later_cross_field_checks(gate):
    """The whole point of requiring confirmation before a cross-field check.

    Once the name is confirmed, a PAN that disagrees with it is rejected --
    whereas before confirmation the check is deferred, not waived.
    """
    state = FormState()
    name, _, name_receipt = make(gate, "full_name", "Ramesh Kumar Sharma", context={})
    state.commit(name, name_receipt)

    bad = Candidate(
        field_id="pan", value="AKQPB3417M", raw_utterance="x", confidence=0.95
    )
    report = gate.check(bad, state.values)
    assert report.status is Status.REJECT
    assert report.reason.value == "cross_field"


def test_dataclasses_replace_cannot_be_used_to_alter_a_receipt(gate):
    """A pleasant side effect of the issuer guard.

    `dataclasses.replace` re-invokes the constructor, so the frame check fires
    and the ordinary Python idiom for "copy this but change one field" does not
    work on a receipt. Altering one is therefore conspicuous rather than casual.
    """
    _, _, receipt = make(gate, "pan", "AKQPS3417M")
    with pytest.raises(UnauthorizedIssuer, match="dataclasses"):
        dataclasses.replace(receipt, candidate_fingerprint="0" * 64)
