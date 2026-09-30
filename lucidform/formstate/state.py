"""Form state: the single write path.

This module is the first of the three enforcement mechanisms in SPEC.md
section 2. There is exactly one way for a value to enter a form, and it is
`commit(candidate, receipt)`. There is no `set`, no `update`, no `__setitem__`,
and no keyword that bypasses the checks.

`commit` does not trust its caller. It recomputes the candidate fingerprint at
the write site and compares it to the one the receipt carries, so a caller that
holds a valid receipt for value A cannot use it to write value B -- including by
accident, which is the likelier failure. Every precondition is re-verified here
rather than assumed to have been checked upstream, because "upstream checked it"
is exactly the assumption that decays as a codebase grows.

A blocked write raises and is logged as a `SILENT_WRITE_BLOCKED` event. It is a
research finding, not a swallowed error: the count of blocked writes is
reported, and a non-zero count during a normal session indicates a defect
somewhere upstream.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Mapping

from lucidform.eval.events import Event, EventLog
from lucidform.formstate.receipt import ConfirmationReceipt
from lucidform.models import Candidate, fingerprint


class SilentWriteBlocked(RuntimeError):
    """A write was attempted that did not satisfy the commit invariant.

    Raised, never swallowed. If this reaches a caller, the correct response is
    to fix the caller, not to catch it.
    """


@dataclass(frozen=True)
class CommitRecord:
    """One entry in the append-only history of what was written and why."""

    field_id: str
    value: str
    candidate_id: str
    affirmed_with: str
    at: str
    replaced: str | None = None


@dataclass(frozen=True)
class DeclineRecord:
    """An optional field the user chose not to answer.

    Recorded distinctly from an empty value: "declined" is a decision the user
    made, and a form reviewer needs to tell it apart from a field the system
    failed to collect.
    """

    field_id: str
    at: str
    said: str = ""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class FormState:
    """Confirmed values for one form-filling session."""

    def __init__(self, log: EventLog | None = None) -> None:
        # Private, and reachable only from this module. Enforced by
        # tests/test_no_silent_write.py, because Python will not enforce it.
        self._values: dict[str, str] = {}
        self._declined: dict[str, DeclineRecord] = {}
        self._history: list[CommitRecord] = []
        self._blocked: int = 0
        self._log = log

    # -- reading -----------------------------------------------------------

    @property
    def values(self) -> Mapping[str, str]:
        """Read-only view. Handing out the dict itself would be a second write
        path, since a caller could mutate it in place."""
        return MappingProxyType(dict(self._values))

    @property
    def history(self) -> tuple[CommitRecord, ...]:
        return tuple(self._history)

    @property
    def declined(self) -> Mapping[str, DeclineRecord]:
        return MappingProxyType(dict(self._declined))

    @property
    def blocked_writes(self) -> int:
        return self._blocked

    def get(self, field_id: str, default: str = "") -> str:
        return self._values.get(field_id, default)

    def is_committed(self, field_id: str) -> bool:
        return field_id in self._values

    def is_resolved(self, field_id: str) -> bool:
        """Committed or explicitly declined -- either way, we are done asking."""
        return field_id in self._values or field_id in self._declined

    def __contains__(self, field_id: object) -> bool:
        return field_id in self._values

    def __len__(self) -> int:
        return len(self._values)

    # -- the only write path -----------------------------------------------

    def commit(self, candidate: Candidate, receipt: ConfirmationReceipt) -> str:
        """Write a confirmed value. The sole mutator of form state.

        Every precondition is re-verified here. Returns the value written.
        """
        value = receipt.validation.normalized_value

        def block(why: str) -> None:
            self._blocked += 1
            if self._log is not None:
                self._log.emit(
                    Event.SILENT_WRITE_BLOCKED,
                    field_id=candidate.field_id,
                    payload={
                        "reason": why,
                        "candidate_id": candidate.candidate_id,
                        "receipt_candidate_id": receipt.candidate_id,
                        "attempted_value": candidate.value,
                    },
                )
            raise SilentWriteBlocked(
                f"refusing to write {candidate.field_id}: {why}"
            )

        # 1. The receipt must be for this field.
        if receipt.field_id != candidate.field_id:
            block(
                f"the receipt authorises {receipt.field_id!r}, not "
                f"{candidate.field_id!r}"
            )

        # 2. The receipt must be for this candidate.
        if receipt.candidate_id != candidate.candidate_id:
            block(
                "the receipt was issued for a different candidate "
                f"({receipt.candidate_id} != {candidate.candidate_id})"
            )

        # 3. The validation report must also be for this candidate. Without
        #    this, a receipt could pair a passing verdict on one value with a
        #    confirmation of another.
        if receipt.validation.candidate_id != candidate.candidate_id:
            block("the validation report covers a different candidate")

        # 4. Validation must have passed.
        if not receipt.validation.passed:
            block("the candidate did not pass validation")

        # 5. The affirmation must have been explicit. An utterance that merely
        #    contained an affirmative token is not consent (see
        #    orchestrate/confirm.py).
        if not receipt.affirmation.explicit:
            block("the user did not explicitly confirm this value")

        # 6. There must be something to write.
        if not value:
            block("the receipt authorises an empty value")

        # 7. The fingerprint, recomputed here rather than trusted. This is what
        #    stops a valid receipt for value A being used to write value B.
        expected = fingerprint(candidate.field_id, value, candidate.candidate_id)
        if receipt.candidate_fingerprint != expected:
            block(
                "the receipt does not match this candidate and value; it was "
                "issued for something else"
            )

        previous = self._values.get(candidate.field_id)
        self._values[candidate.field_id] = value
        self._declined.pop(candidate.field_id, None)
        record = CommitRecord(
            field_id=candidate.field_id,
            value=value,
            candidate_id=candidate.candidate_id,
            affirmed_with=receipt.affirmation.raw_utterance,
            at=_now(),
            replaced=previous,
        )
        self._history.append(record)

        if self._log is not None:
            self._log.emit(Event.COMMIT, field_id=candidate.field_id, payload=record)
        return value

    def decline(self, field_id: str, said: str = "") -> DeclineRecord:
        """Record that the user chose not to answer an optional field.

        Writes no value. Kept separate from `commit` so that declining can
        never be a route to storing something.
        """
        if field_id in self._values:
            raise SilentWriteBlocked(
                f"{field_id} already holds a confirmed value; declining it now "
                "would discard a value the user confirmed"
            )
        record = DeclineRecord(field_id=field_id, at=_now(), said=said)
        self._declined[field_id] = record
        if self._log is not None:
            self._log.emit(Event.CORRECTION, field_id=field_id, payload=record)
        return record
