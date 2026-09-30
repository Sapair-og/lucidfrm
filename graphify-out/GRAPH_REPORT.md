# Graph Report - LucidForm  (2026-10-01)

## Corpus Check
- 120 files · ~272,960 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .jsonl 17, (none) 4, .example 1)

## Summary
- 2002 nodes · 4594 edges · 113 communities (101 shown, 12 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 422 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a4a7366f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_gate_rules.py
- Event
- test_formstate.py
- test_readback.py
- build.js
- SessionGraph
- MissingString
- test_issues_phase1.py
- test_confirm.py
- asr_probe.py
- test_metrics.py
- cli.py
- test_writer.py
- test_extraction.py
- ProbeSummary
- IV. Methodology
- What You Must Do When Invoked
- ValidationGate
- test_issues_phase7.py
- test_no_silent_write.py
- test_gate_crossfield.py
- loader.py
- test_voice.py
- test_checksums.py
- voice.py
- replay.py
- one_field
- test_schema_loader.py
- Title (pick one, or tell me to try again)
- test_adversarial.py
- HelpAgent
- Transcript
- VoiceChannel
- HelpIndex
- corpus.py
- test_session.py
- Intent
- test_personas.py
- test_issues_phase2.py
- test_issues_phase5.py
- netcheck.py
- test_help.py
- Strings
- EventLog
- Extraction
- M0. System design
- graphify reference: extra exports and benchmark
- Status
- M2. The validation gate
- Row
- Prompt for Claude Code — LucidForm Prototype
- test_llm_clients.py
- M3. The write path
- M4. Extraction
- M5. Orchestration and read-back
- Candidate
- graphify reference: query, path, explain
- suggest.py
- LucidForm
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- Aggregate
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- Settings
- golden_sessions.py
- ConsoleChannel
- graphify reference: GitHub clone and cross-repo merge
- build_official_layout.py
- base.py
- Kind
- pytest
- .claude/CLAUDE.md
- extraction-spec.md
- models.py
- test_gate.py
- FormState
- Session
- FieldSpec
- test_issues_phase8.py
- Extractor
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- LucidForm
- Team workflow (5 people, each with their own AI assistant)
- M8. The help agent
- uidai_faq_update.md
- make_genai_client
- III. System Architecture
- ConfirmationReceipt
- load_all
- _Pages
- load_set
- README.md
- Progress log
- GeminiEmbedder
- Live demo — 5 minutes, terminal only
- Team guide
- .commit
- LucidForm — Methodology
- metrics.py
- spell
- test_a_failed_model_call_is_an_unclear_turn_not_a_crash
- passing
- build
- test_a_form_is_filled_over_the_voice_channel
- graphify reference: transcribe video and audio
- chunks
- test_the_readback_sentence_names_the_field_and_the_value
- pathlib

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 78 edges
2. `Candidate` - 69 edges
3. `FormState` - 65 edges
4. `Status` - 65 edges
5. `EventLog` - 52 edges
6. `get_settings()` - 50 edges
7. `Extraction` - 50 edges
8. `Extractor` - 49 edges
9. `load()` - 49 edges
10. `Event` - 47 edges

## Surprising Connections (you probably didn't know these)
- `LF-013 — A quote cut short inside a number defeats the digit check` --references--> `_whole_number()`  [INFERRED]
  docs/ISSUES.md → lucidform/extract/grounding.py
- `The guarantee is enforced, not promised` --references--> `ConfirmationReceipt`  [INFERRED]
  README.md → lucidform/formstate/receipt.py
- `Commit invariant` --references--> `SilentWriteBlocked`  [INFERRED]
  SPEC.md → lucidform/formstate/state.py
- `Step 2.5 - Transcribe video / audio files (only if video files detected)` --references--> `export()`  [INFERRED]
  .claude/skills/graphify/references/transcribe.md → lucidform/formstate/writer.py
- `Conventions` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py

## Import Cycles
- None detected.

## Communities (113 total, 12 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.07
Nodes (56): length_error(), normalize(), parse_date(), date, range_error(), Canonical form of a value: what gets read back, and what gets committed. The…, Wrong size. Returns a human-readable detail, or None if the size is fine., Well-formed, but outside the permitted domain. (+48 more)

### Community 1 - "Event"
Cohesion: 0.13
Nodes (28): Event, str, Read one session log. Used by metrics and by tests; never by the pipeline., read_log(), The event log is the evaluation substrate, so its guarantees are tested.…, Null means "not applicable"; zero would mean "instantaneous". Conflating them…, Hindi utterances must not be mangled into escapes. The logs are read by a human…, Not a swallowed error -- a logged finding (SPEC.md section 2). (+20 more)

### Community 2 - "test_formstate.py"
Cohesion: 0.08
Nodes (37): Gotchas, forge(), gate(), make(), fixture, The single write path, and every way of getting round it that I could think of.…, The fingerprint is recomputed at the write site, not trusted. Constructed by…, A passing verdict on one value must not authorise another. `confirm()` refuses… (+29 more)

### Community 3 - "test_readback.py"
Cohesion: 0.14
Nodes (27): field(), fixture, Read-back rendering: can the user actually check this by ear? For a user who…, A listener can check "example dot invalid" without hearing it letter by letter,…, Spelling a name the user just said would be tedious and no clearer., Presentation differs; the value does not. If rendering altered the value, the…, AKQPS3417M" spoken as a word is an unpronounceable noise that no listener can…, A synthesiser reading "3417" says "three thousand four hundred and seventeen",… (+19 more)

### Community 4 - "build.js"
Cohesion: 0.08
Nodes (33): docx, ref_fs, ref_path, authorsTable(), body(), bodyBlocks(), COL_W, doc (+25 more)

### Community 5 - "SessionGraph"
Cohesion: 0.05
Nodes (38): Orchestrator (LangGraph), Decisions (approved 2026-09-30), ISSUES.md — known problems, root causes, and fixes, LF-004 — Email only syntax-checked, LF-006 — Session ends incomplete, no final review, LF-009 — Near-miss answers get no suggestion, LF-010 — A valid option the model was unsure of is re-asked blindly, LF-011 — Follow-ups (open) (+30 more)

### Community 6 - "MissingString"
Cohesion: 0.40
Nodes (4): KeyError, MissingString, A string key is absent from the requested language's table., Look up a key and fill in its placeholders.

### Community 7 - "test_issues_phase1.py"
Cohesion: 0.12
Nodes (34): LF-007 — Model silently drops/changes digits, check(), digits_agree(), locate(), _loose(), Deterministic checks on the model's output, performed without the model. The…, The digit string a quote spells out, or None if it cannot be read that way., The quote, widened to the whole run of digits it sits inside. A model can quote… (+26 more)

### Community 8 - "test_confirm.py"
Cohesion: 0.07
Nodes (36): RuntimeError, A receipt was constructed outside the confirmation module., UnauthorizedIssuer, confirm(), normalize_utterance(), parse_affirmation(), Lowercase, strip punctuation and filler, collapse whitespace. Apostrophes…, Decide whether an utterance is an explicit confirmation. Returns an… (+28 more)

### Community 9 - "asr_probe.py"
Cohesion: 0.12
Nodes (21): _category(), character_error_rate(), decode_spelled(), levenshtein(), probe(), Path, Does an identifier survive being spoken and heard? METHODOLOGY M0.5 asserts…, Run the synthesise-recognise round trip over every persona's values. (+13 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.06
Nodes (30): tempfile, agg(), fixture, The measures, and the guards on how they may be read. Every number reported in…, Six deliberate errors are planted across the three personas., The headline table must balance. A wrong value is stopped by the gate, stopped…, The correctness invariant. A defect, not a finding., The evidence that the read-back is a stage rather than a courtesy. These are… (+22 more)

### Community 11 - "cli.py"
Cohesion: 0.09
Nodes (44): command, asr_probe_cmd(), extract_cmd(), _extraction_client(), gate_check(), graph_cmd(), _help_agent(), help_ask() (+36 more)

### Community 12 - "test_writer.py"
Cohesion: 0.12
Nodes (30): export(), ExportError, Path, RuntimeError, Read the filled values out of an exported PDF. Used by the tests to verify that…, The export could not be performed. Never partially completed., Write the confirmed values into a copy of the blank form. The template is never…, read_back() (+22 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.08
Nodes (43): Help agent (RAG), Closed rejection taxonomy. Every rejection carries exactly one. Each member…, Reason, extractor(), gate(), fixture, Stage 3: utterance to candidate. No network. Every test here runs against a…, Belt and braces: intent says value, but there is none to propose. (+35 more)

### Community 14 - "ProbeSummary"
Cohesion: 0.18
Nodes (9): is_simulated(), ProbeResult, ProbeSummary, Corrupted identifiers the gate accepted. The set that matters. Every one of…, report(), rows(), Same discipline as the offline extraction corpus: a number detached from how it…, test_a_real_recogniser_would_not_be_labelled_simulated() (+1 more)

### Community 15 - "IV. Methodology"
Cohesion: 0.33
Nodes (6): A. Form representation, B. Synthetic data and its construction, C. Adversarial evaluation corpora, D. Evaluation harness and its honesty constraints, E. Help-agent evaluation, IV. Methodology

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

### Community 17 - "ValidationGate"
Cohesion: 0.12
Nodes (7): date, Deterministic accept/reject on a single candidate value., Validate one candidate against the schema and confirmed values. `committed`…, ValidationGate, Check, One executed validation check. Recorded whether it passed or failed, so the log…, test_an_ambiguous_date_is_still_not_offered()

### Community 18 - "test_issues_phase7.py"
Cohesion: 0.12
Nodes (28): _choose_pdf(), Ask whether to use the user's own PDF and read it (ISSUES.md LF-014). Returns a…, _is_official(), _norm(), open_form(), Path, Read a user's PDF and build a schema for it, or raise SchemaError saying why…, _same_file() (+20 more)

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.12
Nodes (28): ast, Module, _help_violations(), _imported_names(), _parse(), parametrize, Path, _python_files() (+20 more)

### Community 20 - "test_gate_crossfield.py"
Cohesion: 0.06
Nodes (54): LF-003 — PIN / city / state mismatch accepted, check(), _city_agrees(), city_matches_pin_and_state(), CrossFieldResult, doc_number_matches_type(), _or(), pan_matches_surname() (+46 more)

### Community 21 - "loader.py"
Cohesion: 0.11
Nodes (25): LF-001 — Can't fill the official CKYC form, _clean(), CustomForm, _label(), Any, Use a PDF the user brings, instead of the built-in forms (ISSUES.md LF-014).…, The printed text just left of the box on its line, else just above it., _texts() (+17 more)

### Community 22 - "test_voice.py"
Cohesion: 0.11
Nodes (26): Purpose, str, Why the system is listening. The user does not see this; the channel does., CorruptingRecognizer, EchoRecognizer, Returns text handed to it. Lets the channel be tested without audio., Applies documented speech-recognition error patterns, deterministically. **This…, Writes a valid but silent WAV. Exercises the file path without a voice. (+18 more)

### Community 23 - "test_checksums.py"
Cohesion: 0.11
Nodes (28): aadhaar_valid(), corrupt_one_digit(), Checksum primitives for the validation gate. Pure functions over strings. No…, True if `digits` (including its trailing check digit) satisfies Verhoeff., Check digit for a payload that does not yet carry one., Structural + checksum validity of a 12-digit Aadhaar number. The first digit is…, Generate a checksum-valid but entirely fabricated Aadhaar number. Used only to…, Change exactly one digit, producing a checksum-invalid variant. The single-… (+20 more)

### Community 24 - "voice.py"
Cohesion: 0.14
Nodes (12): FasterWhisperRecognizer, PiperSynthesizer, RuntimeError, The voice channel: speech in, speech out, pipeline unchanged. Phase 7 of the…, Local speech synthesis via Piper. Invoked as a subprocess rather than through a…, A speech backend was requested but is not installed., Local speech recognition via faster-whisper (CTranslate2). Local and pinned…, VoiceBackendMissing (+4 more)

### Community 25 - "replay.py"
Cohesion: 0.14
Nodes (11): PersonaChannel, Text channels: a console for a person, and a persona for the replay driver.…, Agree only if the value read back matches ground truth., One exchange, kept for the transcript., A simulated user, driven by a persona's script. Implements both protocols: it…, Turn, Path, Run a persona through the whole pipeline, headlessly. This is the driver every… (+3 more)

### Community 26 - "one_field"
Cohesion: 0.10
Nodes (33): test_form_60_is_not_committed_without_yes(), test_session_rejects_the_shortened_aadhaar(), test_offered_band_denied_is_not_saved(), test_offered_band_needs_a_yes(), test_only_one_suggestion_per_utterance(), fixture, Regression tests for docs/ISSUES.md LF-012: "I have a PAN but can't find the…, schema() (+25 more)

### Community 27 - "test_schema_loader.py"
Cohesion: 0.07
Nodes (26): built_pdf(), overlay(), fixture, parametrize, Round-trip: the generator writes the AcroForm, the loader reads it back.…, A field the PDF does not have must raise, not be skipped. A silently dropped…, One spoken name for two options would make the gate choose for the user., Conversely, a PDF widget nothing validates must raise. (+18 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.25
Nodes (8): I. Introduction, II. Related Work, References, Title (pick one, or tell me to try again), V. Algorithm and Pseudocode, VI. Results, VII. Discussion, VIII. Conclusion and Future Work

### Community 29 - "test_adversarial.py"
Cohesion: 0.12
Nodes (15): _candidate(), committed(), gate(), fixture, parametrize, The adversarial suite -- the evidence for the safety claim. Every case in…, Every code in the taxonomy needs at least one case. An unexercised reason code…, A rejection-only category cannot distinguish a gate from a brick wall. The… (+7 more)

### Community 30 - "HelpAgent"
Cohesion: 0.13
Nodes (10): AnswerClient, HelpAgent, HelpAnswer, Protocol, _question_lines(), emit(), FAQ pages where a question is a line ending in '?' followed by its answer., The embedding call is a live API call too; it sits inside the fallback. (+2 more)

### Community 31 - "Transcript"
Cohesion: 0.19
Nodes (9): Path, Protocol, What the recogniser heard. `confidence` is the recogniser's own estimate where…, SpeechRecognizer, SpeechSynthesizer, Transcript, Guard on the probe itself. If the round trip corrupted values even with a…, test_a_perfect_recogniser_loses_nothing() (+1 more)

### Community 32 - "VoiceChannel"
Cohesion: 0.24
Nodes (6): One audio exchange, retained for the transcript and for error analysis., Speech in, speech out, over the same protocols as the console. Audio input is…, VoiceChannel, VoiceTurn, The gate must stay installable and testable without a gigabyte of model…, test_the_module_imports_without_any_speech_library()

### Community 33 - "HelpIndex"
Cohesion: 0.12
Nodes (16): Chunk, _corpus_digest(), Embedder, HashEmbedder, HelpIndex, _normalise(), Path, Protocol (+8 more)

### Community 34 - "corpus.py"
Cohesion: 0.17
Nodes (15): html, help_build(), Chunk the official sources and embed them (a few minutes on the free tier)., _clean(), _flat(), _html_text(), load_chunks(), load_manifest() (+7 more)

### Community 35 - "test_session.py"
Cohesion: 0.08
Nodes (26): personas(), fixture, parametrize, The orchestrator, and the full pipeline end to end. Two kinds of test here. The…, Explaining again is not helping; the session must be able to move on., The correctness invariant. Not a finding -- a build failure. Any entry here…, A blocked write here would mean a defect upstream, not a caught attack --…, p03 has no email and says so. (+18 more)

### Community 36 - "Intent"
Cohesion: 0.11
Nodes (23): build(), _clean_extraction(), Any, Path, Build the offline extraction fixture corpus. python -m lucidform.eval.fixtures…, The straightforward case: the value was stated and heard correctly., write(), Intent (+15 more)

### Community 37 - "test_personas.py"
Cohesion: 0.08
Nodes (20): personas(), fixture, The synthetic corpus must be internally consistent. Accuracy is measured…, The form states an 18-year minimum, and the gate enforces it., A persona who has no email still has to say so out loud. An empty ground truth…, .invalid is reserved by RFC 2606 and can never resolve. A synthetic corpus that…, The data provenance claim in METHODOLOGY M0.8 is only true if the files…, A persona that cannot answer a required field would abandon it mid-run, which… (+12 more)

### Community 38 - "test_issues_phase2.py"
Cohesion: 0.23
Nodes (12): _gate(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-003: PIN / city / state consistency. The…, schema(), test_correct_pairs_pass(), test_directory_lookup(), test_known_city_in_another_state_is_caught() (+4 more)

### Community 39 - "test_issues_phase5.py"
Cohesion: 0.09
Nodes (29): _address(), Greedy word wrap into lines of the given box counts; the last line takes the…, split_name(), wrap(), _drawn(), _gate(), official(), fixture (+21 more)

### Community 40 - "netcheck.py"
Cohesion: 0.50
Nodes (3): email_domain_ok(), Network checks the gate may be given, but never performs itself (ISSUES.md…, True if the domain publishes a mail server (MX), False if it cannot receive…

### Community 41 - "test_help.py"
Cohesion: 0.10
Nodes (20): HelpReply, BaseModel, The model's entire permitted output., Returns the replies handed to it; an Exception in the list is raised., ScriptedAnswerClient, The help agent: answers a user's question about a field from official…, agent(), parametrize (+12 more)

### Community 42 - "Strings"
Cohesion: 0.10
Nodes (26): available(), load(), The system's own wording, in one language., Strings, LucidForm -- accessibility-first form assistant. The LLM never writes a form…, parametrize, String tables. A missing key must fail loudly. Falling back to another language…, The read-back names the field, so an English label inside a Hindi read-back is… (+18 more)

### Community 43 - "EventLog"
Cohesion: 0.12
Nodes (17): EventLog, _jsonable(), Any, Path, Time a stage and emit once it completes. Mutate the yielded dict to attach the…, Append-only JSONL writer for one session., parse_session(), Turn one log file into per-turn and per-field records. Turns are delimited by… (+9 more)

### Community 44 - "Extraction"
Cohesion: 0.12
Nodes (19): Returns extractions handed to it. For tests that need one exact reply., ScriptedClient, clamp_confidence(), Grounding, Confidence the pipeline will actually use. The model reports its own…, Extraction, BaseModel, The model's entire permitted output. (+11 more)

### Community 45 - "M0. System design"
Cohesion: 0.20
Nodes (10): M0.1 Problem framing, M0.2 The five-stage pipeline, M0.3 Enforcing the constraint rather than asserting it, M0.4 Form representation: parser-assisted, human-verified schema, M0.5 Language selection, M0.6 Deferral of the voice channel, M0.7 Evaluation design, M0.8 Data (+2 more)

### Community 46 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 47 - "Status"
Cohesion: 0.27
Nodes (14): str, Status, _gate(), fixture, Regression tests for docs/ISSUES.md LF-004 (email), LF-005 (income), LF-009…, schema(), test_a_suggestion_never_rides_on_a_pass(), test_domain_without_mail_is_rejected() (+6 more)

### Community 48 - "M2. The validation gate"
Cohesion: 0.22
Nodes (9): M2.1 Construction order, M2.2 Both directions are asserted, M2.3 Check ordering as a defined quantity, M2.4 Normalization reshapes but does not repair, M2.5 A script-dependent validation trap, M2.6 Cross-field checks and the confirmation dependency, M2.7 The validator does not interpret text, M2.8 Isolation (+1 more)

### Community 49 - "Row"
Cohesion: 0.17
Nodes (12): gold_matches(), A numbered gold ("RBI KYC FAQ, Q1") must equal the label -- a substring test…, Row, run(), summarise(), RBI KYC FAQ, Q1' is not a hit for Q10-Q19 (found in review)., An outage must not read as perfect refusal behaviour (found in review)., test_a_numbered_gold_label_matches_only_that_number() (+4 more)

### Community 50 - "Prompt for Claude Code — LucidForm Prototype"
Cohesion: 0.29
Nodes (6): Context, How I want you to work with me, Non-negotiable design constraint, Prompt for Claude Code — LucidForm Prototype, Scope for THIS prototype (deliberately small), What I need from you, in order

### Community 51 - "test_llm_clients.py"
Cohesion: 0.08
Nodes (35): Extraction clients (Gemini), AnthropicExtractionClient, GeminiExtractionClient, make_client(), Model clients for the extraction layer. The extractor talks to a small protocol…, An extraction provider was named that this build has no client for., The live extraction client for `provider`, or for the configured one., The real client. Uses the SDK's structured-output helper, so the response is… (+27 more)

### Community 52 - "M3. The write path"
Cohesion: 0.29
Nodes (7): M3.1 Three mechanisms, and what each actually covers, M3.2 Testing each precondition in isolation, M3.3 Affirmation parsing, and why it is a whitelist, M3.4 Adversarial evaluation of the confirmation step, M3.5 Corrections, declines, and the distinction between them, M3.6 Export, M3. The write path

### Community 53 - "M4. Extraction"
Cohesion: 0.29
Nodes (7): M4.1 The model's output is bounded by a schema, not by instruction, M4.2 Intent is separated from value, M4.3 Two deterministic checks on the model's output, M4.4 What the offline corpus can and cannot measure, M4.5 The extractor does not repair, M4.6 Live testing, M4. Extraction

### Community 54 - "M5. Orchestration and read-back"
Cohesion: 0.29
Nodes (7): M5.1 The orchestrator makes no judgements, M5.2 Read-back as an audibility problem, M5.3 Read-back detects a class of error nothing else can, M5.4 Asking for an explanation is not a failed attempt, M5.5 The simulated user, M5.6 Localisation of what the user hears, M5. Orchestration and read-back

### Community 55 - "Candidate"
Cohesion: 0.15
Nodes (17): RuntimeError, A write was attempted that did not satisfy the commit invariant. Raised, never…, SilentWriteBlocked, Candidate, A proposed value. Explicitly *not* a form value. Frozen: a receipt is bound to…, The central case. A held receipt must not authorise a value it was not issued…, SPEC.md section 2: a blocked write is a research finding, and a non-zero count…, Holding a receipt for the first value does not authorise the second. (+9 more)

### Community 56 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 57 - "suggest.py"
Cohesion: 0.18
Nodes (14): difflib, LF-005 — Income band not derived from an amount, amount_band(), _email(), email_typo(), parse_amount(), Suggestions for a rejected value (ISSUES.md LF-005, LF-009, LF-004). A…, Rupees per year stated in `text`, or None if it holds no clear amount. "45… (+6 more)

### Community 58 - "LucidForm"
Cohesion: 0.12
Nodes (14): Commands, Conventions, Environment, graphify, LucidForm, Non-negotiables, Paper, Phase 3 notes (+6 more)

### Community 59 - "M1. Implementation notes — instrumentation and corpus"
Cohesion: 0.33
Nodes (6): M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 61 - "Aggregate"
Cohesion: 0.14
Nodes (6): Phase 5 notes, Aggregate, True if no session called a real model., Figures that must not be read as results, given how they were produced. Printed…, Of the wrong values proposed, how many did the gate reject?, Of the correct values proposed, how many did the gate wrongly reject? The…

### Community 62 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 63 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 64 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 65 - "Settings"
Cohesion: 0.23
Nodes (5): BaseSettings, Path, Settings, test_sdk_key_variables_are_read_without_the_project_prefix(), test_the_default_provider_is_gemini_and_the_model_is_config()

### Community 66 - "golden_sessions.py"
Cohesion: 0.24
Nodes (10): json, main(), Record what a persona session does, minus what legitimately varies per run. The…, record(), _scrub(), golden(), fixture, parametrize (+2 more)

### Community 69 - "build_official_layout.py"
Cohesion: 0.15
Nodes (20): collections, csv, pdfplumber, cells(), date_slot(), main(), address_block(), doc_numbers() (+12 more)

### Community 70 - "base.py"
Cohesion: 0.21
Nodes (7): InputChannel, OutputChannel, Protocol, The boundary between the pipeline and however the user is actually talking. The…, State a validated value for confirmation. `value` is the exact string that will…, Return what the user said, or None if there is nothing further. None means the…, test_the_fakes_satisfy_the_channel_protocols()

### Community 71 - "Kind"
Cohesion: 0.18
Nodes (7): Kind, What sort of thing is being said, for channels that present them differently., Puppet, A channel driven by a fixed list of replies. Records what was said., Every turn costs an attempt; the field is abandoned; the session still closes., test_a_model_that_always_fails_ends_the_session_cleanly(), test_a_question_is_answered_by_the_help_agent_and_never_becomes_a_value()

### Community 72 - "pytest"
Cohesion: 0.15
Nodes (14): Canvas, build(), _header(), _overlay(), Path, Generate the target fillable PDF (AcroForm). The prototype's form reproduces…, pytest, reportlab_lib_colors (+6 more)

### Community 75 - "models.py"
Cohesion: 0.15
Nodes (17): contextlib, dataclasses, datetime, enum, Append-only session event log -- the evaluation substrate. One record per…, The confirmation receipt: the capability that authorises a write. A receipt is…, Form state: the single write path. This module is the first of the three…, Export confirmed values into the AcroForm PDF. The exporter is deliberately… (+9 more)

### Community 78 - "test_gate.py"
Cohesion: 0.07
Nodes (36): ValidationReport, candidate(), gate(), fixture, Gate-level invariants: the contract the rest of the pipeline relies on. Phase 2…, A rejection must not colour the next verdict. The gate is used in a loop over…, Construction order and instance identity must not matter., An unreachable reason code would be a column in the results table that always… (+28 more)

### Community 79 - "FormState"
Cohesion: 0.11
Nodes (8): CommitRecord, DeclineRecord, FormState, Committed or explicitly declined -- either way, we are done asking., One entry in the append-only history of what was written and why., An optional field the user chose not to answer. Recorded distinctly from an…, Confirmed values for one form-filling session., Read-only view. Handing out the dict itself would be a second write path, since…

### Community 80 - "Session"
Cohesion: 0.24
Nodes (11): Session, fixture, Regression tests for docs/ISSUES.md LF-006: revisit missing fields, final…, schema(), test_a_hedged_yes_does_not_approve(), test_a_missing_field_is_asked_again_before_the_end(), test_an_unclear_review_reply_asks_again(), test_change_a_field_at_the_review() (+3 more)

### Community 81 - "FieldSpec"
Cohesion: 0.11
Nodes (18): LF-002 — Weak Aadhaar validation, Stage 3: an utterance becomes a candidate. A candidate is a *proposal*. Nothing…, build(), build_user_message(), The extraction prompt. Built per field, from the schema the form parser…, Return (system, user) for one extraction., enum_error(), format_error() (+10 more)

### Community 82 - "test_issues_phase8.py"
Cohesion: 0.24
Nodes (10): official(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-015: help for document numbers. The…, run(), test_help_matches_the_chosen_document(), test_how_to_get_the_document_question_gets_lookup_help(), test_no_document_reopens_the_choice() (+2 more)

### Community 83 - "Extractor"
Cohesion: 0.09
Nodes (16): ExtractionClient, ModelReply, Path, Protocol, Replays recorded model responses from disk, keyed by field and utterance. Lets…, One model response, plus what it cost., Anything that can turn a prompt into an `Extraction`., ReplayClient (+8 more)

### Community 84 - "Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms"
Cohesion: 0.50
Nodes (3): A: Form No. 93 – PAN Application Form for Individual (Being citizen of India), FAQ's on PAN, Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms

### Community 85 - "LucidForm"
Cohesion: 0.20
Nodes (10): A real session, Documentation, How it works, LucidForm, Project layout, Quickstart, Results, Team (+2 more)

### Community 86 - "Team workflow (5 people, each with their own AI assistant)"
Cohesion: 0.40
Nodes (4): Handing off to another AI, One-time setup, Per phase, Team workflow (5 people, each with their own AI assistant)

### Community 87 - "M8. The help agent"
Cohesion: 0.33
Nodes (6): M8.1 Scope: explanation, never a value, M8.2 Corpus and chunking, M8.3 Hybrid retrieval, M8.4 The citation check, M8.5 Evaluation, and what it does not measure, M8. The help agent

### Community 89 - "make_genai_client"
Cohesion: 0.29
Nodes (3): GeminiAnswerClient, make_genai_client(), The one place credentials for Gemini are resolved.

### Community 90 - "III. System Architecture"
Cohesion: 0.25
Nodes (8): A. The five-stage pipeline, B. The validation gate and its rejection taxonomy, C. Extraction as a structurally bounded model call, D. Read-back and the confirmation whitelist, E. Three independent enforcement mechanisms, F. The orchestrator as a declared state graph, G. A help agent that cannot write, III. System Architecture

### Community 91 - "ConfirmationReceipt"
Cohesion: 0.12
Nodes (17): Committed values that differ from ground truth. The correctness invariant, not…, ConfirmationReceipt, True if this receipt authorises writing exactly this value., Proof that one specific candidate was validated and explicitly affirmed.…, Affirmation, The user's response to a read-back. `explicit` is True only for an unambiguous,…, 1. Intent, 2. The gating contract — the thesis of the project (+9 more)

### Community 92 - "load_all"
Cohesion: 0.15
Nodes (16): _is_correct(), Is this proposed value the right answer? Compared after normalisation, using…, __iter__(), load_all(), load_persona(), Persona, PersonaError, Path (+8 more)

### Community 93 - "_Pages"
Cohesion: 0.31
Nodes (3): _Pages, One reportlab canvas per PDF page, drawn in PDF user space (origin bottom-left)., One character per box; if it does not fit, shrink across the whole span.

### Community 94 - "load_set"
Cohesion: 0.40
Nodes (5): load_set(), Path, write(), A gold label that matches nothing would score a correct retrieval as a miss., test_every_gold_label_exists_in_the_corpus()

### Community 96 - "Progress log"
Cohesion: 0.29
Nodes (6): 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5, 2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper, 2026-09-30 (night) · Shubh (+Claude) · Pre-push audit, 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs, 2026-10-01 — Review fixes LF-001..LF-010 (Yashvardhan, with Claude Code), Progress log

### Community 98 - "Live demo — 5 minutes, terminal only"
Cohesion: 0.40
Nodes (4): Backup commands (if the network is slow), Live demo — 5 minutes, terminal only, Script — what to type, and what to point out, The one-line pitch while it runs

### Community 99 - "Team guide"
Cohesion: 0.29
Nodes (7): 1. The idea in 60 seconds, 2. Who does what, 3. Setup, 4. The loop for every phase, 5. Saving tokens with graphify, 6. Rules nobody (human or AI) breaks, Team guide

### Community 100 - ".commit"
Cohesion: 0.14
Nodes (12): AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate, Code map, Invariants — never break these (the test suite enforces them), Run, What this is, Working rules for agents, Personas and live evaluation, LF-008 — "I don't have a PAN" skips a required field (+4 more)

### Community 101 - "LucidForm — Methodology"
Cohesion: 0.33
Nodes (5): LucidForm — Methodology, M7.1 Why replace a working loop, M7.2 Parity, not intuition, M7.3 No checkpoint-resume, M7. The orchestrator as a state graph

### Community 102 - "metrics.py"
Cohesion: 0.08
Nodes (30): FieldOutcome, load_sessions(), outcome(), _pct(), percentile(), _personas(), Any, Path (+22 more)

### Community 103 - "spell"
Cohesion: 0.40
Nodes (5): Render a value character by character, digits as words. Letters are upper-cased…, spell(), test_spell_groups_evenly_and_keeps_the_remainder(), test_spell_ignores_whitespace_in_the_source_value(), test_spell_without_grouping()

### Community 104 - "test_a_failed_model_call_is_an_unclear_turn_not_a_crash"
Cohesion: 0.40
Nodes (3): FailingClient, parametrize, test_a_failed_model_call_is_an_unclear_turn_not_a_crash()

### Community 105 - "passing"
Cohesion: 0.50
Nodes (4): gate(), passing(), fixture, A candidate that has genuinely passed validation. Using a real verdict rather…

### Community 106 - "build"
Cohesion: 0.50
Nodes (4): build(), Path, bank(), fixture

### Community 108 - "test_a_form_is_filled_over_the_voice_channel"
Cohesion: 0.50
Nodes (3): The Phase 7 claim, asserted. The orchestrator, gate, confirmation step, and…, test_a_form_is_filled_over_the_voice_channel(), read_back()

### Community 110 - "chunks"
Cohesion: 0.67
Nodes (3): chunks(), fixture, schema()

### Community 115 - "pathlib"
Cohesion: 0.10
Nodes (22): functools, hashlib, io, Settings. Model id is config, never hardcoded -- the extraction-accuracy sweep…, Write confirmed values onto the official CKYC form (ISSUES.md LF-001). The…, A one-page PDF carrying a large diagonal watermark., _stamp_page(), _passages() (+14 more)

## Knowledge Gaps
- **182 isolated node(s):** `fs`, `path`, `{
  Document, Packer, Paragraph, TextRun, AlignmentType, SectionType, Table, TableRow,
  TableCell, WidthType, BorderStyle, ShadingType, LevelFormat,
}`, `ROOT`, `SRC` (+177 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 828 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Candidate` connect `Candidate` to `Event`, `test_formstate.py`, `SessionGraph`, `test_issues_phase1.py`, `test_confirm.py`, `asr_probe.py`, `cli.py`, `test_writer.py`, `ValidationGate`, `test_issues_phase7.py`, `test_gate_crossfield.py`, `test_voice.py`, `test_adversarial.py`, `test_issues_phase2.py`, `test_issues_phase5.py`, `Status`, `LucidForm`, `models.py`, `test_gate.py`, `FormState`, `FieldSpec`, `Extractor`, `III. System Architecture`, `ConfirmationReceipt`, `.commit`, `passing`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `ValidationGate` connect `ValidationGate` to `test_formstate.py`, `test_issues_phase1.py`, `test_confirm.py`, `asr_probe.py`, `cli.py`, `test_writer.py`, `test_extraction.py`, `test_issues_phase7.py`, `test_gate_crossfield.py`, `loader.py`, `test_voice.py`, `test_checksums.py`, `replay.py`, `one_field`, `test_adversarial.py`, `test_session.py`, `test_issues_phase2.py`, `test_issues_phase5.py`, `Extraction`, `Status`, `Candidate`, `base.py`, `Kind`, `models.py`, `test_gate.py`, `Session`, `FieldSpec`, `test_issues_phase8.py`, `passing`, `test_a_form_is_filled_over_the_voice_channel`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M8. The help agent`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `ValidationGate` (e.g. with `asr_probe_cmd()` and `extract_cmd()`) actually correct?**
  _`ValidationGate` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Candidate` (e.g. with `Invariants — never break these (the test suite enforces them)` and `Conventions`) actually correct?**
  _`Candidate` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `FormState` (e.g. with `run_cmd()` and `ReplayRun`) actually correct?**
  _`FormState` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 46 inferred relationships involving `Status` (e.g. with `extract_cmd()` and `gate_check()`) actually correct?**
  _`Status` has 46 INFERRED edges - model-reasoned connections that need verification._