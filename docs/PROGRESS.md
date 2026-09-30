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

---
### 2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper
- **Done:**
  - 5 extended live-only personas (p04–p08); `replay --live --extended --runs-dir`.
  - Live run 1 (8 personas): 11 wrong → 10 gate, 1 read-back, 0 committed. Exposed Hindi enum
    gap ("purush" rejected) → fixed with overlay `enum_names` + 8 adversarial cases.
  - Live run 2: 11 wrong → 8 gate, 3 read-back, 0 committed; FPR 0.9%; accuracy 90.7%; p95 2.84 s.
  - Help eval (30 + 6 controls): hit@4 93.3%, gold-cite 92.9%, controls refused 100%.
  - Paper updated (abstract, §I, §III-F/G, §IV-B/E, §VI, §VII, §VIII, refs 21–25) and built to
    IEEE-layout docx + pdf (`node tools/paper/build.js`, PDF via Word). `docs/demo.md` written.
  - Corrected a stale claim: the gate suite was 51 cases / 12 categories, not "56 / 11"; now 59 / 13.
- **Left:** team review of the paper; Hindi native-speaker review; display-case rule; question-vs-decline;
  real-user study; voice with real speech.
- **Gotchas:**
  - Letter case is inaudible: 2 of 4 read-back catches were case-only; the simulator is stricter than a listener.
  - The one live "false positive" is "5/1/87" flagged ambiguous (correct reading, intended re-ask).
  - Run-to-run nondeterminism: "pan card nahi hai toh kya karu?" was a decline once, a question once.
  - Free tier: `help build` ~5 min (paced); live run of 8 personas ~30 min.
