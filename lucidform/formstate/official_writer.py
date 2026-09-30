"""Write confirmed values onto the official CKYC form (ISSUES.md LF-001).

The official PDF is a flat print layout: no form fields, just printed boxes,
one per character. This draws each confirmed value into its boxes on a
transparent overlay and merges it onto a copy of the form. The source PDF is
never modified.

What gets drawn comes only from FormState -- confirmed values -- plus three
kinds of pure presentation, none of which invents information:

  * reshaping a confirmed value for the paper form: BLOCK letters (the form's
    instruction C), a name split into first / middle / last, an address
    wrapped over three lines, a date split into DD MM YYYY, a state name
    written as its two-letter code from the form's own list;
  * ticking the box that matches a confirmed choice (gender, marital status…);
  * fixed facts about this application that the form requires and that are
    true of every session: Application Type "New", Account Type "Normal", and
    country code IN for an Indian PIN address. The declaration date is the day
    the form is produced.

A field whose `ask_if` condition does not hold is not drawn, even if an older
value is stored for it.
"""

from __future__ import annotations

import datetime as dt
import io
from pathlib import Path
from typing import Mapping

import yaml
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from lucidform.config import get_settings
from lucidform.formstate.state import FormState
from lucidform.formstate.writer import ExportError, _stamp_page
from lucidform.schema.loader import FormSchema

MIN_FONT = 4.5


class _Pages:
    """One reportlab canvas per PDF page, drawn in PDF user space (origin bottom-left)."""

    def __init__(self, sizes: list[tuple[float, float]], font: str, size: float) -> None:
        self.sizes = sizes
        self.font, self.size = font, size
        self.buffers = [io.BytesIO() for _ in sizes]
        self.canvases = [canvas.Canvas(b, pagesize=s) for b, s in zip(self.buffers, sizes)]
        self.used = [False] * len(sizes)

    def _y(self, page: int, bottom: float) -> float:
        return self.sizes[page][1] - bottom

    def boxes(self, slot: Mapping, text: str, upper: bool = True) -> None:
        """One character per box; if it does not fit, shrink across the whole span."""
        text = (text or "").upper() if upper else (text or "")
        if not text:
            return
        page, cells = slot["page"], slot["cells"]
        c = self.canvases[page]
        self.used[page] = True
        height = slot["bottom"] - slot["top"]
        baseline = self._y(page, slot["bottom"]) + height * 0.25
        if len(text) <= len(cells):
            c.setFont(self.font, self.size)
            for ch, (x0, x1) in zip(text, cells):
                c.drawCentredString((x0 + x1) / 2, baseline, ch)
            return
        # Too long for the boxes: write it as one run over the whole span in a
        # smaller font, never truncated -- a cut-off value is a wrong value.
        span = cells[-1][1] - cells[0][0] - 2
        size = self.size
        while size > MIN_FONT and stringWidth(text, self.font, size) > span:
            size -= 0.25
        c.setFont(self.font, size)
        c.drawString(cells[0][0] + 1, baseline, text)

    def date(self, slot: Mapping, iso: str) -> None:
        try:
            d = dt.date.fromisoformat(iso)
        except ValueError:
            return
        page = slot["page"]
        for part, text in (("day", f"{d.day:02d}"), ("month", f"{d.month:02d}"), ("year", f"{d.year:04d}")):
            self.boxes({"page": page, "top": slot["top"], "bottom": slot["bottom"], "cells": slot[part]}, text)

    def tick(self, box: Mapping) -> None:
        page = box["page"]
        c = self.canvases[page]
        self.used[page] = True
        size = box.get("size", 8.5)
        c.setFont("Helvetica-Bold", size + 1)
        x = box["x"] + size / 2
        y = self._y(page, box["top"] + size) + size * 0.15
        c.drawCentredString(x, y, "X")

    def pages(self):
        for c in self.canvases:
            c.save()
        return [PdfReader(b).pages[0] if used else None for b, used in zip(self.buffers, self.used)]


def split_name(full: str) -> tuple[str, str, str]:
    parts = (full or "").split()
    if not parts:
        return "", "", ""
    if len(parts) == 1:
        return parts[0], "", ""
    return parts[0], " ".join(parts[1:-1]), parts[-1]


def wrap(text: str, widths: list[int]) -> list[str]:
    """Greedy word wrap into lines of the given box counts; the last line takes the rest."""
    words, lines = (text or "").split(), []
    for i, width in enumerate(widths):
        if i == len(widths) - 1:
            lines.append(" ".join(words))
            break
        line = ""
        while words and len((line + " " + words[0]).strip()) <= width:
            line = (line + " " + words.pop(0)).strip()
        if not line and words:  # one word longer than the line: let it overflow here
            line = words.pop(0)
        lines.append(line)
    return lines


