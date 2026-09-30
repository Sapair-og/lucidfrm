"""PIN-code region data, for the postal-code / state cross-field check.

India's postal codes encode geography in the leading digit: the first digit
selects one of nine postal regions, each covering a fixed set of states. A PIN
whose first digit does not match the stated state is therefore detectably wrong
without any lookup service, network call, or exhaustive PIN database.

This is a deliberately coarse check. It catches the realistic error -- a
transcription slip or a PIN remembered from a previous address -- while never
rejecting a correct pairing, which matters because the false-positive rate is a
reported measure (METHODOLOGY M0.7). A finer check would need a full PIN
directory and would start rejecting valid edge cases.

Reference: India Post PIN allocation. Union territories and the north-eastern
states are folded into their region.
"""

from __future__ import annotations

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


def pin_matches_state(pin: str, state: str) -> bool | None:
    """True / False, or None when we hold no data for that state.

    None is not a pass. The caller decides what to do with an unknown state --
    the gate declines to run the check rather than inventing a verdict, so an
    unlisted state can never be silently waved through as "matching".
    """
    if not pin or not pin[0].isdigit():
        return False
    allowed = STATE_TO_LEADING.get(state)
    if allowed is None:
        return None
    return pin[0] in allowed
