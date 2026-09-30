# ISSUES.md — known problems, root causes, and fixes

Living log for humans and AI agents. **Before changing behaviour, read this. After fixing
something, update the entry** (status, fix, tests, commit). New problems get the next ID.

Status: `OPEN` · `IN PROGRESS` · `FIXED` · `WONTFIX`

Source of the first batch: manual live run on 2026-09-30, session log
`data/runs/bfcc50e1a3f9479e9a57b4907f401057.jsonl` (synthetic data).

## Decisions (approved 2026-09-30)
| Decision | Choice |
|---|---|
| Official-form scope | Fill all **mandatory** fields of CKYC sections 1–3, not only the 14 existing ones |
| Email verification | Syntax + DNS domain check (MX/A) + typo suggestion. No OTP |
| Address order | Ask **PIN first**, propose district/state from the India Post directory |
| No PAN | Offer **Form 60** (as the official CKYC form does) instead of leaving it blank |
| Work order | Phase 1 safety → 4 session end → 2 address → 3 email/income → 5 official form |
| Invariant | Every new check stays deterministic (no LLM); every suggestion still needs an explicit "yes" |

## Summary
| ID | Problem | Phase | Status |
|---|---|---|---|
| LF-001 | Can't fill the official CKYC form | 5 | OPEN |
| LF-002 | Weak Aadhaar validation (`999999999999` accepted) | 1 | FIXED |
| LF-003 | PIN / city / state mismatch accepted | 2 | OPEN |
| LF-004 | Email only syntax-checked | 3 | OPEN |
| LF-005 | Income band not derived from a stated amount | 3 | OPEN |
| LF-006 | Session ends with required fields empty, no final review | 4 | OPEN |
| LF-007 | Model silently drops/changes digits; grounding doesn't catch it | 1 | FIXED |
| LF-008 | "I don't have a PAN" skips a required field | 1 | FIXED |
| LF-009 | Near-miss answers (`kerela`, `housewife`) rejected with no suggestion | 3 | OPEN |

---

## LF-001 — Can't fill the official CKYC form
- **Symptom:** Only `data/forms/ckyc_individual.pdf` (synthetic 14-field template) is filled.
  The official form (`docs/reference/CKYC_Individual_Official_AMFI.pdf`, 4 pages, from
  portal.amfiindia.com) stays blank.
- **Root cause:** The official PDF has **0 AcroForm fields** (flat print layout), and the
  schema loader only understands AcroForm widgets. It also asks for fields the template lacks.
- **Fix plan:** Coordinate overlay: a YAML map `field_id -> page, x, y, box-per-char?` and a
  reportlab overlay merged with pypdf onto the official page. Extend the schema with the
  mandatory section 1–3 fields (prefix, first/middle/last name, mother's name, marital
  status, citizenship, residential status, POI type + number, district, state code,
  current-address-same flag, declaration place/date). Template export kept as a fallback.
- **Status:** OPEN

## LF-002 — Weak Aadhaar validation
- **Symptom:** `999999999999` was saved as a valid Aadhaar.
- **Root cause:** Gate checks only length, digits, and Verhoeff. `999999999999` happens
  to pass Verhoeff. UIDAI numbers never start with 0 or 1, and that rule wasn't enforced.
  No rule against placeholder numbers.
- **Fix plan:** In `gate/`: first digit 2–9; reject all-same-digit and straight
  ascending/descending runs. Real existence needs UIDAI OTP (not available), so this is
  documented as a limit.
- **Fix (branch `fix-1-safety`):** Aadhaar's "starts with 2–9" rule already existed. Added
  `rules.is_placeholder_number` / `placeholder_error`: rejects all-same-digit numbers and straight
  runs (±1, wrapping 9→0) with reason `format`. Mobile is deliberately excluded, because operators
  really sell repeated-digit numbers. Real existence still needs UIDAI OTP (out of scope).
- **Tests:** `tests/test_issues_phase1.py` (placeholder cases + valid control + mobile control).
- **Status:** FIXED

## LF-003 — PIN / city / state mismatch accepted
- **Symptom:** City `Kota` (Rajasthan), state `Goa`, PIN `466114` (Madhya Pradesh) all saved.
- **Root cause:** `gate/regions.py` checks only the **first PIN digit** (region 4 = MH, MP,
  CG, Goa). City has no cross-check at all.
- **Fix plan:** Bundle a compact India Post PIN directory (pin -> district, state; from the
  data.gov.in All-India Pincode Directory). Exact PIN->state check; city must match the
  PIN's district/office names (fuzzy), else ask which is right. Reorder: PIN asked before
  city/state, and the district/state is proposed from it and read back for a yes.
- **Status:** OPEN

