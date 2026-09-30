# LucidForm

Accessibility-first form assistant. Read `SPEC.md` first — it holds the intent, the
data model, and the gating contract. `METHODOLOGY.md` is the running record of *why*.
This file is working notes plus the project's current state, so a new session can resume.

## Where things stand (updated 2026-09-30)

**What it is.** Shubh's idea and a 5-person VIT Bhopal B.Tech capstone (Shubh Pratap Singh,
Yashvardhan Singh Sarangdevot, Lakshay Gupta, Kanishka Jain, Sanjith). Two jobs: (1) *explain*
KYC form fields — a RAG help agent over official documents; (2) *fill* the form safely — the LLM
proposes, a deterministic gate decides, read-back + explicit "yes" commits. The paper
(`docs/paper-draft.md`) is the deliverable; the whole project is planned at 2–3 months.

**Repo.** https://github.com/ShubhPS/LucidForm — **private**, pushed, CI (GitHub Actions, offline
suite on Ubuntu) green. Default branch `main`. Commits carry **no AI co-author / session trailer**
(user rule). Teammate Yash's separate earlier repo `Sapair-og/Capstone` (Phases 0–1 only, flat
layout) is superseded; we took its graphify + team-workflow docs, then deleted the local clone.

**Stack.** Python 3.13 `.venv` · Gemini `gemini-3.5-flash-lite` (extraction + help answers) ·
`gemini-embedding-001` (768-d) · LangGraph state graph (orchestrator) · BM25 (`rank-bm25`) + dense,
reciprocal rank fusion · pypdf/reportlab (AcroForm) · typer CLI · pytest (489 offline + 4 live) ·
graphify knowledge graph · paper built with docx-js (`tools/paper/`) and exported to PDF via Word.

**Status.** Done: gate + adversarial suites (59 gate / 49 confirmation cases), FormState/receipts,
Gemini client (Anthropic still supported), LangGraph orchestrator, eval harness, RAG help agent,
extended safety test, 8 personas (3 core offline + 5 extended live-only), two live runs, help eval,
paper with live results, demo script, team docs, pre-push audit + 10 code-review fixes.

**Headline numbers (cite these, they are verified).**
- Live run 2 (after the Hindi enum fix): 11 wrong proposals → 8 gate, 3 read-back, **0 committed**;
  gate FPR 0.9%; extraction accuracy 90.7% / 118 proposals; p50/p95 1.04 s / 2.84 s.
- Live run 1: 11 → 10 gate, 1 read-back, 0 committed; FPR 1.8%; 90.8% / 120; p95 32 s (429 back-off).
- Offline core (paper Table II): 6 wrong → 5 gate, 1 read-back, 0 committed.
- Help eval (30 questions + 6 controls): hit@4 28/30, gold-cited 26/28 answers, controls refused 6/6.

