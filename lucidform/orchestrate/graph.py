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

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from lucidform.channels.base import Kind, Purpose
from lucidform.eval.events import Event
from lucidform.models import Status
from lucidform.orchestrate import readback
from lucidform.orchestrate.confirm import confirm

# A full form takes a few hundred steps; LangGraph's default limit of 25 is a
# guard against runaway graphs, which this one cannot be -- every cycle spends
# an attempt, a question, or a field.
RECURSION_LIMIT = 100_000


class TurnState(TypedDict, total=False):
    index: int
    current: Any  # FieldResult for the field in progress
    said: str | None
    extraction: Any
    candidate: Any
    report: Any
    receipt: Any
    route: str
    results: list


# Conditional edges: node -> {route label: destination}.
ROUTES: dict[str, dict[str, str]] = {
    "next_field": {"field": "budget", "done": "close"},
    "budget": {"ask": "ask", "finish": "finish"},
    "listen": {"heard": "extract", "gone": "finish"},
    "extract": {
        "question": "explain",
        "decline": "decline",
        "unclear": "not_understood",
        "value": "gate",
    },
    "explain": {"retry": "budget"},
    "decline": {"retry": "budget", "finish": "finish"},
    "gate": {"pass": "readback", "retry": "budget"},
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
]
NODES = (
    "greet", "next_field", "budget", "ask", "listen", "extract", "explain",
    "decline", "not_understood", "gate", "readback", "listen_confirm",
    "confirm", "commit", "finish", "close",
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
        result = SessionResult(session_id=self.s.log.session_id, fields=final["results"])
        self.s._close(result)
        return result

    # -- nodes -------------------------------------------------------------

    def greet(self, state: TurnState) -> dict:
        self.s.output.say(self.s.strings.get("greeting"), kind=Kind.PROGRESS)
        return {}

    def next_field(self, state: TurnState) -> dict:
        from lucidform.orchestrate.session import FieldResult

        fields = list(self.s.schema)
        index = state["index"] + 1
        while index < len(fields) and self.s.state.is_resolved(fields[index].id):
            index += 1
        if index >= len(fields):
            return {"index": index, "route": "done"}
        return {"index": index, "current": FieldResult(field_id=fields[index].id), "route": "field"}

    def budget(self, state: TurnState) -> dict:
        outcome = state["current"]
        if outcome.attempts < self.s.max_attempts and not outcome.resolved:
            return {"route": "ask"}
        return {"route": "finish"}

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
            return {"said": None, "route": "gone"}
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
        return {"extraction": extraction, "route": route}

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
        candidate = state["extraction"].candidate
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
            return {"said": None, "route": "gone"}
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
        return {"results": [*state["results"], outcome]}

    def close(self, state: TurnState) -> dict:
        return {}

    # -- helpers -----------------------------------------------------------

    def _field(self, state: TurnState):
        return list(self.s.schema)[state["index"]]


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
