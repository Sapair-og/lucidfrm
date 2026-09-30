"""The voice channel, and the claim it exists to test.

Every test here runs without faster-whisper, Piper, or a microphone. That is
the point of the adapter boundary: if the voice channel could only be tested
with a gigabyte of model weights installed, it would not be tested.

The headline assertion is the one at the bottom -- a complete form filled over
the voice channel with the orchestrator, gate, confirmation, and write path
entirely unmodified.
"""

from __future__ import annotations

import wave
from pathlib import Path

import pytest

from lucidform.channels.base import InputChannel, Kind, OutputChannel, Purpose
from lucidform.channels.voice import (
    CorruptingRecognizer,
    EchoRecognizer,
    SilentSynthesizer,
    Transcript,
    VoiceBackendMissing,
    VoiceChannel,
)
from lucidform.eval import asr_probe
from lucidform.eval.events import Event, EventLog, read_log
from lucidform.eval.personas import load_all
from lucidform.gate.gate import ValidationGate
from lucidform.models import Status
from lucidform.orchestrate import readback
from lucidform.schema import loader


@pytest.fixture(scope="module")
def schema():
    return loader.load()


@pytest.fixture(scope="module")
def personas():
    return load_all()


# -- the optional dependency really is optional -------------------------------


def test_the_module_imports_without_any_speech_library():
    """The gate must stay installable and testable without a gigabyte of
    model weights. If this fails, the heavy imports have leaked to module
    scope.

    Deliberately does *not* importlib.reload() the module: doing so mints a
    fresh class object for e.g. VoiceBackendMissing, which then fails
    isinstance/except checks against the class other tests imported earlier
    -- a real bug this test tripped over once already.
    """
    import lucidform.channels.voice as voice

    assert voice.VoiceChannel is not None


def test_asking_for_a_missing_backend_says_how_to_install_it():
    from lucidform.channels.voice import PiperSynthesizer

    with pytest.raises(VoiceBackendMissing, match="requirements-voice"):
        PiperSynthesizer(voice="nonexistent.onnx", binary="definitely-not-a-binary")


def test_the_fakes_satisfy_the_channel_protocols(tmp_path):
    channel = VoiceChannel(
        EchoRecognizer(["hello"]),
        SilentSynthesizer(),
        source=lambda field_id, purpose: None,
    )
    assert isinstance(channel, InputChannel)
    assert isinstance(channel, OutputChannel)


# -- synthesis and recognition round trip -------------------------------------


def test_the_synthesizer_writes_a_playable_wav(tmp_path):
    out = SilentSynthesizer().synthesize("hello", tmp_path / "a.wav")
    assert out.exists()
    with wave.open(str(out), "rb") as fh:
        assert fh.getframerate() == 16000
        assert fh.getnchannels() == 1


def test_the_channel_speaks_everything_it_is_given(tmp_path):
    tts = SilentSynthesizer()
    channel = VoiceChannel(
        EchoRecognizer(), tts, source=lambda f, p: None, audio_dir=tmp_path
    )
    channel.say("What is your PAN number?")
    channel.read_back("pan", "AKQPS3417M", "I have PAN as: A K Q P S three four one seven M.")

    assert len(tts.spoken) == 2
    assert "three" in tts.spoken[1], "the read-back must be spoken as rendered"
    assert len(list(tmp_path.glob("*.wav"))) == 2


def test_audio_events_are_logged_on_both_sides(tmp_path):
    """A voice session's log must record what was said and what was heard, or
    an error cannot be traced back to the audio that caused it."""
    log = EventLog(tmp_path, session_id="voice")
    wav = SilentSynthesizer().synthesize("A K Q P S", tmp_path / "in.wav")

    channel = VoiceChannel(
        EchoRecognizer(["A K Q P S three four one seven M"]),
        SilentSynthesizer(),
        source=lambda f, p: wav,
        log=log,
        audio_dir=tmp_path,
    )
    channel.say("What is your PAN number?")
    heard = channel.listen("pan", Purpose.VALUE)

    events = [r["event"] for r in read_log(log.path)]
    assert Event.TTS_EMIT.value in events
    assert Event.ASR_RESULT.value in events

    asr = [r for r in read_log(log.path) if r["event"] == Event.ASR_RESULT.value][0]
    assert asr["payload"]["text"] == heard
    assert asr["payload"]["purpose"] == "value"
    assert asr["latency_ms"] is not None


