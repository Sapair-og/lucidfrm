# LucidForm — Methodology

A running record of design decisions and their reasoning, written as the work
happens rather than reconstructed afterwards. Phrasing is intended to be
liftable into a paper's methods section.

Each phase appends a section. Nothing here is retro-fitted to make a result look
cleaner than it was.

---

## M0. System design

### M0.1 Problem framing

The system assists users who cannot reliably read a government or banking form
in filling it. The naive design — hand the form and the user's speech to a
language model and let it produce a filled document — is rejected outright. In
that design the model is simultaneously the interpreter of user intent and the
authority that writes the value, so any misinterpretation becomes an
unreviewable write into a legally significant document. For a visually-impaired
user, who cannot visually audit the result, that error is undetectable.

The design adopted here separates interpretation from authority. The model
interprets; a deterministic component decides; the user confirms; only then does
a value enter the form. This separation, rather than the conversational
interface, is the contribution under evaluation.

### M0.2 The five-stage pipeline

A value reaches the form only by traversing, in order:

1. **Form parsing.** Field identity, type, and structural constraints are
   extracted once, ahead of any conversation.
2. **Conversational orchestration.** One field is requested at a time, in plain
   language, with jargon explained on request.
3. **Extraction.** The user's free-text response is converted into a typed
   *candidate* value. A candidate is explicitly not a form value; it is a
   proposal.
4. **Validation.** A deterministic, non-model component accepts or rejects the
   candidate on format, checksum, and cross-field consistency grounds.
5. **Read-back and confirmation.** The system states the validated value back in
   plain language; only an explicit affirmation commits it.

Stage 4 contains no model inference. This is a deliberate architectural
constraint rather than an implementation detail: it means the accept/reject
decision is reproducible, auditable, and independent of model version, sampling,
or prompt phrasing. It also means the safety property can be tested exhaustively
against constructed adversarial inputs, which a model-based validator cannot be.

### M0.3 Enforcing the constraint rather than asserting it

A pipeline description is not a guarantee; it describes what the code does today.
Three mechanisms make the guarantee structural:

*Structural.* Form state exposes no public mutator. The single write path accepts
a confirmation receipt and independently re-verifies, at write time, that the
receipt corresponds to the exact candidate being committed, that validation
passed, and that affirmation was explicit. Re-verification at the write site
means a caller cannot commit value B using a receipt issued for value A.

*Capability.* Confirmation receipts cannot be constructed outside the
confirmation module; construction requires a sentinel held privately there. This
converts the rule that only the confirmation step issues receipts from a
convention into a property of the type.

*Architectural.* A test performs static analysis over the package and fails the
build if the validation or form-state modules acquire a dependency on the model
client, if a receipt is constructed outside the confirmation module, or if
private form state is accessed from elsewhere. This test is the artefact cited
as evidence for the safety claim, because it detects regression of the property
rather than merely documenting it.

### M0.4 Form representation: parser-assisted, human-verified schema

The target form is a fillable PDF (AcroForm). Field identity, widget type,
and structural constraints such as maximum length are read directly from the
document's field dictionary, so field discovery is deterministic and requires no
optical character recognition.

Structural metadata is insufficient for validation. A PDF field dictionary
records that a field is text of at most ten characters; it does not record that
the field holds a PAN, that a PAN matches a specific alphanumeric pattern, or
that its fifth character must agree with the surname recorded elsewhere on the
form. These semantic constraints are supplied by a separate, human-authored
schema overlay that is merged with the parsed structure.

This is stated plainly rather than presented as automatic extraction. The
contribution is the gating architecture, not form understanding; the overlay is
approximately one hundred lines and is authored once per form type. The parser
is generic over AcroForm documents, so substituting a different form is a matter
of supplying a new overlay.

The prototype's target form is generated programmatically to reproduce the field
set of the standard individual KYC form (name, date of birth, gender, parent's
name, PAN, Aadhaar, address, postal code, mobile, email, occupation, income
band). It is a faithful reproduction of the field set rather than the official
document itself. This keeps the corpus reproducible from source and avoids
redistributing a third-party artefact; because the parser is generic, the
official document may be substituted without code changes.

### M0.5 Language selection

The prototype supports English and Hindi. Hindi was selected over other Indian
languages on three grounds: the largest speaker population among the target
users; the strongest open-weight automatic speech recognition and speech
synthesis support, which keeps the pipeline reproducible without a commercial
API; and the ability of the investigator to verify transcripts directly, which
matters because unverifiable transcription would contaminate the extraction
accuracy figures.

The known weakness is stated rather than avoided. Open ASR systems degrade
substantially on Hindi-English code-mixing and, more importantly, on
alphanumeric identifier strings — precisely the highest-stakes tokens on a KYC
form. A misrecognised PAN is both likely and consequential. This is not a
limitation the architecture works around; it is the empirical condition that
makes deterministic validation and explicit read-back load-bearing rather than
decorative, and it is measured directly in the voice-channel evaluation.

