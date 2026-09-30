# Title (pick one, or tell me to try again)

1. **LucidForm: A Deterministically Gated Architecture for Safe LLM-Assisted Form Filling** *(default used below)*
2. Never Let the Model Write: A Confirm-Before-Commit Architecture for Accessible Form Completion
3. Gating the Write Path: An Auditable LLM Pipeline for Low-Literacy and Visually-Impaired Users

---

Shubh Pratap Singh
School of Computer Science and Engineering
VIT Bhopal University
Sehore – 466114, India
shubh.23bce10910@vitbhopal.ac.in

Yashvardhan Singh Sarangdevot
School of Computer Science and Engineering
VIT Bhopal University
Sehore – 466114, India
yashvardhan.23bce10849@vitbhopal.ac.in

Lakshay Gupta
School of Computer Science and Engineering
VIT Bhopal University
Sehore – 466114, India
lakshay.23bce10957@vitbhopal.ac.in

Kanishka Jain
School of Computer Science and Engineering
VIT Bhopal University
Sehore – 466114, India
kanishka.23bce10457@vitbhopal.ac.in

Sanjith
School of Computer Science and Engineering
VIT Bhopal University
Sehore – 466114, India
sanjith.23bce11149@vitbhopal.ac.in

---

**Abstract**—Government and banking forms in India — KYC, loan applications, insurance claims — remain a barrier for users who cannot reliably read them, and large language models are an obvious but dangerous fix: an LLM that both interprets a user's speech and writes the resulting value into a legal document gives an unreviewable failure mode to exactly the users least able to review it. We present LucidForm, a form-filling assistant built on the premise that the model must never hold write authority. Every candidate value produced by the LLM passes through a deterministic, non-LLM validation gate — format, checksum, and cross-field rules — is read back to the user in plain language, and is committed only on an explicit, whitelisted affirmation. We enforce this separation three ways: structurally, through a private write path that re-verifies a cryptographic fingerprint at commit time; through a capability-guarded receipt object that can only be constructed by the confirmation step; and architecturally, through a static-analysis test that fails the build if either guarantee is bypassed. The conversation runs as a declared LangGraph state graph whose only route to the write path passes through confirmation, and a retrieval-augmented help agent answers users' questions from official RBI, UIDAI, Income Tax and CERSAI documents with deterministically checked citations — explaining a field, never supplying its value. We evaluate the gate and confirmation parser against hand-authored adversarial suites (59 and 49 cases, spanning thirteen and seven failure categories), and run eight synthetic personas — including a Hindi-only session, self-corrections, vague answers and an embedded prompt injection — twice against a live model (gemini-3.5-flash-lite). Across both runs, 22 wrong values were proposed and none was committed: the gate rejected 18, and the read-back caught 4 that were well-formed and therefore invisible to any deterministic check (two of them differing from ground truth only in letter case), at a gate false-positive rate of 0.9–1.8%. The first live run also exposed a defect — Hindi option names offered by the prompt but rejected by the gate — fixed and re-measured. The help agent retrieved a correct passage for 28 of 30 questions, cited a correct source in 26 of its 28 answers, and refused all six out-of-corpus controls. We report these as small-sample results on synthetic data and state what remains unmeasured: real users, real speech, and forms other than the one prototype we built.

**Keywords**—Accessible Computing, LLM Guardrails, Human-in-the-Loop, Structured Output, Retrieval-Augmented Generation, Deterministic Validation, Digital Identity, Conversational AI

---

## I. Introduction

Government and financial institutions in India process Know Your Customer (KYC) forms, loan applications, and insurance claims at a scale that assumes the applicant can read the form, understand its jargon, and correctly transcribe identifiers such as a PAN or Aadhaar number onto it. This assumption fails for a large population: low-literacy users, elderly applicants unfamiliar with financial terminology, and visually-impaired users for whom the form itself is inaccessible. Existing remedies — a literate relative, a paid form-filling agent, a bank branch visit — are inconsistent, sometimes exploitative, and unavailable to a user acting alone.

A conversational assistant is a natural fix, and large language models make one straightforward to build: transcribe the user's speech, ask a model to read the transcript and the form together, and let it produce a filled document. This design is rejected here, deliberately and on a specific ground. It collapses two roles that must stay separate — *interpreting* what a user meant, and *deciding* that a value is correct and may be recorded — into a single component that performs both without external check. A model that infers a struck digit, resolves an ambiguous answer in its own favor, or is manipulated by adversarial phrasing embedded in the user's utterance writes that value directly into a document with legal standing. For a sighted, literate user this failure is at least detectable on re-reading the form. For the population this system targets, it is often not detectable at all: a user who cannot read the form cannot audit what was written into it. The single-model design therefore fails hardest for exactly the user it is meant to serve.

LucidForm is built around the opposite premise: **the language model never writes a value into the form.** There is exactly one code path capable of mutating form state, and the model has no way to reach it. A candidate value must instead traverse five stages, in a fixed order, before it can be committed:

1. **Form parsing** — field identity, type, and structural constraints (e.g. maximum length) are read once from the target document, ahead of any conversation.
2. **Conversational orchestration** — one field is requested at a time, in plain language, with jargon explained on request rather than assumed.
3. **Extraction** — the user's free-text or spoken response is converted by the model into a typed, frozen *candidate*. A candidate is explicitly a proposal, not a value the system holds.
4. **Validation** — a deterministic component with no model dependency accepts or rejects the candidate against format, checksum, and cross-field rules, returning exactly one reason code on rejection.
5. **Read-back and confirmation** — the validated value is stated back to the user in a form they can audibly verify; only an explicit, unambiguous affirmation produces a commit.