def test_no_audio_ends_the_field_rather_than_being_read_as_consent(tmp_path):
    channel = VoiceChannel(
        EchoRecognizer(), SilentSynthesizer(), source=lambda f, p: None, audio_dir=tmp_path
    )
    assert channel.listen("pan", Purpose.VALUE) is None


def test_an_empty_transcript_is_an_unusable_answer_not_a_hang_up(tmp_path):
    """Silence recognised as nothing must cause a re-ask, not end the field --
    and must never be treated as agreement."""
    wav = SilentSynthesizer().synthesize("", tmp_path / "quiet.wav")
    channel = VoiceChannel(
        EchoRecognizer([""]), SilentSynthesizer(), source=lambda f, p: wav, audio_dir=tmp_path
    )
    assert channel.listen("pan", Purpose.VALUE) == ""


def test_asr_confidence_is_recorded_but_never_reaches_the_gate(tmp_path):
    """The recogniser's confidence and the extractor's measure different
    things. Merging them would produce a number meaning neither."""
    from lucidform.models import Candidate

    wav = SilentSynthesizer().synthesize("x", tmp_path / "x.wav")
    channel = VoiceChannel(
        EchoRecognizer(["AKQPS3417M"]),
        SilentSynthesizer(),
        source=lambda f, p: wav,
        audio_dir=tmp_path,
    )
    channel.listen("pan", Purpose.VALUE)
    assert channel.transcript[-1].asr_confidence == 1.0

    # The gate's inputs come from the Candidate, which has no ASR field.
    assert "asr" not in " ".join(Candidate.__dataclass_fields__)


# -- the probe ---------------------------------------------------------------


def test_the_decode_is_the_exact_inverse_of_the_read_back(schema):
    """The round trip only measures anything if these two agree."""
    for field_id, value in [
        ("pan", "AKQPS3417M"),
        ("aadhaar", "747910984992"),
        ("pin", "302015"),
        ("mobile", "9812345607"),
    ]:
        field = schema.by_id(field_id)
        spoken = readback.render_value(value, field)
        assert asr_probe.decode_spelled(spoken, field) == value, field_id


def test_homophones_are_decoded_as_the_digit_they_sound_like(schema):
    """"oh" for zero and "for" for four are transcription artefacts, not
    mistakes the user made -- decoding them measures the recogniser rather
    than its spelling convention."""
    field = schema.by_id("pin")
    assert asr_probe.decode_spelled("three oh two oh one five", field) == "302015"
    assert asr_probe.decode_spelled("three zero two zero one five", field) == "302015"


def test_character_error_rate_is_zero_for_an_exact_match():
    assert asr_probe.character_error_rate("abc def", "ABC  def") == 0.0
    assert asr_probe.character_error_rate("abc", "abd") > 0


def test_the_probe_runs_end_to_end_without_any_model(personas, schema, tmp_path):
    summary = asr_probe.probe(
        personas,
        schema,
        CorruptingRecognizer(error_every=7),
        SilentSynthesizer(),
        tmp_path,
    )
    assert summary.results
    assert summary.mean_cer("identifier") is not None
    assert summary.survival_rate("identifier") is not None


def test_a_perfect_recogniser_loses_nothing(personas, schema, tmp_path):
    """Guard on the probe itself.

    If the round trip corrupted values even with a lossless recogniser, every
    figure it produced would be measuring the probe rather than the recogniser.
    """

    class Perfect:
        model = "perfect"

        def transcribe(self, audio: Path, lang: str = "en") -> Transcript:
            text = Path(audio).with_suffix(".txt").read_text(encoding="utf-8")
            return Transcript(text=text, confidence=1.0, model=self.model)

    summary = asr_probe.probe(
        personas, schema, Perfect(), SilentSynthesizer(), tmp_path
    )
    assert summary.survival_rate("identifier") == 1.0
    assert summary.mean_cer("identifier") == 0.0
    assert not summary.corrupted


def test_corrupted_identifiers_are_classified_and_offered_to_the_gate(
    personas, schema, tmp_path
):
    summary = asr_probe.probe(
        personas,
        schema,
        CorruptingRecognizer(error_every=5),
        SilentSynthesizer(),
        tmp_path,
        gate=ValidationGate(schema),
    )
    assert summary.corrupted, "the simulator should corrupt something at this rate"
    for row in summary.corrupted:
        assert row.gate_status in {"pass", "reject"}
    # Every corrupted identifier is either rejected by the gate or reaches the
    # read-back. There is no third outcome.
    assert len(summary.caught) + len(summary.escaped_the_gate) == len(summary.corrupted)


