"""Export: what was confirmed is what lands in the document, and nothing else.

This is the last link in the chain. Every guarantee upstream is worthless if
the exporter adds, defaults, or coerces a value on the way out -- so these
tests check the negative cases as hard as the positive one.
"""

from __future__ import annotations

import pytest

from lucidform.formstate.state import FormState
from lucidform.formstate.writer import ExportError, export, read_back
from lucidform.gate.gate import ValidationGate
from lucidform.models import Candidate
from lucidform.orchestrate.confirm import confirm
from lucidform.schema import loader, make_form

CONTEXT = {"full_name": "Ramesh Kumar Sharma", "state": "Rajasthan"}


@pytest.fixture(scope="module")
def template(tmp_path_factory):
    return make_form.build(out=tmp_path_factory.mktemp("tpl") / "blank.pdf")


@pytest.fixture(scope="module")
def schema(template):
    return loader.load(pdf_path=template)


@pytest.fixture(scope="module")
def gate(schema):
    return ValidationGate(schema)


def commit(state, gate, field_id, value, context=CONTEXT):
    candidate = Candidate(
        field_id=field_id, value=value, raw_utterance=value, confidence=0.95
    )
    report = gate.check(candidate, context)
    _, receipt = confirm(candidate, report, "yes that is correct")
    assert receipt is not None, f"{field_id}={value!r} did not pass the gate"
    return state.commit(candidate, receipt)


def test_confirmed_values_reach_the_document(tmp_path, template, schema, gate):
    state = FormState()
    commit(state, gate, "full_name", "Ramesh Kumar Sharma")
    commit(state, gate, "pan", "AKQPS3417M")
    commit(state, gate, "aadhaar", "747910984992")

    out = export(state, schema, tmp_path / "filled.pdf", template=template)
    written = read_back(out)

    assert written["full_name"] == "Ramesh Kumar Sharma"
    assert written["pan"] == "AKQPS3417M"
    assert written["aadhaar"] == "747910984992"


def test_the_normalized_value_is_what_lands(tmp_path, template, schema, gate):
    """The user confirmed the read-back, which states the normalized form."""
    state = FormState()
    commit(state, gate, "mobile", "+91 98123 45607")

    out = export(state, schema, tmp_path / "filled.pdf", template=template)
    assert read_back(out)["mobile"] == "9812345607"


def test_unconfirmed_fields_are_left_blank(tmp_path, template, schema, gate):
    """The core negative. Anything not confirmed must be empty -- not
    defaulted, not guessed, not carried from the template."""
    state = FormState()
    commit(state, gate, "pan", "AKQPS3417M")

    out = export(state, schema, tmp_path / "filled.pdf", template=template)
    written = read_back(out)

    assert written["pan"] == "AKQPS3417M"
    for field in schema:
        if field.id != "pan":
            assert written[field.id] == "", f"{field.id} was filled without consent"


def test_a_declined_field_is_blank_not_annotated(tmp_path, template, schema, gate):
    """The reason a field is empty belongs in the event log, not the form.

    Writing "declined" into the widget would put text into a form field that
    the user never said, which is the failure this project is about.
    """
    state = FormState()
    commit(state, gate, "pan", "AKQPS3417M")
    state.decline("email", said="mera email nahi hai")

    out = export(state, schema, tmp_path / "filled.pdf", template=template)
    assert read_back(out)["email"] == ""


def test_a_blocked_write_leaves_no_trace_in_the_document(
    tmp_path, template, schema, gate
):
    """End to end, through every layer: a value that failed confirmation must
    not appear in the exported file."""
    from lucidform.formstate.state import SilentWriteBlocked

    state = FormState()
    good = Candidate(
        field_id="pan", value="AKQPS3417M", raw_utterance="x", confidence=0.95
    )
    _, receipt = confirm(good, gate.check(good, CONTEXT), "yes")
    bad = Candidate(
        field_id="pan", value="AKQPB3417M", raw_utterance="x", confidence=0.95
    )
    with pytest.raises(SilentWriteBlocked):
        state.commit(bad, receipt)

    out = export(state, schema, tmp_path / "filled.pdf", template=template)
    written = read_back(out)
    assert written["pan"] == ""
    assert "AKQPB3417M" not in out.read_bytes().decode("latin-1")


def test_a_spoofed_confirmation_never_reaches_the_document(
    tmp_path, template, schema, gate
):
    """The headline case, all the way to the file on disk."""
    state = FormState()
    candidate = Candidate(
        field_id="pan", value="AKQPS3417M", raw_utterance="x", confidence=0.95
    )
    _, receipt = confirm(
        candidate, gate.check(candidate, CONTEXT), "yes I know that's wrong"
    )
    assert receipt is None

    out = export(state, schema, tmp_path / "filled.pdf", template=template)
    assert read_back(out)["pan"] == ""


def test_the_template_is_not_modified(tmp_path, template, schema, gate):
    """Exports must be repeatable, and the blank form must stay blank."""
    before = template.read_bytes()

    state = FormState()
    commit(state, gate, "pan", "AKQPS3417M")
    export(state, schema, tmp_path / "filled.pdf", template=template)

    assert template.read_bytes() == before
    assert all(v == "" for v in read_back(template).values())


def test_exporting_twice_gives_the_same_values(tmp_path, template, schema, gate):
    state = FormState()
    commit(state, gate, "pan", "AKQPS3417M")
    commit(state, gate, "city", "Jaipur")

    first = read_back(export(state, schema, tmp_path / "a.pdf", template=template))
    second = read_back(export(state, schema, tmp_path / "b.pdf", template=template))
    assert first == second


def test_a_missing_template_names_the_fix(tmp_path, schema):
    with pytest.raises(ExportError, match="make_form"):
        export(FormState(), schema, tmp_path / "out.pdf", template=tmp_path / "nope.pdf")


def test_export_refuses_values_for_fields_the_schema_does_not_describe(
    tmp_path, template, schema, gate
):
    """Unreachable through the pipeline -- the gate raises on an unknown field.

    Checked anyway: writing to a widget the schema does not cover would put a
    value somewhere nothing validated.
    """
    state = FormState()
    commit(state, gate, "pan", "AKQPS3417M")
    # Reach past the public API deliberately, to construct the state that
    # would exist if some future code path bypassed the gate.
    object.__getattribute__(state, "__dict__")["_values"]["ghost"] = "x"

    with pytest.raises(ExportError, match="unknown fields"):
        export(state, schema, tmp_path / "out.pdf", template=template)


def test_a_fully_completed_form_round_trips(tmp_path, template, schema, gate):
    """Every field of a real persona, through the whole pipeline and out."""
    from lucidform.eval.personas import load_all

    persona = next(p for p in load_all() if p.persona_id == "p01")
    state = FormState()
    for field in schema:
        truth = persona.truth(field.id)
        if not truth:
            state.decline(field.id)
            continue
        commit(state, gate, field.id, truth, context=state.values)

    out = export(state, schema, tmp_path / "p01.pdf", template=template)
    written = read_back(out)
    for field in schema:
        assert written[field.id] == persona.truth(field.id), field.id
