"""Round-trip: the generator writes the AcroForm, the loader reads it back.

Because the target PDF is generated from the same overlay the loader merges,
these tests check that the two halves genuinely agree rather than that the
parser can cope with one hand-made file. A parser that has only ever seen a
single fixture proves very little.
"""

from __future__ import annotations

import pytest
import yaml

from lucidform.config import get_settings
from lucidform.models import FieldType
from lucidform.schema import loader, make_form


@pytest.fixture(scope="module")
def built_pdf(tmp_path_factory):
    out = tmp_path_factory.mktemp("forms") / "ckyc.pdf"
    return make_form.build(out=out)


@pytest.fixture(scope="module")
def schema(built_pdf):
    return loader.load(pdf_path=built_pdf)


@pytest.fixture(scope="module")
def overlay():
    return loader.load_overlay(get_settings().schema_overlay)


def test_every_overlay_field_survives_the_round_trip(schema, overlay):
    assert schema.ids == tuple(f["id"] for f in overlay["fields"])


def test_max_length_comes_from_the_pdf_not_the_overlay(built_pdf):
    """/MaxLen must be read from the document.

    pypdf's `get_fields()` collapses to the field level and drops /MaxLen,
    which lives on the widget annotation. A parser built on it silently reports
    no length constraint anywhere and falls back to whatever the overlay
    asserts -- making the PDF decorative. This asserts the parser reads the
    document itself.
    """
    parsed = loader.parse_acroform(built_pdf)
    assert parsed, "parser found no widgets"
    assert all(
        entry["max_length"] is not None for entry in parsed.values()
    ), "at least one widget carries no /MaxLen -- the parser is not reading the PDF"
    assert parsed["pan"]["max_length"] == 10
    assert parsed["aadhaar"]["max_length"] == 12
    assert parsed["pin"]["max_length"] == 6


def test_enum_fields_carry_their_option_list(schema):
    gender = schema.by_id("gender")
    assert gender.type is FieldType.ENUM
    assert gender.enum_values == ("Male", "Female", "Transgender")
    assert schema.by_id("state").enum_values, "state must have options"


def test_the_blank_template_has_no_prefilled_values(built_pdf):
    """An unfilled template must not carry a default for any field.

    A pre-selected gender or income band is a value nobody confirmed. If the
    exporter ever wrote the template wholesale, those defaults would land in
    the output as though they had been through the gate.
    """
    from pypdf import PdfReader

    reader = PdfReader(str(built_pdf))
    for page in reader.pages:
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            if obj.get("/T") is None:
                continue
            assert not obj.get("/V"), f"{obj.get('/T')} ships with a default value"


def test_cross_field_dependencies_are_declared(schema):
    """The two cross-field checks must have their inputs wired up."""
    assert schema.by_id("pan").depends_on == ("full_name",)
    assert schema.by_id("pin").depends_on == ("state",)


def test_every_field_has_a_plain_language_prompt_and_gloss(schema):
    """The system exists to explain fields, so an unexplained field is a bug.

    Checked for both languages: a missing Hindi string falls back to English
    silently at runtime, which would show up in a demo as the assistant
    switching language mid-form rather than as an error.
    """
    for field in schema:
        for lang in ("en", "hi"):
            assert field.prompt.get(lang), f"{field.id}: no {lang} prompt"
            assert field.gloss.get(lang), f"{field.id}: no {lang} gloss"


def test_required_fields_are_marked(schema):
    assert schema.by_id("pan").required
    assert not schema.by_id("email").required, "email is the one optional field"


def test_a_field_missing_from_the_pdf_is_fatal(built_pdf, tmp_path, overlay):
    """A field the PDF does not have must raise, not be skipped.

    A silently dropped field is a field the gate never validates and the user
    is never asked for -- it would leave the form incomplete with no error.
    """
    bad = dict(overlay)
    bad["fields"] = overlay["fields"] + [
        {
            "id": "ghost",
            "acroform_name": "ghost_widget",
            "label": "Ghost",
            "type": "text",
        }
    ]
    path = tmp_path / "bad_overlay.yaml"
    path.write_text(yaml.safe_dump(bad, allow_unicode=True), encoding="utf-8")

    with pytest.raises(loader.SchemaError, match="absent from the PDF"):
        loader.load(pdf_path=built_pdf, overlay_path=path)


@pytest.mark.parametrize(
    "names, message",
    [
        ({"Male": ["purush"], "Female": ["purush"]}, "declared for both"),
        ({"Man": ["purush"]}, "non-options"),
    ],
)
def test_an_ambiguous_or_orphan_enum_name_is_fatal(built_pdf, tmp_path, overlay, names, message):
    """One spoken name for two options would make the gate choose for the user."""
    import copy

    bad = copy.deepcopy(overlay)
    gender = next(f for f in bad["fields"] if f["id"] == "gender")
    gender["enum_names"] = names
    path = tmp_path / "bad_overlay.yaml"
    path.write_text(yaml.safe_dump(bad, allow_unicode=True), encoding="utf-8")
    with pytest.raises(loader.SchemaError, match=message):
        loader.load(pdf_path=built_pdf, overlay_path=path)


def test_declared_enum_names_are_loaded(schema):
    gender = schema.by_id("gender")
    assert "purush" in gender.enum_names["Male"]


def test_a_widget_with_no_overlay_entry_is_fatal(built_pdf, tmp_path, overlay):
    """Conversely, a PDF widget nothing validates must raise."""
    bad = dict(overlay)
    bad["fields"] = [f for f in overlay["fields"] if f["id"] != "email"]
    path = tmp_path / "short_overlay.yaml"
    path.write_text(yaml.safe_dump(bad, allow_unicode=True), encoding="utf-8")

    with pytest.raises(loader.SchemaError, match="no overlay entry"):
        loader.load(pdf_path=built_pdf, overlay_path=path)


def test_missing_pdf_names_the_fix():
    """The error should tell you the command to run, not just fail."""
    with pytest.raises(loader.SchemaError, match="make_form"):
        loader.load(pdf_path="does/not/exist.pdf")
