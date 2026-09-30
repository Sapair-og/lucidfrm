"""PIN-code region data, for the postal-code / state cross-field check.

India's postal codes encode geography in the leading digit: the first digit
selects one of nine postal regions, each covering a fixed set of states. A PIN
whose first digit does not match the stated state is therefore detectably wrong
without any lookup service, network call, or exhaustive PIN database.

The leading-digit check is coarse: region 4 covers Maharashtra, Madhya Pradesh,
Chhattisgarh and Goa, so 466114 (Sehore, MP) passed as a Goa PIN (ISSUES.md
LF-003). Where the PIN is in the India Post directory
(`data/pin_directory.json`, built by `tools/build_pin_directory.py`) the state
is checked exactly. A PIN missing from the directory -- new, or outside the
form's state list -- falls back to the region check, so an out-of-date
directory can never reject a real PIN. That matters because the
false-positive rate is a reported measure (METHODOLOGY M0.7).

City names are checked only one way round: a city the directory knows, in no
state matching the PIN or the stated state, is a contradiction. An unknown city
(a village, a locality, a new name) is never rejected.

Reference: India Post PIN allocation. Union territories and the north-eastern
states are folded into their region.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DIRECTORY = Path(__file__).parent / "data" / "pin_directory.json"

# Renamed cities: the directory predates some renames. Both names are the city.
CITY_ALIASES = {
    "bengaluru": "bangalore",
    "mumbai": "bombay",
    "kolkata": "calcutta",
    "chennai": "madras",
    "gurugram": "gurgaon",
    "prayagraj": "allahabad",
    "mysuru": "mysore",
    "belagavi": "belgaum",
    "kalaburagi": "gulbarga",
    "thiruvananthapuram": "trivandrum",
    "puducherry": "pondicherry",
    "vadodara": "baroda",
    "kanpur": "cawnpore",
    "varanasi": "benares",
}

# first PIN digit -> states served by that postal region
PIN_REGIONS: dict[str, frozenset[str]] = {
    "1": frozenset({"Delhi", "Haryana", "Punjab", "Himachal Pradesh"}),
    "2": frozenset({"Uttar Pradesh", "Uttarakhand"}),
    "3": frozenset({"Rajasthan", "Gujarat"}),
    "4": frozenset({"Chhattisgarh", "Madhya Pradesh", "Maharashtra", "Goa"}),
    "5": frozenset({"Andhra Pradesh", "Telangana", "Karnataka"}),
    "6": frozenset({"Tamil Nadu", "Kerala"}),
    "7": frozenset({"West Bengal", "Odisha", "Assam"}),
    "8": frozenset({"Bihar", "Jharkhand"}),
}

# state -> the leading digits that are valid for it
STATE_TO_LEADING: dict[str, frozenset[str]] = {}
for _digit, _states in PIN_REGIONS.items():
    for _state in _states:
        STATE_TO_LEADING.setdefault(_state, frozenset())
        STATE_TO_LEADING[_state] = STATE_TO_LEADING[_state] | {_digit}
del _digit, _states, _state


@lru_cache(maxsize=1)
def _directory() -> dict:
    if not DIRECTORY.exists():
        return {"states": [], "pins": {}, "places": {}}
    return json.loads(DIRECTORY.read_text(encoding="utf-8"))


def pin_place(pin: str) -> tuple[str, str] | None:
    """(state, district) for a PIN in the directory, else None."""
    d = _directory()
    entry = d["pins"].get(pin)
    if entry is None:
        return None
    return d["states"][entry[0]], entry[1]


def city_states(city: str) -> frozenset[str] | None:
    """States where the directory knows a district or town of this name, or None."""
    d = _directory()
    key = " ".join((city or "").casefold().split())
    found: set[str] = set()
    for name in {key, CITY_ALIASES.get(key, key)}:
        for i in d["places"].get(name, ()):
            found.add(d["states"][i])
    return frozenset(found) or None


def propose(field_id: str, committed) -> str | None:
    """A value to offer for a field, derived from confirmed ones (LF-003).

    Only the state, from a confirmed PIN in the directory. It is an offer: it
    is read back and saved only on an explicit yes.
    """
    if field_id == "state" and committed.get("pin"):
        place = pin_place(committed["pin"])
        return place[0] if place else None
    return None


def pin_matches_state(pin: str, state: str) -> bool | None:
    """True / False, or None when we hold no data for that state.

    None is not a pass. The caller decides what to do with an unknown state --
    the gate declines to run the check rather than inventing a verdict, so an
    unlisted state can never be silently waved through as "matching".
    """
    if not pin or pin[0] not in "0123456789":
        return False
    place = pin_place(pin)
    if place is not None:
        return place[0] == state
    allowed = STATE_TO_LEADING.get(state)
    if allowed is None:
        return None
    return pin[0] in allowed
