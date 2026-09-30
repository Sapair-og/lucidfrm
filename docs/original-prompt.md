# Prompt for Claude Code — LucidForm Prototype

## Context
I'm building "LucidForm" — an accessibility-first document/form assistant for
low-literacy and visually-impaired users filling government/banking forms
(KYC, loan applications, insurance claims). It explains form fields in plain
language and can fill the form via voice/conversation. This is a solo
prototype phase for a 4th-year CSE capstone; the full version has a 4-person
team, but right now I need a small, working, demoable slice — plus clean
logging/eval so the results feed into a research paper.

## Non-negotiable design constraint
The LLM never writes a value directly into a form field. The pipeline is:

1. **Form Parser** — extract fields, types, and constraints (regex/format,
   required/optional) from a target form once, up front.
2. **Conversation Orchestrator** — asks one field at a time, in plain
   language, explains jargon on request.
3. **Extraction Layer** — turns the user's free-text/voice answer into a
   typed candidate value (never written to the form yet).
4. **Validation Gate (deterministic, non-LLM)** — checks format/checksum/
   cross-field consistency on the candidate value.
5. **Read-back + Confirmation** — the system states the value back to the
   user in plain language; only on explicit "yes" does it commit to the
   form. No silent writes, ever, under any code path.

This gating is the actual thesis of the project — treat it as the thing to
protect, not boilerplate to skip for speed.

## Scope for THIS prototype (deliberately small)
- **One form type only** — a single publicly available blank template (e.g.
  a standard bank KYC form or a simple insurance claim form as PDF).
- **One language pair** — English + one Indian regional language (your
  choice of what has decent open ASR/TTS support — tell me what you pick
  and why before building).
- **Voice input can start as text input** if voice integration eats too
  much time early — flag this trade-off to me rather than silently
  descoping it.
- **All data is synthetic.** Never use or request real PII, real filled
  forms, or real identity documents. Generate fake identities/values for
  testing and say so explicitly in code comments and docs.

## What I need from you, in order
1. **Propose an architecture + stack** (FastAPI vs. alternatives, PDF/OCR
   parsing library, ASR/TTS options, which LLM API, how state/session is
   stored) and explain trade-offs briefly. Wait for my sign-off before
   scaffolding anything.
2. **Scaffold the project** with the 5-stage pipeline above as clearly
   separated modules/services — I want to be able to point at the
   validation gate in code and say "this is why it's safe," not have it
   tangled into a monolith.
3. **Build incrementally**, one stage at a time, with a way for me to test
   each stage in isolation (e.g., feed the validation gate fake extraction
   output directly) before wiring the full pipeline together.
4. **Build an eval/logging harness from the start**, not bolted on later.
   For every session, log: field-by-field extraction accuracy, how often
   the validation gate caught a bad value, how often a user had to correct
   a read-back, latency per field, and any case where a bad value could
   have slipped through. This is the data the paper's results section
   will be built from — structure it as clean, analyzable output (CSV/JSON)
   from day one.
5. **Write an adversarial test set** for the validation gate specifically —
   try to construct extraction outputs that should be rejected, and confirm
   they are. This is the evidence for the safety claim.
6. **Document methodology as you go** — a running `METHODOLOGY.md` noting
   design decisions and why, in language I can lift into a paper's methods
   section later. Don't wait until the end to write this.

## How I want you to work with me
- Think out loud about trade-offs before writing code, especially anywhere
  a shortcut could quietly reintroduce a silent-write risk.
- Flag scope creep — if something in this prompt looks bigger than a
  prototype should attempt, say so and propose the cut version.
- If a form-parsing or ASR/TTS choice has known weaknesses (e.g., poor
  accuracy for a given language/accent), tell me plainly rather than
  picking the option that looks best in a demo.
- Prioritize correctness and reproducibility of the eval numbers over
  visual polish of the demo.
