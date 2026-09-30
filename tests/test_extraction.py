"""Stage 3: utterance to candidate.

No network. Every test here runs against a scripted or replayed client, so the
suite is green without credentials and the results are not subject to model
variance.

The emphasis is on the three deterministic guards the extractor applies to the
model's reply -- intent separation, grounding, and confidence clamping -- because
those are the parts that hold when the model is wrong, which is the only time
they matter.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lucidform.eval.events import Event, EventLog, read_log
from lucidform.extract import grounding as ground
from lucidform.extract.client import ReplayClient, ScriptedClient
from lucidform.extract.extractor import Extractor
from lucidform.extract.prompt import build
from lucidform.extract.schema import Extraction, Intent
from lucidform.gate.gate import ValidationGate
from lucidform.models import Reason, Status
from lucidform.schema import loader

FIXTURES = Path(__file__).parent / "fixtures" / "extractions.json"


@pytest.fixture(scope="module")
def schema():
    return loader.load()


@pytest.fixture(scope="module")
def gate(schema):
    return ValidationGate(schema)


def extractor(schema, *replies, **kw):
    return Extractor(ScriptedClient(list(replies)), schema, **kw)


def value(**kw) -> Extraction:
    base = dict(
        intent=Intent.VALUE,
        value="AKQPS3417M",
        quote="A K Q P S 3 4 1 7 M",
        confidence=0.94,
        ambiguous=False,
    )
    base.update(kw)
    return Extraction(**base)


# -- intent separation -------------------------------------------------------


def test_a_stated_value_becomes_a_candidate(schema):
    ex = extractor(schema, value())
    outcome = ex.extract("pan", "my pan is A K Q P S 3 4 1 7 M")

    assert outcome.has_candidate
    assert outcome.candidate.value == "AKQPS3417M"
    assert outcome.candidate.field_id == "pan"
    assert outcome.candidate.raw_utterance == "my pan is A K Q P S 3 4 1 7 M"


def test_a_question_never_becomes_a_candidate(schema):
    """The failure this separation exists to prevent.

    "pan kya hota hai" -- what is a PAN? -- collapsed into a value field writes
    the user's own question into the form.
    """
    ex = extractor(schema, Extraction(intent=Intent.QUESTION))
    outcome = ex.extract("pan", "pan kya hota hai")

    assert outcome.asked_a_question
    assert not outcome.has_candidate
    assert outcome.candidate is None


def test_a_decline_never_becomes_a_candidate(schema):
    ex = extractor(schema, Extraction(intent=Intent.DECLINE))
    outcome = ex.extract("email", "mera email nahi hai")

    assert outcome.declined
    assert not outcome.has_candidate


def test_an_unclear_utterance_never_becomes_a_candidate(schema):
    ex = extractor(schema, Extraction(intent=Intent.UNCLEAR))
    assert not ex.extract("pan", "mmm").has_candidate


def test_a_value_intent_with_no_value_produces_nothing(schema):
    """Belt and braces: intent says value, but there is none to propose."""
    ex = extractor(schema, Extraction(intent=Intent.VALUE, value="", quote=""))
    assert not ex.extract("pan", "uh").has_candidate


# -- grounding ---------------------------------------------------------------


def test_a_quote_from_the_utterance_grounds(schema):
    ex = extractor(schema, value(quote="A K Q P S 3 4 1 7 M"))
    outcome = ex.extract("pan", "my pan is A K Q P S 3 4 1 7 M")

    assert outcome.grounding.grounded
    assert outcome.candidate.span is not None
    start, end = outcome.candidate.span
    assert outcome.utterance[start:end] == "A K Q P S 3 4 1 7 M"


def test_an_invented_quote_does_not_ground(schema):
    """A value the model did not take from what the user said.

    This is the hallucination case: a confident, well-formed, entirely
    fabricated value. The gate cannot catch it -- the value is valid -- so it is
    caught here, by string comparison rather than by judgement.
    """
    ex = extractor(schema, value(quote="my pan is AKQPS3417M", confidence=0.99))
    outcome = ex.extract("pan", "I do not remember it")

    assert not outcome.grounding.grounded
    assert outcome.confidence == 0.0
    assert outcome.candidate.ambiguous, (
        "an ungrounded value must also be flagged ambiguous, so it is rejected "
        "even if the confidence threshold is later relaxed"
    )


def test_an_ungrounded_candidate_is_rejected_by_the_gate(schema, gate):
    """End to end: grounding failure reaches a rejection with a reason."""
    ex = extractor(schema, value(quote="not in the utterance", confidence=0.99))
    outcome = ex.extract("pan", "I do not remember it")

    report = gate.check(outcome.candidate, {"full_name": "Ramesh Kumar Sharma"})
    assert report.status is Status.REJECT
    assert report.reason is Reason.AMBIGUOUS_EXTRACTION


def test_grounding_tolerates_whitespace_and_case(schema):
    """A model that reflows spacing is still quoting."""
    ex = extractor(schema, value(quote="a k q p s  3 4 1 7 m"))
    outcome = ex.extract("pan", "My PAN is A K Q P S 3 4 1 7 M")
    assert outcome.grounding.grounded


def test_a_loose_match_reports_no_span_rather_than_a_wrong_one(schema):
    """A wrong span in the log is worse than an absent one."""
    ex = extractor(schema, value(quote="a k q p s  3 4 1 7 m"))
    outcome = ex.extract("pan", "My PAN is A K Q P S 3 4 1 7 M")
    assert outcome.candidate.span is None


def test_an_empty_quote_does_not_ground(schema):
    ex = extractor(schema, value(quote=""))
    assert not ex.extract("pan", "my pan is AKQPS3417M").grounding.grounded


def test_questions_and_declines_are_not_grounded_against_anything(schema):
    """There is no value to anchor, so grounding is vacuously satisfied rather
    than reported as a failure."""
    ex = extractor(schema, Extraction(intent=Intent.QUESTION))
    assert ex.extract("pan", "pan kya hota hai").grounding.grounded


# -- confidence clamping -----------------------------------------------------


def test_confidence_is_passed_through_when_nothing_contradicts_it(schema):
    ex = extractor(schema, value(confidence=0.91))
    assert ex.extract("pan", "my pan is A K Q P S 3 4 1 7 M").confidence == 0.91


def test_an_ambiguous_extraction_is_capped_below_any_threshold(schema):
    ex = extractor(schema, value(confidence=0.99, ambiguous=True))
    outcome = ex.extract("pan", "my pan is A K Q P S 3 4 1 7 M")
    assert outcome.confidence <= 0.4


def test_clamping_only_ever_lowers_confidence():
    """Nothing in the pipeline may talk the model's confidence up."""
    grounded = ground.Grounding(True, None)
    for reported in (0.0, 0.3, 0.5, 0.9, 1.0):
        ex = Extraction(
            intent=Intent.VALUE, value="x", quote="x", confidence=reported
        )
        assert ground.clamp_confidence(ex, grounded) <= reported


