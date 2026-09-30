# LucidForm

An accessibility-first assistant for filling government and banking forms (KYC,
loan applications, insurance claims) by conversation — built for low-literacy and
visually-impaired users.

**The design claim:** the language model never writes a value into the form. It
interprets; a deterministic validator decides; the user confirms; only then is a
value committed. See [`SPEC.md`](SPEC.md) §2 for the contract and
[`METHODOLOGY.md`](METHODOLOGY.md) for the reasoning.

> **All data in this repository is synthetic.** Every identity, PAN, Aadhaar
> number, address, and phone number is fabricated. No real personal data, filled
> form, or identity document is used anywhere in this project.

## The pipeline

```
AcroForm PDF ──▶ Parser ──▶ Orchestrator ──▶ Extraction ──▶ [ VALIDATION GATE ] ──▶ Read-back ──▶ Confirm ──▶ commit
                                             (LLM)          (deterministic,          (plain      (explicit
                                                             no LLM)                  language)   "yes" only)
```

A value that has not traversed every stage cannot reach the form. Enforced three
ways — a private single write path, a capability-guarded receipt, and a static
analysis test that fails the build if either is circumvented.

## Setup

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # Windows
# .venv/bin/pip install -r requirements.txt     # POSIX

cp .env.example .env    # only needed for the extraction layer
```

## Run

```bash
.venv/Scripts/python -m pytest                                  # full suite (no credentials needed)
.venv/Scripts/python -m lucidform.schema.make_form              # generate the target PDF
.venv/Scripts/python -m lucidform.cli schema show               # inspect parsed fields
.venv/Scripts/python -m lucidform.cli gate-check -f pan -v ABCDE1234F
.venv/Scripts/python -m lucidform.cli extract -f pan -u "pan kya hota hai" --replay
.venv/Scripts/python -m lucidform.cli run --persona p02 --replay        # whole form, simulated user
.venv/Scripts/python -m lucidform.cli run                               # whole form, you at the keyboard
.venv/Scripts/python -m lucidform.cli replay --fresh                    # all personas, recorded
.venv/Scripts/python -m lucidform.cli metrics                           # logs -> CSV + headline table
```

## First results

Three synthetic sessions, offline. Six wrong values were proposed; all six were
stopped.

| where a wrong value was stopped | count |
|---|---|
| rejected by the validation gate | 5 |
| denied at read-back — the gate could not, the value was valid | 1 |
| **committed wrong** | **0** |

The gate rejected no correct value (false-positive rate 0%). The sixth error was
a city name misrecognised as a different real city: right type, right length,
consistent with every other field. Nothing deterministic could reject it. That
is what the read-back is for.

Gate recall alone was 83%; the layered system stopped everything — which is the
result the architecture exists to produce.

> Extraction accuracy and latency from an offline run are **not** measurements —
> the corpus is derived from the same ground truth they'd be scored against. The
> report says so in its own output. Run `metrics` after `replay --live` for those.

Every stage is runnable in isolation. `gate-check` feeds the gate a hand-written
candidate with no model, no session and no form; `extract --replay` runs the
extraction layer against the offline corpus and prints the three judgements —
what the model proposed, what the deterministic checks made of it, and what the
gate decided — separately, because the design turns on them being separate.

## Status

| Phase | | |
|---|---|---|
| 0 | Scaffold, schema, event log, architecture test, synthetic corpus | **done** |
| 1 | Validation gate + adversarial suite | **done** |
| 2 | FormState, receipts, commit invariant, export | **done** |
| 3 | Extraction layer | **done** |
| 4 | Orchestrator — full text pipeline | **done** |
| 5 | Eval harness and first results | **done** |
| 6 | Hindi | next |
| 7 | Voice channel (faster-whisper + Piper) | |
| 8 | Accessible web UI (optional) | |

## Layout

| Path | |
|---|---|
| `lucidform/gate/` | The deterministic validator. Imports no LLM, ever. |
| `lucidform/formstate/` | The single write path and its receipt machinery. |
| `lucidform/extract/` | Model-facing extraction, constrained to structured output. |
| `tests/fixtures/extractions.json` | Offline corpus. Expected responses, **not** recordings — see `eval/fixtures.py`. |
| `lucidform/orchestrate/` | Conversation, read-back, confirmation. |
| `lucidform/channels/` | Console and simulated-user channels. Voice slots in here in Phase 7. |
| `lucidform/eval/` | Append-only event log, metrics, replay driver. |
| `tests/adversarial/gate_cases.yaml` | Inputs the gate must reject, by category, with the reason each must carry. |
| `tests/adversarial/affirmation_cases.yaml` | Utterances that must **not** count as consent. |
| `tests/test_no_silent_write.py` | The static-analysis safety test. |
| `docs/original-prompt.md` | The original project brief. |

Capstone prototype — 4th-year B.Tech CSE.
