"""The confirmation receipt: the capability that authorises a write.

A receipt is the only thing `FormState.commit` accepts as permission to store a
value. It records which candidate was confirmed, which validation verdict
covered it, and what the user actually said when affirming.

Receipts can be constructed only from the confirmation module. This is the
second of the three enforcement mechanisms in SPEC.md section 2, and it is what
turns "only the confirmation step issues receipts" from a convention into a
property of the type: any other module that tries to mint one raises.

The runtime guard inspects the calling frame, which stops mistakes -- an
accidental construction in the orchestrator, a helper that drifts into the wrong
module during a refactor. It does not stop someone determined to circumvent it,
and it is not intended to; a caller can always forge a frame. That case is
covered by the static analysis in `tests/test_no_silent_write.py`, which fails
the build rather than the request. The two mechanisms are complementary: one
catches the accident at runtime, the other catches the intent at review time.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone

from lucidform.models import Affirmation, ValidationReport, fingerprint

# The single module permitted to mint receipts. Kept as a string rather than an
# import so that this module has no dependency on the orchestrator -- the
# dependency runs one way, and `formstate/` stays free of anything upstream.
ISSUER_MODULE = "lucidform.orchestrate.confirm"


class UnauthorizedIssuer(RuntimeError):
    """A receipt was constructed outside the confirmation module."""


def _calling_module() -> str:
    """The first module on the stack that is not this one.

    Walked rather than indexed at a fixed depth: a frozen dataclass's generated
    `__init__` executes with this module's globals, so a hardcoded depth lands
    on that synthetic frame and reports the receipt module as its own caller.
    Walking until the module name changes is correct regardless of how many
    frames the dataclass machinery inserts, and does not silently break if that
    changes between Python versions.
    """
    depth = 1
    while True:
        try:
            frame = sys._getframe(depth)
        except ValueError:  # ran off the top of the stack
            return "<unknown>"
        name = frame.f_globals.get("__name__", "")
        if name != __name__:
            return name
        depth += 1


@dataclass(frozen=True)
class ConfirmationReceipt:
    """Proof that one specific candidate was validated and explicitly affirmed.

    `candidate_fingerprint` binds the receipt to a single candidate *and* to the
    exact value that will be written. `FormState.commit` recomputes it at the
    write site, so a receipt issued for one value cannot be used to commit
    another -- the check does not depend on the caller passing the right pair.
    """

    field_id: str
    candidate_id: str
    candidate_fingerprint: str
    validation: ValidationReport
    affirmation: Affirmation
    issued_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __post_init__(self) -> None:
        caller = _calling_module()
        if caller != ISSUER_MODULE:
            raise UnauthorizedIssuer(
                f"{caller} attempted to mint a ConfirmationReceipt. Only "
                f"{ISSUER_MODULE} may issue one -- a receipt is the "
                "authorisation to write to the form, and it is granted only "
                "after an explicit read-back confirmation (SPEC.md section 2)."
            )

        if not self.affirmation.explicit:
            raise UnauthorizedIssuer(
                "refusing to issue a receipt for an affirmation that was not "
                "explicit; there is nothing to authorise"
            )
        if not self.validation.passed:
            raise UnauthorizedIssuer(
                "refusing to issue a receipt for a candidate that failed "
                "validation"
            )

    def matches(self, field_id: str, candidate_id: str, normalized_value: str) -> bool:
        """True if this receipt authorises writing exactly this value."""
        return (
            self.field_id == field_id
            and self.candidate_id == candidate_id
            and self.candidate_fingerprint
            == fingerprint(field_id, normalized_value, candidate_id)
        )