### M0.6 Deferral of the voice channel

The prototype is built text-first. Input and output are abstracted behind
channel interfaces from the first commit, with text implementations initially and
audio implementations added in a later phase without modification to the
pipeline.

The reasoning is recorded explicitly because the deferral is a scope decision,
not an oversight. Speech recognition and synthesis integration touches no part of
the gating architecture under evaluation, while accounting for a substantial
share of implementation effort. Sequencing it after the validation gate, the
adversarial suite, and the evaluation harness ensures that the safety result
exists and is measured regardless of whether the voice channel is completed. The
channel abstraction is written first so that the deferral cannot become a
rewrite.

### M0.7 Evaluation design

Instrumentation is part of the initial build rather than added after results are
needed. Every session emits an append-only event log — one record per pipeline
stage per field, carrying timestamps, the candidate under consideration, the
validation outcome, and the confirmation result. Logs are reduced to tabular form
by a separate analysis step, so the analysis can be re-run without re-running
sessions.

Reported measures are: per-field extraction accuracy against ground truth;
validation gate recall; validation gate false-positive rate; read-back correction
rate; per-stage latency; turns required per committed field; and the count of
committed values differing from ground truth.

Gate recall is reported alongside the false-positive rate as a matter of
methodology. Recall alone is not a meaningful measure of a validator: a component
that rejects every input achieves perfect recall while being useless. The
false-positive rate — valid values wrongly rejected — is what distinguishes a
discriminating gate from an obstructive one, and it is the measure most often
omitted in comparable work.

The count of committed values differing from ground truth is treated as a
correctness invariant rather than a reported finding. Any non-zero value
indicates a defect in the enforcement mechanisms and is resolved before results
are collected.

### M0.8 Data

All identities, identifiers, addresses, and contact details are fabricated. No
real personal data, filled form, or identity document is used at any stage.
Synthetic Aadhaar numbers are constructed to satisfy the Verhoeff checksum so
that the checksum validation path is genuinely exercised; they are generated
algorithmically and are not drawn from any real source. Every persona and fixture
file records this in a header comment.

### M0.9 Adversarial evaluation of the validation gate

The safety claim is evaluated by constructing extraction outputs that must be
rejected and confirming that they are. Cases are organised into categories
reflecting realistic failure modes rather than arbitrary malformed input:
identifiers failing a checksum by a single digit; visually confusable character
substitutions of the kind speech recognition produces; numeric transcription
errors; Hindi-English numeral mixing; instruction-injection attempts embedded in
user utterances; affirmation spoofing, in which an utterance containing an
affirmative token nonetheless does not constitute consent; individually valid but
mutually contradictory cross-field values; empty and whitespace-only input;
over-length input; type coercion; and values well-formed for a different field.

The affirmation-spoofing category tests the confirmation step specifically. An
utterance such as "yes, I know that's wrong" contains an affirmative token while
withholding consent; a substring-based affirmation check accepts it and commits
an unconfirmed value. This is a plausible implementation and a genuine
silent-write path, and it is tested for directly.

---

## M1. Implementation notes — instrumentation and corpus

### M1.1 Form structure is read from the document, not asserted

An early implementation obtained field metadata through the PDF library's
field-level accessor. That accessor aggregates to the field object and does not
expose the maximum-length attribute, which is carried on the widget annotation.
The consequence was subtle: every field reported no length constraint, the
loader fell back to the value asserted in the overlay, and the resulting schema
appeared correct while the document itself had contributed nothing but field
names.

The parser was changed to walk widget annotations directly and to resolve
inherited attributes through the parent chain. This matters for the claim in
M0.4: the separation of parsed structure from authored semantics is only
meaningful if the parsed half is genuinely read from the document. A regression
test asserts that every widget yields a length constraint, so a future
reversion to the aggregated accessor fails the build rather than silently
re-introducing the fallback.

### M1.2 The blank template carries no default values

Enumerated fields are rendered as text widgets rather than dropdown widgets. The
immediate reason is that a blank template must not carry a pre-selected value
for any field: a default gender or income band in an unfilled form is a value no
user has confirmed, and any process that exported the template wholesale would
emit it as though it had passed the gate. A test asserts that no widget in the
generated template carries a value.

A secondary consequence is that the permitted option list is carried entirely by
the authored overlay rather than by the document. This is consistent with the
division described in M0.4 rather than a departure from it — the document
carries structure, the overlay carries meaning — and the loader retains a
consistency check that activates if a document supplying its own option list is
substituted later.

### M1.3 Instrumentation precedes the pipeline

The event log was implemented before any pipeline stage that writes to it. Each
record is appended, flushed, and synchronised to disk individually, so a session
that terminates abnormally retains the records explaining why. Records carry a
monotonic sequence number, making a lost write detectable during analysis rather
than invisible. The writer exposes no update or delete operation; append-only
behaviour is a property of the interface rather than a convention observed by
its callers.

