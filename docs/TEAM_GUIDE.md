# Team guide

Read once. After that, `CONTRIBUTING.md` is the command reference.

## 1. The idea in 60 seconds
LucidForm helps people who can't easily read a form fill in a KYC form by talking, and answers
their questions about it ("PAN kya hota hai?", "Aadhaar dena zaroori hai?") from official RBI,
UIDAI, Income Tax and CERSAI documents, with the source named.

The thing the paper is about: **the AI never writes into the form.** It proposes a value; a plain,
non-AI checker validates it (format, Aadhaar checksum, PAN-vs-surname, PIN-vs-state); the value is
read back; it is saved only when the user clearly says "yes". Three separate mechanisms make it
impossible for code to skip those steps, and the test suite proves each one catches a violation.
The help agent follows the same rule: it explains, it never supplies a value.

```
PDF form → LangGraph orchestrator → Gemini extraction → [VALIDATION GATE] → read-back → "yes" → commit → filled PDF
                                  ↘ question → help agent (RAG) → cited explanation
```

## 2. Who does what
Phases and their status are in `ROADMAP.md`. Owners are blank on purpose — claim one by putting
your name in its row. Phases whose dependencies are done can run in parallel; if you finish
early, add test cases or personas for someone else's phase rather than starting a new one alone.

## 3. Setup
See `CONTRIBUTING.md` → One-time setup. You need Git, Python 3.11+, and an AI coding assistant
that can work in the repo (Claude Code, Codex, Cursor…). A Gemini API key is needed only for live
runs; the whole test suite runs offline.

## 4. The loop for every phase
Branch → work in small commits → `pytest` green → append to `docs/PROGRESS.md` → push → PR →
someone else reviews (skim + run the tests) and merges.

## 5. Saving tokens with graphify
Every new AI session starts blind and burns tokens re-reading files. graphify turns the repo into a
knowledge graph once; after that the AI asks the graph small questions instead.

```bash
graphify update .                                   # refresh after code changes (free, seconds)
graphify query "how does a value get committed to the form?"
graphify explain "FormState"
graphify path "Candidate" "ConfirmationReceipt"
```
Only `graphify-out/graph.json`, `GRAPH_REPORT.md` and `manifest.json` are committed.

**Starter prompt** for every AI session:
```text
You're working on LucidForm, phase <N> (<name>), branch phase-<N>-<slug>.
Read AGENTS.md, the last two entries of docs/PROGRESS.md, and graphify-out/GRAPH_REPORT.md.
Use `graphify query` / `graphify explain` before opening source files.
Keep pytest green (especially tests/test_no_silent_write.py and tests/test_graph.py).
Plan the phase in small steps, show me the plan, then do step 1.
At the end: append to docs/PROGRESS.md, commit, and push the branch.
```

## 6. Rules nobody (human or AI) breaks
1. The LLM never writes a value. Only `FormState.commit()` writes, and it re-checks everything.
2. `gate/` and `formstate/` never import any AI library or the extraction/help/orchestrator code.
3. The help agent never supplies a value — explanation only, with a checked citation.
4. Every new gate rule gets adversarial cases in `tests/adversarial/gate_cases.yaml`, including one that must be accepted.
5. All names and ID numbers are fake. Never put a real Aadhaar/PAN anywhere.
