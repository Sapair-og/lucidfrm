"""Text channels: a console for a person, and a persona for the replay driver.

Both implement the same protocols the voice channel will implement in Phase 7,
so the orchestrator does not change when audio arrives.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field

from lucidform.channels.base import Kind, Purpose
from lucidform.eval.personas import Persona


class ConsoleChannel:
    """A real person at a terminal.

    Output is prefixed by kind rather than coloured alone, so the transcript is
    still readable when piped to a file or through a screen reader -- colour is
    not information a screen reader conveys.
    """

    PREFIX = {
        Kind.PROMPT: "",
        Kind.EXPLANATION: "  ",
        Kind.PROBLEM: "  ",
        Kind.READBACK: "",
        Kind.PROGRESS: "  ",
        Kind.CLOSING: "",
    }

    def __init__(self, stream=None) -> None:
        self.stream = stream or sys.stdout
        if hasattr(self.stream, "reconfigure"):
            # Hindi output through a legacy console code page is unreadable,
            # and a garbled read-back is indistinguishable from a wrong one.
            self.stream.reconfigure(encoding="utf-8", errors="replace")

    def say(self, text: str, *, kind: Kind = Kind.PROMPT) -> None:
        print(f"{self.PREFIX.get(kind, '')}{text}", file=self.stream)

    def read_back(self, field_id: str, value: str, text: str) -> None:
        print(f"\n{text}", file=self.stream)

    def listen(self, field_id: str, purpose: Purpose) -> str | None:
        try:
            return input("> ")
        except (EOFError, KeyboardInterrupt):
            # Not silence, and not consent -- the session records the field as
            # abandoned.
            return None


@dataclass
class Turn:
    """One exchange, kept for the transcript."""

    speaker: str
    text: str
    kind: str = ""
    field_id: str = ""


class PersonaChannel:
    """A simulated user, driven by a persona's script.

    Implements both protocols: it has to hear the read-back in order to answer
    it. That is the point of the design -- it compares the value being read back
    against its own ground truth and answers honestly, so a wrong value is
    denied exactly as a real user would deny it.

    Without that, the read-back correction rate would be a constant chosen by
    whoever wrote the driver rather than a property of the pipeline.
    """

    def __init__(self, persona: Persona, echo: bool = False) -> None:
        self.persona = persona
        self.echo = echo
        self.transcript: list[Turn] = []
        self._next: dict[str, int] = {}
        self._pending_readback: tuple[str, str] | None = None
        self.denials: list[tuple[str, str, str]] = []

    # -- output --------------------------------------------------------------

    def say(self, text: str, *, kind: Kind = Kind.PROMPT) -> None:
        self.transcript.append(Turn("system", text, kind.value))
        if self.echo:
            print(f"[{kind.value}] {text}")

    def read_back(self, field_id: str, value: str, text: str) -> None:
        self._pending_readback = (field_id, value)
        self.transcript.append(Turn("system", text, Kind.READBACK.value, field_id))
        if self.echo:
            print(f"[readback] {text}")

    # -- input ---------------------------------------------------------------

    def listen(self, field_id: str, purpose: Purpose) -> str | None:
        said = (
            self._answer_readback(field_id)
            if purpose is Purpose.CONFIRMATION
            else self._next_utterance(field_id)
        )
        if said is not None:
            self.transcript.append(Turn("user", said, purpose.value, field_id))
            if self.echo:
                print(f"> {said}")
        return said

    def _next_utterance(self, field_id: str) -> str | None:
        index = self._next.get(field_id, 0)
        utterances = self.persona.utterances(field_id)
        if index >= len(utterances):
            # The script is exhausted. Returning None records the field as
            # abandoned rather than silently repeating the last utterance,
            # which would let a persona loop forever and inflate the
            # turns-to-commit figure without bound.
            return None
        self._next[field_id] = index + 1
        return utterances[index]

    def _answer_readback(self, field_id: str) -> str:
        """Agree only if the value read back matches ground truth."""
        pending = self._pending_readback
        self._pending_readback = None
        if pending is None:  # pragma: no cover - orchestrator always reads back first
            return self.persona.deny

        _, value = pending
        truth = self.persona.truth(field_id)
        if value == truth:
            return self.persona.affirm

        self.denials.append((field_id, truth, value))
        return self.persona.deny

    # -- inspection ----------------------------------------------------------

    def utterances_used(self, field_id: str) -> int:
        return self._next.get(field_id, 0)

    def dialogue(self) -> str:
        lines = []
        for turn in self.transcript:
            marker = ">" if turn.speaker == "user" else " "
            lines.append(f"{marker} {turn.text}")
        return "\n".join(lines)
