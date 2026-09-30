"""Measure the official CKYC form's printed boxes and write ckyc_official_layout.yaml.

The official PDF has no form fields, only drawn character boxes. This reads the
vertical box lines of each row with pdfplumber (a dev-only dependency) and
records every cell as [x0, x1] so the runtime writer needs no PDF analysis.

    python tools/build_official_layout.py

Row positions and tick-box rectangles were read off the PDF once (see
docs/ISSUES.md LF-001); the cell boundaries are re-measured every run.
"""

from __future__ import annotations

import collections
from pathlib import Path

import pdfplumber
import yaml

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "data" / "forms" / "official" / "ckyc_individual_amfi.pdf"
OUT = ROOT / "lucidform" / "schema" / "ckyc_official_layout.yaml"


def rows(page) -> dict[int, tuple[list[float], float]]:
    lines = [
        ln for ln in page.lines
        if abs(ln["x0"] - ln["x1"]) < 0.5 and 5 < ln["bottom"] - ln["top"] < 20
    ]
    xs: dict[int, set[float]] = collections.defaultdict(set)
    bottom: dict[int, float] = {}
    for ln in lines:
        k = round(ln["top"])
        xs[k].add(round(ln["x0"], 1))
        bottom[k] = round(ln["bottom"], 1)
    return {k: (sorted(v), bottom[k]) for k, v in xs.items()}


def cells(xs, lo=None, hi=None, max_w=12.0):
    """Consecutive boundary pairs inside [lo, hi] narrow enough to be one box."""
    out = []
    for a, b in zip(xs, xs[1:]):
        if (lo is None or a >= lo - 0.2) and (hi is None or b <= hi + 0.2) and b - a <= max_w:
            out.append([a, b])
    return out


def slot(page, top, bottom, cell_list):
    return {"page": page, "top": float(top), "bottom": float(bottom), "cells": cell_list}


def date_slot(page, top, bottom, cl):
    """D D - M M - Y Y Y Y: ten equal positions, two of them dashes."""
    return {
        "page": page, "top": float(top), "bottom": float(bottom),
        "day": cl[0:2], "month": cl[3:5], "year": cl[6:10],
    }


def tick(page, x, top, size=8.5):
    return {"page": page, "x": x, "top": top, "size": size}