Latency is recorded as null where a stage is unmeasured, and never as zero.
Conflating the two would bias every reported percentile downward by treating
unmeasured stages as instantaneous.

Event types for the deferred voice channel are declared in the initial schema.
Introducing them later would make sessions recorded before and after the change
non-comparable, which would in turn prevent the text and voice conditions from
being analysed against a single schema.

### M1.4 Corpus construction and its self-consistency checks

Three synthetic personas were authored, spanning the conditions the system is
intended to serve: a user with low literacy who reads identifiers aloud digit by
digit; a visually-impaired user for whom the spoken read-back is the only channel
through which an error can be detected; and a user who code-mixes Hindi and
English and requests an explanation of a field before answering it.

Persona utterances are authored rather than generated. The input distribution
that matters — identifiers spelled character by character, values embedded in
surrounding conversational text, an exact income figure offered where the form
expects a band, a request for clarification arriving where a value was expected
— is a property of the user population, and generating it from the same model
under evaluation would make the evaluation partly self-referential.

Corpus validity is enforced by test rather than by inspection. Each persona's
identifiers are checked against the same constraints the gate enforces: checksum
validity, format, the correspondence between the tax identifier's fifth
character and the surname, and the correspondence between postal code and state.
This check exists because an invalid ground truth would be scored against a
wrong answer, and would do so in the direction that makes the gate appear worse
than it is — inflating the false-positive rate with corpus errors rather than
gate errors.

### M1.5 The safety property is a test, not a claim

The static analysis described in M0.3 was implemented in the first phase, before
the modules it constrains exist. Its assertions are negative, so they pass
trivially against absent code; two additional tests prevent that from being
mistaken for verification. One asserts that the analysis has files to analyse,
guarding against a path error silently disabling the entire check. The other
feeds the import rule a known violation and confirms it is detected, and
confirms a module whose name merely shares a prefix with a forbidden one is not.
A rule of this consequence should not be trusted on the strength of a passing
run against code that happens to be clean.

---

## M2. The validation gate

### M2.1 Construction order

The adversarial case set was authored before the validator. This ordering is
methodological rather than stylistic: a case set written after the component it
evaluates tends to describe the behaviour the component already has, and
therefore cannot establish that the component does what was intended. Writing
the cases first fixes the target independently, and any case the validator fails
on first execution is a genuine finding rather than a specification adjusted
after the fact.

The set comprises fifty-six cases across eleven categories. Categories
correspond to realistic failure modes — single-digit checksum errors, visually
confusable character substitutions, numeric transcription failures, script
mixing, instruction injection, cross-field contradiction, invisible characters,
over-length input, type coercion, values well-formed for a different field, and
extractor-reported uncertainty — rather than to arbitrary malformed strings. An
obviously malformed input tests nothing; the informative case is one a careless
implementation would accept.

### M2.2 Both directions are asserted

Each case declares an expected verdict and, for rejections, an expected reason
code. Asserting the reason as well as the verdict matters because the reason
distribution is a reported result: a validator that rejects the right input for
the wrong reason produces a correct safety figure and an incorrect error
analysis.

Approximately a fifth of the cases are controls that must be *accepted*. These
are near-misses of the rejected cases — a correct checksum beside three
corrupted ones, a legal letter in a position where a homoglyph was rejected, a
correctly-paired postal code beside a mismatched one. They exist because a
component that rejects every input satisfies a rejection-only case set
completely while being useless. The controls are what the false-positive rate is
measured against, and several categories are tested for the presence of at least
one control.

### M2.3 Check ordering as a defined quantity

Checks execute in a fixed order and the first failure determines the reported
reason. The order is treated as part of the specification rather than an
implementation detail, because the reported reason distribution shifts if it
changes, and results collected under different orderings are not comparable. It
is asserted by a test that must be edited deliberately for the order to change.

Structural checks precede extraction-quality checks. A value that is malformed
and was also extracted with low confidence is reported as malformed: the
structural defect is objective and yields a specific instruction to the user,
whereas reporting it as a confidence problem would conceal the actual defect
behind a weaker one.

Two codes were separated during this phase that an earlier draft had conflated.
A value of the wrong size and a value of the right size but wrong shape produce
different remediation instructions — "that is the wrong length" against "that
does not look like a PAN" — and are therefore distinct codes rather than a
single malformed-value code. A further code was added for values that are
well-formed but outside their permitted domain, such as a birth date in the
future or one implying an age below the statutory minimum. Adding it was
preferred to overloading the format code, which would have made the reported
distribution less interpretable.

### M2.4 Normalization reshapes but does not repair

Values are normalized before validation, so that spacing, separators, and
letter case do not affect the verdict. Normalization is restricted to
transformations that cannot change which value the user stated: removing
separators from an identifier, folding case, resolving a stated option against
the permitted list case-insensitively, converting an accepted date format to a
canonical one, and removing a country-code prefix where doing so leaves exactly
the expected number of digits.