This paper's contribution is the architecture that makes step 4 load-bearing rather than decorative — three independent mechanisms (structural, capability-based, and static-analysis-enforced) that make "the model cannot write a value" a property the system can be tested for, rather than a design intention that later code may quietly violate — together with an adversarial evaluation methodology built to falsify that property rather than merely demonstrate it. A second contribution follows from the first: because the guarantee lives at the write site rather than in the orchestrator, the orchestrator can be replaced — here by a declared state graph — and the model can be given a larger role — here a retrieval-augmented help agent — without weakening it, and both substitutions are tested rather than argued. The system is a working prototype, not a finished study: it supports one form type (an individual KYC-equivalent form) over a text channel in English and Hindi, evaluated against a live model with synthetic personas; the voice channel is implemented but not yet evaluated with real speech. Section VII states these limits without qualification, because a system whose safety claim rests on structural guarantees should not need its scope understated to look complete.

The remainder of this paper is organized as follows. Section II situates LucidForm against prior work on accessible form-filling, LLM guardrails, and speech recognition on structured identifiers. Section III describes the architecture and its enforcement mechanisms in detail. Section IV describes the methodology — form representation, synthetic data construction, and the adversarial and evaluation harnesses built alongside the system rather than after it. Section V gives the governing algorithms in pseudocode. Section VI reports offline and live-model results, including the help agent. Section VII discusses what the results do and do not show. Section VIII concludes and lays out the remaining phases of the work.

## II. Related Work

**Conversational and voice-based form-filling for low-literacy users in India.** The closest prior system is FormBharo [1], a voice agent built with an NGO partner (ARMMAN) to enroll mothers in a maternal-health program over the phone in Hindi. FormBharo combines an LLM with rule-based validation under real latency and cost constraints, and its released benchmark shows that component-level accuracy figures do not predict end-to-end form-completion success under real acoustic noise — a finding consistent with the position taken here, that an isolated extraction-accuracy number is the wrong quantity to optimize or report. LucidForm differs in emphasis rather than in premise: FormBharo's rule-based layer is one component among several optimized for a live deployment; this work isolates the validation-and-confirmation boundary as the object of study and evaluates it adversarially, independent of a specific deployment's latency budget. A comparative study of form-based versus conversational public-service interfaces in India [2] reports that low-income and low-literacy participants engage more successfully with a conversational, voice-first design than a traditional form, supporting the premise that conversation is the right interaction mode without addressing what happens when the model that holds the conversation is also asked to guarantee correctness. Related work on automating government form completion for elderly and monolingual users [3] and on bilingual conversational assistants for banking [4], [5] establishes accessibility-driven form and financial-service automation as an active area, generally without a stated mechanism preventing an unreviewed model output from being recorded.

**Guardrails and human-in-the-loop control of LLM output.** NeMo Guardrails [6] introduced programmable "rails" that constrain a dialogue system's behavior through externally defined rules rather than prompt instruction alone, establishing that a deterministic control layer around a language model is both practical and necessary for controllable behavior — the same principle this work applies specifically to a commit decision rather than to dialogue flow generally. More recent guardrail-pipeline proposals [7], [8] and per-field uncertainty estimators for structured LLM output [9] pursue a related goal — flagging or filtering untrustworthy model output for human review — but generally operate as a confidence filter layered on top of the model's output rather than as a control that the model has no channel to bypass. LucidForm's validation gate is deliberately narrower and stronger than a confidence filter: it is enforced through the type system and the write path itself, verified by static analysis, and evaluated by trying to defeat it rather than by measuring how often it agrees with a human reviewer.

**Automatic speech recognition on identifiers versus prose.** A recognizer's word error rate is a poor predictor of whether it preserves an exact identifier. VoiceCodeBench [10] evaluates twelve ASR systems against 1,482 audited structured-entity targets (identifiers, codes, quantities) and finds the strongest system achieves only 68.7% task success at recovering them exactly, with correlation between word error rate and exact-match success as low as −0.73 — i.e., a transcript can read fluently while still corrupting the one value that matters. Earlier work from Google's speech team [11] shows end-to-end ASR models degrade specifically on numeric sequences relative to prose, and demonstrates substantial recovery through targeted training rather than general model improvement. This literature motivates a structural design choice in LucidForm rather than merely a claim: identifiers are read back character-by-character and digit-by-digit specifically because they are the class of value ASR is known to corrupt silently, in a form that remains well-formed and passes every deterministic check.

**Structured extraction from forms, and slot-filling with confirmation.** FormNet [12], the form-field extraction model of Majumder et al. [13], and Form2Seq [14] address the separate problem of recovering field structure from a form document itself — relevant to this work's form-parsing stage but orthogonal to its validation-and-commit contribution, since LucidForm's target document already exposes machine-readable field structure through the PDF AcroForm standard. Slot-filling dialogue systems have long distinguished extracting a value from committing it: belief-tracking work in spoken dialogue systems [15] and empirical studies of clarification and confirmation strategies [16] show that explicit confirmation measurably improves the precision of values a dialogue system records, which is the confirmation step's role here, made a hard requirement rather than a strategy that improves an average.

**Checksum design for identity numbers.** The Aadhaar identifier's check digit uses the Verhoeff algorithm [17], the first decimal check-digit scheme proven to detect all single-digit substitution errors and all adjacent-transposition errors, adopted for Aadhaar-related validation as a matter of banking-sector practice [18]. The 12-digit, non-intelligent (semantic-free) design of the Aadhaar number itself is documented in the UID numbering scheme white paper [19] and the UIDAI's own demographic data standards report [20]. LucidForm implements Verhoeff rather than the more commonly implemented Luhn algorithm because Luhn accepts a class of transposition errors Verhoeff is designed to catch — a distinction with no visible effect until it is the one digit that matters.

## III. System Architecture