def _address(p: _Pages, block: Mapping, v: Mapping[str, str], prefix: str, codes: Mapping) -> None:
    lines = wrap(v.get(f"{prefix}address_line", ""), [len(s["cells"]) for s in block["lines"]])
    for slot, line in zip(block["lines"], lines):
        p.boxes(slot, line)
    p.boxes(block["city"], v.get(f"{prefix}city", ""))
    p.boxes(block["district"], v.get(f"{prefix}district", ""))
    p.boxes(block["pin"], v.get(f"{prefix}pin", ""))
    p.boxes(block["state_code"], codes.get(v.get(f"{prefix}state", ""), ""))
    if v.get(f"{prefix}pin"):
        p.boxes(block["country_code"], "IN")


def export_official(
    state: FormState,
    schema: FormSchema,
    out: Path,
    *,
    stamp: str | None = None,
    today: dt.date | None = None,
    template: Path | None = None,
    layout_path: Path | None = None,
) -> Path:
    settings = get_settings()
    template = Path(template or settings.official_pdf)
    layout = yaml.safe_load(Path(layout_path or settings.official_layout).read_text(encoding="utf-8"))
    if not template.exists():
        raise ExportError(f"{template} not found")

    unknown = set(state.values) - set(schema.ids)
    if unknown:
        raise ExportError(f"confirmed values for unknown fields: {sorted(unknown)}")
    # Only values whose field applies; an answer that stopped applying at the
    # review is not printed.
    v = {k: val for k, val in state.values.items() if schema.by_id(k).applies(state.values)}

    reader = PdfReader(str(template))
    sizes = [(float(pg.mediabox.width), float(pg.mediabox.height)) for pg in reader.pages]
    p = _Pages(sizes, layout["font"], layout["font_size"])
    L, codes = layout["fields"], layout["state_codes"]

    for box in layout["constant_ticks"].values():
        p.tick(box)

    first, middle, last = split_name(v.get("full_name", ""))
    p.boxes(L["name"]["prefix"], v.get("prefix", ""))
    p.boxes(L["name"]["first"], first)
    p.boxes(L["name"]["middle"], middle)
    p.boxes(L["name"]["last"], last)
    first, middle, last = split_name(v.get("father_name", ""))
    p.boxes(L["father"]["first"], first)
    p.boxes(L["father"]["middle"], middle)
    p.boxes(L["father"]["last"], last)
    if v.get("dob"):
        p.date(L["dob"], v["dob"])

    pan = v.get("pan", "")
    pan_field = schema.by_id("pan")
    if pan and pan == pan_field.decline_value:
        p.tick(L["form60_tick"])
    else:
        p.boxes(L["pan"], pan)

    for fid in ("gender", "marital_status", "citizenship", "residential_status"):
        if v.get(fid) in L[fid]:
            p.tick(L[fid][v[fid]])

    poi = v.get("poi_type")
    if poi in L["poi_tick"]:
        p.tick(L["poi_tick"][poi])
    if poi in L["poi_number"] and v.get("poi_number"):
        p.boxes(L["poi_number"][poi], v["poi_number"])
    if poi in L["poi_expiry"] and v.get("poi_expiry"):
        p.date(L["poi_expiry"][poi], v["poi_expiry"])

    _address(p, L["address"], v, "", codes)

    if v.get("same_address") == "Yes":
        p.tick(L["same_address_tick"])
    elif v.get("same_address") == "No":
        cur = v.get("cur_poa_type")
        if cur in L["cur_poa_tick"]:
            p.tick(L["cur_poa_tick"][cur])
        elif cur in layout["deemed_codes"]:
            p.tick(L["cur_poa_tick"]["deemed"])
            p.boxes(L["deemed_code"], layout["deemed_codes"][cur])
        if cur in L["cur_poa_number"] and v.get("cur_poa_number"):
            p.boxes(L["cur_poa_number"][cur], v["cur_poa_number"])
        _address(p, L["cur_address"], v, "cur_", codes)

    if v.get("mobile"):
        p.boxes({**L["mobile"]["country"], "cells": L["mobile"]["country"]["cells"][1:]}, "91")
        p.boxes(L["mobile"]["number"], v["mobile"])
    if v.get("email"):
        # Email is case-insensitive in practice, but kept as confirmed: BLOCK
        # letters would print a different-looking address from the one read back.
        p.boxes(L["email"], v["email"], upper=False)
    p.boxes(L["place"], v.get("place", ""))
    p.date(L["declaration_date"], (today or dt.date.today()).isoformat())

    writer = PdfWriter(clone_from=reader)
    for page, overlay in zip(writer.pages, p.pages()):
        if overlay is not None:
            page.merge_page(overlay)
    if stamp:
        for page in writer.pages[:2]:
            page.merge_page(_stamp_page(stamp, page.mediabox.width, page.mediabox.height))

    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)
    return out
