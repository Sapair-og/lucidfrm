"""Record what a persona session does, minus what legitimately varies per run.

The golden file pins the orchestrator's observable behaviour -- every event, in
order, with its payload, and everything said to the user -- so replacing the
orchestrator can be checked for parity rather than eyeballed. It was generated
from the pre-LangGraph loop; regenerating it after a deliberate behaviour change
is a reviewable diff, not a silent update.

    python -m tests.golden_sessions          # rewrite tests/fixtures/session_golden.json
"""

from __future__ import annotations

import json
import tempfile
from dataclasses import asdict
from pathlib import Path

from lucidform.eval.events import read_log
from lucidform.eval.personas import load_all
from lucidform.eval.replay import run_persona
from lucidform.extract.client import ReplayClient
from lucidform.schema import loader

FIXTURES = Path(__file__).parent / "fixtures"
GOLDEN = FIXTURES / "session_golden.json"

# Identifiers, clocks and timings differ on every run by construction.
VOLATILE = {
    "at",
    "candidate_id",
    "created_at",
    "issued_at",
    "committed_at",
    "candidate_fingerprint",
    "fingerprint",
    "session_id",
    "ts",
}


def _scrub(value):
    if isinstance(value, dict):
        return {k: _scrub(v) for k, v in sorted(value.items()) if k not in VOLATILE}
    if isinstance(value, list):
        return [_scrub(v) for v in value]
    return value


def record(lang: str | None = None) -> dict:
    schema = loader.load()
    client = ReplayClient(FIXTURES / "extractions.json")
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        for persona in sorted(load_all(), key=lambda p: p.persona_id):
            pid = persona.persona_id
            run = run_persona(persona, schema, client, runs_dir=Path(tmp), lang=lang)
            events = [
                {
                    "event": r["event"],
                    "field_id": r["field_id"],
                    "turn_idx": r["turn_idx"],
                    "payload": _scrub(r["payload"]),
                }
                for r in read_log(run.log_path)
            ]
            said = [asdict(turn) for turn in run.channel.transcript]
            out[pid] = {"events": events, "said": said}
    return out


def main() -> None:
    golden = {"en": record("en"), "hi": record("hi")}
    GOLDEN.write_text(json.dumps(golden, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {GOLDEN}")


if __name__ == "__main__":
    main()
