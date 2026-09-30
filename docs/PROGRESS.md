# Progress log

Append-only. Newest entry at the bottom. Each entry: who, phase, done, left, gotchas.

---
### 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5
- **Done:** scaffold, gate + adversarial suites, FormState/receipts/export, extraction, orchestrator,
  eval harness; first offline results (6 wrong proposals → 5 gate, 1 read-back, 0 committed).
- **Gotchas:** see CLAUDE.md "Gotchas" — `/MaxLen` lives on widget annotations; Verhoeff not Luhn;
  never `\d` in a rule (matches Devanagari digits).

---
### 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs
- **Done:**
  - Gemini extraction client (`gemini-3.5-flash-lite`) behind the existing client protocol; live tests
    pass (`pytest -m live`). Fixed: API keys in `.env` were never read (env_prefix bug).
  - Orchestrator rewritten as a LangGraph state machine; byte-identical to the old loop on all
    persona sessions (en + hi golden files). Fixed: hang-up at read-back no longer re-asks.
  - Help agent v1: 557 chunks from 6 pinned official sources, Gemini embeddings + BM25 with RRF,
    cited answers with a deterministic citation check and gloss fallback. CLI: `help build`, `help ask`.
  - Safety test extended to LangGraph/Gemini/help, including a transitive-import check.
  - Team docs: AGENTS.md, ROADMAP.md (5 authors, owners blank), CONTRIBUTING.md, TEAM_GUIDE.md, CI.
- **Left:** Phase 7 live evaluation (more personas, `replay --live`, help eval), Phase 8 paper update.
- **Gotchas:**
  - Free-tier Gemini limits tokens per minute: `help build` embeds in paced batches (~5 min).
  - Offline replays deliberately use the gloss, not the help agent, so goldens stay deterministic.
  - "pan card nahi hai toh kya karu" retrieves PAN-application FAQs rather than RBI FAQ Q5
    (Form 60) — the field label biases the query. Measured in Phase 7 before tuning.