Transformations that would infer a value are excluded. A short identifier is not
padded, a failed checksum is not corrected, digits in another script are not
transliterated, and an unlisted response is not resolved to the nearest
permitted option. Each of these would commit a value derived by inference rather
than stated by the user, which is the failure the architecture exists to
prevent, reached by a different route. The distinction is enforced by tests
asserting that such inputs pass through normalization unchanged and are then
rejected.

The normalized value is what the read-back states and what is committed. The
user therefore confirms the value that will actually be stored rather than their
own phrasing of it.

### M2.5 A script-dependent validation trap

Python's built-in digit predicate, and the corresponding regular-expression
class, both match Devanagari digits. A validator built on either accepts a
postal code written in Devanagari as a valid six-digit code, and then writes
characters into the form that no downstream system will interpret as a number.

This is not a hypothetical input for this system: the target users include
Hindi-English code-mixing speakers, and a speech recogniser operating on Hindi
audio can emit Devanagari numerals. All numeric rules therefore use explicit
ASCII character ranges, and a regression test asserts both that the language
considers such strings to be digits and that the validation rules do not. Input
is additionally subjected to compatibility normalization so that full-width
digit forms cannot bypass an ASCII range.

### M2.6 Cross-field checks and the confirmation dependency

Two checks read a second field: an identifier whose fifth character encodes the
holder's surname initial, and a postal code whose leading digit determines its
region and therefore its state. Both catch values that are individually
well-formed and would pass every single-field check.

A cross-field check runs only when the field it depends on has been *confirmed*.
Validating a candidate against an unconfirmed value would allow a value the user
has not reviewed to influence which values the validator accepts, establishing a
second and indirect path by which unconfirmed input shapes the form.

A check that cannot run is recorded as skipped, never as passed, and skipping
does not reject the value. The distinction is load-bearing in both directions:
recording a skipped check as a pass would inflate the validator's apparent
accuracy with checks that never executed, while treating it as a failure would
block users on a check that could not be performed. The same value is rejected
once its dependency is confirmed, so the guard defers a check rather than
waiving it.

The postal-region check declines to produce a verdict for states it holds no
data for, rather than defaulting to acceptance. The region table is deliberately
coarse: it catches the realistic error — a transcription slip, or a code
remembered from a previous address — without rejecting correct pairings, which
matters because false positives are a reported measure.

### M2.7 The validator does not interpret text

Instruction-injection cases are rejected by the same length and shape rules as
any other malformed value. This is a property of the architecture rather than a
defence built for the purpose: the component performs measurement, pattern
matching, and arithmetic, and contains no code path in which the content of a
string influences the decision procedure. An instruction cannot be obeyed by a
component that performs no interpretation.

A separate test subjects the validator to hostile input — null bytes, very long
strings, template and path-traversal syntax, format specifiers — and asserts
that every case is rejected cleanly rather than raising. An exception escaping
the validator would be handled upstream, and an upstream handler is where a
permissive fallback branch tends to be introduced under time pressure.

### M2.8 Isolation

The validator is reachable from the command line with a hand-written candidate
value and optional confirmed context, without a model, a session, or a form.
This satisfies the requirement that each stage be testable in isolation before
the pipeline is assembled, and it is the intended way for a reviewer to inspect
the safety claim directly. The command reports the verdict, the reason, the
value that would be committed, and every check that ran, and returns a
process exit status reflecting the verdict so it can be scripted.

---

## M3. The write path

### M3.1 Three mechanisms, and what each actually covers

The guarantee that no value enters the form without validation and explicit
confirmation is enforced three times over. The mechanisms are not redundant;
each covers a failure mode the others do not.

*Structural.* Form state exposes no public mutator. The single write operation
accepts a confirmation receipt and re-verifies, at the write site, that the
receipt was issued for the field being written, that it was issued for the
exact candidate being committed, that the validation report it carries covers
that same candidate, that validation passed, that affirmation was explicit,
that the value is non-empty, and that a cryptographic fingerprint recomputed
from the candidate and the value matches the one the receipt carries. Each
condition is checked independently rather than being assumed to have been
established upstream. The final check is the one that matters most: because the
fingerprint is recomputed rather than trusted, a receipt issued for one value
cannot authorise writing a different one, and this holds regardless of how the
caller obtained the pair.

*Capability.* Receipts cannot be constructed outside the confirmation module. A
runtime guard inspects the calling frame and refuses construction from anywhere
else. This catches the realistic failure — a helper that drifts into the wrong
module during a refactor, or an orchestrator that constructs a receipt directly
because it already has all the parts — rather than a determined bypass, which
frame inspection cannot prevent. The limitation is documented in the module
itself rather than left implicit.

