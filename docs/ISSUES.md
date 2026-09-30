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
| Reshape vs repair | CLAUDE.md forbids *normalization* from repairing (snapping enums, mapping "teen lakh" to a band). LF-005/LF-009 don't change that: normalization is untouched. Instead deterministic code **proposes** a value, which is read back and committed only on an explicit yes. The user decides, not the system or the model |

## Summary
| ID | Problem | Phase | Status |
|---|---|---|---|
| LF-001 | Can't fill the official CKYC form | 5 | FIXED |
| LF-002 | Weak Aadhaar validation (`999999999999` accepted) | 1 | FIXED |
| LF-003 | PIN / city / state mismatch accepted | 2 | FIXED |
| LF-004 | Email only syntax-checked | 3 | FIXED |
| LF-005 | Income band not derived from a stated amount | 3 | FIXED |
| LF-006 | Session ends with required fields empty, no final review | 4 | FIXED |
| LF-007 | Model silently drops/changes digits; grounding doesn't catch it | 1 | FIXED |
| LF-008 | "I don't have a PAN" skips a required field | 1 | FIXED |
| LF-009 | Near-miss answers (`kerela`, `housewife`) rejected with no suggestion | 3 | FIXED |
| LF-010 | A valid option the model was unsure of ("voter card") is re-asked blindly | 5 | FIXED |
| LF-011 | Follow-ups found while fixing the above | — | OPEN |
| LF-012 | User has a PAN/Aadhaar but can't find the number; no guidance | 6 | FIXED |

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
- **Fix (branch `fix-5-official-form`):**
  - The official PDF is committed at `data/forms/official/ckyc_individual_amfi.pdf` (source:
    portal.amfiindia.com/spages/ckyc-kra-kyc-formforindividuals.pdf).
  - `lucidform/schema/ckyc_official.yaml`: 28 fields for sections 1–4 + declaration place.
    `inherit: <id>` pulls a field from `ckyc_form.yaml`, so prompts and rules stay in one place.
    New overlay keys: `ask_if` (conditional fields: `poi_number` only for Passport/Voter
    ID/DL/NREGA/NPR, `poi_expiry` only for Passport/DL, the `cur_*` current-address block only
    if `same_address: No`) and `date_future` (expiry must be after today).
    `FieldSpec.applies(values)` is the single test used by the graph, review, result and writer.
  - `loader.load_official()` builds the schema from the overlay alone (no AcroForm).
  - `tools/build_official_layout.py` measures every printed box from the PDF's vector lines
    (pdfplumber, dev-only) → `lucidform/schema/ckyc_official_layout.yaml` (cells as [x0,x1]).
    Tick boxes, state codes (the form's own page-4 list: OR, TS, UA…) and deemed-PoA codes are
    in the same file.
  - `formstate/official_writer.export_official`: reportlab overlay merged onto a copy of the
    4-page form. One character per box, BLOCK letters (email keeps its case), and anything too
    long is shrunk across the span, never truncated. Presentation only: name split
    first/middle/last, address wrapped 49/49/30, DD-MM-YYYY, state → code. The only
    constants are Application Type New, Account Type Normal, country IN, and today's
    declaration date. Values whose field no longer applies are not printed.
  - Cross-field: the PIN/city/state checks take an address prefix (`cur_*` is checked against its own
    PIN). Passport `^[A-Z][0-9]{7}$` and Voter ID `^[A-Z]{3}[0-9]{7}$` are checked against the chosen
    type. DL/NREGA/NPR are length-only because formats vary by state.
  - Proposals: district and state from the PIN (and `cur_*` from `cur_pin`), and place of signing from city.
  - Graph: skips fields that don't apply. The end revisit now covers fields that start to apply
    after a change at the review (each field revisited at most once).
  - CLI: `run --form official`. The `lucidform` launcher now fills the official form.
- **Verified live (2026-10-01):** a full Gemini session → 20 answers, approved, clean PDF.
  Pages were rendered and checked by eye; tests assert the positions of drawn text.
- **Tests:** `tests/test_issues_phase5.py`.
- **Status:** FIXED

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
- **Fix (branch `fix-2-address`):**
  - Data: `lucidform/gate/data/pin_directory.json` (18,719 PINs → state + district; 23,904
    place names → states, from districts and head/sub post offices only, because village branch
    offices would add false matches). Rebuild: `python tools/build_pin_directory.py <csv>`.
    Source CSV: India Post All-India Pincode Directory, mirrored at
    github.com/saravanakumargn/All-India-Pincode-Directory. It is older than some renames, so
    `regions.CITY_ALIASES` maps Bengaluru→Bangalore, Mumbai→Bombay, etc.
  - `regions.pin_place`, `city_states`, and `pin_matches_state` (exact via the directory; a PIN not in
    the directory falls back to the old first-digit region check, so a stale directory never
    rejects a real PIN).
  - `crossfield.py`: `pin` (vs state, then vs city), new `state` (vs PIN and city) and `city`
    (vs PIN or state) checks. **A city is rejected only if the directory knows it and in no
    matching state.** An unknown city or locality (e.g. Rawatbhata) always passes.
  - Order: `address_line, pin, city, state`. The state is **proposed** from the confirmed PIN
    (`regions.propose`, graph node `propose`: budget → propose → gate → read-back → yes).
    A "no" falls through to the normal question.
  - Persona p02's deliberate mis-hearing changed from Kolhapur to **Kollam** (same state as
    its PIN), because the gate now catches Kolhapur and the fixture exists to show an error
    only the read-back can catch. Offline Table II numbers unchanged (tests pinned).
  - Golden sessions re-recorded. Every persona commits identical values, with one fewer turn
    (state accepted with "yes").
