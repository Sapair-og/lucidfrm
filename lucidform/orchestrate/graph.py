"""The conversation as a LangGraph state machine.

Same stages, same decisions, same events as the loop it replaced -- the golden
parity test (`tests/test_graph.py`) holds it to that byte for byte. What the
graph adds is that the control flow is data: every transition is a declared
edge, so "commit is reachable only through confirm" is something a test can
read off the graph instead of something a reader has to trace through a loop.

    greet -> next_field -> budget -> ask -> listen -> extract -+-> gate -> readback -> listen_confirm -> confirm -> commit
                              ^                               +-> explain        (question)                   |
                              |                               +-> decline        (decline)                    |
                              |                               +-> not_understood                              |
                              +------------- any rejection, denial, or retry --------------------------------+
    finish -> next_field ... -> close

The safety argument does not move into the graph. `FormState` is held by the
runner, never placed in graph state, and `FormState.commit` re-verifies the
receipt whatever edge led to it: a mis-wired graph would produce a blocked,
logged write, not a silent one. The graph is an orchestrator, not an authority.

Checkpoint-resume is deliberately not enabled. Resuming would mean rebuilding
FormState from saved values, and the only legitimate way values enter FormState
is `commit()` with a fresh receipt -- restoring them from a checkpoint would be
exactly the unconfirmed write the project exists to prevent (METHODOLOGY M7).
"""

from __future__ import annotations

import re
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from lucidform.channels.base import Kind, Purpose
from lucidform.eval.events import Event
from lucidform.gate import regions
from lucidform.models import Candidate, Status
from lucidform.orchestrate import readback
from lucidform.orchestrate.confirm import confirm, parse_affirmation

# A full form takes a few hundred steps; LangGraph's default limit of 25 is a
# guard against runaway graphs, which this one cannot be -- every cycle spends
# an attempt, a question, or a field.
RECURSION_LIMIT = 100_000


class TurnState(TypedDict, total=False):
    index: int
    current: Any  # FieldResult for the field in progress
    said: str | None
    extraction: Any
    proposed: Any  # candidate offered to the gate: extracted, or a decline alternative
    candidate: Any
    report: Any
    receipt: Any
    route: str
    results: list
    queue: list  # schema indices still to visit
    correcting: bool  # the current field is being changed at the user's request
    revisited: list  # field ids already revisited at the end
    reviews: int
    approved: bool
    gone: bool  # the input channel ended (hang-up / EOF): nobody to revisit or review with
    suggested: bool  # a suggestion was already offered for this utterance


# Conditional edges: node -> {route label: destination}.
ROUTES: dict[str, dict[str, str]] = {
    "next_field": {"field": "budget", "done": "wrap_up"},
    "wrap_up": {"again": "next_field", "review": "review", "end": "close"},
    "listen_review": {
        "approved": "close",
        "change": "next_field",
        "unclear": "wrap_up",
        "gone": "close",
    },
    "budget": {"ask": "ask", "propose": "propose", "finish": "finish"},
    "listen": {"heard": "extract", "gone": "finish"},
    "extract": {
        "question": "explain",
        "decline": "decline",
        "unclear": "not_understood",
        "value": "gate",
    },
    "explain": {"retry": "budget"},
    "decline": {"retry": "budget", "finish": "finish", "alternative": "gate"},
    "gate": {"pass": "readback", "retry": "budget", "suggest": "gate"},
    "listen_confirm": {"heard": "confirm", "gone": "finish"},
    "confirm": {"affirmed": "commit", "retry": "budget"},
}
# Unconditional edges.
EDGES: list[tuple[str, str]] = [
    ("greet", "next_field"),
    ("ask", "listen"),
    ("not_understood", "budget"),
    ("readback", "listen_confirm"),
    ("commit", "finish"),
    ("finish", "next_field"),
    ("review", "listen_review"),
    ("propose", "gate"),
]
NODES = (
    "greet", "next_field", "budget", "propose", "ask", "listen", "extract", "explain",
    "decline", "not_understood", "gate", "readback", "listen_confirm",
    "confirm", "commit", "finish", "wrap_up", "review", "listen_review", "close",
)


