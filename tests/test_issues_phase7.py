"""Regression tests for docs/ISSUES.md LF-014: filling the user's own PDF."""

from __future__ import annotations

import pytest
from reportlab.pdfgen import canvas

from lucidform.cli import _choose_pdf
from lucidform.eval.events import EventLog
from lucidform.extract.client import ScriptedClient
from lucidform.extract.extractor import Extractor
from lucidform.formstate.state import FormState
from lucidform.formstate.writer import export, read_back
from lucidform.gate.gate import ValidationGate
from lucidform.models import Candidate, FieldType, Status
from lucidform.orchestrate.session import Session
from lucidform.schema.custom import open_form
from lucidform.schema.loader import SchemaError
from tests.make_custom_form import build
from tests.test_session import Puppet, value


@pytest.fixture
def bank(tmp_path):
    return build(tmp_path / "bank.pdf")


def test_known_fields_take_our_rules(bank):
    form = open_form(bank)
    by_widget = {f.acroform_name: f for f in form.schema.fields}
    assert by_widget["txtApplicantName"].id == "full_name"
    assert by_widget["PAN_No"].type is FieldType.PAN
    assert by_widget["Text12"].id == "pin"  # recognised by its tooltip
    assert by_widget["cboGender"].enum_values == ("Male", "Female", "Other")
    assert "Male, Female, Other" in by_widget["cboGender"].ask("en")


def test_other_peoples_names_stay_generic(bank):
    by_widget = {f.acroform_name: f for f in open_form(bank).schema.fields}
    for name in ("NomineeName", "BankBranch"):
        assert by_widget[name].type is FieldType.TEXT and not by_widget[name].required
    assert "Nominee Name" in by_widget["NomineeName"].ask("en")


def test_tick_boxes_are_listed_not_asked(bank):
    form = open_form(bank)
    assert form.skipped == ("I agree",)
    assert "chkAgree" not in {f.acroform_name for f in form.schema.fields}


def test_rules_still_apply_on_a_custom_form(bank):
    schema = open_form(bank).schema
    cand = Candidate(field_id="pan", value="ABCDE12345", raw_utterance="x", confidence=0.9)
    assert ValidationGate(schema).check(cand, {}).status is Status.REJECT


def test_windows_copy_as_path_quotes_are_accepted(bank):
    assert open_form(f'"{bank}"').kind == "acroform"


def test_official_form_is_recognised():
    assert open_form("data/forms/official/ckyc_individual_amfi.pdf").kind == "official"


@pytest.mark.parametrize("problem", ["missing", "not_pdf", "flat"])
def test_unusable_files_are_refused_with_a_reason(tmp_path, problem):
    if problem == "missing":
        path, reason = tmp_path / "nope.pdf", "no file"
    elif problem == "not_pdf":
        path, reason = tmp_path / "a.txt", "not a PDF"
        path.write_text("hi")
    else:
        path, reason = tmp_path / "flat.pdf", "no fillable fields"
        c = canvas.Canvas(str(path))
        c.drawString(100, 700, "Name: ________")
        c.save()
    with pytest.raises(SchemaError, match=reason):
        open_form(path)


def test_fill_and_export_a_custom_form(bank, tmp_path):
    form = open_form(bank)
    ids = ("full_name", "pan", "nominee_name")
    sub = type(form.schema)(
        form_id=form.schema.form_id, version=1, title="t",
        fields=tuple(form.schema.by_id(i) for i in ids),
    )
    log = EventLog(tmp_path, session_id="custom")
    channel = Puppet(["ramesh kumar sharma", "yes", "AKQPS3417M", "yes", "sunita sharma", "yes", "yes"])
    state = FormState(log=log)
    result = Session(
        schema=sub,
        extractor=Extractor(ScriptedClient([
            value(value="Ramesh Kumar Sharma", quote="ramesh kumar sharma"),
            value(value="AKQPS3417M", quote="AKQPS3417M"),
            value(value="Sunita Sharma", quote="sunita sharma"),
        ]), sub, log=log),
        gate=ValidationGate(sub), state=state,
        input_channel=channel, output_channel=channel, log=log,
    ).run()
    assert result.approved
    out = export(state, sub, tmp_path / "filled.pdf", template=form.pdf)
    written = read_back(out)
    assert written["txtApplicantName"] == "Ramesh Kumar Sharma"
    assert written["PAN_No"] == "AKQPS3417M"
    assert written["NomineeName"] == "Sunita Sharma"


def test_custom_form_dates_are_written_day_first(bank, tmp_path):
    form = open_form(bank)

    class Values:
        values = {"dob": "1987-03-14"}

    out = export(Values(), form.schema, tmp_path / "d.pdf", template=form.pdf, date_format="%d/%m/%Y")
    assert read_back(out)["DOB"] == "14/03/1987"


class _Console(Puppet):
    pass


def test_ask_then_paste_path(bank):
    channel = _Console(["yes", "C:/no/such/file.pdf", str(bank)])
    form = _choose_pdf(channel, None, "en")
    assert form is not None and form.kind == "acroform"
    said = " ".join(t for _, t in channel.said)
    assert "cannot use that file" in said and "ticked or signed by hand" in said


def test_saying_no_keeps_the_built_in_form():
    assert _choose_pdf(_Console(["no"]), None, "en") is None


def test_three_bad_paths_fall_back(tmp_path):
    channel = _Console(["yes", "a", "b", "c"])
    assert _choose_pdf(channel, None, "en") is None
    assert any("built-in KYC form" in t for _, t in channel.said)