*Architectural.* Static analysis over the package fails the build if the
validation or write modules acquire a dependency on the model client, if a
receipt is constructed outside the confirmation module, or if private form
state is accessed from elsewhere. This is the mechanism that covers deliberate
circumvention, because it operates at review time rather than request time.

The three were verified to detect violations rather than merely to pass:
violations of each rule were introduced deliberately and confirmed to fail the
build with the offending file and line identified, then reverted. A negative
assertion that has never been observed to fail is not evidence.

### M3.2 Testing each precondition in isolation

The write path's preconditions are tested individually. For each, a case exists
that satisfies every other precondition and violates only that one, so a check
removed during a later refactor causes exactly one test to fail rather than
none. Constructing those cases requires receipts whose parts disagree with each
other, which the constructor guard prevents — including via the standard
library's dataclass replacement function, whose blockage is itself asserted.
Such receipts are therefore built by allocating the object directly and writing
its fields, simulating the state that would exist if a defect produced an
inconsistent receipt. How the receipt arose is immaterial to the write path,
which re-derives what it needs from the candidate in front of it.

### M3.3 Affirmation parsing, and why it is a whitelist

The read-back is the final barrier between a candidate value and the document.
It resolves one question: did the user agree?

The obvious implementation searches the utterance for an affirmative token, and
it fails on inputs that are entirely ordinary. "Yes, I know that's wrong"
contains an affirmative token and is a rejection. "Yes, but the last digit
should be a three" is a correction. "Yesterday I gave you the wrong number"
contains an affirmative token inside an unrelated word. Under a substring
check, each commits a value the user has just disputed — and does so for a user
who, by the premise of this work, cannot inspect the document afterwards to
discover it.

The parser is therefore a whitelist over the whole utterance rather than a
search within it. An utterance confirms only when the entirety of it, after
normalisation and removal of politeness markers, matches a recognised
affirmation. Negation and correction cues, and hedging expressions, defeat
confirmation before the whitelist is consulted. The recognised set is
deliberately small, and each entry is a phrase whose only reading is agreement.

Acknowledgement tokens are excluded by design. These signal that the user heard
the read-back rather than that they agree with it; accepting them would convert
every conversational back-channel into a committed value. Their exclusion is
recorded as a decision rather than left as an omission, because it has a cost:
a user who intended agreement is asked again.

**The costs are asymmetric, and the design reflects that.** A false negative
costs a re-ask, and the correct value still reaches the form. A false positive
writes a value into a legal document that the user did not agree to. These are
not comparable quantities, so the decision threshold is not placed midway
between them. The false-negative rate is measured and reported rather than
assumed to be zero; a parser tuned so strictly that ordinary users cannot
complete a form would be a different failure, not a safer one.

### M3.4 Adversarial evaluation of the confirmation step

Forty-nine cases across seven categories: plain affirmations in both languages,
affirmation spoofing, substring traps, hedged confirmations, acknowledgement
tokens, plain denials, and silence or transcription artefacts. Utterances are
written in the romanised form a transcriber or recogniser actually produces for
code-mixed speech.

Thirteen cases are controls that must confirm. Without them the suite would be
satisfied by a parser that refuses everything, which is exactly the degenerate
solution the asymmetry above could otherwise motivate.

A separate test implements the naive substring parser and asserts that it is
defeated by at least eight of the suite's rejection cases. This establishes
that the suite discriminates between the two implementations, rather than being
a set of cases any parser would pass — the same reasoning applied to the
validation gate's controls, in the opposite direction.

### M3.5 Corrections, declines, and the distinction between them

A field may be corrected after being committed. The correction requires its own
validation and its own confirmation; a receipt issued for the earlier value
does not authorise the later one. The history retains both entries and records
which value was replaced, so a correction is visible in the record rather than
overwriting it.

Declining an optional field is recorded distinctly from an empty value. A
reviewer needs to distinguish a field the user chose not to answer from one the
system failed to collect, and the two have different implications for the
completeness of the form. Declining writes nothing and cannot discard an
already-confirmed value, which would otherwise make it a route to unsetting a
confirmed value without any confirmation of its own.

### M3.6 Export

The exporter reads only confirmed values and writes only those. It performs no
validation, defaulting, or coercion, since each would constitute a decision
taken after the point at which the user gave consent, concerning a document
they cannot read.

A field with no confirmed value is left blank. A declined field is blank and
indistinguishable in the document from one never reached; the reason a field is
empty belongs in the event log, and encoding it in the form would place text
into a field the user never uttered. The template is never modified, so exports
are repeatable and comparable.

The export is verified end to end against a complete synthetic persona: every
field driven through validation, confirmation, and commit, then read back out
of the produced document and compared against ground truth. Negative cases are
tested with equal weight — a value whose write was blocked is confirmed absent
from the file's bytes, not merely absent from the field.

---

## M4. Extraction

### M4.1 The model's output is bounded by a schema, not by instruction

