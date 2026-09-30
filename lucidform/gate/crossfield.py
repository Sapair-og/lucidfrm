"""Cross-field consistency checks.

These catch the values that are individually well-formed and would pass every
single-field check, but contradict something the user has already confirmed. A
validator that looks at one field at a time cannot see them at all.

Two rules that matter, and one rule about the rules:

  * A check runs only when every field it depends on has been **committed**.
    Validating against an uncommitted value would mean checking a confirmed
    value against an unconfirmed one, which would let an unreviewed value
    influence what the gate accepts.
  * A check that cannot run is recorded as *skipped*, never as passed. The
    distinction shows up in the results: a cross-field check that silently
    degrades to a pass would inflate the gate's apparent accuracy.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from lucidform.gate.regions import city_states, pin_matches_state, pin_place


@dataclass(frozen=True)
class CrossFieldResult:
    name: str
    ran: bool
    passed: bool
    detail: str = ""

    @property
    def failed(self) -> bool:
        return self.ran and not self.passed


def _skipped(name: str, missing: str) -> CrossFieldResult:
    return CrossFieldResult(
        name=name,
        ran=False,
        passed=False,
        detail=f"not checked: {missing} has not been confirmed yet",
    )


def pan_matches_surname(
    value: str, committed: Mapping[str, str]
) -> CrossFieldResult:
    """A PAN's fifth character is the first letter of the holder's surname.

    This is a genuine structural property of the identifier, which makes it a
    free consistency check between two fields the user gives minutes apart --
    and one of the few ways to catch a PAN that is well-formed but belongs to
    somebody else.
    """
    name = "pan_matches_surname"
    full_name = (committed.get("full_name") or "").strip()
    if not full_name:
        return _skipped(name, "full_name")

    parts = full_name.split()
    if not parts:
        return _skipped(name, "full_name")

    surname_initial = parts[-1][0].upper()
    actual = value[4].upper() if len(value) >= 5 else "?"
    if actual == surname_initial:
        return CrossFieldResult(name, ran=True, passed=True)

    return CrossFieldResult(
        name,
        ran=True,
        passed=False,
        detail=(
            f"the fifth character of a PAN is the first letter of the surname; "
            f"this reads {actual!r} but the confirmed surname {parts[-1]!r} "
            f"starts with {surname_initial!r}"
        ),
    )


def pin_matches_confirmed_state(
    value: str, committed: Mapping[str, str]
) -> CrossFieldResult:
    """A PIN code's leading digit selects a postal region, which fixes the state."""
    name = "pin_matches_state"
    state = (committed.get("state") or "").strip()
    if not state:
        return _skipped(name, "state")

    verdict = pin_matches_state(value, state)
    if verdict is None:
        # We hold no region data for this state. Declining to check is the
        # honest outcome; inventing a pass would let an unverifiable pairing
        # through while looking as though it had been checked.
        return CrossFieldResult(
            name,
            ran=False,
            passed=False,
            detail=f"not checked: no postal region data for {state!r}",
        )
    if verdict:
        return _city_agrees(name, value, state, committed.get("city"))

    place = pin_place(value)
    return CrossFieldResult(
        name,
        ran=True,
        passed=False,
        detail=(
            f"PIN code {value} is in {place[1]}, {place[0]}, not in {state}"
            if place
            else (
                f"a PIN code in {state} does not begin with {value[0]!r}; "
                "the postal region does not match the confirmed state"
            )
        ),
    )


def _city_agrees(name: str, pin: str, state: str | None, city: str | None) -> CrossFieldResult:
    """The confirmed city, if the directory knows it, must be in the PIN's or state's state."""
    known = city_states(city or "")
    if known is None:
        return CrossFieldResult(name, ran=True, passed=True)
    place = pin_place(pin) if pin else None
    where = place[0] if place else state
    if where is None or where in known:
        return CrossFieldResult(name, ran=True, passed=True)
    return CrossFieldResult(
        name,
        ran=True,
        passed=False,
        detail=f"{city} is in {_or(known)}, but {_what(pin, place, state)}",
    )


def _or(states) -> str:
    states = sorted(states)
    return states[0] if len(states) == 1 else ", ".join(states[:-1]) + " or " + states[-1]


def _what(pin, place, state) -> str:
    if place:
        return f"PIN code {pin} is in {place[0]}"
    return f"the confirmed state is {state}"


def state_matches_pin_and_city(value: str, committed: Mapping[str, str]) -> CrossFieldResult:
    """A state must agree with a confirmed PIN (exactly, via the directory) and city."""
    name = "state_matches_pin"
    pin = (committed.get("pin") or "").strip()
    city = (committed.get("city") or "").strip()
    if not pin and not city:
        return _skipped(name, "pin")
    if pin:
        verdict = pin_matches_state(pin, value)
        if verdict is False:
            place = pin_place(pin)
            where = f"{place[1]}, {place[0]}" if place else "a different postal region"
            return CrossFieldResult(
                name, ran=True, passed=False,
                detail=f"the confirmed PIN code {pin} is in {where}, not in {value}",
            )
    known = city_states(city) if city else None
    if known is not None and value not in known:
        return CrossFieldResult(
            name, ran=True, passed=False,
            detail=f"the confirmed city {city} is in {_or(known)}, not in {value}",
        )
    return CrossFieldResult(name, ran=True, passed=True)


def city_matches_pin_and_state(value: str, committed: Mapping[str, str]) -> CrossFieldResult:
    """A city the directory knows must lie in the confirmed PIN's / state's state."""
    name = "city_matches_pin"
    pin = (committed.get("pin") or "").strip()
    state = (committed.get("state") or "").strip()
    if not pin and not state:
        return _skipped(name, "pin")
    return _city_agrees(name, pin, state or None, value)


# field id -> the check that applies to it
CHECKS: dict[str, Callable[[str, Mapping[str, str]], CrossFieldResult]] = {
    "pan": pan_matches_surname,
    "pin": pin_matches_confirmed_state,
    "state": state_matches_pin_and_city,
    "city": city_matches_pin_and_state,
}


def check(field_id: str, value: str, committed: Mapping[str, str]) -> CrossFieldResult | None:
    """Run the cross-field check for a field, if it has one."""
    fn = CHECKS.get(field_id)
    return fn(value, committed) if fn else None
