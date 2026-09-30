"""Static analysis of the silent-write guarantee.

SPEC.md section 2 states that the LLM never writes a form value, and that the
guarantee rests on three mechanisms. Two of them -- a private single write path
and a capability-guarded receipt -- are properties of the code as written today.
Nothing stops a later change from routing around them.

This module is the third mechanism. It parses the package and fails the build if
any of the following becomes true:

  * `gate/` or `formstate/` acquires a dependency on the model client or on the
    extraction layer;
  * a `ConfirmationReceipt` is constructed outside the confirmation module;
  * private form state is read or written outside its own module.

These tests are the artefact cited as evidence for the safety claim, because
they detect *regression* of the property rather than merely documenting it. A
test that passes vacuously today -- because the module it guards has not been
written yet -- still guards it the day it is.

If you are here because one of these failed: the fix is almost never to relax
the test. It is to route the write back through
`FormState.commit(candidate, receipt)`.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1] / "lucidform"

# Modules that must stay free of any model dependency, so that the accept /
# reject decision and the write path remain reproducible and independent of
# model version, sampling, or prompt phrasing (METHODOLOGY M0.2).
LLM_FREE_PACKAGES = ("gate", "formstate")

FORBIDDEN_IMPORTS = ("anthropic", "lucidform.extract", "openai", "httpx")

RECEIPT_ISSUER = PACKAGE / "orchestrate" / "confirm.py"
STATE_MODULE = PACKAGE / "formstate" / "state.py"

PRIVATE_STATE_ATTR = "_values"


def _python_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.py") if "__pycache__" not in p.parts)


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _imported_names(tree: ast.Module) -> list[tuple[str, int]]:
    """Every module name this file imports, with line numbers."""
    found: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend((alias.name, node.lineno) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.append((node.module, node.lineno))
                # `from lucidform import extract` reads as module `lucidform`
                # with name `extract` -- reconstruct the dotted path so it is
                # caught by the same prefix check.
                found.extend(
                    (f"{node.module}.{alias.name}", node.lineno)
                    for alias in node.names
                )
    return found


def _rel(path: Path) -> str:
    return path.relative_to(PACKAGE.parent).as_posix()


@pytest.mark.parametrize("package", LLM_FREE_PACKAGES)
def test_decision_and_write_paths_import_no_model(package: str) -> None:
    """The gate and the write path must not be able to call a model.

    This is the load-bearing test. A validator that can consult a model is not
    deterministic, cannot be exhaustively tested against the adversarial suite,
    and produces accept/reject decisions that change with the model version.
    """
    root = PACKAGE / package
    violations: list[str] = []

    for path in _python_files(root):
        for name, lineno in _imported_names(_parse(path)):
            for forbidden in FORBIDDEN_IMPORTS:
                if name == forbidden or name.startswith(forbidden + "."):
                    violations.append(f"{_rel(path)}:{lineno} imports {name}")

    assert not violations, (
        f"lucidform/{package}/ must contain no model dependency -- "
        "the accept/reject decision and the write path are deterministic by "
        "design (SPEC.md section 2). Found:\n  " + "\n  ".join(violations)
    )


def test_receipts_are_minted_only_by_the_confirmation_module() -> None:
    """`ConfirmationReceipt(...)` may be called only in orchestrate/confirm.py.

    The receipt is the capability that authorises a write. If any other module
    can mint one, the confirmation step becomes optional -- which is precisely
    the silent write this project exists to rule out.
    """
    violations: list[str] = []

    for path in _python_files(PACKAGE):
        if path == RECEIPT_ISSUER:
            continue
        for node in ast.walk(_parse(path)):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = (
                func.id
                if isinstance(func, ast.Name)
                else func.attr
                if isinstance(func, ast.Attribute)
                else None
            )
            if name == "ConfirmationReceipt":
                violations.append(f"{_rel(path)}:{node.lineno}")

    assert not violations, (
        "ConfirmationReceipt may only be constructed in "
        f"{_rel(RECEIPT_ISSUER)}. Constructed at:\n  " + "\n  ".join(violations)
    )


def test_private_form_state_is_not_touched_from_outside() -> None:
    """`FormState._values` is reachable only from formstate/state.py.

    Python has no enforced privacy, so the underscore is a convention that this
    test upgrades into a build failure. Any external access is a second write
    path, whether or not it was intended as one.
    """
    violations: list[str] = []

    for path in _python_files(PACKAGE):
        if path == STATE_MODULE:
            continue
        for node in ast.walk(_parse(path)):
            if isinstance(node, ast.Attribute) and node.attr == PRIVATE_STATE_ATTR:
                violations.append(f"{_rel(path)}:{node.lineno}")

    assert not violations, (
        f"FormState.{PRIVATE_STATE_ATTR} is private to {_rel(STATE_MODULE)}. "
        "Use commit(candidate, receipt) -- it re-verifies the receipt against "
        "the candidate at the write site. Touched at:\n  "
        + "\n  ".join(violations)
    )


def test_the_scan_actually_sees_the_package() -> None:
    """Guard against the suite passing because it scanned nothing.

    Every test above is a negative assertion, so a broken path would make all
    of them pass while checking no code at all. This asserts the scan has
    something to scan.
    """
    files = _python_files(PACKAGE)
    assert len(files) >= 5, f"only found {len(files)} python files under {PACKAGE}"
    assert (PACKAGE / "gate").is_dir()
    assert (PACKAGE / "formstate").is_dir()


def test_forbidden_import_detection_works() -> None:
    """Prove the import check can actually fail.

    A rule this important should not be trusted on the strength of a green run
    against code that happens to be clean. This feeds it a known violation.
    """
    tree = ast.parse("import anthropic\nfrom lucidform.extract import extractor\n")
    names = [n for n, _ in _imported_names(tree)]

    def is_violation(name: str) -> bool:
        return any(
            name == f or name.startswith(f + ".") for f in FORBIDDEN_IMPORTS
        )

    assert any(is_violation(n) for n in names if n == "anthropic")
    assert any(is_violation(n) for n in names if n.startswith("lucidform.extract"))
    assert not is_violation("lucidform.models")
    # Prefix matching must not fire on a module that merely starts with the
    # same letters -- `anthropic_helpers` is not `anthropic`.
    assert not is_violation("anthropic_helpers")