Extraction is the single point at which a model's judgement enters the system.
The response is constrained to a fixed schema with six fields: an intent
classification, a proposed value, a verbatim quotation from the utterance, a
confidence score, an ambiguity flag, and a list of alternative readings.

This is a structural boundary rather than a stylistic one. The schema contains
no field in which the model could assert that a value is valid, that a check has
been performed, or that a value should be written. A model cannot request an
action for which the response format has no expression, so the prompt does not
need to forbid it and a prompt-injection attempt has no channel through which to
succeed. A response that does not conform to the schema is an error at the API
boundary rather than free text the pipeline must interpret; there is no fallback
branch in which an unparsed reply could be treated as a value.

### M4.2 Intent is separated from value

The schema distinguishes four things a user may be doing: stating a value,
asking what the field means, declining to answer, and saying something from
which no value can be recovered. Only the first produces a candidate.

The separation exists because collapsing it is a realistic and consequential
failure. A user who asks "what is a PAN?" before answering is behaving exactly
as the system intends — the system's stated purpose is to explain fields in
plain language — and an extractor that returns a value for every utterance
writes that question into the field. The failure is silent: the value is
syntactically odd but the pipeline has no way to distinguish it from a genuine
answer. Declines are separated for the same reason, and additionally because a
declined optional field and an unanswered one have different implications for
the completeness of the form.

### M4.3 Two deterministic checks on the model's output

Both are performed without a model, so both are reproducible and testable in
the manner of the validation gate.

**Grounding.** The model must quote, character for character, the region of the
utterance from which the value was taken. The quotation is then located in the
original text. If it does not appear there, the value was not derived from
anything the user said, and the extraction is not trusted regardless of the
confidence the model reports.

The scope of this check is worth stating precisely, because it is easy to
overclaim. It establishes that an extraction is anchored to something the user
actually said. It does not establish that the value is a correct reading of that
region: a model may quote a spoken digit sequence faithfully and still
transcribe it wrongly. Detecting that is the validation gate's function, and
then the read-back's. Grounding closes one specific gap — a value with no basis
in the utterance at all, which the gate cannot detect because such a value is
frequently well-formed — and no more than that is claimed for it.

**Confidence clamping.** The model reports its own confidence, and a model has
no privileged access to whether it is mistaken. Where a deterministic check
contradicts the self-report, the check prevails: an ungrounded extraction is
assigned zero confidence, and an extraction the model itself flagged as
ambiguous is capped below any usable acceptance threshold. The operation is
monotonic in one direction only — nothing in the pipeline can raise a
confidence score. Ungrounded values are additionally marked ambiguous, so they
are rejected by the gate's ambiguity check as well as by its confidence
threshold, and remain rejected if that threshold is later relaxed.

### M4.4 What the offline corpus can and cannot measure

The evaluation harness runs against either a live model or a corpus of expected
responses held on disk. The corpus is derived from persona ground truth together
with hand-written entries for the cases that must not extract cleanly.

**It is not a recording, and the distinction determines what may be reported.**
Replaying against it exercises the entire pipeline deterministically and will
detect a regression anywhere in intent handling, grounding, validation,
read-back, confirmation, commit, or export. It cannot measure extraction
accuracy, because the expected values were written from the same ground truth
that accuracy would be scored against. Offline accuracy against this corpus is
necessarily perfect and carries no information.

Extraction accuracy is consequently a live-model measurement. The same replay
driver accepts either client, so identical sessions run both ways: offline for
correctness, live for the accuracy figure. Presenting the offline number as an
accuracy result would be circular, and the corpus file states this in its own
header, with a test asserting that the statement is present.

The hand-written entries are where the corpus does substantive work. They encode
utterances that must not extract cleanly — a question, a decline, an identifier
containing a visually confusable character, a figure given where an enumerated
band is required — so that the pipeline's handling of each is exercised on every
test run without a network call.

### M4.5 The extractor does not repair

An instructive case arises with enumerated fields. A user asked for an income
band replies "about three lakh". The permitted option "1–5 Lakh" contains that
figure, and mapping one to the other is arithmetic rather than guesswork.

The extractor nevertheless does not perform the mapping. It reports the figure
as stated with low confidence, the gate rejects it as not an option, and the
user is asked again with the options read out. The reasoning is that the
alternative establishes a precedent — the model selecting among permitted values
on the user's behalf — whose boundary is difficult to draw and impossible to
audit from the outside. A user who says "about three lakh" may be estimating,
and the band they would themselves select is not reliably recoverable from the
figure. The same argument applies to occupations described in the user's own
words rather than in the form's vocabulary.

The prompt is written accordingly. It supplies shape information so that spoken
input can be transcribed into written form, and it explicitly instructs the
model not to validate and not to correct a value it believes to be wrong. A
prompt directing the model to return only valid values would relocate the
accept/reject decision into the model, and would do so invisibly: a silently
withheld invalid value is indistinguishable from a user who never supplied one,
leaving the user repeating themselves with no indication of the problem.

### M4.6 Live testing