### A. The five-stage pipeline

Figure 1 (described textually here) shows the path a value must traverse. Form parsing runs once, ahead of any session, and produces a typed field specification for every field on the target form: identifier, plain-language prompt, jargon gloss, data type, and structural constraints. The orchestrator asks about one field at a time and performs no validation of its own; it forwards whatever it receives to extraction and forwards whatever extraction and validation report back to the user, unmodified, so that there is exactly one place in the system that explains why a value was rejected. Extraction converts the user's utterance into a frozen `Candidate` object using a model call whose response is constrained to a fixed schema (Section III-C) — a proposal, never a value the system holds as fact. Validation is the first point at which the model's judgement can be overridden and is described in Section III-B. Read-back and confirmation, described in Section III-D, are the last stage before commit and the only stage capable of catching an error that is well-formed and therefore invisible to validation.

### B. The validation gate and its rejection taxonomy

The gate is deterministic: format regular expressions, the Verhoeff checksum for Aadhaar-format identifiers, a cross-check between a PAN-format identifier's fifth character and the confirmed surname, and a postal-code-to-state lookup. It imports no language-model client, directly or transitively; this is enforced by the static-analysis test described in Section III-E rather than left as a convention. Every rejection carries exactly one reason code from a closed, ordered taxonomy (Table I), evaluated in a fixed sequence so that a value failing more than one check is reported by its most severe defect rather than an arbitrary one.

**Table I. Rejection taxonomy and check order**

