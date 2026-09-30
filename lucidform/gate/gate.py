"""The validation gate.

Stage 4 of the pipeline, and the component the project's safety claim rests on.
It decides whether a candidate value may be offered to the user for
confirmation. It contains no model inference, reads no network, and holds no
state beyond the schema it was constructed with -- so its verdict is
reproducible, auditable, and unchanged by model version, sampling, or prompt
phrasing (METHODOLOGY M0.2).

The gate does not interpret text. It measures, matches, and computes. An
utterance instructing it to skip validation is rejected by the same length and
shape rules as any other malformed value, because there is no code path in
which the content of a string influences the decision procedure.
"""

from __future__ import annotations

import datetime as dt
from typing import Mapping

from lucidform.gate import crossfield, rules
from lucidform.gate.checksums import aadhaar_valid
from lucidform.models import (
    Candidate,
    Check,
    FieldSpec,
    FieldType,
    Reason,
    Status,
    ValidationReport,
)
from lucidform.schema.loader import FormSchema

# The order checks run in. Fixed, and stable across runs: the reason
# distribution reported in the results section shifts if it changes, so this
# tuple is the definition of record (SPEC.md section 5).
#
# Structural verdicts come first because they are objective and produce a
# specific thing to say to the user. The extractor's own quality signals come
# last: a value that is structurally perfect but which the extractor was unsure
# of is a weaker, different finding than a malformed one, and running
# confidence first would hide malformed values behind a confidence complaint.
CHECK_ORDER = (
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


class ValidationGate:
    """Deterministic accept/reject on a single candidate value."""

    def __init__(
        self,
        schema: FormSchema,
        min_confidence: float = 0.55,
        *,
        today: dt.date | None = None,
    ) -> None:
        self.schema = schema
        self.min_confidence = min_confidence
        # Injectable so date-dependent rules are testable without freezing the
        # clock globally, and so a replayed session can be re-scored against
        # the date it actually ran on.
        self._today = today

    @property
    def today(self) -> dt.date:
        return self._today or dt.date.today()

    def check(
        self,
        candidate: Candidate,
        committed: Mapping[str, str] | None = None,
    ) -> ValidationReport:
        """Validate one candidate against the schema and confirmed values.

        `committed` holds values the user has already confirmed. Cross-field
        checks read only from it -- never from other pending candidates.
        """
        committed = dict(committed or {})
        field = self.schema.by_id(candidate.field_id)
        value = rules.normalize(candidate.value, field)
        checks: list[Check] = []

        def reject(reason: Reason, detail: str) -> ValidationReport:
            return ValidationReport(
                status=Status.REJECT,
                candidate_id=candidate.candidate_id,
                field_id=field.id,
                normalized_value="",  # nothing is offered for confirmation
                reason=reason,
                detail=detail,
                checks=tuple(checks),
            )

        for reason in CHECK_ORDER:
            outcome = self._run(reason, value, field, candidate, committed, checks)
            if outcome is not None:
                return reject(reason, outcome)

        return ValidationReport(
            status=Status.PASS,
            candidate_id=candidate.candidate_id,
            field_id=field.id,
            normalized_value=value,
            checks=tuple(checks),
        )

    # -- individual checks -------------------------------------------------
    # Each returns a failure detail, or None to pass. Each appends to `checks`
    # so the log records what was actually exercised, not only what tripped.

    def _run(
        self,
        reason: Reason,
        value: str,
        field: FieldSpec,
        candidate: Candidate,
        committed: Mapping[str, str],
        checks: list[Check],
    ) -> str | None:
        handler = {
            Reason.EMPTY: self._empty,
            Reason.TYPE_MISMATCH: self._length,
            Reason.FORMAT: self._format,
            Reason.ENUM: self._enum,
            Reason.CHECKSUM: self._checksum,
            Reason.RANGE: self._range,
            Reason.CROSS_FIELD: self._crossfield,
            Reason.AMBIGUOUS_EXTRACTION: self._ambiguous,
            Reason.LOW_CONFIDENCE: self._confidence,
        }[reason]
        return handler(value, field, candidate, committed, checks)

    def _empty(self, value, field, candidate, committed, checks) -> str | None:
        detail = "" if value else "no value was heard"
        checks.append(Check("non_empty", passed=bool(value), detail=detail))
        return detail or None

    def _length(self, value, field, candidate, committed, checks) -> str | None:
        # An enum's size is fully determined by its option list. Checking
        # length as well would report a size complaint for a value whose real
        # problem is that it is not one of the options.
        if field.type is FieldType.ENUM:
            return None
        detail = rules.length_error(value, field)
        checks.append(Check("length", passed=detail is None, detail=detail or ""))
        return detail

    def _format(self, value, field, candidate, committed, checks) -> str | None:
        if field.type is FieldType.ENUM:
            return None
        detail = rules.format_error(value, field)
        checks.append(Check("format", passed=detail is None, detail=detail or ""))
        return detail

    def _enum(self, value, field, candidate, committed, checks) -> str | None:
        if not field.enum_values:
            return None
        detail = rules.enum_error(value, field)
        checks.append(Check("enum", passed=detail is None, detail=detail or ""))
        return detail

    def _checksum(self, value, field, candidate, committed, checks) -> str | None:
        if field.type is not FieldType.AADHAAR:
            return None
        ok = aadhaar_valid(value)
        detail = "" if ok else "the check digit does not match; one digit is wrong"
        checks.append(Check("verhoeff", passed=ok, detail=detail))
        return detail or None

    def _range(self, value, field, candidate, committed, checks) -> str | None:
        detail = rules.range_error(value, field, today=self.today)
        if field.type is FieldType.DATE:
            checks.append(Check("range", passed=detail is None, detail=detail or ""))
        return detail

    def _crossfield(self, value, field, candidate, committed, checks) -> str | None:
        result = crossfield.check(field.id, value, committed)
        if result is None:
            return None
        checks.append(
            Check(
                result.name,
                # A skipped check is recorded as not passed, with its reason.
                # Recording it as a pass would inflate the gate's apparent
                # accuracy with checks that never ran.
                passed=result.ran and result.passed,
                detail=result.detail,
            )
        )
        return result.detail if result.failed else None

    def _ambiguous(self, value, field, candidate, committed, checks) -> str | None:
        detail = (
            "the utterance had more than one reading" if candidate.ambiguous else ""
        )
        checks.append(
            Check("unambiguous", passed=not candidate.ambiguous, detail=detail)
        )
        return detail or None

    def _confidence(self, value, field, candidate, committed, checks) -> str | None:
        ok = candidate.confidence >= self.min_confidence
        detail = (
            ""
            if ok
            else (
                f"extraction confidence {candidate.confidence:.2f} is below the "
                f"{self.min_confidence:.2f} threshold"
            )
        )
        checks.append(Check("confidence", passed=ok, detail=detail))
        return detail or None
