"""The adversarial suite -- the evidence for the safety claim.

Every case in `adversarial/gate_cases.yaml` is run through the real gate, and
both the verdict and the reason code are asserted. Catching the right input for
the wrong reason still means the error analysis in the results section is
wrong, so the reason is not treated as incidental.

The control cases (`expect: pass`) matter as much as the rejections. They are
what the false-positive rate is measured against, and without them a gate that
rejected every input would score perfectly on this file.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from lucidform.gate.gate import CHECK_ORDER, ValidationGate
from lucidform.models import Candidate, Reason, Status
from lucidform.schema import loader

CASES_FILE = Path(__file__).parent / "adversarial" / "gate_cases.yaml"


def _load():
    with CASES_FILE.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


SUITE = _load()


def _flatten():
    for category in SUITE["categories"]:
        for i, case in enumerate(category["cases"]):
            label = (
                f"{category['name']}[{i}]:{case['field']}="
                f"{str(case['value'])[:24]!r}"
            )
            yield pytest.param(category["name"], case, id=label)


@pytest.fixture(scope="module")
def gate():
    return ValidationGate(loader.load(), min_confidence=0.55)


@pytest.fixture(scope="module")
def committed():
    return dict(SUITE["context"])


def _candidate(case) -> Candidate:
    return Candidate(
        field_id=case["field"],
        value=str(case["value"]),
        raw_utterance=str(case.get("utterance", case["value"])),
        confidence=float(case.get("confidence", 0.95)),
        ambiguous=bool(case.get("ambiguous", False)),
    )


@pytest.mark.parametrize("category,case", list(_flatten()))
def test_adversarial_case(gate, committed, category, case):
    report = gate.check(_candidate(case), committed)

    if case["expect"] == "pass":
        assert report.status is Status.PASS, (
            f"[{category}] control case wrongly rejected as "
            f"{report.reason.value if report.reason else '?'}: {report.detail}\n"
            "A false positive is a real user being told a correct answer is "
            "wrong -- it is measured, not tolerated."
        )
        assert report.normalized_value, "a passing report must carry a value to commit"
    else:
        assert report.status is Status.REJECT, (
            f"[{category}] this value was accepted and should not have been. "
            f"{case.get('note', '')}"
        )
        assert report.reason is Reason(case["reason"]), (
            f"[{category}] rejected for the wrong reason: expected "
            f"{case['reason']}, got {report.reason.value}. "
            f"detail: {report.detail}"
        )
        assert report.detail, "a rejection must explain itself to the user"
        assert not report.normalized_value, (
            "a rejected candidate must offer nothing for confirmation"
        )


def test_the_suite_covers_every_reason_code_the_gate_can_emit():
    """Every code in the taxonomy needs at least one case.

    An unexercised reason code is an untested branch of the gate, and a column
    in the results table that would silently always read zero.
    """
    exercised = {
        case["reason"]
        for category in SUITE["categories"]
        for case in category["cases"]
        if case["expect"] == "reject"
    }
    expected = {r.value for r in CHECK_ORDER}
    assert exercised == expected, (
        f"reason codes with no adversarial case: {sorted(expected - exercised)}"
    )


def test_the_suite_has_controls_in_the_categories_that_need_them():
    """A rejection-only category cannot distinguish a gate from a brick wall.

    The categories listed here each test a rule that could be satisfied by
    rejecting everything of that shape, so each needs a near-miss control.
    """
    needs_control = {
        "checksum_single_digit",
        "homoglyph_substitution",
        "cross_field_contradiction",
        "enum_near_miss",
        "type_coercion",
        "extraction_quality",
    }
    for category in SUITE["categories"]:
        if category["name"] not in needs_control:
            continue
        verdicts = {c["expect"] for c in category["cases"]}
        assert "pass" in verdicts, f"{category['name']} has no control case"


def test_every_case_declares_why_it_exists():
    """A case with no rationale cannot be assessed by a reader of the paper."""
    for category in SUITE["categories"]:
        assert category.get("rationale", "").strip(), f"{category['name']}: no rationale"
        assert category["cases"], f"{category['name']}: no cases"


def test_the_suite_is_not_trivially_small():
    total = sum(len(c["cases"]) for c in SUITE["categories"])
    assert total >= 40, f"only {total} adversarial cases"
    assert len(SUITE["categories"]) >= 10


def test_gate_never_raises_on_hostile_input(gate, committed):
    """The gate must reject, never crash.

    An exception escaping the gate would be handled somewhere upstream, and the
    handler is where a "well, let it through" branch gets written under time
    pressure. Rejecting cleanly leaves no such opening.
    """
    hostile = [
        "\x00\x01\x02",
        "A" * 10_000,
        "🙂" * 50,
        "'; DROP TABLE forms; --",
        "{{7*7}}",
        "../../etc/passwd",
        "\\u0000",
        "%n%n%n",
    ]
    for field_id in ("pan", "aadhaar", "full_name", "dob", "gender", "pin"):
        for value in hostile:
            report = gate.check(
                Candidate(
                    field_id=field_id,
                    value=value,
                    raw_utterance=value,
                    confidence=0.9,
                ),
                committed,
            )
            assert report.status is Status.REJECT, f"{field_id} accepted {value!r}"
            assert report.reason is not None