One test suite calls the live API, and is skipped when no credentials are
present. It asserts the contract rather than the answers: that the schema is
accepted by the API, that the verbatim-quotation instruction produces groundable
quotations, that questions and declines are classified as such, and that an
utterance instructing the model to report validation as complete cannot produce
a response outside the schema.

Whether a specific model transcribes a specific utterance correctly is an
evaluation question, measured over the corpus, not an assertion in a unit test —
where it would convert a model update into a build failure.

---

## M5. Orchestration and read-back

### M5.1 The orchestrator makes no judgements

The component that sequences the conversation is deliberately thin. It decides
which field to ask about and what to do with each stage's result; it never
inspects a value to determine whether it is acceptable. Reproducing any part of
that reasoning would create a second validator, unaudited and free to drift out
of agreement with the first.

The same principle governs how rejections are reported. When validation
rejects a value, the validator's own explanation is passed to the user
unmodified. Re-phrasing it in the orchestrator would place a second,
untested explanation in front of the person least able to work around a
misleading one.

### M5.2 Read-back as an audibility problem

For a user who cannot see the form, the read-back is not a summary of the value
— it is the only representation of that value they will ever receive. If it is
not checkable by ear, the confirmation step is ceremonial: the user assents to
something they had no means of verifying.

Presentation is therefore type-dependent. Identifiers are rendered character by
character, because an identifier spoken as a word is an unpronounceable sequence
that cannot be compared against a card the user is holding. Digits are rendered
as words, because a synthesiser reading a four-digit group as a cardinal number
has silently regrouped it and the listener cannot determine which digits the
system holds. Long numeric identifiers are delivered in groups with a pause
between them, since an unbroken twelve-digit sequence exceeds what a listener
can hold in memory long enough to compare. Punctuation inside an address is
spoken as words, because a symbol a synthesiser skips is a symbol the user
cannot confirm.

Dates invert the rule: the stored form is ISO-8601, which is unreadable aloud,
so the read-back gives the day, month name, and year.

In every case the stored value is unchanged and only its presentation differs.
The value confirmed is always exactly the value that will be written; a
rendering that altered the value would reintroduce the original failure with
additional steps.

### M5.3 Read-back detects a class of error nothing else can

The evaluation corpus includes a case in which a city name is misrecognised as a
different, real city. The value is well-formed, of correct type and length, and
consistent with every other field. Every check the validator performs accepts
it, and no downstream component can detect it, because there is nothing about
the value that is wrong — it is simply not what the user said.

Only the read-back catches it, and only because the user is listening. This case
is the argument for read-back being a pipeline stage rather than a courtesy, and
it is exercised on every test run: the simulated user compares the value read
back against its own ground truth and denies it, the field is re-asked, and the
correct value is committed on the second attempt.

Including it also makes the read-back correction rate a measurement rather than
a constant. A corpus in which the validator catches every error would report a
correction rate of zero regardless of whether the read-back functioned at all.

### M5.4 Asking for an explanation is not a failed attempt

Sessions are bounded by two independent limits. The number of times a field may
be re-asked is capped, after which the field is recorded as abandoned rather
than left empty — the distinction matters because an abandoned field and an
unanswered one have different implications for the completeness of the form, and
neither may be silently treated as a value.

Requests for explanation are bounded separately and do not count against the
retry limit. Asking what a field means is the system operating as intended: the
stated purpose is to explain fields in plain language. Charging such a request
against the retry budget would penalise precisely the users the work exists to
serve, and would cause a user who needed two explanations to exhaust their
attempts without ever having given a wrong answer.

Silence is treated as neither consent nor an answer. A channel returning no
input marks the field abandoned.

### M5.5 The simulated user

Persona-driven sessions run the complete pipeline with every real component;
only the person is simulated, and offline, the model. The simulated user
implements the same input and output interfaces as the console, and receives the
value being read back as structured data alongside the rendered sentence. It
then compares that value against its own ground truth and answers honestly.

This is what makes the read-back correction rate a property of the pipeline
rather than a figure chosen by whoever wrote the driver. A simulated user that
always affirmed would report a perfect session regardless of what was read back
to it.

When a persona's script is exhausted the channel returns nothing rather than
repeating its final utterance, so a persona cannot loop indefinitely and inflate
the turns-per-field measure without bound.

### M5.6 Localisation of what the user hears

Field prompts, jargon explanations, spoken field names, and the system's own
sentences are all translated. The field's canonical name remains English, since
it identifies the field in the document, the event log, and the results table;
what is translated is only what the user hears.

Spoken field names were initially left untranslated, which produced read-backs
carrying an English field name inside an otherwise Hindi sentence. This is the
single place where a language inconsistency has a cost beyond awkwardness: the
read-back is the sentence the user is asked to attest to.