## LF-004 — Email only syntax-checked
- **Symptom:** `uhauihiuah@hhd.com` accepted.
- **Root cause:** Gate has only a format check.
- **Fix plan:** DNS lookup of the domain (MX, falling back to A). Unresolvable domains are rejected. Offline
  / DNS error → check skipped and logged (never a false reject). Typo suggestions for
  common providers (`gmial.com` -> `gmail.com?`). Mailbox existence is out of scope (needs OTP).
- **Status:** OPEN

## LF-005 — Income band not derived from an amount
- **Symptom:** `1 lakh`, `45 lakh` rejected as "not one of the options".
- **Root cause:** Income is a strict enum. Nothing converts an amount to a band.
- **Fix plan:** Deterministic amount parser (digits, `lakh`/`crore`/`hazaar`, Hindi/English
  number words, decimals) -> rupees -> band (lower bound inclusive). Read back as
  "45 lakh a year falls in Above 25 Lakh. Is that correct?"
- **Status:** OPEN

## LF-006 — Session ends incomplete, no final review
- **Symptom:** PAN, mobile, and income left blank; the program ended and wrote the PDF anyway.
- **Root cause:** After `max_attempts` a field is marked abandoned and the graph moves on.
  `finish`/`close` never revisits open required fields and never shows a summary.
- **Fix plan:** After the last field, loop over unresolved **required** fields ("PAN is still
  missing, do you want to give it now?"). Then read back every committed value; user can
  say "change <field>". Export only after a final explicit yes. If required fields remain
  empty at exit, stamp the PDF **INCOMPLETE**.
- **Status:** OPEN

## LF-007 — Model silently drops/changes digits
- **Symptom:** User typed 13 nines for Aadhaar; the model returned 12 and it was saved.
  Mobile `45555555555` (11 digits) became `4555555555`.
- **Root cause:** `extract/grounding.py` verifies the model's *quote* appears in the
  utterance, but never checks that the *value* agrees with the quote. The quote was
  honest and the value was not.
- **Fix plan:** For digit-bearing fields (aadhaar, pan digits, mobile, pin, dob), compare
  the digit sequence in the value with the digit sequence in the quote (after converting
  English/Hindi number words). Mismatch -> ungrounded -> confidence 0 -> rejected, and the
  user is told what was heard.
- **Fix (branch `fix-1-safety`):** `extract/grounding.py` gained `spoken_digits` (digits,
  English + romanised Hindi digit words, `double`/`triple`; compound words like "twenty"
  make the quote unreadable, so the check skips instead of risking a false reject) and
  `digits_agree`. Aadhaar/mobile/PIN: on a mismatch the candidate uses **the digits the user
  said** (`Grounding.replacement`), so the gate rejects with its normal message ("expected
  exactly 12 characters, got 13"). PAN: a mismatch makes the extraction ungrounded
  (confidence 0, rejected). Mobile country codes (+91/0091/0) are not mismatches.
- **Tests:** `tests/test_issues_phase1.py` (13-nines Aadhaar, 11-digit mobile, +91 control,
  PAN 8006 vs 8206).
- **Status:** FIXED

## LF-008 — "I don't have a PAN" skips a required field
- **Symptom:** PAN declined and left blank.
- **Root cause:** A decline on a required field is treated like a decline on an optional one.
- **Fix plan:** For PAN, a decline offers **Form 60** (explained via the help agent). A yes
  commits `FORM 60` as the PAN field value, and the PAN-surname check is skipped for it.
  Other required fields: the decline is recorded and the field is revisited at the end (LF-006).
- **Fix (branch `fix-1-safety`):** New overlay keys `decline_value` / `decline_offer`
  (`FieldSpec.decline_value`). PAN declares `decline_value: Form 60`. A decline on such a
  field explains Form 60, then sends a `Candidate("Form 60")` through the **normal** path:
  gate (a `decline_alternative` pass, which skips the PAN format and surname rules) → read-back →
  explicit yes → `FormState.commit`. There is no new write path. Graph: `decline --alternative--> gate`;
  the gate node now reads `state["proposed"]` (set by `extract` or `decline`).
- **Tests:** `tests/test_issues_phase1.py` (offer + commit on yes; "no" then a real PAN;
  surname check skipped). `test_declining_a_required_field_is_refused` now uses Aadhaar.
- **Status:** FIXED

## LF-009 — Near-miss answers get no suggestion
- **Symptom:** `kerela` and `housewife` were rejected outright.
- **Root cause:** Enum validation is exact. The model's `alternatives` are logged but unused.
- **Fix plan:** Deterministic synonym table (housewife -> Homemaker, kheti -> Agriculture…)
  plus edit-distance match against the enum, offered as a question ("Did you mean Kerala?").
  Commit only on an explicit yes.
- **Status:** OPEN