- **Tests:** `tests/test_issues_phase2.py` (Kota/Goa/466114, unknown-city control, renamed
  city, directory miss fallback, state proposal needs yes).
- **Status:** FIXED

## LF-004 — Email only syntax-checked
- **Symptom:** `uhauihiuah@hhd.com` accepted.
- **Root cause:** Gate has only a format check.
- **Fix plan:** DNS lookup of the domain (MX, falling back to A). Unresolvable domains are rejected. Offline
  / DNS error → check skipped and logged (never a false reject). Typo suggestions for
  common providers (`gmial.com` -> `gmail.com?`). Mailbox existence is out of scope (needs OTP).
- **Fix (branch `fix-3-email-income`):**
  - `gate/suggest.email_typo`: a domain within 0.85 similarity of a common provider
    (gmail.com, yahoo.co.in, rediffmail.com…) is rejected (`format`) and the corrected
    address is **offered** (read back, needs yes).
  - Domain check: `ValidationGate(domain_check=...)` is injected because the gate reads no network.
    `lucidform/netcheck.email_domain_ok` requires an **MX record** (dnspython). NXDOMAIN or no MX →
    reject ("does not receive email"). Timeout/DNS failure → skipped, never rejected.
    `hhd.com` has a website but no MX, so it's rejected. Only the live interactive `run` injects it;
    persona replays keep their synthetic `example.invalid` domains and record the check as skipped.
  - `dnspython>=2.6` added to requirements.txt.
- **Limit:** mailbox existence needs an OTP email (out of scope, decided 2026-09-30).
- **Tests:** `tests/test_issues_phase3.py` (typo, no-MX reject, lookup failure passes, offline skip).
- **Status:** FIXED

## LF-005 — Income band not derived from an amount
- **Symptom:** `1 lakh`, `45 lakh` rejected as "not one of the options".
- **Root cause:** Income is a strict enum. Nothing converts an amount to a band.
- **Fix plan:** Deterministic amount parser (digits, `lakh`/`crore`/`hazaar`, Hindi/English
  number words, decimals) -> rupees -> band (lower bound inclusive). Read back as
  "45 lakh a year falls in Above 25 Lakh. Is that correct?"
