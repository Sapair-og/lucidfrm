# LucidForm — roadmap

Team: Shubh Pratap Singh · Yashvardhan Singh Sarangdevot · Lakshay Gupta · Kanishka Jain · Sanjith.
Claim a phase by writing your name in its **Owner** cell (tiny PR) before starting, so nobody
builds the same thing twice. Each phase lands on its own branch with tests green.

| # | Phase | Depends on | Owner | Branch | Status |
|---|---|---|---|---|---|
| 0 | Scaffold, schema, event log, architecture test, synthetic corpus | — | | main | ✅ done |
| 1 | Validation gate + adversarial suite (56 gate / 49 confirmation cases) | 0 | | main | ✅ done |
| 2 | FormState, receipts, commit invariant, PDF export | 1 | | main | ✅ done |
| 3 | Extraction: Gemini (default) + Anthropic clients, grounding, clamping | 1 | | main | ✅ done |
| 4 | Orchestrator as a LangGraph state machine (golden parity with the old loop) | 2, 3 | | main | ✅ done |
| 5 | Evaluation harness: replay, metrics, layered-defence table | 4 | | main | ✅ done |
| 6 | Help agent v1: RAG over RBI / UIDAI / Income Tax / CERSAI with checked citations | 4 | | main | ✅ done |
| 7 | Live evaluation at scale: more personas, `replay --live`, help-agent eval | 3, 5, 6 | | `phase-7-live-eval` | ⏳ in progress |
| 8 | Paper: live results, help-agent section, figures | 7 | | `phase-8-paper` | ⏳ in progress |
| 9 | Hindi completion: native-speaker review, grammar, translated gate messages, digit words | 4 | | `phase-9-hindi` | ☐ |
| 10 | Voice with real backends (faster-whisper + Piper), identifier round-trip probe | 4 | | `phase-10-voice` | ☐ |
| 11 | Help agent v2: better query formulation, retrieval eval on code-mixed questions | 6, 7 | | `phase-11-help-v2` | ☐ |
| 12 | Ingestion: OCR of scanned/photographed forms into the same field schema | 0 | | `phase-12-ocr` | ☐ |
| 13 | Second form type (e.g. insurance claim) — tests generality of the overlay approach | 1 | | `phase-13-second-form` | ☐ |
| 14 | Accessible web UI behind the channel interface | 4 | | `phase-14-web` | ☐ |
| 15 | Session resume by replaying commit receipts from the event log (never restoring values) | 4 | | `phase-15-resume` | ☐ |

Phases whose dependencies are done can run in parallel.

## Invariants every phase keeps
See `AGENTS.md`. The short version: the LLM never writes a value; `FormState.commit` is the only
write; the gate and write path import no model; the help agent explains and never supplies a value.
