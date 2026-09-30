"""The voice channel: speech in, speech out, pipeline unchanged.

Phase 7 of the plan, and the point at which the deferral recorded in
METHODOLOGY M0.6 pays off or does not. Nothing in the orchestrator, the gate,
the confirmation step, or the write path changes to accommodate audio. This
module implements the same two protocols the console channel implements, and
that is the whole of the integration.

**The heavy dependencies are optional and imported lazily.** Speech recognition
and synthesis pull in roughly a gigabyte of libraries and model weights, and the
validation gate -- the part the project is actually about -- must remain
installable and testable without them. Every import of `faster_whisper` or
`piper` happens inside a function, so this module imports cleanly on a machine
that has neither, and the test suite exercises the channel against fake
backends.

    pip install -r requirements-voice.txt

**What speech recognition does to this problem.** Recognisers are trained and
benchmarked on prose. A KYC form is mostly not prose: it is names, dates, and
alphanumeric identifiers read out character by character, which is the input
shape recognisers handle worst. A misrecognised PAN is both likely and
consequential, and it is the reason the deterministic gate and the explicit
read-back are load-bearing rather than decorative. `lucidform/eval/asr_probe.py`
measures that degradation directly rather than asserting it.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import wave
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from lucidform.channels.base import Kind, Purpose
from lucidform.eval.events import Event, EventLog


class VoiceBackendMissing(RuntimeError):
    """A speech backend was requested but is not installed."""


@dataclass(frozen=True)
class Transcript:
    """What the recogniser heard.

    `confidence` is the recogniser's own estimate where it provides one. It is
    kept separate from the extractor's confidence and never merged: they measure
    different things, and combining them would produce a number that means
    neither. The gate sees only the extractor's.
    """

    text: str
    confidence: float | None = None
    language: str = ""
    duration_s: float | None = None
    model: str = ""


class SpeechRecognizer(Protocol):
    def transcribe(self, audio: Path, lang: str = "en") -> Transcript: ...


class SpeechSynthesizer(Protocol):
    def synthesize(self, text: str, out: Path, lang: str = "en") -> Path: ...


# -- backends ----------------------------------------------------------------


class FasterWhisperRecognizer:
    """Local speech recognition via faster-whisper (CTranslate2).

    Local and pinned rather than a hosted API, so a recorded evaluation is
    reproducible: the same audio and the same model version yield the same
    transcript, with no network variance folded into the latency figures.

    `beam_size` and `temperature` are fixed rather than left to the library's
    defaults for the same reason -- a sampled transcript would make the
    degradation measurement irreproducible.
    """

    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
        beam_size: int = 5,
    ) -> None:
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:  # pragma: no cover - depends on install
            raise VoiceBackendMissing(
                "faster-whisper is not installed. Install the voice extras: "
                "pip install -r requirements-voice.txt"
            ) from exc

        self.model_size = model_size
        self.beam_size = beam_size
        self._model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio: Path, lang: str = "en") -> Transcript:
        segments, info = self._model.transcribe(
            str(audio),
            language=lang,
            beam_size=self.beam_size,
            temperature=0.0,  # deterministic; see the class docstring
            condition_on_previous_text=False,
        )
        segments = list(segments)
        text = " ".join(s.text.strip() for s in segments).strip()

        # Whisper reports average log-probability per segment. Exponentiating
        # gives a rough per-token probability -- reported for analysis, never
        # used as a gate input.
        confidences = [
            s.avg_logprob for s in segments if getattr(s, "avg_logprob", None) is not None
        ]
        confidence = None
        if confidences:
            import math

            confidence = round(math.exp(sum(confidences) / len(confidences)), 4)

        return Transcript(
            text=text,
            confidence=confidence,
            language=getattr(info, "language", lang),
            duration_s=getattr(info, "duration", None),
            model=f"faster-whisper/{self.model_size}",
        )


class PiperSynthesizer:
    """Local speech synthesis via Piper.

    Invoked as a subprocess rather than through a binding: Piper ships as a
    standalone binary, and shelling out keeps the dependency to a file on disk
    rather than a Python package that must match the interpreter.
    """

    def __init__(self, voice: Path | str, binary: str = "piper") -> None:
        self.voice = Path(voice)
        self.binary = binary
        if shutil.which(binary) is None:
            raise VoiceBackendMissing(
                f"{binary!r} is not on PATH. Install Piper and a voice model; "
                "see requirements-voice.txt"
            )
        if not self.voice.exists():
            raise VoiceBackendMissing(f"Piper voice model not found: {self.voice}")

    def synthesize(self, text: str, out: Path, lang: str = "en") -> Path:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [self.binary, "--model", str(self.voice), "--output_file", str(out)],
            input=text.encode("utf-8"),
            check=True,
            capture_output=True,
        )
        return out


# -- fakes, for tests and for running the pipeline without audio -------------


class EchoRecognizer:
    """Returns text handed to it. Lets the channel be tested without audio."""

    def __init__(self, transcripts: list[str] | None = None) -> None:
        self._queue = list(transcripts or [])
        self.model = "echo"

    def transcribe(self, audio: Path, lang: str = "en") -> Transcript:
        text = self._queue.pop(0) if self._queue else ""
        return Transcript(text=text, confidence=1.0, language=lang, model="echo")


class CorruptingRecognizer:
    """Applies documented speech-recognition error patterns, deterministically.

    **This simulates recognition; it does not perform it. Numbers produced with
    it are not measurements**, for the same reason the offline extraction corpus
    cannot measure extraction accuracy: the errors were chosen rather than
    observed. It exists so the probe's analysis can be developed and tested
    without a gigabyte of model weights, and so the pipeline's handling of
    corrupted audio input is exercised on every test run.

    The substitutions are the error classes recognisers actually produce on
    spelled-out identifiers -- letter/digit homophones, dropped short tokens,
    and merged adjacent digits. They are applied on a fixed schedule driven by a
    seed rather than sampled, so a probe run is reproducible.

    Replace it with `FasterWhisperRecognizer` to obtain real figures.
    """

    # Spoken forms a recogniser genuinely confuses. The letter O and the digit
    # zero are the canonical case and the one that breaks identifiers.
    CONFUSIONS = {
        "zero": "o",
        "o": "zero",
        "one": "won",
        "two": "to",
        "four": "for",
        "eight": "ate",
        "b": "d",
        "m": "n",
        "s": "f",
    }

    def __init__(self, error_every: int = 4, seed: int = 0) -> None:
        # Corrupt one token in every `error_every`, counting across the whole
        # run so the rate is exact rather than probabilistic.
        self.error_every = max(1, error_every)
        self._counter = seed
        self.model = f"simulated/every-{self.error_every}-tokens"

    def transcribe(self, audio: Path, lang: str = "en") -> Transcript:
        # The fake reads the text back out of the WAV's companion file written
        # by SilentSynthesizer, so the round trip exercises real file handling.
        sidecar = Path(audio).with_suffix(".txt")
        text = sidecar.read_text(encoding="utf-8") if sidecar.exists() else ""

        tokens = text.split()
        out: list[str] = []
        for token in tokens:
            self._counter += 1
            if self._counter % self.error_every:
                out.append(token)
                continue
            lowered = token.casefold()
            if lowered in self.CONFUSIONS:
                out.append(self.CONFUSIONS[lowered])
            elif len(out) >= 1:
                # Drop the token: a short spoken character the recogniser
                # missed entirely, which is what shortens an identifier.
                continue
            else:
                out.append(token)

        return Transcript(
            text=" ".join(out),
            confidence=0.62,
            language=lang,
            model=self.model,
        )


class SilentSynthesizer:
    """Writes a valid but silent WAV. Exercises the file path without a voice."""

    def __init__(self) -> None:
        self.spoken: list[str] = []

    def synthesize(self, text: str, out: Path, lang: str = "en") -> Path:
        self.spoken.append(text)
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(out), "wb") as fh:
            fh.setnchannels(1)
            fh.setsampwidth(2)
            fh.setframerate(16000)
            fh.writeframes(b"\x00\x00" * 1600)  # 0.1s of silence
        # A sidecar carrying what was "spoken", so a simulated recogniser has
        # something to work from. A real synthesiser writes no such file, and a
        # real recogniser never looks for one.
        out.with_suffix(".txt").write_text(text, encoding="utf-8")
        return out


# -- the channel -------------------------------------------------------------


@dataclass
class VoiceTurn:
    """One audio exchange, retained for the transcript and for error analysis."""

    speaker: str
    text: str
    kind: str = ""
    field_id: str = ""
    audio: Path | None = None
    asr_confidence: float | None = None


class VoiceChannel:
    """Speech in, speech out, over the same protocols as the console.

    Audio input is supplied by a `source` callable rather than read from a
    microphone here, so the same channel drives a live session, a set of
    pre-recorded files, and the synthesis-to-recognition probe. Capturing from a
    microphone is the caller's concern.
    """

    def __init__(
        self,
        recognizer: SpeechRecognizer,
        synthesizer: SpeechSynthesizer,
        source,
        log: EventLog | None = None,
        lang: str = "en",
        audio_dir: Path | None = None,
    ) -> None:
        self.recognizer = recognizer
        self.synthesizer = synthesizer
        # source(field_id, purpose) -> Path | None. None ends the field, exactly
        # as a console user pressing Ctrl-D does.
        self.source = source
        self.log = log
        self.lang = lang
        self.audio_dir = Path(audio_dir or tempfile.mkdtemp(prefix="lucidform-tts-"))
        self.transcript: list[VoiceTurn] = []
        self._spoken = 0

    # -- output --------------------------------------------------------------

    def say(self, text: str, *, kind: Kind = Kind.PROMPT) -> None:
        self._speak(text, kind)

    def read_back(self, field_id: str, value: str, text: str) -> None:
        # The read-back carries the value as data as well as as speech, so a
        # simulated listener can answer it honestly and a voice implementation
        # can slow the delivery of the part being confirmed.
        self._speak(text, Kind.READBACK, field_id=field_id, value=value)

    def _speak(
        self, text: str, kind: Kind, field_id: str = "", value: str = ""
    ) -> None:
        self._spoken += 1
        out = self.audio_dir / f"say_{self._spoken:03d}_{kind.value}.wav"
        audio = self.synthesizer.synthesize(text, out, self.lang)
        self.transcript.append(VoiceTurn("system", text, kind.value, field_id, audio))
        if self.log is not None:
            self.log.emit(
                Event.TTS_EMIT,
                field_id=field_id or None,
                payload={
                    "text": text,
                    "kind": kind.value,
                    "value": value,
                    "audio": str(audio),
                },
            )

    # -- input ---------------------------------------------------------------

    def listen(self, field_id: str, purpose: Purpose) -> str | None:
        audio = self.source(field_id, purpose)
        if audio is None:
            return None

        if self.log is not None:
            with self.log.timed(Event.ASR_RESULT, field_id=field_id) as box:
                result = self.recognizer.transcribe(Path(audio), self.lang)
                box.update(
                    {
                        "text": result.text,
                        "asr_confidence": result.confidence,
                        "model": result.model,
                        "language": result.language,
                        "duration_s": result.duration_s,
                        "purpose": purpose.value,
                        "audio": str(audio),
                    }
                )
        else:
            result = self.recognizer.transcribe(Path(audio), self.lang)

        self.transcript.append(
            VoiceTurn(
                "user",
                result.text,
                purpose.value,
                field_id,
                Path(audio),
                result.confidence,
            )
        )
        # An empty transcript is silence, and silence is not consent. Returned
        # as an empty string rather than None so the orchestrator treats it as
        # an unusable answer and re-asks, rather than as the user hanging up.
        return result.text

    def dialogue(self) -> str:
        return "\n".join(
            f"{'>' if t.speaker == 'user' else ' '} {t.text}" for t in self.transcript
        )
