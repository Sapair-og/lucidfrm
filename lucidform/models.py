"""Core types shared across the pipeline.

Deliberately free of I/O and of any model client, so that `gate/` and
`formstate/` can depend on this module without acquiring an LLM dependency.
See SPEC.md section 2.
"""

from __future__ import annotations

import enum
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


class FieldType(str, enum.Enum):
    TEXT = "text"
    NAME = "name"
    DATE = "date"
    ENUM = "enum"
    EMAIL = "email"
    PHONE = "phone"
    PAN = "pan"
    AADHAAR = "aadhaar"
    PIN = "pin"
    IFSC = "ifsc"


class Status(str, enum.Enum):
    PASS = "pass"
    REJECT = "reject"


class Reason(str, enum.Enum):
    """Closed rejection taxonomy. Every rejection carries exactly one.

    Each member becomes a column in the results table, so adding one is a
    deliberate change to the reported measures, not an implementation detail.

    The codes are chosen so that each maps to a distinct thing you would say to
    the user. TYPE_MISMATCH and FORMAT are the pair most easily conflated:
    TYPE_MISMATCH is "that is the wrong length" and FORMAT is "that is the
    right length but does not look like a PAN". They produce different
    remediation prompts, so they are different codes.
    """

    EMPTY = "empty"
    TYPE_MISMATCH = "type_mismatch"  # wrong size
    FORMAT = "format"  # right size, wrong shape
    ENUM = "enum"  # not one of the permitted options
    CHECKSUM = "checksum"  # well-formed but arithmetically impossible
    RANGE = "range"  # well-formed but outside the permitted domain
    CROSS_FIELD = "cross_field"  # contradicts an already-confirmed value
    AMBIGUOUS_EXTRACTION = "ambiguous_extraction"
    LOW_CONFIDENCE = "low_confidence"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class FieldSpec:
    """One form field: structure from the PDF, semantics from the YAML overlay.

    `acroform_name` is the raw PDF field name; `id` is our stable identifier.
    They differ because PDF field names are not guaranteed stable or readable,
    and the overlay is keyed by `id`.
    """

    id: str
    acroform_name: str
    label: str
    type: FieldType
    required: bool = True
    prompt: dict[str, str] = field(default_factory=dict)  # lang -> plain-language ask
    gloss: dict[str, str] = field(default_factory=dict)  # lang -> jargon explanation
    # lang -> what to call this field when speaking to the user. `label` stays
    # the canonical English name used in the PDF, the logs, and the results
    # table; this is only for what the user hears.
    labels: dict[str, str] = field(default_factory=dict)
    max_length: int | None = None
    pattern: str | None = None
    enum_values: tuple[str, ...] = ()
    # Field ids this one is validated against (e.g. pan -> name, pin -> state).
    depends_on: tuple[str, ...] = ()

    def name(self, lang: str) -> str:
        """What to call this field out loud.

        An English label inside a Hindi read-back is the one place a language
        slip actually costs something: the read-back is what the user is being
        asked to attest to.
        """
        return self.labels.get(lang) or self.label

    def ask(self, lang: str) -> str:
        return self.prompt.get(lang) or self.prompt.get("en") or self.label

    def explain(self, lang: str) -> str:
        return self.gloss.get(lang) or self.gloss.get("en") or ""


def fingerprint(field_id: str, normalized_value: str, candidate_id: str) -> str:
    """Bind a receipt to one exact candidate and one exact committed value.

    The unit separator prevents field boundaries from being forged by a value
    that happens to contain the delimiter.
    """
    payload = f"{field_id}\x1f{normalized_value}\x1f{candidate_id}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Candidate:
    """A proposed value. Explicitly *not* a form value.

    Frozen: a receipt is bound to a candidate by id and value, so mutating one
    would silently decouple it from any receipt already issued for it. To revise
    a value, mint a new candidate.
    """

    field_id: str
    value: str
    raw_utterance: str
    confidence: float
    # Character span of `value` within `raw_utterance`, when the extractor can
    # locate it. Absence is itself a signal the value was inferred, not quoted.
    span: tuple[int, int] | None = None
    ambiguous: bool = False
    candidate_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    created_at: str = field(default_factory=_now)


@dataclass(frozen=True)
class Check:
    """One executed validation check. Recorded whether it passed or failed, so
    the log shows what was actually exercised rather than only what tripped."""

    name: str
    passed: bool
    detail: str = ""


@dataclass(frozen=True)
class ValidationReport:
    status: Status
    candidate_id: str
    field_id: str
    # Canonical form of the value. This, not Candidate.value, is what gets
    # committed and what the receipt fingerprint covers.
    normalized_value: str = ""
    reason: Reason | None = None
    detail: str = ""
    checks: tuple[Check, ...] = ()
    created_at: str = field(default_factory=_now)

    def __post_init__(self) -> None:
        if self.status is Status.REJECT and self.reason is None:
            raise ValueError("a rejection must carry a reason code")
        if self.status is Status.PASS and self.reason is not None:
            raise ValueError("a pass must not carry a reason code")

    @property
    def passed(self) -> bool:
        return self.status is Status.PASS


@dataclass(frozen=True)
class Affirmation:
    """The user's response to a read-back.

    `explicit` is True only for an unambiguous, whole-utterance yes. An
    utterance that merely *contains* an affirmative token does not qualify --
    see the confirmation_spoofing cases in tests/adversarial/cases.yaml.
    """

    explicit: bool
    raw_utterance: str
    basis: str = ""  # which rule decided, for the audit trail
    created_at: str = field(default_factory=_now)