def test_a_model_reporting_impossible_confidence_is_clamped():
    """Pydantic bounds the field, so this checks the guard behind it."""
    grounded = ground.Grounding(True, None)
    ex = Extraction(intent=Intent.VALUE, value="x", quote="x", confidence=1.0)
    assert 0.0 <= ground.clamp_confidence(ex, grounded) <= 1.0


def test_low_confidence_reaches_the_gate_as_a_rejection(schema, gate):
    ex = extractor(schema, value(confidence=0.2))
    outcome = ex.extract("pan", "my pan is A K Q P S 3 4 1 7 M")
    report = gate.check(outcome.candidate, {"full_name": "Ramesh Kumar Sharma"})
    assert report.reason is Reason.LOW_CONFIDENCE


# -- the schema is the boundary ----------------------------------------------


def test_the_model_has_no_field_in_which_to_request_a_write():
    """The structural argument, asserted rather than asserted-in-prose.

    The reply schema has no field for an instruction, a status claim, or a
    commit request. A model cannot ask for something the schema cannot express.
    """
    permitted = set(Extraction.model_fields)
    assert permitted == {
        "intent",
        "value",
        "quote",
        "confidence",
        "ambiguous",
        "alternatives",
    }
    for forbidden in ("commit", "write", "validated", "approved", "skip_validation"):
        assert forbidden not in permitted


