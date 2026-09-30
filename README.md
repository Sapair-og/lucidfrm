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

cp .env.example .env    # GEMINI_API_KEY, only needed for live runs
```

## Run

```bash
.venv/Scripts/python -m pytest                                  # full suite (no credentials needed)
.venv/Scripts/python -m pytest -m live                          # live Gemini contract tests
.venv/Scripts/python -m lucidform.cli help build                # embed the official sources (once)
.venv/Scripts/python -m lucidform.cli help ask -f pan -q "pan kya hota hai"
.venv/Scripts/python -m lucidform.cli graph                     # the LangGraph orchestrator as Mermaid
.venv/Scripts/python -m lucidform.schema.make_form              # generate the target PDF
.venv/Scripts/python -m lucidform.cli schema show               # inspect parsed fields
.venv/Scripts/python -m lucidform.cli gate-check -f pan -v ABCDE1234F
.venv/Scripts/python -m lucidform.cli extract -f pan -u "pan kya hota hai" --replay
.venv/Scripts/python -m lucidform.cli run --persona p02 --replay        # whole form, simulated user
.venv/Scripts/python -m lucidform.cli run                               # whole form, you at the keyboard
.venv/Scripts/python -m lucidform.cli replay --fresh                    # all personas, recorded
.venv/Scripts/python -m lucidform.cli metrics                           # logs -> CSV + headline table
```

## Results

**Live** (`gemini-3.5-flash-lite`, 8 synthetic personas incl. a Hindi-only session and an
embedded prompt injection, two runs — logs in `data/runs_live_v1/`, `data/runs_live/`):

| | Run 1 | Run 2 |
|---|---|---|
| wrong values proposed | 11 | 11 |
| rejected by the gate | 10 | 8 |
| denied at read-back | 1 | 3 |
| **committed wrong** | **0** | **0** |
| gate false-positive rate | 1.8% | 0.9% |
| extraction accuracy | 90.8% | 90.7% |

Run 1 exposed a real defect (Hindi option names offered by the prompt, rejected by the gate);
it was fixed with adversarial cases before run 2. **Help agent** (30 questions + 6 controls):
correct passage retrieved 28/30, correct source cited in 26/28 answers, 6/6 controls refused.
Reproduce: `replay --live --extended --runs-dir data/runs_live`, `metrics --runs data/runs_live --out data/results/live`,
`help eval`. The paper is `docs/paper-draft.md` (build: `node tools/paper/build.js`).

**Offline** (core personas, replayed): six wrong values were proposed; all six were stopped.

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

Phases, owners and status live in [`ROADMAP.md`](ROADMAP.md). Done so far: gate, write path,
Gemini extraction, LangGraph orchestrator, eval harness, and the RAG help agent. Team workflow:
[`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/TEAM_GUIDE.md`](docs/TEAM_GUIDE.md); agent handoff:
[`AGENTS.md`](AGENTS.md).

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