- **Fix (branch `fix-3-email-income`):** `gate/suggest.parse_amount` / `amount_band` (plain code):
  digits with Indian grouping, decimals, English/Hindi number words, scales
  (hundred/sau, thousand/hazaar/k, lakh/lac, crore/cr), and monthly → ×12 ("30 hazaar mahina").
  A bare number word or a figure under 1,000 without a scale is not an amount (so "I **do** not
  know" is not 2). Two numbers ("5 or 6 lakh") → no offer. Bands: upper bound inclusive
  (1 lakh → 1-5 Lakh, 25 lakh → 10-25 Lakh, 45 lakh → Above 25 Lakh). Overlay flag
  `amount_bands: true` on `income_band`. The gate still rejects the raw amount (`enum`) and
  **offers** the band; it's saved only on yes.
- **Tests:** `tests/test_issues_phase3.py`.
- **Status:** FIXED

## LF-006 — Session ends incomplete, no final review
- **Symptom:** PAN, mobile, and income left blank; the program ended and wrote the PDF anyway.
- **Root cause:** After `max_attempts` a field is marked abandoned and the graph moves on.
  `finish`/`close` never revisits open required fields and never shows a summary.
- **Fix plan:** After the last field, loop over unresolved **required** fields ("PAN is still
  missing, do you want to give it now?"). Then read back every committed value; user can
  say "change <field>". Export only after a final explicit yes. If required fields remain
  empty at exit, stamp the PDF **INCOMPLETE**.
- **Fix (branch `fix-4-session-end`):** New graph nodes `wrap_up` → `review` → `listen_review`
  (`orchestrate/graph.py`); `next_field` now walks a `queue` of schema indices.
  1. **Revisit:** after the first pass, every unresolved field is queued once more
     ("Before we finish, let us go back to what is still missing: …").
  2. **Review:** every committed value is read back (spoken form); missing ones are listed.
     `Purpose.REVIEW` listen. An explicit yes (same whole-utterance whitelist as
     confirmation) sets `SessionResult.approved`. "change <field>" is resolved by
     `field_named()` against the overlay's new `aliases` (whole phrase, longest wins; no guess
     → "did not understand"), and that field is re-asked with `correcting=True`. A new commit
     replaces the old value through the normal receipt path. Bounded by `Session.max_reviews` (5).
  3. **Hang-up:** a `None` from the channel sets `gone`; there's no revisit or review with nobody there.
  4. **Export:** `writer.export(..., stamp=)` watermarks `INCOMPLETE` (required fields missing)
     or `NOT CONFIRMED BY APPLICANT` (no final yes). The CLI prints `approved yes/no`.
  - Revisited/corrected fields replace their earlier `FieldResult`, with counters summed.
  - `PersonaChannel` answers the review with "yes" (each value was already checked against
    ground truth at its own read-back).
  - Golden sessions re-recorded. Verified the event stream is identical to the old golden up to
    the new tail (`readback` summary + review `user_utterance`) for p01–p03, en + hi.
- **Tests:** `tests/test_issues_phase4.py`; `test_session.py` updated (question cap is per
  visit; the summary event is logged; the out-of-attempts test supplies replies for the revisit).
- **Status:** FIXED

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
- **Fix (branch `fix-3-email-income`):** `ValidationReport.suggestion` (only on a rejection, never
  on a pass). `gate/suggest.suggest`: (1) overlay `suggest_names` (human-written, e.g.
  housewife→Homemaker, kheti→Agriculture, company→Salaried), matched as a whole phrase;
  (2) `difflib` closest option at ≥0.8 with a unique best (kerela→Kerala). Graph: `gate
  --suggest--> gate` with the offered `Candidate`, then read-back → yes. There's at most one offer per
  utterance (`suggested` flag), and a denied offer is a normal attempt.
  - `suggest_names` ≠ `enum_names`: enum_names *are* the option (accepted silently, reshaping);
    suggest_names are only *offered*. Don't move entries between them.
  - Metrics: the first `validation` in a turn is the gate's verdict on the model; a later one
    is the offer (`Turn.offered`) and only updates the committable value. State proposals
    (LF-003) now emit their own `field_asked`, so they're separate turns.
  - Golden sessions re-recorded. Identical commits; p01/p03 own-words occupation/income
    now resolve via the offer (two fewer turns each).
- **Tests:** `tests/test_issues_phase3.py`.
- **Status:** FIXED

## LF-010 — A valid option the model was unsure of is re-asked blindly
- **Symptom (live, 2026-10-01):** "voter card" for proof of identity was rejected: "the utterance
  had more than one reading".
- **Root cause:** "voter card" is a declared `enum_name` of Voter ID, so every structural check
  passed. But Gemini marked its own reading ambiguous (confidence 0.4), and the gate's
  AMBIGUOUS_EXTRACTION check rejected it with nothing to offer.
- **Fix (branch `fix-5-official-form`):** for an **enum** field whose normalized value is exactly an
  option, a rejection for AMBIGUOUS_EXTRACTION or LOW_CONFIDENCE offers that option
  (read back, explicit yes). Other types, e.g. an ambiguous "5/1/87" date, are still re-asked.
- **Tests:** `tests/test_issues_phase5.py`.
- **Status:** FIXED

## LF-011 — Follow-ups (open)
- Document numbers (`poi_number`, type text) are read back as a word, not spelled out
  character by character like PAN/Aadhaar. Add a spell-out flag in the overlay.
- The Hindi strings added in LF-003..LF-001 (proposal, suggestion, review, the new official-form
  prompts) need a native-speaker review, as `CLAUDE.md` already notes for older prompts.
- The official form marks Email as mandatory. Here it stays optional (inherited), because
  many target users have none.
- Citizenship "Other" ticks the box, but the country name/code is not asked yet.
- The official form doesn't take the Aadhaar number (only "proof of possession", masked),
  so the official flow doesn't ask it. The template form still does.
- The PIN directory predates 2020 and omits NE states and some UTs. Their PINs fall back to
  the region check (LF-003).
- Paper/README numbers: offline Table II is unchanged, but live figures predate these fixes
  and should be re-measured (`replay --live`).

## LF-012 — "I have a PAN but can't find the number" gets no guidance
- **Symptom (requested 2026-10-01):** the help agent explains *what* a PAN is, but a user who has
  one and doesn't know the number got no way to find it. Worse, "I don't have the number" could be
  classified as a decline, which offers Form 60 to someone who has a PAN.
- **Fix (branch `fix-6-find-help`):**
  - New extraction intent `find` (`extract/schema.py`, prompt rule): has the document but doesn't
    know or can't find the number, or asks how to find or download it. It's distinct from `decline`
    and `question`.
  - Overlay key `find_help` (en/hi), human-written, **official links only**, checked reachable on
    2026-10-01: PAN via DigiLocker ("PAN Verification Record"), incometax.gov.in → Instant e-PAN →
    Check Status/Download PAN (Aadhaar + OTP), or old ITR/Form 16/passbook. Aadhaar via
    myaadhaar.uidai.gov.in/retrieve-eid-uid, mAadhaar/DigiLocker, or helpline 1947. The NSDL e-PAN
    page timed out and was left out.
  - Video help is a **YouTube search link**, not a specific video: a single video can't be vetted
    for accuracy or availability over time, and the search always works.
  - Graph: `extract --find--> find_help --> budget`. It speaks the guide, logs `jargon_explained`
    with `help: find`, and asks again. It shares the `max_questions` budget (help isn't a failed
    attempt). A field without `find_help` falls back to the normal explanation. The PAN `decline_offer`
    now tells people with a PAN to say "I can't find it".
  - Metrics count `find` turns as help requests, like questions.
- **Verified live:** Gemini returned `find` for "mere paas pan hai par number yaad nahi",
  "I have a PAN card but I lost it" and "pan number kaise pata karu"; `decline` for "I don't have
  a PAN"; `question` for "pan kya hota hai".
- **Limit:** links are read out as text. For a voice-only user they should also be sent by
  SMS/WhatsApp (future work). The Hindi text needs native review (LF-011).
- **Tests:** `tests/test_issues_phase6.py`.
- **Status:** FIXED
