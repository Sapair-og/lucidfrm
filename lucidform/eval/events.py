"""Append-only session event log -- the evaluation substrate.

One record per pipeline stage per field. Written as JSONL so a run can be
inspected mid-flight and reduced to CSV later without re-running sessions.

The log is append-only by construction: the file is opened in append mode and
this module exposes no update or delete. Rewriting history would invalidate
every number derived from it (SPEC.md section 3).
"""

from __future__ import annotations

import enum
import json
import os
import time
import uuid
from contextlib import contextmanager
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


class Event(str, enum.Enum):
    SESSION_START = "session_start"
    FIELD_ASKED = "field_asked"
    USER_UTTERANCE = "user_utterance"
    JARGON_EXPLAINED = "jargon_explained"
    EXTRACTION = "extraction"
    VALIDATION = "validation"
    READBACK = "readback"
    CONFIRMATION = "confirmation"
    COMMIT = "commit"
    CORRECTION = "correction"
    # A write was attempted that did not satisfy the commit invariant. This is a
    # research finding, not a swallowed error -- see SPEC.md section 2.
    SILENT_WRITE_BLOCKED = "silent_write_blocked"
    SESSION_END = "session_end"
    # Phase 7 (voice channel). Declared here so the log schema does not change
    # when the audio adapters land.
    ASR_RESULT = "asr_result"
    TTS_EMIT = "tts_emit"


def _jsonable(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return {k: _jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    return value


class EventLog:
    """Append-only JSONL writer for one session."""

    def __init__(
        self,
        runs_dir: Path,
        session_id: str | None = None,
        meta: dict[str, Any] | None = None,
    ) -> None:
        self.session_id = session_id or uuid.uuid4().hex
        self.runs_dir = Path(runs_dir)
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.runs_dir / f"{self.session_id}.jsonl"
        self._seq = 0
        self.emit(Event.SESSION_START, payload=meta or {})

    def emit(
        self,
        event: Event,
        *,
        field_id: str | None = None,
        turn_idx: int | None = None,
        t_start: float | None = None,
        t_end: float | None = None,
        payload: Any = None,
    ) -> dict[str, Any]:
        self._seq += 1
        record = {
            "session_id": self.session_id,
            "seq": self._seq,
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": event.value,
            "field_id": field_id,
            "turn_idx": turn_idx,
            # Milliseconds. Null when the stage is instantaneous or unmeasured;
            # metrics treats null as "not applicable", never as zero.
            "latency_ms": None
            if t_start is None or t_end is None
            else round((t_end - t_start) * 1000, 3),
            "payload": _jsonable(payload) if payload is not None else {},
        }
        # Append + flush + fsync: a crash mid-session must not lose the events
        # that explain why it crashed.
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        return record

    @contextmanager
    def timed(
        self,
        event: Event,
        *,
        field_id: str | None = None,
        turn_idx: int | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Time a stage and emit once it completes.

        Mutate the yielded dict to attach the payload; it is read after the
        block exits, so the payload can depend on the stage's own result.
        """
        box: dict[str, Any] = {}
        t0 = time.perf_counter()
        try:
            yield box
        finally:
            self.emit(
                event,
                field_id=field_id,
                turn_idx=turn_idx,
                t_start=t0,
                t_end=time.perf_counter(),
                payload=box,
            )

    def close(self, payload: Any = None) -> None:
        self.emit(Event.SESSION_END, payload=payload or {})


def read_log(path: Path) -> list[dict[str, Any]]:
    """Read one session log. Used by metrics and by tests; never by the pipeline."""
    with Path(path).open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]
