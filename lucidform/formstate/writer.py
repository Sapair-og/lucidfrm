"""Export confirmed values into the AcroForm PDF.

The exporter is deliberately dull. It reads `FormState.values`, which contains
only values that passed the gate and were explicitly confirmed, and writes those
and nothing else. It performs no validation, no defaulting, and no coercion --
every one of those would be a decision made after the point at which the user
gave consent, about a document they cannot read.

Two properties it must have, both tested:

  * A field with no confirmed value is left blank. Never defaulted, never
    filled from a persona, never carried over from the template.
  * A field the user declined is blank and indistinguishable from one never
    reached. The *reason* a field is empty lives in the event log, which is
    where a reviewer should look; encoding it in the PDF would put text into a
    form field that the user never said.
"""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from pypdf import PdfReader, PdfWriter

from lucidform.config import get_settings
from lucidform.formstate.state import FormState
from lucidform.schema.loader import FormSchema


class ExportError(RuntimeError):
    """The export could not be performed. Never partially completed."""


def export(
    state: FormState,
    schema: FormSchema,
    out: Path,
    template: Path | None = None,
    stamp: str | None = None,
) -> Path:
    """Write the confirmed values into a copy of the blank form.

    The template is never modified; a new document is produced each time, so an
    export can be repeated and compared.
    """
    settings = get_settings()
    template = Path(template or settings.form_pdf)
    out = Path(out)

    if not template.exists():
        raise ExportError(
            f"{template} not found. Generate it with: "
            "python -m lucidform.schema.make_form"
        )

    values: Mapping[str, str] = state.values
    unknown = set(values) - set(schema.ids)
    if unknown:
        # Cannot happen through the pipeline, since the gate rejects unknown
        # fields. Checked anyway: writing to a widget the schema does not
        # describe would put a value somewhere nothing validated.
        raise ExportError(f"confirmed values for unknown fields: {sorted(unknown)}")

    # Map our stable field ids onto the PDF's widget names.
    by_widget = {
        schema.by_id(field_id).acroform_name: value
        for field_id, value in values.items()
    }

    reader = PdfReader(str(template))
    writer = PdfWriter(clone_from=reader)
    # Without NeedAppearances, many viewers render a filled field as blank --
    # which for this project would mean a user being told the form is complete
    # while it appears empty to whoever receives it.
    writer.set_need_appearances_writer(True)

    for page in writer.pages:
        present = {
            str(annot.get_object().get("/T"))
            for annot in (page.get("/Annots") or [])
            if annot.get_object().get("/T") is not None
        }
        on_this_page = {k: v for k, v in by_widget.items() if k in present}
        if on_this_page:
            writer.update_page_form_field_values(page, on_this_page)

    if stamp:
        # LF-006: a form that is not finished and approved must say so on its
        # face, so nobody mistakes it for a completed application.
        for page in writer.pages:
            page.merge_page(_stamp_page(stamp, page.mediabox.width, page.mediabox.height))

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)
    return out


def _stamp_page(text: str, width: float, height: float):
    """A one-page PDF carrying a large diagonal watermark."""
    import io

    from reportlab.pdfgen import canvas

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(float(width), float(height)))
    c.setFillColorRGB(0.85, 0.1, 0.1, alpha=0.35)
    c.setFont("Helvetica-Bold", 44)
    c.translate(float(width) / 2, float(height) / 2)
    c.rotate(35)
    c.drawCentredString(0, 0, text)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def read_back(pdf: Path) -> dict[str, str]:
    """Read the filled values out of an exported PDF.

    Used by the tests to verify that what was committed is what landed in the
    document, and available for a reviewer who wants to check an export without
    opening a viewer.
    """
    reader = PdfReader(str(pdf))
    fields = reader.get_fields() or {}
    out: dict[str, str] = {}
    for name, obj in fields.items():
        value = obj.get("/V")
        out[str(name)] = "" if value is None else str(value)
    return out