def _build(runner) -> StateGraph:
    g = StateGraph(TurnState)
    for name in NODES:
        g.add_node(name, getattr(runner, name))
    g.add_edge(START, "greet")
    for src, dst in EDGES:
        g.add_edge(src, dst)
    for src, paths in ROUTES.items():
        g.add_conditional_edges(src, _route, paths)
    g.add_edge("close", END)
    return g


def _route(state: TurnState) -> str:
    return state["route"]


class SessionGraph:
    """Runs one `Session` through the graph. Holds the stateful collaborators."""

    def __init__(self, session) -> None:
        self.s = session
        self._compiled = _build(self).compile()

    def run(self):
        from lucidform.orchestrate.session import SessionResult

        final = self._compiled.invoke(
            {"index": -1, "results": []}, config={"recursion_limit": RECURSION_LIMIT}
        )
        values = self.s.state.values
        result = SessionResult(
            session_id=self.s.log.session_id,
            # A field that stopped applying (its condition changed at the
            # review) is not part of the outcome.
            fields=[r for r in final["results"] if self.s.schema.by_id(r.field_id).applies(values)],
            approved=bool(final.get("approved")),
        )
        self.s._close(result)
        return result

    # -- nodes -------------------------------------------------------------

    def greet(self, state: TurnState) -> dict:
        self.s.output.say(self.s.strings.get("greeting"), kind=Kind.PROGRESS)
        return {
            "queue": list(range(len(self.s.schema))),
            "correcting": False,
            "revisited": [],
            "reviews": 0,
            "approved": False,
            "gone": False,
        }

    def next_field(self, state: TurnState) -> dict:
        from lucidform.orchestrate.session import FieldResult

        fields = list(self.s.schema)
        queue = list(state["queue"])
        while queue:
            index = queue.pop(0)
            # A field the user asked to change is asked again even though it
            # already holds a value; otherwise resolved fields are skipped.
            if state.get("correcting") or (
                not self.s.state.is_resolved(fields[index].id)
                and fields[index].applies(self.s.state.values)
            ):
                return {
                    "index": index,
                    "queue": queue,
                    "current": FieldResult(field_id=fields[index].id),
                    "route": "field",
                }
        return {"queue": [], "correcting": False, "route": "done"}

    def budget(self, state: TurnState) -> dict:
        outcome = state["current"]
        if outcome.attempts < self.s.max_attempts and not outcome.resolved:
            if outcome.attempts == 0 and not outcome.proposed and self._proposal(state):
                return {"route": "propose"}
            return {"route": "ask"}
        return {"route": "finish"}

    def propose(self, state: TurnState) -> dict:
        # LF-003: offer the state that a confirmed PIN code fixes. The offer
        # takes the normal gate -> read-back -> explicit yes path; a "no"
        # falls through to the ordinary question.
        field, outcome = self._field(state), state["current"]
        outcome.proposed = True
        value, params = self._proposal(state)
        # A proposal is a turn of its own: the user is asked something.
        self.s.log.emit(
            Event.FIELD_ASKED,
            field_id=field.id,
            turn_idx=outcome.attempts,
            payload={"attempt": outcome.attempts, "proposal": value},
        )
        key = "proposal" if "pin" in params else f"proposal_{field.id}"
        self.s.output.say(self.s.strings.say(key, **params), kind=Kind.EXPLANATION)
        proposed = Candidate(
            field_id=field.id, value=value, raw_utterance="", confidence=1.0
        )
        return {"proposed": proposed}

    def _proposal(self, state: TurnState) -> tuple[str, dict] | None:
        field = self._field(state)
        offer = regions.propose(field.id, self.s.state.values)
        if offer is None or (field.enum_values and offer[0] not in field.enum_values):
            return None
        return offer

    def ask(self, state: TurnState) -> dict:
        field, outcome = self._field(state), state["current"]
        self.s.log.emit(
            Event.FIELD_ASKED,
            field_id=field.id,
            turn_idx=outcome.attempts,
            payload={"attempt": outcome.attempts},
        )
        self.s.output.say(field.ask(self.s.lang), kind=Kind.PROMPT)
        return {}

    def listen(self, state: TurnState) -> dict:
        field, outcome = self._field(state), state["current"]
        said = self.s.input.listen(field.id, Purpose.VALUE)
        if said is None:
            outcome.abandoned = True
            return {"said": None, "gone": True, "route": "gone"}
        self.s.log.emit(
            Event.USER_UTTERANCE,
            field_id=field.id,
            turn_idx=outcome.attempts,
            payload={"text": said, "purpose": Purpose.VALUE.value},
        )
        return {"said": said, "route": "heard"}

    def extract(self, state: TurnState) -> dict:
        field = self._field(state)
        extraction = self.s.extractor.extract(field.id, state["said"])
        if extraction.asked_a_question:
            route = "question"
        elif extraction.declined:
            route = "decline"
        elif not extraction.has_candidate:
            route = "unclear"
        else:
            route = "value"
        return {
            "extraction": extraction,
            "proposed": extraction.candidate,
            "suggested": False,
            "route": route,
        }

    def explain(self, state: TurnState) -> dict:
        outcome = state["current"]
        if outcome.questions >= self.s.max_questions:
            # Explaining again is not helping. Treat it as an attempt so the
            # session can move on rather than looping.
            outcome.attempts += 1
            return {"route": "retry"}
        outcome.questions += 1
        self.s._explain(self._field(state), state["said"])
        return {"route": "retry"}

    def decline(self, state: TurnState) -> dict:
        field, outcome = self._field(state), state["current"]
        if field.decline_value:
            # LF-008: offer the declared alternative (PAN -> Form 60). It goes
            # through the gate, the read-back and the explicit yes like any
            # value; the user can still say no.
            offer = field.decline_offer.get(self.s.lang) or field.decline_offer.get("en")
            if offer:
                self.s.output.say(offer, kind=Kind.EXPLANATION)
            proposed = Candidate(
                field_id=field.id,
                value=field.decline_value,
                raw_utterance=state["said"],
                confidence=1.0,
            )
            return {"proposed": proposed, "route": "alternative"}
        if field.required:
            self.s.output.say(self.s.strings.get("required"), kind=Kind.PROBLEM)
            outcome.attempts += 1
            return {"route": "retry"}
        self.s.state.decline(field.id, said=state["said"])
        self.s.output.say(self.s.strings.get("declined"), kind=Kind.PROGRESS)
        outcome.declined = True
        return {"route": "finish"}

    def not_understood(self, state: TurnState) -> dict:
        self.s.output.say(self.s.strings.get("not_understood"), kind=Kind.PROBLEM)
        state["current"].attempts += 1
        return {}

    def gate(self, state: TurnState) -> dict:
        field, outcome = self._field(state), state["current"]
        candidate = state["proposed"]
        report = self.s.gate.check(candidate, self.s.state.values)
        self.s.log.emit(
            Event.VALIDATION, field_id=field.id, turn_idx=outcome.attempts, payload=report
        )
        if report.status is not Status.PASS:
            outcome.rejections.append(report.reason.value)
            # The gate's own wording reaches the user. It is written to be said
            # aloud, and re-phrasing it here would put a second, untested
            # explanation in front of the person who needs it most.
            self.s.output.say(
                self.s.strings.say("problem", detail=report.detail), kind=Kind.PROBLEM
            )
            if report.suggestion and not state.get("suggested"):
                # LF-005/LF-009: offer what they may have meant. It is a new
                # candidate: through the gate again, read back, and saved only
                # on an explicit yes. One suggestion per utterance, so a
                # suggestion can never chain into another.
                self.s.output.say(
                    self.s.strings.say("suggestion", value=report.suggestion),
                    kind=Kind.EXPLANATION,
                )
                offered = Candidate(
                    field_id=field.id,
                    value=report.suggestion,
                    raw_utterance=candidate.raw_utterance,
                    confidence=1.0,
                )
                return {"proposed": offered, "suggested": True, "report": report, "route": "suggest"}
            outcome.attempts += 1
            return {"candidate": None, "report": report, "route": "retry"}
        return {"candidate": candidate, "report": report, "route": "pass"}

    def readback(self, state: TurnState) -> dict:
        field, outcome = self._field(state), state["current"]
        value = state["report"].normalized_value
        text = readback.render(value, field, self.s.strings.get("readback"), self.s.lang)
        self.s.log.emit(
            Event.READBACK,
            field_id=field.id,
            turn_idx=outcome.attempts,
            payload={"value": value, "spoken": text},
        )
        self.s.output.read_back(field.id, value, text)
        return {}

    def listen_confirm(self, state: TurnState) -> dict:
        field, outcome = self._field(state), state["current"]
        said = self.s.input.listen(field.id, Purpose.CONFIRMATION)
        if said is None:
            # The user is gone. Ending the field here, rather than re-asking,
            # is the one deliberate behaviour change from the loop this replaced.
            outcome.abandoned = True
            return {"said": None, "gone": True, "route": "gone"}
        # Logged with the same event type as any other thing the user said, so
        # the metrics can count turns and measure latency without special-casing
        # the confirmation reply. `purpose` is what distinguishes them.
        self.s.log.emit(
            Event.USER_UTTERANCE,
            field_id=field.id,
            turn_idx=outcome.attempts,
            payload={"text": said, "purpose": Purpose.CONFIRMATION.value},
        )
        return {"said": said, "route": "heard"}

    def confirm(self, state: TurnState) -> dict:
        field, outcome = self._field(state), state["current"]
        affirmation, receipt = confirm(state["candidate"], state["report"], state["said"])
        self.s.log.emit(
            Event.CONFIRMATION, field_id=field.id, turn_idx=outcome.attempts, payload=affirmation
        )
        if receipt is None:
            outcome.corrections += 1
            self.s.log.emit(
                Event.CORRECTION,
                field_id=field.id,
                turn_idx=outcome.attempts,
                payload={"value_rejected": state["report"].normalized_value, "said": state["said"]},
            )
            self.s.output.say(self.s.strings.get("denied"), kind=Kind.PROBLEM)
            outcome.attempts += 1
            return {"receipt": None, "route": "retry"}
        return {"receipt": receipt, "route": "affirmed"}

    def commit(self, state: TurnState) -> dict:
        # The only write in the whole system. FormState re-verifies the receipt
        # against the candidate here, so this node cannot be tricked by state.
        self.s.state.commit(state["candidate"], state["receipt"])
        self.s.output.say(self.s.strings.get("confirmed"), kind=Kind.PROGRESS)
        state["current"].committed = True
        return {"receipt": None}

    def finish(self, state: TurnState) -> dict:
        field, outcome = self._field(state), state["current"]
        if not outcome.resolved and not outcome.abandoned:
            outcome.abandoned = True
            self.s.output.say(
                self.s.strings.say("out_of_attempts", label=field.name(self.s.lang)),
                kind=Kind.PROGRESS,
            )
        # A revisited or corrected field replaces its earlier result, so the
        # session reports each field once, as it finally stands.
        earlier = [r for r in state["results"] if r.field_id != outcome.field_id]
        for prior in state["results"]:
            if prior.field_id == outcome.field_id:
                # Counters describe the whole effort spent on the field.
                outcome.attempts += prior.attempts
                outcome.questions += prior.questions
                outcome.rejections[:0] = prior.rejections
                outcome.corrections += prior.corrections
        if not outcome.resolved and self.s.state.is_committed(field.id):
            # The user asked to change a value and then gave no new one: the
            # earlier confirmed value stands.
            outcome.committed, outcome.abandoned = True, False
        return {"results": [*earlier, outcome]}

    # -- end of form: revisit, then review (ISSUES.md LF-006) --------------

    def wrap_up(self, state: TurnState) -> dict:
        if state.get("gone"):
            return {"route": "end"}
        fields = list(self.s.schema)
        values = self.s.state.values
        seen = state.get("revisited") or []
        # Fields still missing that apply. A field that newly applies after a
        # change at the review (a passport number, once the proof became a
        # passport) is visited too; each field is revisited at most once.
        missing = [
            i for i, f in enumerate(fields)
            if f.applies(values) and not self.s.state.is_resolved(f.id) and f.id not in seen
        ]
        if missing:
            labels = ", ".join(fields[i].name(self.s.lang) for i in missing)
            self.s.output.say(self.s.strings.say("revisit", fields=labels), kind=Kind.PROGRESS)
            return {
                "queue": missing,
                "revisited": [*seen, *(fields[i].id for i in missing)],
                "route": "again",
            }
        if self.s.state.values and state.get("reviews", 0) < self.s.max_reviews:
            return {"route": "review"}
        return {"route": "end"}

    def review(self, state: TurnState) -> dict:
        lang = self.s.lang
        lines = [
            f"{f.name(lang)}: {readback.render_value(self.s.state.get(f.id), f, lang)}"
            for f in self.s.schema
            if self.s.state.is_committed(f.id) and f.applies(self.s.state.values)
        ]
        self.s.log.emit(Event.READBACK, payload={"summary": lines})
        self.s.output.say(self.s.strings.get("review_intro"), kind=Kind.READBACK)
        for line in lines:
            self.s.output.say(line, kind=Kind.READBACK)
        missing = [
            f.name(lang)
            for f in self.s.schema
            if f.applies(self.s.state.values) and not self.s.state.is_resolved(f.id)
        ]
        if missing:
            self.s.output.say(
                self.s.strings.say("incomplete", count=len(missing), fields=", ".join(missing)),
                kind=Kind.PROBLEM,
            )
        self.s.output.say(self.s.strings.get("review_prompt"), kind=Kind.PROMPT)
        return {}

    def listen_review(self, state: TurnState) -> dict:
        said = self.s.input.listen("review", Purpose.REVIEW)
        reviews = state.get("reviews", 0) + 1
        if said is None:
            return {"route": "gone", "reviews": reviews}
        self.s.log.emit(
            Event.USER_UTTERANCE, payload={"text": said, "purpose": Purpose.REVIEW.value}
        )
        if parse_affirmation(said).explicit:
            self.s.output.say(self.s.strings.get("review_done"), kind=Kind.PROGRESS)
            return {"route": "approved", "approved": True, "reviews": reviews}
        index = field_named(said, list(self.s.schema))
        if index is None:
            self.s.output.say(self.s.strings.get("review_unclear"), kind=Kind.PROBLEM)
            return {"route": "unclear", "reviews": reviews}
        return {"route": "change", "queue": [index], "correcting": True, "reviews": reviews}

    def close(self, state: TurnState) -> dict:
        return {}

    # -- helpers -----------------------------------------------------------

    def _field(self, state: TurnState):
        return list(self.s.schema)[state["index"]]


