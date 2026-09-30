# LucidForm — Specification

Read this before changing anything. It holds the intent, the data model, and the
guardrails. `CLAUDE.md` is only working notes; `METHODOLOGY.md` is the running
record of *why* each decision was made.

## 1. Intent

An accessibility-first assistant that helps low-literacy and visually-impaired
users fill government and banking forms (KYC, loan applications, insurance
claims). It explains each field in plain language and fills the form through
conversation.

This repository is the **solo prototype phase** of a 4th-year capstone. Its
output is (a) a small working slice and (b) clean, analyzable eval data for a
paper's results section. Correctness and reproducibility of the numbers outrank
demo polish, always.

## 2. The gating contract — the thesis of the project

**The LLM never writes a value into a form.** There is exactly one code path
that mutates form state, and it is not reachable from the model.

```
  1. Form Parser         AcroForm PDF + YAML overlay -> FieldSpec[]
  2. Orchestrator        asks ONE field at a time, in plain language
  3. Extraction          free text -> Candidate  (typed, frozen, uncommitted)
  4. Validation Gate     deterministic, non-LLM: format / checksum / cross-field
  5. Read-back           states the value back in plain language
  6. Confirmation        explicit "yes" -> ConfirmationReceipt -> commit
```

A value that has not traversed 3 -> 4 -> 5 -> 6 cannot reach the form. There is
no fast path, no "trusted" field, no admin override.

### Three enforcement mechanisms

| # | Kind | Mechanism |
|---|---|---|
| 1 | Structural | `FormState._values` is private. `commit(receipt)` is the only mutator, and it re-verifies the receipt against the candidate before writing. |
| 2 | Capability | `ConfirmationReceipt` requires an issuer sentinel held privately in `orchestrate/confirm.py`. It cannot be minted anywhere else. |
| 3 | Architectural | `tests/test_no_silent_write.py` AST-scans the package and fails the build if any of the above is circumvented. |

Mechanism 3 exists because 1 and 2 rely on nobody adding a shortcut later. The
test is the artefact that makes the safety claim checkable rather than asserted.

### Commit invariant

`FormState.commit(receipt)` writes only if **all** hold:

- `receipt.candidate_fingerprint == sha256(field_id | normalized_value | candidate_id)`
- `receipt.validation.status is Status.PASS`
- `receipt.affirmation.explicit is True`

Any failure raises `SilentWriteBlocked` and emits a `SILENT_WRITE_BLOCKED`
event. A blocked write is a *logged research finding*, not a swallowed error.

## 3. Non-negotiables

- **No real PII, ever.** Every identity, PAN, Aadhaar, and address in this repo
  is fabricated. Aadhaar numbers are Verhoeff-valid by construction so the
  checksum path is exercised; they are generated, never sourced. Every persona
  and fixture file carries a `SYNTHETIC` header.
- **The gate imports no LLM.** `lucidform/gate/` and `lucidform/formstate/` must
  never import `anthropic` or `lucidform.extract`. Enforced by test.
- **The event log is append-only.** Rows are never updated or deleted. The log
  is the eval substrate; rewriting it invalidates the results.
- **`escaped_errors` must be 0.** A committed value that differs from the
  persona's ground truth is a build failure, not a finding to report.
- **Extraction returns data, not instructions.** The model is constrained by a
  structured-output schema to `{value, confidence, span, ambiguous}`. It has no
  channel through which to request a write.

## 4. Data model

| Type | Lives in | Notes |
|---|---|---|
| `FieldSpec` | `models.py` | id, label, plain-language prompt, type, required, constraints, jargon gloss |
| `Candidate` | `models.py` | **frozen**. field_id, raw_utterance, value, confidence, span, candidate_id |
| `ValidationReport` | `models.py` | status, reason code, detail, checks_run — one reason per rejection |
| `Affirmation` | `models.py` | explicit: bool, raw utterance, parse basis |
| `ConfirmationReceipt` | `formstate/receipt.py` | candidate_fingerprint, validation, affirmation, issued_at |
| `FormState` | `formstate/state.py` | private `_values`; `commit()` is the only mutator |

## 5. Rejection taxonomy

Every rejection carries exactly one code. Each becomes a column in the results
table, so the set is closed and additions are deliberate.

| Code | Means | Said to the user as |
|---|---|---|
| `EMPTY` | nothing, or only invisible characters | "I did not catch a value" |
| `TYPE_MISMATCH` | wrong size | "that is the wrong length" |
| `FORMAT` | right size, wrong shape | "that does not look like a PAN" |
| `ENUM` | not one of the permitted options | "please choose one of these" |
| `CHECKSUM` | well-formed but arithmetically impossible | "one digit is wrong" |
| `RANGE` | well-formed but outside the permitted domain | "that date is in the future" |
| `CROSS_FIELD` | contradicts an already-confirmed value | "that does not match your surname" |
| `AMBIGUOUS_EXTRACTION` | extractor reported more than one reading | "I heard two things" |
| `LOW_CONFIDENCE` | extractor was unsure | "could you repeat that" |

### Check order

Fixed, and stable across runs — the reported reason distribution shifts if it
changes. Defined in `gate/gate.py`:

`EMPTY` → `TYPE_MISMATCH` → `FORMAT` → `ENUM` → `CHECKSUM` → `RANGE` →
`CROSS_FIELD` → `AMBIGUOUS_EXTRACTION` → `LOW_CONFIDENCE`

Structural verdicts come first because they are objective and actionable.
Extraction-quality signals come last: a value that is structurally perfect but
which the extractor was unsure of is a different, weaker finding than one that
is malformed, and conflating the two would hide malformed values behind a
confidence complaint.

Enum fields are validated by membership alone — a length check on an enum is
subsumed by the option list, and would report `TYPE_MISMATCH` for a value whose
real problem is that it is not an option.

Normalization runs **before** every check, so `+91 98123 45607` and
`9812345607` are the same value, and the read-back states the normalized form —
the user confirms what will actually be written.

## 6. Scope of this prototype

**In:** one form type (CKYC-equivalent individual KYC, fillable AcroForm);
English + Hindi; text channel; CLI; full eval harness; adversarial gate suite.

**Out:** OCR of scanned forms; multiple form types; open-ended bilingual chat;
voice (Phase 7, behind the channel adapter); web UI (Phase 8, optional).

Deferrals are recorded in `METHODOLOGY.md` with their reasoning. Nothing is
silently descoped.

## 7. Eval outputs

`data/runs/*.jsonl` (append-only events) -> `data/results/*.csv`:

- per-field extraction accuracy vs ground truth (exact + normalized)
- **gate recall** — caught_bad / total_bad
- **gate false-positive rate** — rejected_good / total_good
- read-back correction rate
- latency p50/p95 per stage
- turns-to-commit per field
- `escaped_errors` (must be 0)

Recall without the false-positive rate is not a result: a gate that rejects
everything scores perfect recall and is useless. Both are reported together.