String lookup is strict. A missing key raises rather than falling back to
another language, because a silent fallback presents to the user as the
assistant changing language mid-sentence — indistinguishable, for someone who
cannot read the screen, from a malfunction, and considerably harder to notice in
testing than an exception. Tests assert that the language tables have identical
key sets and equivalent placeholder sets, compared as unordered collections:
Hindi word order places a total before a count where English does the reverse,
which is correct translation rather than an error.

One question is deferred to the Hindi evaluation phase rather than decided here:
whether digits in a Hindi session should be spoken as Hindi or English number
words. Many speakers in the target population read digits in English while
speaking Hindi, so the answer depends on the user population rather than on
consistency, and is not something to settle by assumption.

---

## M6. Measurement

### M6.1 Analysis is separated from collection

The analysis step reads recorded logs and re-runs no sessions. This was the
reason for making the event log the primary artefact rather than computing
figures during a run: the analysis can be corrected, extended, or disputed and
then re-applied to data already collected, and a change in how a measure is
defined does not require re-running the experiment.

Three grains of table are produced. A per-turn table records every ask-and-answer
cycle with the extraction, the validation verdict, and the confirmation
alongside each other. A per-field table records how each field ended, with the
committed value and the ground truth side by side so the accuracy figure can be
audited rather than trusted. A per-session table and a single-row summary
aggregate these.

Turns are delimited by the system's question rather than by the retry index
recorded in the log. Requests for explanation do not advance that index, so
grouping on it would merge a question and the answer that followed into a single
record and conceal the question entirely.

### M6.2 Which measures require ground truth

Extraction accuracy, gate recall, and the gate's false-positive rate all
require knowing the correct answer, and are therefore computable only for
synthetic-persona sessions. Latency, turns per field, the rejection-reason
distribution, and the read-back correction rate require no ground truth and are
computable for any session, including one with a real user.

Sessions without a persona are excluded from the first group and retained in the
second. The alternative — scoring them against an assumed answer — would
manufacture accuracy figures from data that contains no such information.

Proposals are compared against ground truth after normalisation, using the same
rules the validator applies, so a value differing only in spacing or a country
code counts as the same answer. Judging a proposal on its punctuation would
inflate the reported error rate with differences that never reach the form.

### M6.3 The layered result

The measure the architecture is designed to produce is not a single accuracy
figure but the division of labour between the layers that stop a wrong value:

| where a wrong value was stopped | count |
|---|---|
| rejected by the validation gate | 5 |
| denied at read-back (gate could not: the value was valid) | 1 |
| committed wrong | 0 |

Six wrong values were proposed across three sessions; all six were stopped. The
gate stopped five. The sixth was a city name misrecognised as a different real
city — correct in type, length, and format, and consistent with every other
field. No deterministic check could reject it, because nothing about it was
malformed; it was simply not what the user said. It was stopped at read-back.

This is the finding the architecture exists to produce. Gate recall alone was
83%; the layered system stopped everything. Reporting only the gate's recall
would understate the system, and reporting only the end-to-end figure would
conceal which mechanism did the work and why both are needed.

A test asserts that these three counts sum to the number of wrong proposals. If
they do not, a case is being double-counted or, worse, a wrong value is
unaccounted for — which would mean one nobody stopped.

### M6.4 Recall is reported with its false-positive rate

The gate's recall is reported alongside the proportion of correct values it
wrongly rejected. This is a methodological commitment rather than a completeness
gesture: recall alone is not a meaningful measure of a validator, because a
component rejecting every input achieves perfect recall while being unusable.
The false-positive rate is what distinguishes a discriminating gate from an
obstructive one, and it is the measure most often absent from comparable work.

In these sessions the gate rejected no correct value. That figure is as much a
part of the result as the recall, and a future change that raised recall by
tightening a rule would be visible here as a cost rather than appearing as an
unqualified improvement.

The count of committed values differing from ground truth is treated as a
correctness invariant rather than a reported measure. The analysis command exits
with a failure status when it is non-zero, so a defect of this kind cannot be
mistaken for a result to be discussed.

### M6.5 Figures that are not measurements

Two figures the analysis computes are not results when produced offline, and the
report states so in the output rather than in a footnote.

Extraction accuracy against the offline corpus is an artefact of construction:
the corpus's expected values were derived from the same ground truth the
accuracy is scored against, so the figure carries no information about a model's
behaviour. Latency measured offline is dictionary-lookup time, not inference
time. Both warnings are emitted automatically whenever every session in the set
was produced by a replay client, and the provenance is carried in the summary
table itself so that a row lifted into a document retains it.

A third warning fires when a rate is computed over a small denominator. Gate
recall here rests on six wrong proposals, which is too few to quote as a
percentage; the counts are the honest presentation, and the report says so.

These warnings exist because the failure they prevent is not hypothetical. A
number detached from how it was produced is precisely how a circular result
enters a paper, and the offline accuracy figure of 87% is exactly the sort of
number that would survive into a results table unchallenged.

---

*(Subsequent sections are appended as each phase completes.)*
