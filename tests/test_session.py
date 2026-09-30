"""The orchestrator, and the full pipeline end to end.

Two kinds of test here. The first drives one field at a time with a hand-built
channel, so each branch of the loop is exercised in isolation. The second runs
whole personas through every stage and checks the properties that only exist end
to end -- above all that no committed value differs from ground truth.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from lucidform.channels.base import Kind, Purpose
from lucidform.channels.text import PersonaChannel
from lucidform.eval.events import Event, EventLog, read_log
from lucidform.eval.personas import load_all
from lucidform.eval.replay import run_persona
from lucidform.extract.client import ReplayClient, ScriptedClient
from lucidform.extract.extractor import Extractor
from lucidform.extract.schema import Extraction, Intent
from lucidform.formstate.state import FormState
from lucidform.gate.gate import ValidationGate
from lucidform.orchestrate.session import Session
from lucidform.schema import loader

FIXTURES = Path(__file__).parent / "fixtures" / "extractions.json"


@pytest.fixture(scope="module")
def schema():
    return loader.load()


@pytest.fixture(scope="module")
def personas():
    return {p.persona_id: p for p in load_all()}


class Puppet:
    """A channel driven by a fixed list of replies. Records what was said."""

    def __init__(self, replies: list[str | None]) -> None:
        self._replies = list(replies)
        self.said: list[tuple[str, str]] = []
        self.readbacks: list[tuple[str, str]] = []

    def say(self, text: str, *, kind: Kind = Kind.PROMPT) -> None:
        self.said.append((kind.value, text))

    def read_back(self, field_id: str, value: str, text: str) -> None:
        self.readbacks.append((field_id, value))
        self.said.append((Kind.READBACK.value, text))

    def listen(self, field_id: str, purpose: Purpose) -> str | None:
        return self._replies.pop(0) if self._replies else None

    def kinds(self) -> list[str]:
        return [k for k, _ in self.said]


def one_field(schema, field_id, extractions, replies, tmp_path, **kw):
    """Run the session over a single field."""
    single = type(schema)(
        form_id=schema.form_id,
        version=schema.version,
        title=schema.title,
        fields=(schema.by_id(field_id),),
    )
    log = EventLog(tmp_path, session_id=f"one-{field_id}")
    channel = Puppet(replies)
    state = FormState(log=log)
    session = Session(
        schema=single,
        extractor=Extractor(ScriptedClient(extractions), single, log=log),
        gate=ValidationGate(single),
        state=state,
        input_channel=channel,
        output_channel=channel,
        log=log,
        **kw,
    )
    return session.run(), state, channel, log


def value(**kw) -> Extraction:
    base = dict(
        intent=Intent.VALUE,
        value="Jaipur",
        quote="jaipur",
        confidence=0.94,
        ambiguous=False,
    )
    base.update(kw)
    return Extraction(**base)


# -- the happy path ----------------------------------------------------------


def test_a_confirmed_value_is_committed(schema, tmp_path):
    result, state, channel, _ = one_field(
        schema, "city", [value()], ["jaipur", "yes that is correct"], tmp_path
    )
    assert state.get("city") == "Jaipur"
    assert result.fields[0].committed
    assert channel.readbacks == [("city", "Jaipur")]


def test_the_value_read_back_is_the_value_committed(schema, tmp_path):
    """Otherwise the user confirms one thing and the form receives another."""
    _, state, channel, _ = one_field(
        schema,
        "mobile",
        [value(value="+91 98123 45607", quote="98123 45607")],
        ["my number is 98123 45607", "yes"],
        tmp_path,
    )
    field_id, read = channel.readbacks[0]
    assert read == state.get(field_id) == "9812345607"


# -- the branches ------------------------------------------------------------


def test_a_question_is_answered_and_does_not_count_as_an_attempt(schema, tmp_path):
    """Asking what a field means is the system working as intended.

    Charging it against the retry budget would penalise exactly the users this
    project exists for.
    """
    result, state, channel, _ = one_field(
        schema,
        "pan",
        [Extraction(intent=Intent.QUESTION), value(value="AKQPS3417M", quote="akqps3417m")],
        ["what does that mean", "akqps3417m", "yes"],
        tmp_path,
    )
    outcome = result.fields[0]
    assert outcome.questions == 1
    assert outcome.attempts == 0, "an explanation must not consume a retry"
    assert outcome.committed
    assert Kind.EXPLANATION.value in channel.kinds()


def test_the_explanation_is_the_fields_own_gloss(schema, tmp_path):
    _, _, channel, _ = one_field(
        schema,
        "pan",
        [Extraction(intent=Intent.QUESTION), value(value="AKQPS3417M", quote="akqps3417m")],
        ["what does that mean", "akqps3417m", "yes"],
        tmp_path,
    )
    explanations = [t for k, t in channel.said if k == Kind.EXPLANATION.value]
    assert "Permanent Account Number" in explanations[0]


def test_endless_questions_are_bounded(schema, tmp_path):
    """Explaining again is not helping; the session must be able to move on."""
    result, _, _, _ = one_field(
        schema,
        "pan",
        [Extraction(intent=Intent.QUESTION)] * 8,
        ["eh?"] * 8,
        tmp_path,
        max_questions=2,
    )
    assert result.fields[0].abandoned
    # max_questions bounds each visit; the end-of-form revisit is a second visit.
    assert result.fields[0].questions <= 2 * 2


def test_declining_an_optional_field_is_recorded_not_committed(schema, tmp_path):
    result, state, _, _ = one_field(
        schema, "email", [Extraction(intent=Intent.DECLINE)], ["i don't have one"], tmp_path
    )
    assert result.fields[0].declined
    assert "email" not in state
    assert state.declined["email"].said == "i don't have one"


def test_declining_a_required_field_is_refused(schema, tmp_path):
    """The form is rejected without it, so the user is told rather than
    silently allowed to skip."""
    # Aadhaar: required, and with no declared alternative (PAN has Form 60).
    result, state, channel, _ = one_field(
        schema,
        "aadhaar",
        [Extraction(intent=Intent.DECLINE), value(value="234123412346", quote="234123412346")],
        ["i don't have one", "234123412346", "yes"],
        tmp_path,
    )
    assert result.fields[0].committed
    assert "aadhaar" not in state.declined
    assert any("cannot be left out" in t for _, t in channel.said)


def test_a_rejected_value_is_explained_in_the_gates_own_words(schema, tmp_path):
    """Re-phrasing the gate's wording here would put a second, untested
    explanation in front of the person who most needs it."""
    result, _, channel, _ = one_field(
        schema,
        "pin",
        [value(value="3O2015", quote="3o2015"), value(value="302015", quote="302015")],
        ["3 o 2 0 1 5", "302015", "yes"],
        tmp_path,
    )
    problems = [t for k, t in channel.said if k == Kind.PROBLEM.value]
    assert any("six digits" in p for p in problems)
    assert result.fields[0].rejections == ["format"]
    assert result.fields[0].committed


def test_a_denied_readback_is_recorded_as_a_correction(schema, tmp_path):
    result, state, _, log = one_field(
        schema,
        "city",
        [value(value="Kollam", quote="kochi"), value(value="Kochi", quote="kochi")],
        ["kochi", "no that's wrong", "kochi", "yes"],
        tmp_path,
    )
    assert result.fields[0].corrections == 1
    assert state.get("city") == "Kochi"
    events = [r["event"] for r in read_log(log.path)]
    assert Event.CORRECTION.value in events


def test_a_spoofed_confirmation_does_not_commit(schema, tmp_path):
    """End to end, through the orchestrator: "yes I know that's wrong" must
    leave the field unwritten."""
    result, state, _, _ = one_field(
        schema,
        "city",
        [value()] * 3,
        ["jaipur", "yes I know that's wrong"] * 3,
        tmp_path,
    )
    assert "city" not in state
    assert result.fields[0].abandoned
    assert result.fields[0].corrections >= 1


def test_a_field_that_runs_out_of_attempts_is_abandoned_not_left_empty(schema, tmp_path):
    result, state, _, _ = one_field(
        schema,
        "pin",
        # three attempts, then three more when the field is revisited at the end
        [value(value="not a pin", quote="not a pin")] * 6,
        ["not a pin"] * 6,
        tmp_path,
        max_attempts=3,
    )
    assert result.fields[0].abandoned
    assert not result.complete
    assert "pin" not in state


def test_silence_abandons_the_field_rather_than_being_read_as_consent(schema, tmp_path):
    """A user who hangs up has not agreed to anything."""
    result, state, _, _ = one_field(schema, "city", [value()], ["jaipur", None], tmp_path)
    assert result.fields[0].abandoned
    assert "city" not in state


def test_a_hang_up_at_the_read_back_ends_the_field_without_re_asking(schema, tmp_path):
    """Once the user is gone, asking the question again is talking to nobody.

    The pre-LangGraph loop re-asked here and only stopped because the second
    listen also returned None; with a live channel that is a phantom turn.
    """
    result, _, channel, log = one_field(
        schema, "city", [value(), value()], ["jaipur", None, "jaipur", "yes"], tmp_path
    )
    asked = [r for r in read_log(log.path) if r["event"] == Event.FIELD_ASKED.value]
    assert result.fields[0].abandoned
    assert len(asked) == 1
    assert channel.kinds().count(Kind.PROMPT.value) == 1


# -- the help agent ------------------------------------------------------------


class StubHelper:
    def __init__(self):
        self.asked = []

    def answer(self, field, question, lang):
        from lucidform.help.answer import HelpAnswer

        self.asked.append((field.id, question, lang))
        return HelpAnswer(
            spoken="A PAN is your tax number. (Source: Income Tax PAN FAQ, Q1.)",
            source="rag",
            retrieved_ids=["pan-q1"],
            cited_ids=["pan-q1"],
            cited_labels=["Income Tax PAN FAQ, Q1"],
        )


def test_a_question_is_answered_by_the_help_agent_and_never_becomes_a_value(schema, tmp_path):
    helper = StubHelper()
    result, state, channel, log = one_field(
        schema,
        "pan",
        [Extraction(intent=Intent.QUESTION), value(value="AKQPS3417M", quote="akqps3417m")],
        ["pan kya hota hai", "akqps3417m", "yes"],
        tmp_path,
        helper=helper,
    )
    assert helper.asked == [("pan", "pan kya hota hai", "en")]
    assert (Kind.EXPLANATION.value, "A PAN is your tax number. (Source: Income Tax PAN FAQ, Q1.)") in channel.said
    explained = [r for r in read_log(log.path) if r["event"] == Event.JARGON_EXPLAINED.value]
    assert explained[0]["payload"]["source"] == "rag"
    assert explained[0]["payload"]["cited_labels"] == ["Income Tax PAN FAQ, Q1"]
    # The answer is not the value: what was committed came from the user's own reply.
    assert state.values == {"pan": "AKQPS3417M"}
    assert result.fields[0].questions == 1 and result.fields[0].attempts == 0


# -- logging -----------------------------------------------------------------


def test_every_stage_is_logged_in_order(schema, tmp_path):
    _, _, _, log = one_field(
        schema, "city", [value()], ["jaipur", "yes"], tmp_path
    )
    events = [r["event"] for r in read_log(log.path)]
    expected = [
        Event.SESSION_START.value,
        Event.FIELD_ASKED.value,
        Event.USER_UTTERANCE.value,
        Event.EXTRACTION.value,
        Event.VALIDATION.value,
        Event.READBACK.value,
        Event.USER_UTTERANCE.value,
        Event.CONFIRMATION.value,
        Event.COMMIT.value,
        Event.READBACK.value,  # the final summary (LF-006)
        Event.SESSION_END.value,
    ]
    assert events == expected


def test_the_session_close_records_the_outcome(schema, tmp_path):
    _, _, _, log = one_field(schema, "city", [value()], ["jaipur", "yes"], tmp_path)
    end = read_log(log.path)[-1]
    assert end["payload"]["committed"] == ["city"]
    assert end["payload"]["blocked_writes"] == 0


# -- whole personas ----------------------------------------------------------


@pytest.fixture(scope="module")
def runs(schema, personas):
    client = ReplayClient(FIXTURES)
    tmp = Path(tempfile.mkdtemp())
    return {
        pid: run_persona(p, schema, client, runs_dir=tmp)
        for pid, p in personas.items()
    }


@pytest.mark.parametrize("persona_id", ["p01", "p02", "p03"])
def test_no_committed_value_differs_from_ground_truth(runs, persona_id):
    """The correctness invariant. Not a finding -- a build failure.

    Any entry here means a value the user did not agree to reached the form.
    """
    run = runs[persona_id]
    assert run.escaped_errors == [], (
        f"{persona_id} committed values that differ from ground truth: "
        f"{run.escaped_errors}"
    )


@pytest.mark.parametrize("persona_id", ["p01", "p02", "p03"])
def test_no_write_was_blocked_during_a_normal_session(runs, persona_id):
    """A blocked write here would mean a defect upstream, not a caught attack --
    nothing in a well-behaved session should ever attempt an unauthorised write.
    """
    assert runs[persona_id].state.blocked_writes == 0


@pytest.mark.parametrize("persona_id", ["p01", "p02", "p03"])
def test_every_field_is_resolved(runs, schema, persona_id):
    run = runs[persona_id]
    assert not run.result.abandoned, [f.field_id for f in run.result.abandoned]
    for field in schema:
        assert run.state.is_resolved(field.id), field.id


def test_a_declined_optional_field_stays_empty(runs):
    """p03 has no email and says so."""
    run = runs["p03"]
    assert "email" not in run.state
    assert "email" in run.state.declined
    assert [f.field_id for f in run.result.declined] == ["email"]


def test_a_question_is_handled_mid_session(runs):
    """p03 asks what a PAN is before answering it."""
    pan = next(f for f in runs["p03"].result.fields if f.field_id == "pan")
    assert pan.questions == 1
    assert pan.committed


def test_the_gate_catches_the_homoglyph(runs):
    """p02 reads her PAN with a letter O where a digit belongs."""
    pan = next(f for f in runs["p02"].result.fields if f.field_id == "pan")
    assert pan.rejections == ["format"]
    assert pan.committed


def test_the_readback_catches_what_nothing_else_could(runs):
    """p02's city is misheard as another real city: well-formed, valid, wrong.

    Every check the gate performs passes it. Only the read-back can catch it,
    which is the whole argument for the read-back being a pipeline stage.
    """
    run = runs["p02"]
    assert run.channel.denials == [("city", "Kochi", "Kollam")]
    assert run.state.get("city") == "Kochi"


def test_out_of_enum_answers_are_re_asked_not_mapped(runs):
    """"About seven lakh" must not be silently resolved to a band."""
    for persona_id in ("p01", "p03"):
        band = next(
            f for f in runs[persona_id].result.fields if f.field_id == "income_band"
        )
        assert band.rejections == ["enum"]
        assert band.committed


def test_the_session_log_identifies_which_client_produced_it(runs):
    """A results table must never conflate a corpus replay with a live run."""
    start = read_log(runs["p01"].log_path)[0]
    assert start["payload"]["client"] == "ReplayClient"
    assert start["payload"]["persona_id"] == "p01"


def test_a_persona_run_produces_a_readable_transcript(runs):
    dialogue = runs["p01"].channel.dialogue()
    assert "What is your full name" in dialogue
    assert "Is that correct?" in dialogue
    assert dialogue.count(">") >= 14, "the user should speak at least once per field"


def test_a_model_that_always_fails_ends_the_session_cleanly(schema, tmp_path):
    """Every turn costs an attempt; the field is abandoned; the session still closes."""

    class Down:
        model = "down"

        def complete(self, system, user):
            raise ConnectionError("network unreachable")

    single = type(schema)(
        form_id=schema.form_id, version=schema.version, title=schema.title,
        fields=(schema.by_id("city"),),
    )
    log = EventLog(tmp_path, session_id="down")
    channel = Puppet(["jaipur", "jaipur", "jaipur"])
    state = FormState(log=log)
    result = Session(
        schema=single, extractor=Extractor(Down(), single, log=log),
        gate=ValidationGate(single), state=state, input_channel=channel,
        output_channel=channel, log=log,
    ).run()

    events = [r["event"] for r in read_log(log.path)]
    assert result.fields[0].abandoned and result.fields[0].attempts == 3
    assert "city" not in state
    assert events[-1] == Event.SESSION_END.value
    assert channel.kinds().count(Kind.PROBLEM.value) == 3