def test_simulated_runs_are_labelled_as_not_being_measurements(
    personas, schema, tmp_path
):
    """Same discipline as the offline extraction corpus: a number detached from
    how it was produced is how a circular result reaches a paper."""
    summary = asr_probe.probe(
        personas, schema, CorruptingRecognizer(), SilentSynthesizer(), tmp_path
    )
    assert asr_probe.is_simulated(summary)
    text = asr_probe.report(summary)
    assert "NOT MEASUREMENTS" in text
    assert "requirements-voice.txt" in text


def test_a_real_recogniser_would_not_be_labelled_simulated():
    summary = asr_probe.ProbeSummary(
        results=[
            asr_probe.ProbeResult(
                persona_id="p01",
                field_id="pan",
                category="identifier",
                spoken_text="A",
                truth="A",
                transcript="A",
                model="faster-whisper/small",
            )
        ]
    )
    assert not asr_probe.is_simulated(summary)
    assert "NOT MEASUREMENTS" not in asr_probe.report(summary)


# -- the whole pipeline, over voice -------------------------------------------


def test_a_form_is_filled_over_the_voice_channel(schema, personas, tmp_path):
    """The Phase 7 claim, asserted.

    The orchestrator, gate, confirmation step, and write path are the same
    objects the text channel uses. Only the channel differs -- which is what
    METHODOLOGY M0.6 promised the adapter boundary would buy.
    """
    from lucidform.eval.events import EventLog
    from lucidform.extract.client import ReplayClient
    from lucidform.extract.extractor import Extractor
    from lucidform.formstate.state import FormState
    from lucidform.orchestrate.session import Session

    persona = next(p for p in personas if p.persona_id == "p01")
    tts = SilentSynthesizer()
    log = EventLog(tmp_path, session_id="voice-session")

    # A speaker: renders the persona's next utterance to audio, so the session
    # genuinely goes through synthesis and recognition rather than strings.
    pending: dict[str, int] = {}
    last_readback: dict[str, str] = {}
    spoken_texts: list[str] = []

    def source(field_id: str, purpose: Purpose):
        if purpose is Purpose.CONFIRMATION:
            said = (
                persona.affirm
                if last_readback.get(field_id) == persona.truth(field_id)
                else persona.deny
            )
        else:
            index = pending.get(field_id, 0)
            utterances = persona.utterances(field_id)
            if index >= len(utterances):
                return None
            pending[field_id] = index + 1
            said = utterances[index]
        spoken_texts.append(said)
        return tts.synthesize(said, tmp_path / f"user_{len(spoken_texts):03d}.wav")

    class Listening(VoiceChannel):
        def read_back(self, field_id: str, value: str, text: str) -> None:
            last_readback[field_id] = value
            super().read_back(field_id, value, text)

    channel = Listening(
        # Reads back exactly what was synthesised: a lossless recogniser, so
        # this test measures the wiring rather than transcription quality.
        recognizer=type(
            "Lossless",
            (),
            {
                "model": "lossless",
                "transcribe": lambda self, audio, lang="en": Transcript(
                    text=Path(audio).with_suffix(".txt").read_text(encoding="utf-8"),
                    confidence=1.0,
                    model="lossless",
                ),
            },
        )(),
        synthesizer=tts,
        source=source,
        log=log,
        audio_dir=tmp_path,
    )

    state = FormState(log=log)
    session = Session(
        schema=schema,
        extractor=Extractor(
            ReplayClient(Path(__file__).parent / "fixtures" / "extractions.json"),
            schema,
            log=log,
        ),
        gate=ValidationGate(schema),
        state=state,
        input_channel=channel,
        output_channel=channel,
        log=log,
    )
    result = session.run()

    assert len(result.committed) == 14, [f.field_id for f in result.abandoned]
    assert state.blocked_writes == 0
    for field in schema:
        assert state.get(field.id) == persona.truth(field.id), field.id

    events = [r["event"] for r in read_log(log.path)]
    assert Event.ASR_RESULT.value in events
    assert Event.TTS_EMIT.value in events
    assert Event.COMMIT.value in events
