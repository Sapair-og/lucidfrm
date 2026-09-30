# AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate

Read this file, then `ROADMAP.md`, then `docs/ISSUES.md` (known problems + fixes), then the last two entries of `docs/PROGRESS.md`.
If `graphify-out/GRAPH_REPORT.md` exists, prefer `graphify query "<question>"` /
`graphify explain "<Symbol>"` over opening files. Design intent lives in `SPEC.md`;
the reasoning behind each decision in `METHODOLOGY.md`; the paper in `docs/paper-draft.md`.

## What this is
LucidForm fills Indian KYC-style forms for low-literacy and visually-impaired users by
conversation, and answers their questions about the form from official documents.

**Core rule: the LLM never writes a value into the form.**
```
Parser → LangGraph orchestrator → Extraction (Gemini) → [VALIDATION GATE] → Read-back → Confirm → Commit
                                 ↘ question → Help agent (RAG over RBI/UIDAI/Income Tax/CERSAI) → explanation only
```

## Code map
| Path | Role |
|---|---|
| `lucidform/schema/` | AcroForm parser + human-authored YAML overlay → `FieldSpec` |
| `lucidform/orchestrate/graph.py` | the conversation as a LangGraph state machine |
| `lucidform/orchestrate/session.py` | `Session` API; holds the collaborators |
| `lucidform/orchestrate/confirm.py` | whole-utterance affirmation whitelist; the **only** receipt issuer |
| `lucidform/extract/` | schema-bounded extraction (Gemini default, Anthropic optional), grounding, clamping |
| `lucidform/gate/` | deterministic validator: 9 checks, fixed order, one reason per rejection |
| `lucidform/formstate/` | `FormState.commit` = the **only** write path; re-verifies receipt + fingerprint |
| `lucidform/help/` | RAG help agent: corpus chunking, hybrid index, cited answers with a citation check |
| `lucidform/eval/` | append-only event log, persona replay, metrics |
| `tests/test_no_silent_write.py` | the architectural safety test |

## Invariants — never break these (the test suite enforces them)
1. `FormState.commit(candidate, receipt)` is the only mutator. No setter, no admin path.
2. `gate/` and `formstate/` import no model SDK, agent framework, or `extract`/`help`/`llm`/`orchestrate`, even transitively.
3. `ConfirmationReceipt` is constructed only in `orchestrate/confirm.py`.
4. `help/` has no route to the form: no `formstate`/`gate`/`orchestrate` import, no `Candidate`.
5. Every gate rule has adversarial cases **and** an accepting control case.
6. Gate recall is never reported without its false-positive rate. Offline replay never yields an accuracy number.
7. All personal data is synthetic.

## Run
```bash
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python -m pytest              # offline, no key needed
.venv/Scripts/python -m pytest -m live      # calls Gemini; needs GEMINI_API_KEY in .env
```

## Working rules for agents
- One branch per phase (`phase-N-<slug>`), PR into `main`; never push to `main` directly.
- Before ending a session, append to `docs/PROGRESS.md`: who, phase, done, left, gotchas.
- Keep `pytest` green, especially `tests/test_no_silent_write.py` and `tests/test_graph.py`.
- Commits carry no AI co-author line.