**Decisions already made — don't re-litigate.**
- Gemini is the default provider (user's key); model ids are config only.
- LangGraph replaces the plain loop; checkpoint-resume is **not** enabled (restoring FormState from
  a checkpoint would be an unconfirmed write). Resume = replay commit receipts (roadmap phase 15).
- RAG = own pipeline (approach A: embeddings + BM25 + RRF), not Gemini managed File Search.
- The help agent explains; it never supplies a value. Enforced by the safety test.
- Extended personas are live-only (no offline fixtures) so the offline numbers stay pinned.
- Demo = terminal, typed, live Gemini (`docs/demo.md`). No voice/web UI this round.
- ROADMAP owner column intentionally blank — the team claims phases.

**Open items / next.** Team review of the paper · native-speaker review of Hindi prompts + digit
pronunciation · deterministic display-case for text fields (case is inaudible at read-back) ·
question-vs-decline for "pan card nahi hai toh kya karu?" (flip-flops across runs) · real-user study ·
voice with real speech · model-tier sweep · optional `/code-review ultra` (run from *inside*
`LucidForm/` — from the parent folder it reports "no commits") · decide public vs private and add
teammates as collaborators · **rotate the Gemini and Firecrawl keys** (both were pasted in chat).

**Resume a session.** Read `docs/PROGRESS.md` (last entry) and `ROADMAP.md`; `git log --oneline -15`;
`.venv/Scripts/python -m pytest -q` (expect 489 passed). Keys live in `.env` (gitignored):
`GEMINI_API_KEY`, `LUCIDFORM_GEMINI_MODEL`, `FIRECRAWL_API_KEY` (the Firecrawl MCP tool itself is
keyless here and won't use it — Exa `web_fetch` worked for blocked pages).

## Non-negotiables

- **The LLM never writes a form value.** `FormState.commit(candidate, receipt)`
  is the only mutator, and it re-verifies all seven preconditions at the write
  site — including recomputing the fingerprint, so a receipt for value A cannot
  write value B. No `set()`, no `update()`, no "trusted" field, no admin path.
- **The gate imports no LLM.** Nothing under `lucidform/gate/` or
  `lucidform/formstate/` may import a model SDK (`anthropic`, `google.genai`,
  `openai`), an agent framework (`langgraph`, `langchain`), or
  `lucidform.extract` / `.help` / `.llm` / `.orchestrate` -- directly or
  transitively. `tests/test_no_silent_write.py` fails the build if it does.
- **The help agent has no route to the form.** `lucidform/help/` may not import
  `formstate`, `gate` or `orchestrate`, and may not build a `Candidate` or a
  receipt. It explains; the user answers.
- **Receipts are minted in one place.** `ConfirmationReceipt.__post_init__`
  walks the stack and refuses construction from anywhere but
  `orchestrate/confirm.py`. This stops accidents; the AST test stops intent.
- **The event log is append-only.** Never `UPDATE` or delete a row in
  `data/runs/*.jsonl`. It is the eval substrate; rewriting it invalidates results.
- **No real PII.** Every identity is fabricated. Synthetic Aadhaar numbers are
  Verhoeff-valid by construction so the checksum path is exercised — generated,
  never sourced. Every persona/fixture carries a `SYNTHETIC` header.
- **`escaped_errors` must be 0.** A committed value differing from ground truth is
  a build failure, not a finding.

## Gotchas

- `uv` is not installed on this machine. Use `.venv` + `requirements.txt`.
- Affirmation parsing is a **whitelist over the whole utterance**, never a
  substring search. `"yes I know that's wrong"` contains `yes` and must NOT
  commit; so must `"yesterday I gave you the wrong number"`. See the
  `affirmation_spoofing` and `substring_traps` categories in
  `tests/adversarial/affirmation_cases.yaml`.
- `ok` / `acha` are deliberately **not** confirmations — they acknowledge hearing
  the read-back, not agreement. Adding them would convert every back-channel into
  a committed value.
- Aadhaar uses the **Verhoeff** checksum, not Luhn. Luhn silently accepts numbers
  Verhoeff rejects.
- **Never use `\d` or `str.isdigit()` in a validation rule.** Both match
  Devanagari digits — `"३०२०१५".isdigit()` is `True`. A rule built on either
  accepts `३०२०१५` as a PIN code. Every numeric pattern in `gate/rules.py` uses
  an explicit ASCII `[0-9]`. There is a regression test pinning this.
- Normalization **reshapes, never repairs.** Stripping `+91` and spaces from a
  phone number is reshaping. Padding a short Aadhaar, transliterating Devanagari
  digits, or snapping an enum to its nearest option is repairing — it commits a
  value the user never said.
- **Enum options may have declared names** (`enum_names` in the overlay, e.g.
  `Male: [पुरुष, purush]`): exactly the names the Hindi prompt says aloud, matched
  exactly after case-folding. That is reshaping. Adding a synonym the prompt does
  not offer ("mard", "kheti") or any fuzzy match is repairing -- don't. The loader
  refuses a name declared for two options.
- The phone prefix strip only fires when removing it leaves exactly 10 digits,
  so a genuine `91`-prefixed subscriber number keeps its leading 9.
- PAN's 5th character is the surname initial — that is a *cross-field* check
  against the name field, not a format check. It belongs in `crossfield.py`.
- `pypdf` returns AcroForm field names, not labels. Plain-language prompts and
  jargon glosses live in the YAML overlay, keyed by field name.
- **`reader.get_fields()` drops `/MaxLen`.** It collapses to the field level;
  `/MaxLen` lives on the *widget annotation*. A parser built on `get_fields()`
  reports `max_length=None` for every field and silently falls back to whatever
  the overlay asserts — making the PDF decorative. `loader.parse_acroform()`
  walks `page["/Annots"]` instead, and follows `/Parent` because AcroForm
  attributes are inheritable.
- **reportlab's `acroForm.choice()` crashes on `value=""`** (`UnboundLocalError`
  on `lbextras`) — it only supports a non-empty default. Enums are therefore
  rendered as text widgets, which is the right call anyway: a blank KYC template
  must not ship with a pre-selected gender or income band.
- CLI reconfigures stdout to UTF-8. The Windows console's legacy code page turns
  Devanagari into `?` — a garbled Hindi read-back is indistinguishable to the
  user from a wrong value.
- `dataclasses.replace()` on a `ConfirmationReceipt` **raises** — it re-invokes
  the constructor, so the issuer frame-check fires. That is intentional; to build
  a deliberately-inconsistent receipt in a test, allocate with `object.__new__`
  and set fields via `object.__setattr__` (see `forge()` in `test_formstate.py`).
- The receipt's frame check walks the stack until the module name differs from
  `receipt.py`. Do **not** replace it with a fixed `sys._getframe(N)` — a frozen
  dataclass's generated `__init__` runs with the defining module's globals, so a
  fixed depth reports the receipt module as its own caller.
- YAML parses bare `yes`/`no` as booleans. Quote them in the adversarial case
  files, or `utterance: yes` arrives as `True`.
- `pypdf` needs `set_need_appearances_writer(True)` on export, or many viewers
  render filled fields as blank.
- A rejection carries exactly **one** reason code. If two checks fail, the first
  in gate order wins — order is defined in `gate/gate.py` and must stay stable, or
  the results table shifts between runs.

## Conventions

- Every field constraint has an adversarial case that must be rejected. Write the
  case in `tests/adversarial/gate_cases.yaml` *before* the rule that catches it.
  Confirmation cases go in `affirmation_cases.yaml`. Both files need **control
  cases** too — a gate that rejects everything scores perfect recall.
- Timestamps stored UTC, ISO-8601, in the event log. Convert at display time.
- `Candidate` is frozen. If you need a changed value, make a new candidate with a
  new `candidate_id` — mutating one would decouple it from any issued receipt.
- Model ID is config, never hardcoded — the extraction-accuracy sweep across
  model tiers depends on it.
- Comments explain *why*, not what.

## Commands

```bash
.venv/Scripts/python -m pytest                      # offline suite (489), no key, free
.venv/Scripts/python -m pytest -m live              # 4 live Gemini contract tests (costs quota)
.venv/Scripts/python -m pytest tests/test_no_silent_write.py   # the safety test
.venv/Scripts/python -m lucidform.schema.make_form  # regenerate the target PDF (tests do it too)
.venv/Scripts/python -m lucidform.cli schema show
.venv/Scripts/python -m lucidform.cli gate-check --field pan --value ABCDE1234F
.venv/Scripts/python -m lucidform.cli run [--persona p02 --replay] [--export out.pdf]
.venv/Scripts/python -m lucidform.cli help build | help ask -f pan -q "..." [--lang hi] | help eval
.venv/Scripts/python -m lucidform.cli replay --live --extended --runs-dir data/runs_live
.venv/Scripts/python -m lucidform.cli metrics --runs data/runs_live --out data/results/live
.venv/Scripts/python -m lucidform.cli graph          # LangGraph as Mermaid
node tools/paper/build.js                            # paper md -> docs/LucidForm_Paper_Draft.docx
graphify update .                                    # refresh the code graph (free)
```

## Environment

Copy `.env.example` -> `.env`. Nothing is required for the gate or the offline
suite; only extraction, the help agent and `help build` touch the API. Provider is
`LUCIDFORM_EXTRACTION_PROVIDER` (default `gemini`). The Anthropic SDK also resolves an
`ant auth login` profile. Project permissions allowlist is `.claude/settings.local.json`
(gitignored); if prompts keep appearing, the user can Shift+Tab to accept-edits/auto.
No pandoc/LibreOffice/pdftoppm on this machine: build docx with Node (`tools/paper`), export PDF
through Word COM, and render pages with `pypdfium2` to check layout.

## Phase 3 notes

- **`tests/fixtures/extractions.json` is not a recording.** It holds *expected*
  responses derived from persona ground truth. Offline replay verifies the
  pipeline; it cannot measure extraction accuracy (that would be circular).
  Accuracy is a live-model measurement only. Regenerate with
  `python -m lucidform.eval.fixtures`; a test asserts the file is in sync.
- The extractor **never repairs**. "about three lakh" stays `"teen lakh"` and is
  rejected by the gate as ENUM — mapping it to `1-5 Lakh` would be the model
  choosing for the user. Same for occupations described in the user's own words.
- Grounding proves a value is *anchored* to something the user said. It does not
  prove the reading is correct — the gate and read-back cover that. Don't
  overclaim it in the paper.
- Confidence clamping is monotonic downward only. Nothing may raise the model's
  self-reported confidence.
- Anthropic credentials resolve at **request** time, not client construction —
  so an unauthenticated run fails inside `.extract()`, not in `__init__`.

## Phase 4 notes

- The orchestrator makes **no judgements**. It never inspects a value to decide
  if it's acceptable — that's the gate. The gate's own `detail` string is what
  reaches the user; don't re-phrase it in `session.py`.
- Questions do **not** count against `max_attempts` (they have their own
  `max_questions` cap). Charging an explanation request against the retry budget
  penalises exactly the users this project is for.
- `FieldSpec.label` stays English — it's the identifier in the PDF, the logs and
  the results table. `FieldSpec.name(lang)` is what the user *hears*. The
  read-back uses `name()`.
- `PersonaChannel` implements **both** channel protocols — it has to hear the
  read-back to answer it. That's what makes the correction rate a measurement
  rather than a constant.
- When a persona's script runs out the channel returns `None` → field abandoned.
  Never repeat the last utterance; that lets a persona loop forever.
- Placeholder order in `strings_hi.yaml` may legitimately differ from English
  (Hindi puts `{total}` before `{done}`). Tests compare sorted sets, not order.
- **Open Phase 6 question:** should digits in a Hindi session be spoken as Hindi
  or English number words? Many target users read digits in English while
  speaking Hindi. Needs a native-speaker call, not a guess.

## Phase 5 notes

- **A turn is delimited by `FIELD_ASKED`, not by `turn_idx`.** A question doesn't
  advance `turn_idx`, so grouping on it merges a question with the answer that
  followed and hides the question entirely.
- Proposals are compared to ground truth **after** `rules.normalize` — otherwise
  `+91 98123 45607` scores as wrong against `9812345607` and the error rate is
  inflated by punctuation that never reaches the form.
- Accuracy / recall / FPR need a persona. Latency, turns, rejection reasons and
  the correction rate don't. A session with no `persona_id` contributes to the
  second group only — never score it against an assumed answer.
- `metrics` **exits non-zero** if `escaped_errors > 0`. It's a defect, not a
  number to discuss.
- The report auto-prints caveats when every session used a replay client
  (accuracy is circular, latency is dictionary lookups) and when a rate rests on
  <10 wrong proposals. `summary.csv` carries `offline_only` + `clients` so a row
  lifted into a document keeps its provenance.
- The three layers (gate / read-back / escaped) must **sum** to wrong proposals.
  A test asserts it — if they don't, something is double-counted or unaccounted.

## Extraction clients (Gemini)

- `extract/client.py`: `GeminiExtractionClient` sends `response_json_schema=Extraction` and then
  re-validates with Pydantic — a malformed reply raises, it is never coerced. AFC is disabled.
- `make_client()` picks the provider; `lucidform/llm.py` holds the one `make_genai_client()`,
  `with_retries()` (429/5xx + httpx transport errors, honours RetryInfo, capped at 60 s) and
  `json_config()`. Nothing under `gate/`/`formstate/` may import `llm`.
- **A failed model call is an UNCLEAR turn, not a crash**: `Extractor._extract` catches it,
  logs `error` on the extraction event, and the user is asked again (one attempt spent).
  `KeyError` (replay-corpus miss) and `AssertionError` (test double over-call) are re-raised.
- `config.py`: SDK key names are read **without** the `LUCIDFORM_` prefix via `validation_alias`
  (before this fix `.env` keys were silently ignored).

## Orchestrator (LangGraph)

- `orchestrate/graph.py` — 16 nodes, declared `EDGES` + conditional `ROUTES`; `Session.run()` is a
  facade over `SessionGraph`. Nodes are thin wrappers; FormState is held by the runner, never in
  graph state. `RECURSION_LIMIT` is large on purpose (a full form is hundreds of steps).
- **Golden parity**: `tests/fixtures/session_golden.json` was recorded from the pre-LangGraph loop
  (core personas p01–p03, en + hi). Any behaviour change must show up as a reviewed diff:
  `python -m tests.golden_sessions` regenerates it — check `git diff --numstat` is only the change
  you intended (so far: additive `"help": "gloss"` and `"error": null` keys).
- Deliberate change from the old loop: a hang-up at read-back ends the field (old loop re-asked).
- Test: `commit` is reachable only from `confirm` (read off the graph's edges).

## Help agent (RAG)

- `help/corpus.py`: 6 sources in `data/help/sources/`, pinned by SHA-256 in `manifest.json`
  (test-verified). Stored byte-exact via `.gitattributes` (`-text`) — Windows autocrlf once broke
  the hashes in a fresh clone. Two sources came via Exa web fetch (Income Tax 403, UIDAI moved).
- Structural chunks (FAQ Q&A / numbered paragraph) → 557 chunks with citation labels.
- `help/index.py`: Gemini embeddings + BM25, RRF top-4, duplicate passages dropped. Index files in
  `data/help/` (`index.npz` gitignored, rebuild with `help build` ≈5 min — free tier limits tokens
  per minute, so batches are 20 with a 4 s pause). Offline tests use `HashEmbedder` (bag-of-words
  stand-in — tests wiring, not retrieval quality).
- `help/answer.py`: reply schema `{answer, cited_ids, answerable}`; every citation must be a
  retrieved passage, else fall back to the gloss with "not certain". Retrieval itself is inside the
  fallback. The query appends the field's English label (helps terse questions, biases some).
- Offline replays pass **no** helper (gloss only) so goldens stay deterministic; live `run`/`replay`
  load it if the index exists.
- `help/evaluate.py`: numbered golds ("RBI KYC FAQ, Q1") match **exactly**; phrase golds (UIDAI
  questions) by substring. Errored controls are excluded from refusal rate and counted as `errors`.

## Personas and live evaluation

- Core `data/personas/p01–p03` (offline fixtures exist, numbers pinned by tests); extended
  `data/personas/extended/p04–p08` (live-only): Hindi session with Hindi number words (p04),
  self-correction + digit grouping (p05), vague answers + "5/1/87" (p06), embedded prompt injection
  (p07), question-first + Bengaluru/Bangalore (p08). Aadhaars from `synthetic_aadhaar(seed 20260930)`.
- Live logs: `data/runs_live_v1/` (run 1, kept as evidence of the Hindi enum gap) and
  `data/runs_live/` (run 2); tables in `data/results/live_v1/`, `data/results/live/`. Always pass
  `--runs-dir` and `--out` for live work or offline tables get overwritten.
- **Letter case is inaudible**: the simulated user compares read-back character for character, so
  it denies case-only differences a real listener would accept (2 of run 2's 3 read-back catches).
  Don't "fix" the simulator to flatter numbers; the real fix is a display-case rule (roadmap 9b).
- The one live "false positive" is "5/1/87" flagged ambiguous — correct reading, intended re-ask.
- `metrics` counts a `correction` event as a read-back denial only if it has `value_rejected`;
  `FormState.decline()` also emits `correction` (without it) — don't misread those as denials.

## Paper

- Source of truth: `docs/paper-draft.md` (title = option 1 in its preamble; 5 authors). Build:
  `node tools/paper/build.js` → IEEE-style A4 docx (one-column title/authors, two-column body,
  Times New Roman); export PDF via Word COM; preview pages with pypdfium2 into `tools/paper/preview/`
  (gitignored). `Research paper sample.docx` (an unrelated Alzheimer's paper) was only a format
  reference and has been deleted.
- Sections added this round: III-F LangGraph, III-G help agent, IV-B extended personas, IV-E help
  eval, VI results (offline + 2 live runs + help), VII limitations, VIII future work, refs 21–25.
- The draft previously claimed "56 gate cases, eleven categories" — wrong; the real suite is 59/13.
  Recount from `tests/adversarial/*.yaml` before quoting any suite size.

## Repo hygiene (checked in the pre-push audit)

- A fresh clone must pass: `git clone . /tmp/x && cd /tmp/x && pytest` — `tests/conftest.py`
  builds the gitignored blank form PDF; the corpus is byte-exact.
- No secrets in history (`git log -p --all | grep` for the key prefixes before any push).
- The graphify post-commit hook rebuilds `graphify-out/` after every commit, so those three files
  always show as modified — harmless; include them in the next commit.
- `.claude/settings.json` wires graphify PreToolUse hooks; teammates without graphify installed see
  hook errors until they install it (CONTRIBUTING covers it).

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
