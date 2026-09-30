"""Build lucidform/gate/data/pin_directory.json from the India Post pincode CSV.

Source: India Post "All India Pincode Directory" (data.gov.in), mirrored at
https://github.com/saravanakumargn/All-India-Pincode-Directory
(all-india-pincode-html-csv.csv). Run:

    python tools/build_pin_directory.py path/to/all-india-pincode-html-csv.csv

Output (compact, committed):
    states     list of state names, spelled as the form's `state` enum
    pins       "PIN" -> [state index, district]
    places     place name (casefolded) -> sorted state indices where a district or
               a head/sub post office (a town, not a village branch) has that name
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "lucidform" / "gate" / "data" / "pin_directory.json"
OVERLAY = ROOT / "lucidform" / "schema" / "ckyc_form.yaml"

# Directory spellings -> the form's enum spellings.
STATE_FIX = {
    "andaman & nicobar islands": "Andaman and Nicobar Islands",
    "andaman and nicobar islands": "Andaman and Nicobar Islands",
    "dadra & nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "dadra and nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "daman & diu": "Dadra and Nagar Haveli and Daman and Diu",
    "daman and diu": "Dadra and Nagar Haveli and Daman and Diu",
    "jammu & kashmir": "Jammu and Kashmir",
    "jammu and kashmir": "Jammu and Kashmir",
    "pondicherry": "Puducherry",
    "orissa": "Odisha",
    "chattisgarh": "Chhattisgarh",
    "uttaranchal": "Uttarakhand",
    "delhi": "Delhi",
    "new delhi": "Delhi",
}
OFFICE_SUFFIX = re.compile(r"\s+(h\.?o|s\.?o|b\.?o|g\.?p\.?o|mdg|ndg)\.?(\s*\(.*\))?$", re.I)


def _title(s: str) -> str:
    return " ".join(w.capitalize() for w in s.strip().split())


def main(src: Path) -> None:
    enum_states = next(
        f["enum_values"] for f in yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))["fields"]
        if f["id"] == "state"
    )
    by_fold = {s.casefold(): s for s in enum_states}

    def state_of(raw: str) -> str | None:
        key = " ".join(raw.strip().casefold().split())
        return by_fold.get(key) or STATE_FIX.get(key)

    states: list[str] = []
    idx: dict[str, int] = {}
    pins: dict[str, tuple[int, str]] = {}
    places: dict[str, set[int]] = defaultdict(set)
    unknown: set[str] = set()

    with src.open(encoding="utf-8", errors="replace", newline="") as fh:
        for row in csv.DictReader(fh):
            row = {k.strip().casefold(): (v or "").strip() for k, v in row.items() if k}
            pin = row.get("pincode", "")
            state = state_of(row.get("statename", ""))
            if not re.fullmatch(r"[1-9][0-9]{5}", pin):
                continue
            if state is None:
                unknown.add(row.get("statename", ""))
                continue
            si = idx.setdefault(state, len(states))
            if si == len(states):
                states.append(state)
            district = _title(row.get("districtname", "") or row.get("district", ""))
            pins.setdefault(pin, (si, district))
            if district:
                places[district.casefold()].add(si)
            office = row.get("officename", "")
            otype = row.get("officetype", "").upper()
            if otype in ("H.O", "S.O", "HO", "SO") or re.search(r"\b(h\.?o|s\.?o)\b", office, re.I):
                name = OFFICE_SUFFIX.sub("", office).strip()
                if name:
                    places[name.casefold()].add(si)

    missing = set(enum_states) - set(states)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(
            {
                "source": "India Post All India Pincode Directory (data.gov.in), via "
                "github.com/saravanakumargn/All-India-Pincode-Directory",
                "states": states,
                "pins": {p: [s, d] for p, (s, d) in sorted(pins.items())},
                "places": {k: sorted(v) for k, v in sorted(places.items())},
            },
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    print(f"{len(pins)} PINs, {len(places)} places, {len(states)} states -> {OUT}")
    if unknown:
        print("unmapped state names (rows skipped):", sorted(unknown))
    if missing:
        print("enum states with no PINs:", sorted(missing))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