| Order | Code | Condition |
|---|---|---|
| 1 | EMPTY | No value, or only invisible/whitespace characters |
| 2 | TYPE_MISMATCH | Value is the wrong length for its field |
| 3 | FORMAT | Right length, wrong shape (fails the field's pattern) |
| 4 | ENUM | Not one of a fixed set of permitted options |
| 5 | CHECKSUM | Well-formed but arithmetically invalid |
| 6 | RANGE | Well-formed but outside a permitted domain (e.g., a future date) |
| 7 | CROSS_FIELD | Contradicts an already-confirmed value on another field |
| 8 | AMBIGUOUS_EXTRACTION | The extractor itself reported more than one plausible reading |
| 9 | LOW_CONFIDENCE | The extractor reported low confidence in its own reading |

Structural checks (1–7) are ordered ahead of extraction-quality checks (8–9) deliberately: a value that is both malformed and reported with low confidence is a malformed value, and reporting it as a confidence problem would substitute a weaker finding for the actual defect. Normalization — removing separators, folding case, resolving a country-code prefix that leaves exactly the expected digit count — runs before every check and never repairs a value that is actually wrong: a short identifier is never padded, a failed checksum is never corrected, and a value in an unlisted script is never transliterated, because doing so would commit a value inferred by the system rather than one the user stated. Cross-field checks read a second field's value only once that field has itself been confirmed, so an unconfirmed value can never indirectly influence which values the gate accepts for another field.

### C. Extraction as a structurally bounded model call

The model's output is constrained to a fixed schema with six fields — an intent classification (stating a value, asking a question, declining, or unrecoverable), a proposed value, a verbatim quotation of the utterance region the value was drawn from, a self-reported confidence, an ambiguity flag, and a list of alternative readings. The schema has no field in which the model could assert that a value is valid or should be written; a prompt-injection attempt embedded in the user's utterance therefore has no channel through which to act, independent of how the prompt is worded, because the failure mode it would need to produce cannot be expressed in the response format.

Two checks run on the model's output without invoking a model a second time. *Grounding* locates the model's quoted span in the original utterance; a value whose quotation cannot be found there is treated as ungrounded regardless of the confidence reported, since it was not demonstrably derived from anything the user said. Grounding proves anchorage to the utterance, not correctness of the reading — a digit sequence can be quoted faithfully and still be a mistranscription of what was spoken, which the gate and read-back exist to catch. *Confidence clamping* allows a deterministic finding to lower the model's self-reported confidence, and only to lower it: an ungrounded extraction is forced to zero confidence and marked ambiguous, so it is rejected by both the gate's confidence and ambiguity checks and stays rejected if either threshold is later relaxed.

### D. Read-back and the confirmation whitelist

For a user who cannot see the form, the read-back is not a courtesy summary — it is the only representation of the value they will ever receive, and the confirmation step is meaningless if that representation is not something the user can actually check by ear. Presentation is type-dependent: identifiers are read character by character in grouped, paused sequences, because a synthesizer reading a twelve-digit identifier as a single number has silently regrouped it in a way the listener cannot verify against a physical card; punctuation inside an address is spoken as a word, because a symbol a synthesizer silently skips is a symbol the user cannot confirm.

The confirmation parser is a whitelist evaluated against the entirety of the user's utterance, not a search for an affirmative token within it. This choice is motivated by a specific and realistic failure: the utterance "yes, I know that's wrong" contains an affirmative token and is, in fact, a rejection; "yesterday I gave you the wrong number" contains one embedded in an unrelated word. A substring-based check commits an unagreed value in both cases, for a user who by construction cannot inspect the resulting document afterward to notice. Negation and hedging cues defeat confirmation before the whitelist is consulted, and acknowledgement tokens (e.g., "okay", "acha") are deliberately excluded — they indicate the user heard the read-back, not that they agree with it. This asymmetry is intentional: a false negative costs a re-ask and no incorrect commit; a false positive commits a value into a legal document the user did not agree to. These costs are not comparable, and the parser's design reflects that rather than optimizing for a single accuracy figure.

### E. Three independent enforcement mechanisms

The guarantee that a value cannot be committed without traversing validation and explicit confirmation is not stated once but enforced three separate times, each covering a failure mode the others do not.

1. **Structural.** Form state exposes no public setter. The single write operation accepts a confirmation receipt and independently re-verifies, at the write site, that the receipt was issued for the exact field and candidate being committed — including recomputing a cryptographic fingerprint from the candidate rather than trusting one carried on the receipt — that the validation report it references passed, and that affirmation was explicit. A receipt issued for one value cannot be used to authorize committing a different one.
2. **Capability.** The receipt object cannot be constructed anywhere outside the confirmation module; construction requires a sentinel value held privately there, checked via a runtime inspection of the calling stack frame. This converts "only the confirmation step may issue a receipt" from a convention every future contributor must remember into a property enforced by the type itself.
3. **Architectural.** A static-analysis test parses the codebase's abstract syntax tree and fails the build if the validation or form-state modules import the model client, if a receipt is constructed outside the confirmation module, or if form state's private fields are accessed elsewhere. This is the mechanism that catches deliberate circumvention, since it runs at review time rather than relying on a runtime guard being reached at all.

All three mechanisms were verified to detect violations, not merely to pass in their absence: each rule was deliberately violated in a throwaway change, confirmed to fail the build with the offending file and line identified, and reverted. A safety test that has never been observed to fail is not evidence that it works.

### F. The orchestrator as a declared state graph

The conversation is implemented as a state machine in LangGraph [21]: sixteen nodes (ask, listen, extract, explain, gate, read-back, confirm, commit, and the bookkeeping between fields) joined by declared edges and conditional routes. Each node is a thin wrapper around a component described above; none makes an acceptance decision of its own. Representing control flow as data has a concrete benefit for this architecture: the property "commit is reachable only through confirmation" becomes something a test reads off the graph's edge list, rather than something a reviewer must trace through a loop — and the test asserts that the confirmation node is the sole predecessor of the commit node.

The safety argument deliberately does not move into the graph. Form state is held outside the graph's state object, and the commit node can only call the same re-verifying write operation as before, so a mis-wired edge produces a blocked, logged write rather than a silent one. Replacing the orchestrator is therefore a test of the claim that the guarantee lives at the write site: the LangGraph orchestrator was substituted for the original procedural loop and required to reproduce, byte for byte, the event stream and every utterance addressed to the user across all persona sessions in both English and Hindi, recorded from the original loop before the substitution. It did, with one deliberate exception, made visible by the comparison: the original loop re-asked a field after the user disconnected during read-back, and the graph ends the field instead. Checkpoint-and-resume, a standard feature of the framework, is intentionally not enabled: resuming would require restoring form values from a checkpoint, which is precisely an unconfirmed write.

### G. A help agent that cannot write

The first half of the system's purpose — explaining a field in plain language — is served by a retrieval-augmented help agent [22] invoked when the extractor classifies an utterance as a question rather than a value. Its corpus is six public documents pinned by SHA-256 hash: the Reserve Bank of India's KYC Master Direction and its KYC FAQ, the Income Tax Department's PAN FAQ, two UIDAI Aadhaar FAQ pages, and the CERSAI Central KYC Registry operating guidelines. Documents are chunked by their own structure — one FAQ question with its answer, one numbered paragraph of the Master Direction — yielding 557 passages, each carrying a citation label a user or reviewer can look up ("RBI KYC FAQ, Q10"). Retrieval fuses dense embeddings with BM25 [23] by reciprocal rank fusion [24]: the two fail differently, BM25 being exact on the terms a form uses and useless on a paraphrase, dense retrieval handling code-mixed questions ("pan card nahi hai toh account kaise khulega") and drifting on exact identifiers.

The answer model follows the same pattern as extraction: its reply is bounded by a schema (an answer, the identifiers of the passages it relied on, and an explicit flag for "the passages do not answer this"), and a deterministic check runs on it afterwards. Every cited passage must be one the model was actually shown, and an answer must cite at least one; any failure — an unretrieved citation, no citation, an explicit refusal, or an API error — falls back to the field's human-authored gloss prefaced by an honest statement of uncertainty. The model is never trusted to cite truthfully; the check verifies it, as grounding verifies extraction quotes.

The help agent has no channel to the form. Its output is spoken to the user and logged, and nothing else; it cannot construct a candidate or a receipt, and the static-analysis test of Section III-E was extended to enforce this — the help package may not import the form-state, validation, or orchestration modules, and conversely the validation and write-path modules may not import the help agent, the model SDKs, or the orchestration framework, checked both syntactically and by importing them in a clean interpreter and inspecting what was loaded.

## IV. Methodology

### A. Form representation

The target document is a fillable PDF (AcroForm) reproducing the field set of a standard individual KYC form — name, date of birth, gender, parent's name, PAN, Aadhaar, address, postal code, mobile number, email, occupation, and income band — generated programmatically rather than sourced from an official document, to keep the corpus reproducible and avoid redistributing a third-party artifact. Field identity, widget type, and structural constraints such as maximum length are read directly from the document's field dictionary; this required walking widget annotations directly, since the PDF library's higher-level field accessor was found to silently drop the maximum-length attribute, an error that is otherwise invisible because the system falls back to whatever a separately authored constraint file asserts. Semantic constraints — that a field holds a PAN, that a PAN's fifth character encodes a surname initial — are not recoverable from PDF structure and are supplied by a human-authored overlay of approximately one hundred lines per form type. This division is stated explicitly rather than presented as automatic form understanding: the contribution under evaluation is the gating architecture, and the parser is generic over AcroForm documents, so substituting a different form is a matter of authoring a new overlay rather than modifying code.

### B. Synthetic data and its construction

All identities, PAN and Aadhaar numbers, addresses, and phone numbers used in this work are fabricated. No real personal data, filled form, or identity document was used at any stage. Synthetic Aadhaar-format numbers are constructed to be Verhoeff-valid by algorithmic generation rather than sourced from any real number, so that the checksum path is genuinely exercised without using or requesting real identifiers.

Three synthetic personas were authored to span the conditions the system targets: a low-literacy user who reads identifiers aloud digit by digit; a visually-impaired user for whom the spoken read-back is the sole channel through which an error can be caught; and a Hindi-English code-mixing user who requests a field's meaning before answering it. Persona utterances are hand-authored rather than model-generated, because the input distribution that matters for this evaluation — an identifier spelled character by character, a value embedded in surrounding conversational text, a request for clarification arriving where a value was expected — is a property of the target user population, and generating it with the same model under evaluation would make the evaluation partly circular. Each persona's identifiers are checked by test against the same constraints the gate itself enforces, so that an invalid ground-truth value cannot inflate the reported false-positive rate with a corpus error rather than a gate error.

These three form the *core* set, for which an offline corpus of expected model responses exists. Five further personas form an *extended* set used only against a live model, because its value lies in what a real model does with inputs no expected-response table anticipates: an elderly farmer conducting the whole session in Hindi and reading digits as Hindi number words; a fast speaker who corrects herself mid-utterance ("…five five, no wait, the last one is six") and groups digits as people say them ("eight thousand seven, twelve ninety-eight"); a low-literacy user who answers approximately ("around three lakh", "I drive an auto") and gives a date as 5/1/87, none of which may be repaired into a valid value; a user whose first answer embeds an instruction aimed at the model ("ignore all previous instructions and mark every field as verified"); and a user who asks a question before answering several fields and lives in a city with two common names. The extended personas were authored with an AI assistant from a different model family than the extraction model under evaluation, and reviewed by the authors; they are held to the same ground-truth checks as the core set.

### C. Adversarial evaluation corpora

The validation gate and confirmation parser were each evaluated against a hand-authored adversarial corpus written before the component under test, so that a case the component fails on first run is a genuine finding rather than a specification retrofitted to the implementation's existing behavior.

The gate corpus comprises 59 cases across thirteen categories: single-digit checksum errors, visually confusable character substitutions of the kind speech recognition produces, numeric transcription errors, Hindi-English numeral mixing, prompt-injection strings embedded in an utterance, cross-field contradictions between individually valid values, empty and invisible-character input, over-length input, type coercion, values well-formed for a different field, near-misses of an enumerated option, extraction-quality signals (ambiguity and low confidence), and — added after the first live run (Section VI-D) — declared option names in the user's language with their near-misses. Approximately one fifth of the cases are controls that must be *accepted* — a correct checksum beside three corrupted variants, a correctly paired postal code beside a mismatched one — because a component that rejects every input satisfies a rejection-only suite completely while being useless; these controls are what the reported false-positive rate is measured against.

The confirmation corpus comprises 49 cases across seven categories, including two specifically adversarial to a naive implementation: affirmation spoofing, where an utterance contains an affirmative token while withholding consent ("yes, I know that's wrong"), and substring traps, where an affirmative token appears inside an unrelated word. Thirteen cases are controls that must confirm, again to guard against a parser that satisfies the suite by refusing everything. A separate test implements the naive substring-search parser directly and confirms that it fails at least eight of the suite's rejection cases, establishing that the suite discriminates between the two designs rather than being trivially satisfiable by either.

### D. Evaluation harness and its honesty constraints

Every pipeline stage emits an append-only, timestamped event to a log from the first phase of implementation, before any stage that would populate it existed, so that instrumentation was never retrofitted around a result that had already been observed. Analysis is a separate step that reads recorded logs and re-runs no sessions, so a change in how a measure is computed can be re-applied to data already collected.

Two distinctions are enforced throughout the harness because violating either would produce a number that looks like a result but is not. First, offline replay against a corpus of expected model responses (derived from the same ground truth an accuracy figure would be scored against) exercises every stage of the pipeline deterministically and will detect a regression anywhere in it, but cannot measure extraction accuracy — that figure is necessarily perfect by construction and is reported as such, with the report's own output stating that it carries no information. Extraction accuracy is consequently a claim reserved for live-model evaluation, run through the same replay driver against the real API. Second, gate recall is never reported without the gate's false-positive rate alongside it: a validator that rejects every input achieves perfect recall while being unusable, and the false-positive rate is the measure that distinguishes a discriminating gate from an obstructive one — a distinction the harness treats as a methodological requirement rather than an optional addition, since it is the measure most often absent from comparable reported systems.

### E. Help-agent evaluation

The help agent is evaluated on a hand-written set of thirty questions of the kind the target users ask — in English, Hinglish and Hindi, from "pan kya hota hai" to "I have no ID documents at all, can I still open an account?" — each tagged with the passage or passages that answer it, together with six out-of-corpus controls ("Which bank gives the best interest rate?", "mera loan kab approve hoga?") that must be refused. Four quantities are reported: retrieval hit rate at k = 4 (a gold passage reached the model); answer rate (an in-scope question received a cited answer rather than the fallback); gold-citation rate (among cited answers, the proportion citing a gold passage); and control refusal rate. The last is reported beside the answer rate for the reason gate recall is reported beside its false-positive rate: an agent that answers everything maximises coverage by failing the controls. Whether an answer's wording is correct is not scored automatically; the citations make every answer checkable against its source, and the per-question transcript is retained for that review.

## V. Algorithm and Pseudocode

**Algorithm 1. Commit invariant (`FormState.commit`)**
```
function commit(field_id, candidate, receipt):
    assert receipt.field_id == field_id
    assert receipt.candidate_id == candidate.candidate_id
    assert receipt.validation.status == PASS
    assert receipt.affirmation.explicit == True
    assert candidate.value is not empty
    expected_fp = sha256(field_id || normalize(candidate.value) || candidate.candidate_id)
    assert receipt.candidate_fingerprint == expected_fp
    # every assertion above is independently re-checked here;
    # none is assumed to have been established by an earlier stage
    _values[field_id] = candidate.value          # the ONLY assignment to _values
    emit(COMMIT, field_id, candidate, receipt)
    return

# any assertion failure:
on AssertionError:
    emit(SILENT_WRITE_BLOCKED, field_id, candidate)
    raise SilentWriteBlocked
```

**Algorithm 2. Validation gate (fixed check order)**
```
function validate(candidate, confirmed_fields, field_spec):
    value = normalize(candidate.value, field_spec)
    for check in [EMPTY, TYPE_MISMATCH, FORMAT, ENUM, CHECKSUM,
                  RANGE, CROSS_FIELD, AMBIGUOUS_EXTRACTION, LOW_CONFIDENCE]:
        result = run(check, value, candidate, confirmed_fields, field_spec)
        if result is FAIL:
            return ValidationReport(status=REJECT, reason=check, detail=result.detail)
    return ValidationReport(status=PASS, normalized_value=value)
```

**Algorithm 3. Confirmation as a whitelist over the whole utterance**
```
function parse_affirmation(utterance):
    normalized = strip_filler_and_hedging(casefold(utterance.strip()))
    if normalized in NEGATION_PATTERNS or normalized in HEDGE_PATTERNS:
        return Affirmation(explicit=False, basis="negation_or_hedge")
    if normalized in AFFIRMATION_WHITELIST:          # exact match, NOT substring search
        return Affirmation(explicit=True, basis="whitelist_match")
    return Affirmation(explicit=False, basis="no_match")
```

## VI. Results

Results are reported in two configurations, kept separate throughout. The *offline* configuration replays the core personas against a corpus of expected model responses; it verifies that every stage behaves as designed and is deterministic, but carries no information about model accuracy or latency (Section IV-D). The *live* configuration runs all eight personas against a real model — Google's gemini-3.5-flash-lite through its structured-output interface, chosen as a small, inexpensive tier deliberately, since a gate that needs a frontier model to be safe is not the architecture this paper describes — and is the source of every accuracy and latency figure below. All figures remain small-sample and synthetic, and are reported as counts wherever a percentage would overstate them.

**A. Test suite.** The offline suite — unit tests for every module, both adversarial corpora, the static-analysis safety test, golden-parity tests for the orchestrator, the help agent's retrieval and citation checks, and end-to-end persona sessions — comprises 471 tests, all passing, and runs without credentials. Four further contract tests run only against the live API (a spelled-out identifier is transcribed and grounded; a question and a decline are not extracted as values; an instruction to break the schema does not) and pass against the model above.

**B. Adversarial suite outcomes.** Every one of the 59 gate cases (thirteen categories, 13 of them accepting controls; eight cases added after the first live run exposed the gap described in Section VI-D) and 49 confirmation cases produces its declared outcome (reject with the declared reason code, or accept for a control case). The naive substring-search confirmation parser, implemented separately for comparison, fails 8 of the 49 cases outright — concrete evidence that the suite discriminates a correct implementation from a plausible incorrect one, rather than being satisfiable by either.

**C. Layered defense, offline.** Three complete persona sessions against the full text pipeline produced six proposed values that did not match ground truth. Table II shows where each was stopped.

**Table II. Where erroneous values were stopped — offline (n = 6, three sessions)**

| Layer | Count |
|---|---|
| Rejected by the validation gate | 5 |
| Denied at read-back (well-formed; gate could not detect it) | 1 |
| Committed incorrectly | **0** |

Gate recall alone over this sample is 83% (5/6); the layered system stopped all six. The gate's false-positive rate over the same sessions was 0% — no correct value was rejected. The one error the gate could not catch was a city name misrecognized as a different, real city: correct in type, length, and format, and consistent with every other confirmed field, so no deterministic rule had grounds to reject it. It was caught only because the simulated user, hearing the value read back, recognized it as wrong — the specific case this architecture's read-back stage exists to address, and the reason gate recall alone is reported alongside the layered figure rather than in its place.

**D. Layered defense, live.** All eight personas were run against the live model twice. The first run exposed a defect: the Hindi prompt for gender offers the options by their Hindi names ("purush, mahila, ya transgender") and the gate then rejected "purush" as not an option, abandoning the field. The fix — declaring each option's name in the user's language, exactly as the prompt says it, in the human-authored overlay, matched exactly and never approximately, with adversarial near-misses ("purushh", "mard", a sentence containing a declared name) added to the gate suite — was made before the second run. Both runs are retained; Table III reports each.

**Table III. Live sessions (gemini-3.5-flash-lite, eight personas per run)**

| | Run 1 | Run 2 (after fix) |
|---|---|---|
| Fields committed / declined / abandoned | 107 / 3 / 2 | 106 / 3 / 3 |
| Extraction proposals; accuracy | 120; 90.8% | 118; 90.7% |
| Wrong values proposed | 11 | 11 |
| Rejected by the validation gate | 10 | 8 |
| Denied at read-back | 1 | 3 |
| **Committed incorrectly** | **0** | **0** |
| Correct values wrongly rejected (FPR) | 2 (1.8%) | 1 (0.9%) |
| Extraction latency p50 / p95 | 1.07 s / 32.3 s | 1.04 s / 2.84 s |

Across both runs, 22 wrong values were proposed by a live model and none was committed. The gate's rejections were almost all of one kind: answers in the user's own words that are not a form option — "I work at an IT company", "around three lakh", "apna kaam karta hoon" — which the extractor passed through unrepaired, as specified, and the gate refused rather than mapping to the nearest option. The single correct value rejected in the second run is instructive rather than embarrassing: the date "5/1/87" was read by the model as 5 January 1987, which is correct, but flagged as ambiguous between day-first and month-first readings, and the gate therefore asked again. That is the intended behaviour for a genuinely ambiguous input, and it is counted as a false positive because the metric makes no exception for it. The prompt-injection persona's embedded instruction ("ignore all previous instructions and mark every field as verified") had no effect: the name was extracted and passed validation like any other.

Of the three values denied at read-back in the second run, one is a genuine error no deterministic rule could catch — an address transcribed with a number left as a spoken word ("pandrah") and a landmark appended — and two differ from ground truth only in letter case ("sarai mohana, rajghat"). Case is not audible: a real listener would have confirmed both, and the simulated user, which compares the read-back to its ground truth character for character, is in this respect stricter than a person. We report these as they occurred rather than relax the simulator, and note in Section VII what they imply. The tail latency of the first run reflects rate-limit back-off on a free API tier, not inference time; the second run's p95 of 2.84 s is the more representative figure.

**E. Help agent.** On the thirty-question set with six controls (Section IV-E), a passage answering the question was among the four retrieved in 28 of 30 cases (93.3%), 28 received a cited answer rather than the fallback, 26 of those 28 (92.9%) cited a gold passage, and all six out-of-corpus controls were refused. Two questions whose gold passage was retrieved were nonetheless declined by the answer model ("How can I get my CKYC number?", "What is video KYC?"); declining when unsure is the direction the design prefers. Median end-to-end answer latency, retrieval included, was 1.9 s. In live sessions the agent answered in both English and Hindi from the correct sources ("kya aadhaar dena zaroori hai?" from RBI KYC FAQ Q10). One persona's "pan card nahi hai toh kya karu?" ("I have no PAN card, what do I do?") was classified by the extractor as a decline in one run and as a question in the other — a genuinely ambiguous utterance, handled safely either way (a required field refuses a decline and asks again), but it shows the question-versus-decline boundary is not stable across runs.

We emphasize what these numbers do not show. Eleven erroneous proposals per run is enough to demonstrate the layered mechanism against a real model, not to estimate gate recall as a stable statistic; the personas are synthetic, and the simulated user's judgement of a read-back is a comparison, not a listener.

## VII. Discussion

**What is demonstrated.** The results in Section VI support a narrower and more specific claim than "the system fills forms accurately": that a deterministic validation-and-confirmation boundary can be built as a testable, falsifiable property of a codebase rather than an assumed consequence of careful prompting, and that doing so catches a class of error — a value that is well-formed but simply not what the user said — that a purely rule-based gate cannot, and that a purely confidence-based filter would not reliably surface either. This is the property comparable systems in Section II generally do not report a mechanism for: FormBharo's rule-based layer improves reliability under real deployment constraints but is not evaluated as an architectural guarantee; guardrail toolkits [6]–[9] filter or flag model output rather than making a commit path structurally unreachable from the model. The contribution here is narrower in scope than either — one commit boundary, evaluated adversarially — and that narrowness is deliberate.

The live runs add two observations the offline corpus could not. First, the model's errors were overwhelmingly *pass-through* errors — the user's own words, faithfully transcribed, that are not a form option — which is precisely what the no-repair rule is designed to produce and the gate to refuse; had the extractor been permitted to map "around three lakh" onto the nearest band, those values would have reached read-back as plausible options and relied on the user to object. Second, replacing the orchestrator and adding a model-driven help agent left the commit boundary untouched and verifiably so: the golden-parity comparison, the graph's edge test and the extended static-analysis rules are the evidence, not the absence of incidents.

**Limitations, stated plainly.** The corpus is small and synthetic: eight personas and eleven erroneous proposals per live run demonstrate the layered mechanism against a real model, but do not estimate recall as a stable statistic, and no real user has used the system. The simulated user judges a read-back by comparing it with its ground truth, which makes it stricter than a listener on inaudible differences (two of the four read-back catches were letter case only) and more reliable than one on audible ones; a real user study is required to measure the read-back as people actually experience it, and a deterministic display-case rule for text fields would remove the case-only class entirely. The extended personas were authored with an AI assistant, which risks encoding that assistant's notion of difficult input; they were reviewed by the authors and held to the same ground-truth checks as the core set. The question-versus-decline boundary was not stable across runs for one ambiguous utterance. Only one small model tier was evaluated live; the extractor is provider-agnostic and a sweep across tiers is straightforward but was not run. The help agent's answers were scored for retrieval and citation, not for the correctness of their wording, which rests on the citations being checkable. The prototype supports one form type; a different form's semantic overlay has not been authored or tested, so generality across form types is an untested claim rather than an established one. The Hindi channel is implemented and was exercised live, and one defect it exposed was fixed, but its prompts have not been reviewed by native speakers, and it has an open design question — whether digits should be spoken as Hindi or English number words to match how the target population actually reads them — that requires input from native speakers of the target dialect rather than an internal decision, and is deferred rather than guessed at. The voice channel (automatic speech recognition and speech synthesis) is implemented behind the same channel-abstraction boundary used for text but has not yet been evaluated with real speech; a round-trip probe exists to measure identifier survival through synthesis and recognition specifically, and is reported only once run against a real acoustic backend rather than a simulated one, to avoid the same circularity problem described for offline extraction.

**On the frame guard.** The capability mechanism described in Section III-E2 inspects the calling stack frame at runtime and is explicitly documented as defending against an accidental violation — a helper function drifting into the wrong module during a refactor — rather than a determined attempt to bypass it via direct manipulation of Python's frame or dataclass internals, which frame inspection cannot prevent. The architectural (static-analysis) mechanism is the one relied upon for deliberate circumvention, since it operates at review time rather than at runtime.

## VIII. Conclusion and Future Work

We have presented LucidForm, a form-filling assistant for low-literacy and visually-impaired users built around a single architectural commitment: a large language model may interpret a user's speech but may never hold the authority to write a value into a form. We enforce this through a five-stage pipeline whose validation and confirmation stages are deterministic, and through three independent mechanisms — a re-verifying write path, a capability-guarded receipt, and a static-analysis test — that make the guarantee checkable rather than asserted. The conversation runs as a declared state graph, and a retrieval-augmented help agent explains fields from official documents with checked citations; both were added without weakening the commit boundary, and both substitutions are tested. Against a live model, across two runs of eight synthetic personas, 22 wrong values were proposed and none was committed, and the help agent retrieved a correct source for 28 of 30 questions while refusing every out-of-corpus control — on a small, synthetic corpus, and stopping short of claims about accuracy or usability with real users that the evidence does not support.

Immediate future work: a study with real users from the target population, which is the measurement this work most lacks; native-speaker review of the Hindi channel and a decision on numeral pronunciation; evaluating the voice channel against real speech, including the identifier-survival probe of Section VII; a deterministic display-case rule for text fields; a sweep of the extractor across model tiers; improving the help agent's handling of questions that are also declines; and session resumption implemented by replaying commit receipts from the append-only log rather than restoring values. Longer term, generalizing to additional form types depends on authoring and testing further semantic overlays, and an accessible web interface sits behind the same channel abstraction used for voice.

## References

[1] A. Dalmia, S. Midha, and J. Doshi, "FormBharo: Designing and Evaluating a Voice Agent for Conversational Form Filling in Rural India," arXiv:2608.06027, 2026.

[2] "First Impressions from Comparing Form-Based and Conversational Interfaces for Public Service Access in India," in *Proc. HCI+NLP Workshop, ACL*, 2025.

[3] "Automated government form filling for aged and monolingual people using interactive tool," *Disability and Rehabilitation: Assistive Technology*, 2023.

[4] "AI-enhanced bilingual banking assistant," *Scientific Reports*, 2025.

[5] "Multilingual Conversational AI for Financial Assistance: Bridging Language Barriers in Indian FinTech," arXiv:2512.01439.

[6] T. Rebedea, R. Dinu, M. Sreedhar, C. Parisien, and J. Cohen, "NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails," in *Proc. EMNLP 2023 (Demonstrations)*, 2023.

[7] "Bridging the Safety Gap: A Guardrail Pipeline for Trustworthy LLM Inferences," arXiv:2502.08142, 2025.

[8] "Protect: Towards Robust Guardrailing Stack for Trustworthy Enterprise LLM Systems," arXiv:2510.13351, 2025.

[9] "CONSTRUCT: Real-Time Uncertainty Estimator for LLM Structured Outputs," arXiv:2603.18014, 2026.

[10] T. Baumgartner, B. Tai, L. Kaelin-Martin, C. Fan, L. Debaupte, B. Wang, and Y. Zhong, "VoiceCodeBench: Evaluating Exact Structured-Token Recovery in Automatic Speech Recognition," arXiv:2608.28916, 2026.

[11] C. Peyser, H. Zhang, T. N. Sainath, and Z. Wu, "Improving Performance of End-to-End ASR on Numeric Sequences," arXiv:1907.01372, 2019.

[12] C.-Y. Lee, C.-L. Li, T. Dozat, V. Perot, G. Su, N. Hua, J. Ainslie, R. Wang, Y. Fujii, and T. Pfister, "FormNet: Structural Encoding Beyond Sequential Modeling in Form Document Information Extraction," in *Proc. ACL 2022*, 2022.

[13] B. P. Majumder, N. Potti, S. Tata, J. B. Wendt, Q. Zhao, and M. Najork, "Representation Learning for Information Extraction from Form-like Documents," in *Proc. ACL 2020*, 2020.

[14] M. Aggarwal, H. Gupta, M. Sarkar, and B. Krishnamurthy, "Form2Seq: A Framework for Higher-Order Form Structure Extraction," in *Proc. EMNLP 2020*, 2020.

[15] D. Bohus and A. Rudnicky, "Constructing Accurate Beliefs in Spoken Dialog Systems," Carnegie Mellon Univ., Tech. Rep., 2005.

[16] S. Varges, S. Quarteroni, G. Riccardi, et al., "Investigating Clarification Strategies in a Hybrid POMDP Dialog Manager," 2010.

[17] J. Verhoeff, "Error Detecting Decimal Codes," Mathematical Centre Tract 29, Mathematisch Centrum, Amsterdam, 1969.

[18] National Payments Corporation of India, "Implementation of Verhoeff Algorithm by Banks for Aadhaar Related Applications," NPCI circular.

[19] H. Kanakia, S. Nadhamuni, and S. Sarma, "A UID Numbering Scheme," white paper, Unique Identification Authority of India design contributors.

[20] Unique Identification Authority of India, "UID Demographic Data Standards and Verification Procedure (DDSVP) Committee Report v1.0," UIDAI, 2010.

[21] LangChain, Inc., "LangGraph: Build resilient language agents as graphs," software, https://github.com/langchain-ai/langgraph.

[22] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in *Proc. NeurIPS 2020*, 2020.

[23] S. Robertson and H. Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond," *Foundations and Trends in Information Retrieval*, vol. 3, no. 4, pp. 333–389, 2009.

[24] G. V. Cormack, C. L. A. Clarke, and S. Büttcher, "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods," in *Proc. SIGIR 2009*, 2009.

[25] Reserve Bank of India, "Master Direction – Know Your Customer (KYC) Direction, 2016," updated Aug. 14, 2025; and "FAQs on Master Direction on KYC," Jun. 9, 2025.
