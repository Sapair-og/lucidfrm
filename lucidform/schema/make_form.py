"""Generate the target fillable PDF (AcroForm).

The prototype's form reproduces the field set of the standard individual KYC
form. It is generated from `ckyc_form.yaml` rather than shipped as a binary so
the corpus is reproducible from source and no third-party document is
redistributed (METHODOLOGY M0.4).

Generating the form also gives a genuine round-trip test: this module writes the
AcroForm, `loader.py` reads it back, and `tests/test_schema_loader.py` asserts
the two agree. A parser that only ever sees one hand-made file proves less.

The PDF itself is English -- it stands in for a real government form, which is
English. The plain-language and Hindi layer lives in the conversation, which is
the actual point of the system.

    python -m lucidform.schema.make_form
"""

from __future__ import annotations

from pathlib import Path

import yaml
from reportlab.lib.colors import Color, black, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from lucidform.config import get_settings

PAGE_W, PAGE_H = A4
MARGIN = 45
LABEL_SIZE = 9
FIELD_H = 20
ROW_GAP = 34
BORDER = Color(0.55, 0.55, 0.6)


def _overlay(path: Path | None = None) -> dict:
    path = path or get_settings().schema_overlay
    with Path(path).open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _header(c: canvas.Canvas, spec: dict, page: int) -> float:
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, PAGE_H - MARGIN, spec["title"])
    c.setFont("Helvetica", 7.5)
    c.setFillColor(Color(0.4, 0.4, 0.4))
    c.drawString(
        MARGIN,
        PAGE_H - MARGIN - 14,
        "SYNTHETIC TEMPLATE - generated for research. Not an official form. "
        "Do not submit. Do not enter real personal data.",
    )
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN, f"Page {page}")
    c.setFillColor(black)
    c.line(MARGIN, PAGE_H - MARGIN - 22, PAGE_W - MARGIN, PAGE_H - MARGIN - 22)
    return PAGE_H - MARGIN - 52


def build(out: Path | None = None, overlay: Path | None = None) -> Path:
    spec = _overlay(overlay)
    settings = get_settings()
    out = Path(out) if out else settings.form_pdf
    out.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(out), pagesize=A4)
    c.setTitle(spec["title"])
    page = 1
    y = _header(c, spec, page)
    form = c.acroForm

    for fld in spec["fields"]:
        if y < MARGIN + ROW_GAP * 2:
            c.showPage()
            page += 1
            y = _header(c, spec, page)
            form = c.acroForm

        required = " *" if fld.get("required", True) else ""
        c.setFont("Helvetica", LABEL_SIZE)
        c.drawString(MARGIN, y, f"{fld['label']}{required}")

        width = PAGE_W - 2 * MARGIN
        common = dict(
            name=fld["acroform_name"],
            tooltip=fld["label"],
            x=MARGIN,
            y=y - FIELD_H - 4,
            width=width,
            height=FIELD_H,
            borderColor=BORDER,
            fillColor=white,
            textColor=black,
            forceBorder=True,
            fontName="Helvetica",
            fontSize=10,
        )

        # Enums are rendered as text widgets, not dropdowns. A blank KYC
        # template must not ship with a pre-selected gender or income band --
        # a default value in an unfilled form is a value nobody confirmed.
        # (reportlab's choice widget also requires a non-empty default, so a
        # blank dropdown is not available to us in any case.) The permitted
        # option list is therefore a semantic constraint carried by the
        # overlay, which is exactly the split METHODOLOGY M0.4 describes: the
        # document carries structure, the overlay carries meaning.
        max_len = fld.get("max_length")
        if fld["type"] == "enum":
            max_len = max(len(v) for v in fld["enum_values"])

        # maxlen becomes /MaxLen in the field dictionary -- the one genuine
        # constraint the PDF itself carries.
        form.textfield(value="", maxlen=max_len, **common)

        y -= ROW_GAP

    c.setFont("Helvetica", 7)
    c.setFillColor(Color(0.45, 0.45, 0.45))
    c.drawString(MARGIN, MARGIN - 12, "* required")
    c.save()
    return out


if __name__ == "__main__":  # pragma: no cover
    path = build()
    print(f"wrote {path}")