def main() -> None:
    with pdfplumber.open(PDF) as pdf:
        p1, p2 = rows(pdf.pages[0]), rows(pdf.pages[1])

    def r1(top):
        return p1[top]

    def name_row(top):
        xs, bot = r1(top)
        return {
            "prefix": slot(0, top, bot, cells(xs, 130.7, 160.4)),
            "first": slot(0, top, bot, cells(xs, 172.1, 291.1)),
            "middle": slot(0, top, bot, cells(xs, 307.4, 426.5)),
            "last": slot(0, top, bot, cells(xs, 442.8, 561.9)),
        }

    def address_block(t1, t2, t3, t4):
        (x1, b1), (x2, b2), (x3, b3), (x4, b4) = r1(t1), r1(t2), r1(t3), r1(t4)
        return {
            "lines": [
                slot(0, t1, b1, cells(x1)),
                slot(0, t2, b2, cells(x2)),
                slot(0, t3, b3, cells(x3, 76.2, 373.0)),
            ],
            "city": slot(0, t3, b3, cells(x3, 462.0, 561.0)),
            "district": slot(0, t4, b4, cells(x4, 76.2, 195.3)),
            "pin": slot(0, t4, b4, cells(x4, 263.1, 322.6)),
            "state_code": slot(0, t4, b4, cells(x4, 408.2, 428.0)),
            "country_code": slot(0, t4, b4, cells(x4, 541.1, 561.0)),
        }

    def doc_numbers(tops):
        names = ["Passport", "Voter ID", "Driving Licence", "NREGA Job Card", "NPR Letter"]
        return {n: slot(0, t, r1(t)[1], cells(r1(t)[0])) for n, t in zip(names, tops)}

    dob_xs, dob_b = r1(263)
    pexp_xs, pexp_b = r1(377)
    dlexp_xs, dlexp_b = r1(408)
    pan_xs, pan_b = r1(292)
    mob_xs, mob_b = p2[64]
    mobile_cells = cells(mob_xs, 408.2, 557.0)
    email_xs, email_b = p2[80]
    date_xs, date_b = p2[275]
    # The declaration date's second "D" box is drawn wider than the others
    # (61.9 to 82.5, its grey placeholder centred near 72), so it is taken
    # whole rather than measured as a regular cell.
    d1 = [50.5, 61.9]
    d2 = [61.9, 82.5]
    decl_date = {
        "page": 1, "top": 275.0, "bottom": date_b,
        "day": [d1, d2],
        "month": cells(date_xs, 84.5, 107.2),
        "year": cells(date_xs, 118.6, 163.9),
    }

    layout = {
        "source_pdf": "data/forms/official/ckyc_individual_amfi.pdf",
        "font": "Helvetica-Bold",
        "font_size": 8,
        "constant_ticks": {
            "application_type_new": tick(0, 235.6, 144.0),
            "account_type_normal": tick(0, 235.6, 170.6),
        },
        "fields": {
            "name": name_row(209),
            "father": name_row(236),
            "dob": date_slot(0, 263, dob_b, cells(dob_xs)),
            "pan": slot(0, 292, pan_b, cells(pan_xs)),
            "form60_tick": tick(0, 300.1, 294.5, 7.4),
            "gender": {
                "Male": tick(0, 130.8, 278.9),
                "Female": tick(0, 219.8, 278.9),
                "Transgender": tick(0, 300.1, 278.9),
            },
            "marital_status": {
                "Married": tick(0, 131.5, 308.8, 7.4),
                "Unmarried": tick(0, 221.3, 308.8, 7.4),
                "Others": tick(0, 300.1, 308.8, 7.4),
            },
            "citizenship": {
                "Indian": tick(0, 131.5, 322.9, 7.6),
                "Other": tick(0, 221.3, 322.9, 7.6),
            },
            "residential_status": {
                "Resident Individual": tick(0, 131.5, 336.2, 7.6),
                "Non Resident Indian": tick(0, 221.3, 336.2, 7.6),
                "Foreign National": tick(0, 303.2, 337.2, 7.0),
                "Person of Indian Origin": tick(0, 384.5, 336.7, 7.0),
            },
            "poi_tick": {
                "Passport": tick(0, 38.5, 379.1),
                "Voter ID": tick(0, 38.5, 394.3),
                "Driving Licence": tick(0, 38.5, 409.4),
                "NREGA Job Card": tick(0, 38.5, 424.7),
                "NPR Letter": tick(0, 38.5, 439.8),
                "Aadhaar": tick(0, 38.5, 455.0),
            },
            "poi_number": doc_numbers([379, 395, 409, 424, 438]),
            "poi_expiry": {
                "Passport": date_slot(0, 377, pexp_b, cells(pexp_xs)),
                "Driving Licence": date_slot(0, 408, dlexp_b, cells(dlexp_xs)),
            },
            "address": address_block(510, 522, 536, 548),
            "same_address_tick": tick(0, 32.3, 585.5),
            "cur_poa_tick": {
                "Passport": tick(0, 38.5, 610.4),
                "Voter ID": tick(0, 38.5, 625.7),
                "Driving Licence": tick(0, 38.5, 640.8),
                "NREGA Job Card": tick(0, 38.5, 656.0),
                "NPR Letter": tick(0, 38.5, 671.2),
                "Aadhaar": tick(0, 38.5, 686.4),
                "deemed": tick(0, 38.5, 734.4),
            },
            "cur_poa_number": doc_numbers([611, 626, 640, 655, 670]),
            "deemed_code": slot(0, 733, r1(733)[1], cells(r1(733)[0])),
            "cur_address": address_block(760, 772, 786, 798),
            "mobile": {
                "country": slot(1, 64, mob_b, mobile_cells[0:3]),
                "number": slot(1, 64, mob_b, mobile_cells[4:14]),
            },
            "email": slot(1, 80, email_b, cells(email_xs)),
            "declaration_date": decl_date,
            "place": slot(1, 275, date_b, cells(date_xs, 238.3, 357.4)),
        },
        # Two-letter codes exactly as printed on page 4 of the form (Motor
        # Vehicles Act list): note OR for Odisha, TS for Telangana, UA for
        # Uttarakhand.
        "state_codes": {
            "Andhra Pradesh": "AP", "Assam": "AS", "Bihar": "BR", "Chhattisgarh": "CG",
            "Delhi": "DL", "Goa": "GA", "Gujarat": "GJ", "Haryana": "HR",
            "Himachal Pradesh": "HP", "Jharkhand": "JH", "Karnataka": "KA", "Kerala": "KL",
            "Madhya Pradesh": "MP", "Maharashtra": "MH", "Odisha": "OR", "Punjab": "PB",
            "Rajasthan": "RJ", "Tamil Nadu": "TN", "Telangana": "TS", "Uttar Pradesh": "UP",
            "Uttarakhand": "UA", "West Bengal": "WB",
        },
        # Section 3, IV: codes for a deemed proof of address (page 3 of the form).
        "deemed_codes": {
            "Utility Bill": "01", "Property Tax Receipt": "02",
            "Pension Order": "03", "Employer Letter": "04",
        },
    }
    OUT.write_text(
        "# Generated by tools/build_official_layout.py -- do not edit by hand.\n"
        + yaml.safe_dump(layout, sort_keys=False, width=200),
        encoding="utf-8",
    )
    n = sum(1 for _ in yaml.safe_load(OUT.read_text(encoding="utf-8"))["fields"])
    print(f"wrote {OUT} ({n} layout entries)")


if __name__ == "__main__":
    main()
