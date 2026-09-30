"""The boundary between the pipeline and however the user is actually talking.

The orchestrator never touches a console, a microphone, or a file. It says
things and it listens for things, through the two protocols below. That is what
makes the deferred voice channel a swap of two classes rather than a rewrite
(METHODOLOGY M0.6), and it is also what makes a simulated user possible: the
replay driver implements the same protocols as the console.

`read_back` is a separate method rather than another `say`, and deliberately so.
The read-back is the moment the user is asked to attest to a value, so the
channel receives the *value* as structured data alongside the words. A simulated
user can then compare it to ground truth and answer honestly, which is what
makes the read-back correction rate a measurement rather than a constant. A
voice channel will want the same separation for a different reason: a value
being read for confirmation should be spoken more slowly than surrounding
narration.
"""

from __future__ import annotations

import enum
from typing import Protocol, runtime_checkable


class Purpose(str, enum.Enum):
    """Why the system is listening. The user does not see this; the channel does."""

    VALUE = "value"
    CONFIRMATION = "confirmation"


class Kind(str, enum.Enum):
    """What sort of thing is being said, for channels that present them differently."""

    PROMPT = "prompt"
    EXPLANATION = "explanation"
    PROBLEM = "problem"
    READBACK = "readback"
    PROGRESS = "progress"
    CLOSING = "closing"


@runtime_checkable
class OutputChannel(Protocol):
    def say(self, text: str, *, kind: Kind = Kind.PROMPT) -> None: ...

    def read_back(self, field_id: str, value: str, text: str) -> None:
        """State a validated value for confirmation.

        `value` is the exact string that will be committed if the user agrees;
        `text` is how it was rendered for a person to hear.
        """
        ...


@runtime_checkable
class InputChannel(Protocol):
    def listen(self, field_id: str, purpose: Purpose) -> str | None:
        """Return what the user said, or None if there is nothing further.

        None means the session cannot continue for this field -- the user hung
        up, or a simulated user ran out of script. It is recorded as an
        abandoned field, never as silence that could be read as consent.
        """
        ...
