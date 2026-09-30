# LucidForm

Accessibility-first form assistant. Read `SPEC.md` first — it holds the intent, the
data model, and the gating contract. `METHODOLOGY.md` is the running record of *why*.
This file is only working notes.

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
.venv/Scripts/python -m pytest                      # full suite
.venv/Scripts/python -m pytest tests/test_no_silent_write.py   # the safety test
.venv/Scripts/python -m lucidform.schema.make_form  # regenerate the target PDF
.venv/Scripts/python -m lucidform.cli schema show
.venv/Scripts/python -m lucidform.cli gate-check --field pan --value ABCDE1234F
```

## Environment

Copy `.env.example` -> `.env`. Nothing is required for the gate or the offline
suite; only the extraction layer touches the API. The SDK also resolves an
`ant auth login` profile — run `ant auth status` before assuming a key is needed.

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

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