def test_a_reply_that_does_not_fit_the_schema_is_an_error_not_a_fallback():
    """There is no free-text branch for the pipeline to interpret."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Extraction.model_validate({"intent": "please_commit_this", "value": "x"})
    with pytest.raises(ValidationError):
        Extraction.model_validate({"intent": "value", "confidence": 7.0})


def test_prompt_carries_the_field_but_asks_for_no_judgement(schema):
    """The prompt must not move validation into the model.

    A prompt saying "only return valid values" relocates the accept/reject
    decision to the model, invisibly -- a silently dropped invalid value looks
    exactly like a user who never said one.
    """
    system, user = build(schema.by_id("pan"), "my pan is AKQPS3417M")

    assert "PAN" in user
    assert "my pan is AKQPS3417M" in user
    assert "Do not validate" in system
    assert "not filling in the form" in system
    for phrase in ("only return valid", "reject", "must be valid"):
        assert phrase not in system.casefold()


def test_enum_prompts_forbid_substituting_the_nearest_option(schema):
    _, user = build(schema.by_id("occupation"), "i have my own shop")
    assert "do not substitute" in user.casefold()
    assert "Business" in user


# -- logging -----------------------------------------------------------------


def test_extraction_is_logged_with_both_confidence_figures(schema, tmp_path):
    """The reported and the clamped value are both recorded.

    The gap between them is the measure of how often a deterministic check
    disagreed with the model, which is a result worth having.
    """
    log = EventLog(tmp_path, session_id="extract")
    ex = Extractor(
        ScriptedClient([value(confidence=0.99, ambiguous=True)]), schema, log=log
    )
    ex.extract("pan", "my pan is A K Q P S 3 4 1 7 M")

    record = [r for r in read_log(log.path) if r["event"] == Event.EXTRACTION.value][0]
    assert record["payload"]["reported_confidence"] == 0.99
    assert record["payload"]["confidence"] <= 0.4
    assert record["latency_ms"] is not None


def test_a_question_is_logged_too(schema, tmp_path):
    log = EventLog(tmp_path, session_id="q")
    ex = Extractor(ScriptedClient([Extraction(intent=Intent.QUESTION)]), schema, log=log)
    ex.extract("pan", "pan kya hota hai")

    record = [r for r in read_log(log.path) if r["event"] == Event.EXTRACTION.value][0]
    assert record["payload"]["intent"] == "question"


# -- the replay corpus -------------------------------------------------------


@pytest.fixture(scope="module")
def replay():
    return ReplayClient(FIXTURES)


def test_the_fixture_corpus_is_in_sync_with_its_generator():
    """The file is generated; a stale checked-in copy would silently diverge."""
    from lucidform.eval.fixtures import build as rebuild

    with FIXTURES.open(encoding="utf-8") as fh:
        on_disk = json.load(fh)
    assert on_disk == rebuild(), (
        "tests/fixtures/extractions.json is stale. Regenerate with: "
        "python -m lucidform.eval.fixtures"
    )


def test_the_corpus_states_that_it_is_not_a_recording():
    """Guards the honesty claim in METHODOLOGY M4.4.

    If this file ever were presented as recorded model output, the extraction
    accuracy figure derived from it would be circular.
    """
    with FIXTURES.open(encoding="utf-8") as fh:
        raw = json.load(fh)
    assert "not recordings" in raw["note"]
    assert "cannot measure" in raw["note"]


def test_replaying_p03_pan_yields_a_question_then_a_value(schema, replay):
    ex = Extractor(replay, schema)

    first = ex.extract("pan", "pan kya hota hai")
    assert first.asked_a_question and not first.has_candidate

    second = ex.extract("pan", "C J M P K one nine five three R")
    assert second.has_candidate
    assert second.candidate.value == "CJMPK1953R"


def test_replaying_p02_pan_yields_the_homoglyph_the_gate_then_rejects(
    schema, replay, gate
):
    """The corpus's job in one test: an error the extractor faithfully
    reproduces, caught downstream rather than repaired upstream."""
    ex = Extractor(replay, schema)
    outcome = ex.extract("pan", "B F T P N eight two O six C")

    assert outcome.candidate.value == "BFTPN82O6C"
    report = gate.check(outcome.candidate, {"full_name": "Lakshmi Devi Nair"})
    assert report.reason is Reason.FORMAT


def test_replaying_an_out_of_enum_income_is_rejected_not_mapped(
    schema, replay, gate
):
    """"About three lakh" must not become "1-5 Lakh" inside the extractor."""
    ex = Extractor(replay, schema)
    outcome = ex.extract("income_band", "teen lakh ke aas paas")

    assert outcome.candidate.value == "teen lakh"
    assert gate.check(outcome.candidate).reason is Reason.ENUM

    retry = ex.extract("income_band", "one to five lakh")
    assert gate.check(retry.candidate).status is Status.PASS


def test_every_persona_utterance_has_a_recorded_response(schema, replay):
    """Otherwise the Phase 5 replay driver stalls partway through a session."""
    from lucidform.eval.personas import load_all

    ex = Extractor(replay, schema)
    for persona in load_all():
        for field in schema:
            for utterance in persona.utterances(field.id):
                ex.extract(field.id, utterance)  # raises KeyError if missing


# -- a failing model call costs an attempt, never the session --------------------


class FailingClient:
    model = "failing"

    def __init__(self, exc):
        self.exc = exc

    def complete(self, system, user):
        raise self.exc


@pytest.mark.parametrize(
    "exc",
    [RuntimeError("network down"), ValueError("empty or blocked reply"), TimeoutError("read timeout")],
)
def test_a_failed_model_call_is_an_unclear_turn_not_a_crash(schema, exc, tmp_path):
    from lucidform.eval.events import EventLog, read_log

    log = EventLog(tmp_path, session_id="fail")
    outcome = Extractor(FailingClient(exc), schema, log=log).extract("pan", "A K Q P S 3 4 1 7 M")

    assert outcome.intent is Intent.UNCLEAR
    assert not outcome.has_candidate
    assert outcome.error and type(exc).__name__ in outcome.error
    logged = [r for r in read_log(log.path) if r["event"] == "extraction"][-1]
    assert logged["payload"]["error"] == outcome.error


def test_a_replay_corpus_miss_still_raises(schema, replay):
    """A missing fixture is a broken corpus, not a model failure -- it must be loud."""
    with pytest.raises(KeyError):
        Extractor(replay, schema).extract("pan", "an utterance nobody recorded")
