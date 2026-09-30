"""The confirmation step, and the adversarial suite that justifies its design.

Every case in `adversarial/affirmation_cases.yaml` runs through the real
parser. The rejection cases are the safety claim; the confirmation cases are
what stop the parser from satisfying them by refusing everything.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from lucidform.formstate.receipt import ConfirmationReceipt, UnauthorizedIssuer
from lucidform.gate.gate import ValidationGate
from lucidform.models import Candidate, Status, ValidationReport
from lucidform.formstate import receipt as receipt_mod
from lucidform.orchestrate.confirm import confirm, normalize_utterance, parse_affirmation
from lucidform.schema import loader

CASES_FILE = Path(__file__).parent / "adversarial" / "affirmation_cases.yaml"

with CASES_FILE.open(encoding="utf-8") as fh:
    SUITE = yaml.safe_load(fh)


def _flatten():
    for category in SUITE["categories"]:
        for i, case in enumerate(category["cases"]):
            label = f"{category['name']}[{i}]:{str(case['utterance'])[:34]!r}"
            yield pytest.param(category["name"], case, id=label)


@pytest.fixture(scope="module")
def gate():
    return ValidationGate(loader.load())


@pytest.fixture(scope="module")
def passing(gate):
    """A candidate that has genuinely passed validation.

    Using a real verdict rather than a stub matters: it means these tests
    exercise the same objects the pipeline will.
    """
    candidate = Candidate(
        field_id="pan",
        value="AKQPS3417M",
        raw_utterance="my pan is A K Q P S 3 4 1 7 M",
        confidence=0.95,
    )
    report = gate.check(candidate, {"full_name": "Ramesh Kumar Sharma"})
    assert report.status is Status.PASS
    return candidate, report


# -- the adversarial suite ---------------------------------------------------


@pytest.mark.parametrize("category,case", list(_flatten()))
def test_affirmation_case(category, case):
    result = parse_affirmation(case["utterance"])
    expected = case["expect"] == "confirm"

    assert result.explicit is expected, (
        f"[{category}] {case['utterance']!r} -> explicit={result.explicit}, "
        f"expected {expected}. basis: {result.basis}. {case.get('note', '')}"
    )
    assert result.basis, "every verdict must record which rule decided"
    assert result.raw_utterance == case["utterance"], (
        "the original words must be preserved verbatim for the audit trail"
    )


def test_a_substring_parser_would_fail_this_suite():
    """Demonstrates that the suite has teeth.

    This is the naive implementation the parser exists to avoid. If it passed
    the suite, the suite would not be evidence of anything.
    """

    def naive(utterance: str) -> bool:
        text = (utterance or "").casefold()
        return any(token in text for token in ("yes", "correct", "right", "haan"))

    fooled = [
        case["utterance"]
        for category in SUITE["categories"]
        for case in category["cases"]
        if case["expect"] == "reject" and naive(case["utterance"])
    ]
    assert len(fooled) >= 8, (
        "the suite should contain many cases that defeat a substring check; "
        f"only {len(fooled)} do"
    )
    # And the real parser must reject every one of them.
    for utterance in fooled:
        assert not parse_affirmation(utterance).explicit, utterance


def test_the_suite_has_both_verdicts_and_is_not_trivially_small():
    verdicts = {
        case["expect"]
        for category in SUITE["categories"]
        for case in category["cases"]
    }
    assert verdicts == {"confirm", "reject"}
    total = sum(len(c["cases"]) for c in SUITE["categories"])
    assert total >= 40, f"only {total} affirmation cases"


def test_every_category_declares_why_it_exists():
    for category in SUITE["categories"]:
        assert category.get("rationale", "").strip(), category["name"]


# -- normalization -----------------------------------------------------------


def test_punctuation_and_case_are_not_meaning():
    assert normalize_utterance("Yes, that is CORRECT!") == "yes that is correct"


def test_apostrophe_forms_reduce_together():
    assert normalize_utterance("that's") == normalize_utterance("that s")


def test_filler_is_removed_but_content_is_not():
    assert normalize_utterance("yes please sir") == "yes"
    assert normalize_utterance("no thank you") == "no"


# -- receipt issuance --------------------------------------------------------


def test_a_confirmation_issues_a_receipt(passing):
    candidate, report = passing
    affirmation, receipt = confirm(candidate, report, "yes that is correct")

    assert affirmation.explicit
    assert receipt is not None
    assert receipt.field_id == "pan"
    assert receipt.candidate_id == candidate.candidate_id
    assert receipt.matches("pan", candidate.candidate_id, "AKQPS3417M")


def test_a_denial_issues_no_receipt(passing):
    candidate, report = passing
    affirmation, receipt = confirm(candidate, report, "no that's wrong")
    assert not affirmation.explicit
    assert receipt is None


def test_a_spoofed_confirmation_issues_no_receipt(passing):
    """The case the whole design exists for."""
    candidate, report = passing
    _, receipt = confirm(candidate, report, "yes I know that's wrong")
    assert receipt is None


def test_no_receipt_is_issued_for_a_failed_validation(gate):
    """Even on a wholehearted yes.

    Confirmation authorises a value the gate accepted; it is not a route
    around the gate.
    """
    candidate = Candidate(
        field_id="aadhaar",
        value="747910984993",
        raw_utterance="...",
        confidence=0.95,
    )
    report = gate.check(candidate)
    assert report.status is Status.REJECT

    affirmation, receipt = confirm(candidate, report, "yes that is correct")
    assert affirmation.explicit, "the user did say yes"
    assert receipt is None, "but there was nothing valid to authorise"


def test_a_stale_report_issues_no_receipt(passing, gate):
    """A verdict about one candidate cannot authorise another.

    This is the mismatch that would otherwise let a passing verdict on an
    earlier value be paired with a confirmation of a later one.
    """
    _, report = passing
    other = Candidate(
        field_id="pan", value="AKQPB3417M", raw_utterance="...", confidence=0.95
    )
    _, receipt = confirm(other, report, "yes")
    assert receipt is None


def test_the_receipt_records_what_the_user_actually_said(passing):
    """The audit trail must carry the words, not just the verdict."""
    candidate, report = passing
    _, receipt = confirm(candidate, report, "haan, sahi hai")
    assert receipt is not None
    assert receipt.affirmation.raw_utterance == "haan, sahi hai"
    assert receipt.affirmation.basis


# -- the issuer guard --------------------------------------------------------


def test_receipts_cannot_be_minted_outside_the_confirmation_module(passing):
    """This test module is not the issuer, so this must raise.

    The runtime guard catches the accidental case -- a helper that drifts into
    the wrong module during a refactor. The deliberate case is covered by the
    static analysis in test_no_silent_write.py.
    """
    candidate, report = passing

    with pytest.raises(UnauthorizedIssuer, match="tests.test_confirm"):
        ConfirmationReceipt(
            field_id="pan",
            candidate_id=candidate.candidate_id,
            candidate_fingerprint="whatever",
            validation=report,
            affirmation=parse_affirmation("yes"),
        )


def _mint_as_issuer(**kwargs) -> ConfirmationReceipt:
    """Construct a receipt from a frame that reports itself as the issuer.

    The receipt carries two preconditions beyond the issuer check -- that the
    affirmation was explicit and that validation passed -- and they are
    unreachable from a test module because the issuer check fires first. This
    helper executes the construction in a namespace whose module name is the
    issuer's, so those inner guards can be exercised directly.

    That this works at all is the point made in the receipt's own docstring:
    the frame check stops mistakes, not intent. The static analysis in
    test_no_silent_write.py is what covers the deliberate case.
    """
    namespace = {
        "__name__": receipt_mod.ISSUER_MODULE,
        "ConfirmationReceipt": ConfirmationReceipt,
        "kwargs": kwargs,
    }
    exec("result = ConfirmationReceipt(**kwargs)", namespace)  # noqa: S102
    return namespace["result"]


def test_the_helper_really_does_bypass_the_issuer_check(passing):
    """Guard on the guard.

    If this helper silently stopped working, the two tests below would pass
    for the wrong reason -- catching the issuer error instead of the
    precondition they mean to test.
    """
    candidate, report = passing
    receipt = _mint_as_issuer(
        field_id="pan",
        candidate_id=candidate.candidate_id,
        candidate_fingerprint="x",
        validation=report,
        affirmation=parse_affirmation("yes"),
    )
    assert receipt.field_id == "pan"


def test_the_receipt_refuses_a_non_explicit_affirmation(passing):
    """Defence in depth inside the receipt itself.

    `confirm()` already declines to call the constructor in this case. The
    receipt re-checks anyway, so a future edit inside the confirmation module
    cannot mint one by skipping that branch.
    """
    candidate, report = passing

    with pytest.raises(UnauthorizedIssuer, match="not.*explicit"):
        _mint_as_issuer(
            field_id="pan",
            candidate_id=candidate.candidate_id,
            candidate_fingerprint="x",
            validation=report,
            affirmation=parse_affirmation("no"),
        )


def test_the_receipt_refuses_a_failed_validation(gate):
    candidate = Candidate(
        field_id="aadhaar", value="747910984993", raw_utterance="x", confidence=0.9
    )
    failed = gate.check(candidate)

    with pytest.raises(UnauthorizedIssuer, match="failed validation"):
        _mint_as_issuer(
            field_id="aadhaar",
            candidate_id=candidate.candidate_id,
            candidate_fingerprint="x",
            validation=failed,
            affirmation=parse_affirmation("yes"),
        )