_NON_WORD = re.compile(r"[^a-z0-9' ]+")


def field_named(utterance: str, fields) -> int | None:
    """Index of the field the user named, by its declared aliases or label.

    Whole-phrase matches only; the longest wins, so "father's name" beats
    "name". None when nothing matches: the user is asked again rather than
    the system guessing which field they meant.
    """
    text = " " + " ".join(_NON_WORD.sub(" ", (utterance or "").casefold()).split()) + " "
    best: tuple[int, int] | None = None
    for i, f in enumerate(fields):
        names = {*f.aliases, f.label, f.id.replace("_", " "), *f.labels.values()}
        for name in names:
            phrase = " ".join(_NON_WORD.sub(" ", name.casefold()).split())
            if phrase and f" {phrase} " in text and (best is None or len(phrase) > best[0]):
                best = (len(phrase), i)
    return best[1] if best else None


# -- structure, for tests and the paper figure -------------------------------------


class _Stub:
    def __getattr__(self, name):
        return lambda state: {}


def _structure():
    return _build(_Stub()).compile().get_graph()


def node_names() -> list[str]:
    return [n for n in _structure().nodes if not n.startswith("__")]


def edges() -> list[tuple[str, str]]:
    return [(e.source, e.target) for e in _structure().edges]


def mermaid() -> str:
    return _structure().draw_mermaid()
