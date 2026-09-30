# Graph Report - LucidForm  (2026-10-01)

## Corpus Check
- 119 files · ~270,932 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .jsonl 17, (none) 4, .example 1)

## Summary
- 1987 nodes · 4542 edges · 109 communities (99 shown, 10 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 421 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `21437f03`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_gate_rules.py
- EventLog
- test_formstate.py
- test_readback.py
- build.js
- SessionGraph
- MissingString
- test_issues_phase1.py
- test_confirm.py
- readback.py
- test_metrics.py
- cli.py
- test_writer.py
- test_extraction.py
- asr_probe.py
- IV. Methodology
- What You Must Do When Invoked
- FormSchema
- test_issues_phase7.py
- test_no_silent_write.py
- test_gate_crossfield.py
- loader.py
- test_voice.py
- test_personas.py
- voice.py
- PersonaChannel
- test_session.py
- test_schema_loader.py
- Title (pick one, or tell me to try again)
- Candidate
- HelpAgent
- probe
- VoiceChannel
- HelpIndex
- corpus.py
- ExtractionOutcome
- Intent
- grounding.py
- Status
- ValidationGate
- pathlib
- test_help.py
- Strings
- write_tables
- Extraction
- M0. System design
- graphify reference: extra exports and benchmark
- test_issues_phase3.py
- M2. The validation gate
- evaluate.py
- Prompt for Claude Code — LucidForm Prototype
- test_llm_clients.py
- M3. The write path
- M4. Extraction
- M5. Orchestration and read-back
- official_writer.py
- graphify reference: query, path, explain
- suggest.py
- LucidForm
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- Aggregate
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- decode_spelled
- graph.py
- Purpose
- graphify reference: GitHub clone and cross-repo merge
- build_official_layout.py
- FieldSpec
- character_error_rate
- get_settings
- .claude/CLAUDE.md
- extraction-spec.md
- gate.py
- test_gate.py
- FormState
- SessionResult
- build
- ISSUES.md — known problems, root causes, and fixes
- Extractor
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- LucidForm
- Team workflow (5 people, each with their own AI assistant)
- M8. The help agent
- uidai_faq_update.md
- models.py
- III. System Architecture
- LucidForm — Specification
- Persona
- _Pages
- field_named
- README.md
- Progress log
- build_pin_directory.py
- Live demo — 5 minutes, terminal only
- Team guide
- AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate
- LucidForm — Methodology
- metrics.py
- _whole_number
- test_a_failed_model_call_is_an_unclear_turn_not_a_crash
- passing
- percentile
- answer.py

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 76 edges
2. `Candidate` - 69 edges
3. `Status` - 65 edges
4. `FormState` - 63 edges
5. `get_settings()` - 50 edges
6. `EventLog` - 50 edges
7. `Extraction` - 49 edges
8. `load()` - 49 edges
9. `Event` - 47 edges
10. `Extractor` - 47 edges

## Surprising Connections (you probably didn't know these)
- `The guarantee is enforced, not promised` --references--> `ConfirmationReceipt`  [INFERRED]
  README.md → lucidform/formstate/receipt.py
- `Three enforcement mechanisms` --references--> `ConfirmationReceipt`  [INFERRED]
  SPEC.md → lucidform/formstate/receipt.py
- `Commit invariant` --references--> `SilentWriteBlocked`  [INFERRED]
  SPEC.md → lucidform/formstate/state.py
- `Conventions` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py
- `A. The five-stage pipeline` --references--> `Candidate`  [INFERRED]
  docs/paper-draft.md → lucidform/models.py

## Import Cycles
- None detected.

## Communities (109 total, 10 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.06
Nodes (66): LF-002 — Weak Aadhaar validation, enum_error(), format_error(), is_placeholder_number(), length_error(), normalize(), parse_date(), placeholder_error() (+58 more)

### Community 1 - "EventLog"
Cohesion: 0.08
Nodes (44): Event, EventLog, _jsonable(), Any, Path, str, Time a stage and emit once it completes. Mutate the yielded dict to attach the…, Read one session log. Used by metrics and by tests; never by the pipeline. (+36 more)

### Community 2 - "test_formstate.py"
Cohesion: 0.07
Nodes (47): RuntimeError, A write was attempted that did not satisfy the commit invariant. Raised, never…, SilentWriteBlocked, forge(), gate(), make(), fixture, The single write path, and every way of getting round it that I could think of.… (+39 more)

### Community 3 - "test_readback.py"
Cohesion: 0.15
Nodes (26): field(), fixture, Read-back rendering: can the user actually check this by ear? For a user who…, A listener can check "example dot invalid" without hearing it letter by letter,…, Spelling a name the user just said would be tedious and no clearer., Presentation differs; the value does not. If rendering altered the value, the…, AKQPS3417M" spoken as a word is an unpronounceable noise that no listener can…, A synthesiser reading "3417" says "three thousand four hundred and seventeen",… (+18 more)

### Community 4 - "build.js"
Cohesion: 0.08
Nodes (33): docx, ref_fs, ref_path, authorsTable(), body(), bodyBlocks(), COL_W, doc (+25 more)

### Community 5 - "SessionGraph"
Cohesion: 0.19
Nodes (5): LF-006 — Session ends incomplete, no final review, Runs one `Session` through the graph. Holds the stateful collaborators., SessionGraph, TurnState, TypedDict

### Community 6 - "MissingString"
Cohesion: 0.40
Nodes (4): KeyError, MissingString, A string key is absent from the requested language's table., Look up a key and fill in its placeholders.

### Community 7 - "test_issues_phase1.py"
Cohesion: 0.18
Nodes (23): check(), Ground an extraction against the utterance it claims to come from. Only value-…, FieldType, _extraction(), _gate(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-002, LF-007, LF-008. Inputs are taken… (+15 more)

### Community 8 - "test_confirm.py"
Cohesion: 0.07
Nodes (38): RuntimeError, A receipt was constructed outside the confirmation module., UnauthorizedIssuer, confirm(), normalize_utterance(), parse_affirmation(), Lowercase, strip punctuation and filler, collapse whitespace. Apostrophes…, Decide whether an utterance is an explicit confirmation. Returns an… (+30 more)

### Community 9 - "readback.py"
Cohesion: 0.15
Nodes (15): Rendering a validated value so a person can check it by ear. This is the last…, The value, as it should be heard., The full read-back sentence. `template` comes from the string table so the…, Render a value character by character, digits as words. Letters are upper-cased…, Emails are spoken with 'at' and 'dot', and the local part spelled out. The…, render(), render_value(), spell() (+7 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.06
Nodes (29): agg(), fixture, The measures, and the guards on how they may be read. Every number reported in…, Six deliberate errors are planted across the three personas., The headline table must balance. A wrong value is stopped by the gate, stopped…, The correctness invariant. A defect, not a finding., The evidence that the read-back is a stage rather than a courtesy. These are…, A false positive is a real user told their correct answer is wrong. (+21 more)

### Community 11 - "cli.py"
Cohesion: 0.08
Nodes (43): command, asr_probe_cmd(), extract_cmd(), _extraction_client(), gate_check(), graph_cmd(), _help_agent(), help_ask() (+35 more)

### Community 12 - "test_writer.py"
Cohesion: 0.12
Nodes (30): graphify reference: transcribe video and audio, Step 2.5 - Transcribe video / audio files (only if video files detected), export(), Path, Read the filled values out of an exported PDF. Used by the tests to verify that…, Write the confirmed values into a copy of the blank form. The template is never…, read_back(), commit() (+22 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.08
Nodes (39): Help agent (RAG), extractor(), gate(), fixture, Stage 3: utterance to candidate. No network. Every test here runs against a…, Belt and braces: intent says value, but there is none to propose., A value the model did not take from what the user said. This is the…, End to end: grounding failure reaches a rejection with a reason. (+31 more)

### Community 14 - "asr_probe.py"
Cohesion: 0.20
Nodes (8): is_simulated(), ProbeResult, ProbeSummary, Does an identifier survive being spoken and heard? METHODOLOGY M0.5 asserts…, Corrupted identifiers the gate accepted. The set that matters. Every one of…, report(), rows(), test_a_real_recogniser_would_not_be_labelled_simulated()

### Community 15 - "IV. Methodology"
Cohesion: 0.33
Nodes (6): A. Form representation, B. Synthetic data and its construction, C. Adversarial evaluation corpora, D. Evaluation harness and its honesty constraints, E. Help-agent evaluation, IV. Methodology

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

### Community 18 - "test_issues_phase7.py"
Cohesion: 0.08
Nodes (39): _choose_pdf(), Ask whether to use the user's own PDF and read it (ISSUES.md LF-014). Returns a…, _clean(), CustomForm, _is_official(), _label(), _norm(), open_form() (+31 more)

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.12
Nodes (28): ast, Module, _help_violations(), _imported_names(), _parse(), parametrize, Path, _python_files() (+20 more)

### Community 20 - "test_gate_crossfield.py"
Cohesion: 0.06
Nodes (55): LF-003 — PIN / city / state mismatch accepted, check(), _city_agrees(), city_matches_pin_and_state(), CrossFieldResult, doc_number_matches_type(), _or(), pan_matches_surname() (+47 more)

### Community 21 - "loader.py"
Cohesion: 0.14
Nodes (24): _build(), _inherited(), load(), load_official(), load_overlay(), parse_acroform(), Any, Path (+16 more)

### Community 22 - "test_voice.py"
Cohesion: 0.12
Nodes (24): CorruptingRecognizer, EchoRecognizer, Returns text handed to it. Lets the channel be tested without audio., Applies documented speech-recognition error patterns, deterministically. **This…, Writes a valid but silent WAV. Exercises the file path without a voice., SilentSynthesizer, personas(), fixture (+16 more)

### Community 23 - "test_personas.py"
Cohesion: 0.06
Nodes (43): aadhaar_valid(), corrupt_one_digit(), Checksum primitives for the validation gate. Pure functions over strings. No…, True if `digits` (including its trailing check digit) satisfies Verhoeff., Check digit for a payload that does not yet carry one., Structural + checksum validity of a 12-digit Aadhaar number. The first digit is…, Generate a checksum-valid but entirely fabricated Aadhaar number. Used only to…, Change exactly one digit, producing a checksum-invalid variant. The single-… (+35 more)

### Community 24 - "voice.py"
Cohesion: 0.13
Nodes (13): FasterWhisperRecognizer, PiperSynthesizer, RuntimeError, The voice channel: speech in, speech out, pipeline unchanged. Phase 7 of the…, Local speech synthesis via Piper. Invoked as a subprocess rather than through a…, A speech backend was requested but is not installed., Local speech recognition via faster-whisper (CTranslate2). Local and pinned…, VoiceBackendMissing (+5 more)

### Community 25 - "PersonaChannel"
Cohesion: 0.16
Nodes (7): Phase 4 notes, PersonaChannel, Agree only if the value read back matches ground truth., One exchange, kept for the transcript., A simulated user, driven by a persona's script. Implements both protocols: it…, Turn, What to call this field out loud. An English label inside a Hindi read-back is…

### Community 26 - "test_session.py"
Cohesion: 0.06
Nodes (59): Kind, What sort of thing is being said, for channels that present them differently., test_session_rejects_the_shortened_aadhaar(), test_offered_band_denied_is_not_saved(), test_offered_band_needs_a_yes(), test_only_one_suggestion_per_utterance(), Regression tests for docs/ISSUES.md LF-012: "I have a PAN but can't find the…, test_aadhaar_find_help_uses_uidai() (+51 more)

### Community 27 - "test_schema_loader.py"
Cohesion: 0.07
Nodes (26): built_pdf(), overlay(), fixture, parametrize, Round-trip: the generator writes the AcroForm, the loader reads it back.…, A field the PDF does not have must raise, not be skipped. A silently dropped…, One spoken name for two options would make the gate choose for the user., Conversely, a PDF widget nothing validates must raise. (+18 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.25
Nodes (8): I. Introduction, II. Related Work, References, Title (pick one, or tell me to try again), V. Algorithm and Pseudocode, VI. Results, VII. Discussion, VIII. Conclusion and Future Work

### Community 29 - "Candidate"
Cohesion: 0.09
Nodes (22): Validate one candidate against the schema and confirmed values. `committed`…, Candidate, Check, A proposed value. Explicitly *not* a form value. Frozen: a receipt is bound to…, One executed validation check. Recorded whether it passed or failed, so the log…, Closed rejection taxonomy. Every rejection carries exactly one. Each member…, Reason, _candidate() (+14 more)

### Community 30 - "HelpAgent"
Cohesion: 0.13
Nodes (10): AnswerClient, HelpAgent, HelpAnswer, Protocol, _question_lines(), emit(), FAQ pages where a question is a line ending in '?' followed by its answer., The embedding call is a live API call too; it sits inside the fallback. (+2 more)

### Community 31 - "probe"
Cohesion: 0.16
Nodes (13): Path, Protocol, What the recogniser heard. `confidence` is the recogniser's own estimate where…, SpeechRecognizer, SpeechSynthesizer, Transcript, _category(), probe() (+5 more)

### Community 32 - "VoiceChannel"
Cohesion: 0.24
Nodes (6): One audio exchange, retained for the transcript and for error analysis., Speech in, speech out, over the same protocols as the console. Audio input is…, VoiceChannel, VoiceTurn, The gate must stay installable and testable without a gigabyte of model…, test_the_module_imports_without_any_speech_library()

### Community 33 - "HelpIndex"
Cohesion: 0.14
Nodes (14): Chunk, _corpus_digest(), Embedder, HashEmbedder, HelpIndex, _normalise(), Path, Protocol (+6 more)

### Community 34 - "corpus.py"
Cohesion: 0.18
Nodes (14): html, _clean(), _flat(), _html_text(), load_chunks(), load_manifest(), _pdf_text(), Path (+6 more)

### Community 36 - "Intent"
Cohesion: 0.11
Nodes (23): json, build(), _clean_extraction(), Any, Path, Build the offline extraction fixture corpus. python -m lucidform.eval.fixtures…, The straightforward case: the value was stated and heard correctly., write() (+15 more)

### Community 37 - "grounding.py"
Cohesion: 0.15
Nodes (19): LF-007 — Model silently drops/changes digits, clamp_confidence(), digits_agree(), Grounding, locate(), _loose(), Deterministic checks on the model's output, performed without the model. The…, The digit string a quote spells out, or None if it cannot be read that way. (+11 more)

### Community 38 - "Status"
Cohesion: 0.21
Nodes (16): str, Status, About three lakh" must not become "1-5 Lakh" inside the extractor., test_replaying_an_out_of_enum_income_is_rejected_not_mapped(), _gate(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-003: PIN / city / state consistency. The… (+8 more)

### Community 39 - "ValidationGate"
Cohesion: 0.08
Nodes (23): Deterministic accept/reject on a single candidate value., ValidationGate, _drawn(), _gate(), parametrize, Regression tests for docs/ISSUES.md LF-001: filling the official CKYC form., (text, x, y_from_top) for every string drawn on the page, via pypdf., Characters drawn inside one row of boxes, left to right. (+15 more)

### Community 40 - "pathlib"
Cohesion: 0.12
Nodes (16): functools, Settings. Model id is config, never hardcoded -- the extraction-accuracy sweep…, __iter__(), PersonaError, RuntimeError, Synthetic persona loading. A persona is a fabricated user: ground-truth field…, A persona is internally inconsistent. Always fatal. A persona whose ground…, String table loading. Keys are looked up strictly. A missing key raises rather… (+8 more)

### Community 41 - "test_help.py"
Cohesion: 0.09
Nodes (24): HelpReply, BaseModel, The model's entire permitted output., Returns the replies handed to it; an Exception in the list is raised., ScriptedAnswerClient, reciprocal_rank_fusion(), The help agent: answers a user's question about a field from official…, agent() (+16 more)

### Community 42 - "Strings"
Cohesion: 0.10
Nodes (26): available(), load(), The system's own wording, in one language., Strings, LucidForm -- accessibility-first form assistant. The LLM never writes a form…, parametrize, String tables. A missing key must fail loudly. Falling back to another language…, The read-back names the field, so an English label inside a Hindi read-back is… (+18 more)

### Community 43 - "write_tables"
Cohesion: 0.29
Nodes (8): Path, _write_csv(), write_tables(), So a reader can audit the accuracy figure rather than trusting it., test_all_tables_are_written(), test_the_fields_table_records_ground_truth_beside_what_was_committed(), test_the_summary_is_a_single_row(), test_the_turns_table_has_one_row_per_turn()

### Community 44 - "Extraction"
Cohesion: 0.14
Nodes (12): Extraction, BaseModel, The model's entire permitted output., The structural argument, asserted rather than asserted-in-prose. The reply…, There is no free-text branch for the pipeline to interpret., test_a_reply_that_does_not_fit_the_schema_is_an_error_not_a_fallback(), test_the_model_has_no_field_in_which_to_request_a_write(), test_declining_pan_offers_form_60_and_commits_on_yes() (+4 more)

### Community 45 - "M0. System design"
Cohesion: 0.20
Nodes (10): M0.1 Problem framing, M0.2 The five-stage pipeline, M0.3 Enforcing the constraint rather than asserting it, M0.4 Form representation: parser-assisted, human-verified schema, M0.5 Language selection, M0.6 Deferral of the voice channel, M0.7 Evaluation design, M0.8 Data (+2 more)

### Community 46 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 47 - "test_issues_phase3.py"
Cohesion: 0.20
Nodes (15): _gate(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-004 (email), LF-005 (income), LF-009…, schema(), test_a_suggestion_never_rides_on_a_pass(), test_amount_band(), test_domain_without_mail_is_rejected() (+7 more)

### Community 48 - "M2. The validation gate"
Cohesion: 0.22
Nodes (9): M2.1 Construction order, M2.2 Both directions are asserted, M2.3 Check ordering as a defined quantity, M2.4 Normalization reshapes but does not repair, M2.5 A script-dependent validation trap, M2.6 Cross-field checks and the confirmation dependency, M2.7 The validator does not interpret text, M2.8 Isolation (+1 more)

### Community 49 - "evaluate.py"
Cohesion: 0.12
Nodes (19): gold_matches(), load_set(), Path, Measure the help agent against the hand-written question set. Four numbers,…, A numbered gold ("RBI KYC FAQ, Q1") must equal the label -- a substring test…, Row, run(), summarise() (+11 more)

### Community 50 - "Prompt for Claude Code — LucidForm Prototype"
Cohesion: 0.29
Nodes (6): Context, How I want you to work with me, Non-negotiable design constraint, Prompt for Claude Code — LucidForm Prototype, Scope for THIS prototype (deliberately small), What I need from you, in order

### Community 51 - "test_llm_clients.py"
Cohesion: 0.06
Nodes (34): BaseSettings, Path, Settings, AnthropicExtractionClient, GeminiExtractionClient, make_client(), An extraction provider was named that this build has no client for., The live extraction client for `provider`, or for the configured one. (+26 more)

### Community 52 - "M3. The write path"
Cohesion: 0.29
Nodes (7): M3.1 Three mechanisms, and what each actually covers, M3.2 Testing each precondition in isolation, M3.3 Affirmation parsing, and why it is a whitelist, M3.4 Adversarial evaluation of the confirmation step, M3.5 Corrections, declines, and the distinction between them, M3.6 Export, M3. The write path

### Community 53 - "M4. Extraction"
Cohesion: 0.29
Nodes (7): M4.1 The model's output is bounded by a schema, not by instruction, M4.2 Intent is separated from value, M4.3 Two deterministic checks on the model's output, M4.4 What the offline corpus can and cannot measure, M4.5 The extractor does not repair, M4.6 Live testing, M4. Extraction

### Community 54 - "M5. Orchestration and read-back"
Cohesion: 0.29
Nodes (7): M5.1 The orchestrator makes no judgements, M5.2 Read-back as an audibility problem, M5.3 Read-back detects a class of error nothing else can, M5.4 Asking for an explanation is not a failed attempt, M5.5 The simulated user, M5.6 Localisation of what the user hears, M5. Orchestration and read-back

### Community 55 - "official_writer.py"
Cohesion: 0.15
Nodes (18): io, _address(), export_official(), date, Path, Write confirmed values onto the official CKYC form (ISSUES.md LF-001). The…, Greedy word wrap into lines of the given box counts; the last line takes the…, split_name() (+10 more)

### Community 56 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 57 - "suggest.py"
Cohesion: 0.23
Nodes (11): difflib, LF-005 — Income band not derived from an amount, amount_band(), _email(), email_typo(), parse_amount(), Suggestions for a rejected value (ISSUES.md LF-005, LF-009, LF-004). A…, Rupees per year stated in `text`, or None if it holds no clear amount. "45… (+3 more)

### Community 58 - "LucidForm"
Cohesion: 0.11
Nodes (16): Commands, Conventions, Environment, Gotchas, graphify, LucidForm, Paper, Personas and live evaluation (+8 more)

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

### Community 65 - "decode_spelled"
Cohesion: 0.33
Nodes (6): decode_spelled(), Turn a spelled-out transcript back into a value. The exact inverse of…, The round trip only measures anything if these two agree., oh" for zero and "for" for four are transcription artefacts, not mistakes the…, test_homophones_are_decoded_as_the_digit_they_sound_like(), test_the_decode_is_the_exact_inverse_of_the_read_back()

### Community 66 - "graph.py"
Cohesion: 0.11
Nodes (20): langgraph_graph, _build(), edges(), mermaid(), node_names(), The conversation as a LangGraph state machine. Same stages, same decisions,…, _route(), _structure() (+12 more)

### Community 67 - "Purpose"
Cohesion: 0.18
Nodes (6): Purpose, str, Why the system is listening. The user does not see this; the channel does., Return what the user said, or None if there is nothing further. None means the…, ConsoleChannel, A real person at a terminal. Output is prefixed by kind rather than coloured…

### Community 69 - "build_official_layout.py"
Cohesion: 0.24
Nodes (15): collections, pdfplumber, cells(), date_slot(), main(), address_block(), doc_numbers(), name_row() (+7 more)

### Community 70 - "FieldSpec"
Cohesion: 0.18
Nodes (8): Code map, InputChannel, OutputChannel, Protocol, State a validated value for confirmation. `value` is the exact string that will…, FieldSpec, One form field: structure from the PDF, semantics from the YAML overlay.…, Session

### Community 71 - "character_error_rate"
Cohesion: 0.40
Nodes (5): character_error_rate(), levenshtein(), Edit distance. Implemented rather than imported to avoid a dependency in a…, Edit distance normalised by reference length, case- and space-insensitive., test_character_error_rate_is_zero_for_an_exact_match()

### Community 72 - "get_settings"
Cohesion: 0.19
Nodes (14): Canvas, get_settings(), build(), _header(), _overlay(), Path, Generate the target fillable PDF (AcroForm). The prototype's form reproduces…, reportlab_lib_colors (+6 more)

### Community 75 - "gate.py"
Cohesion: 0.13
Nodes (21): contextlib, dataclasses, datetime, enum, The boundary between the pipeline and however the user is actually talking. The…, Text channels: a console for a person, and a persona for the replay driver.…, Append-only session event log -- the evaluation substrate. One record per…, Path (+13 more)

### Community 78 - "test_gate.py"
Cohesion: 0.08
Nodes (34): candidate(), gate(), fixture, Gate-level invariants: the contract the rest of the pipeline relies on. Phase 2…, A rejection must not colour the next verdict. The gate is used in a loop over…, Construction order and instance identity must not matter., An unreachable reason code would be a column in the results table that always…, Pinned deliberately. The reported reason distribution shifts if this changes,… (+26 more)

### Community 79 - "FormState"
Cohesion: 0.07
Nodes (23): Returns extractions handed to it. For tests that need one exact reply., ScriptedClient, CommitRecord, DeclineRecord, FormState, Committed or explicitly declined -- either way, we are done asking., One entry in the append-only history of what was written and why., An optional field the user chose not to answer. Recorded distinctly from an… (+15 more)

### Community 80 - "SessionResult"
Cohesion: 0.22
Nodes (3): Orchestrator (LangGraph), FieldResult, SessionResult

### Community 81 - "build"
Cohesion: 0.29
Nodes (7): build(), build_user_message(), The extraction prompt. Built per field, from the schema the form parser…, Return (system, user) for one extraction., The prompt must not move validation into the model. A prompt saying "only…, test_enum_prompts_forbid_substituting_the_nearest_option(), test_prompt_carries_the_field_but_asks_for_no_judgement()

### Community 82 - "ISSUES.md — known problems, root causes, and fixes"
Cohesion: 0.18
Nodes (10): Decisions (approved 2026-09-30), ISSUES.md — known problems, root causes, and fixes, LF-001 — Can't fill the official CKYC form, LF-004 — Email only syntax-checked, LF-009 — Near-miss answers get no suggestion, LF-010 — A valid option the model was unsure of is re-asked blindly, LF-011 — Follow-ups (open), LF-012 — "I have a PAN but can't find the number" gets no guidance (+2 more)

### Community 83 - "Extractor"
Cohesion: 0.13
Nodes (12): ExtractionClient, ModelReply, Path, Protocol, Replays recorded model responses from disk, keyed by field and utterance. Lets…, One model response, plus what it cost., Anything that can turn a prompt into an `Extraction`., ReplayClient (+4 more)

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

### Community 89 - "models.py"
Cohesion: 0.13
Nodes (16): _calling_module(), ConfirmationReceipt, The confirmation receipt: the capability that authorises a write. A receipt is…, True if this receipt authorises writing exactly this value., The first module on the stack that is not this one. Walked rather than indexed…, Proof that one specific candidate was validated and explicitly affirmed.…, Affirmation, fingerprint() (+8 more)

### Community 90 - "III. System Architecture"
Cohesion: 0.25
Nodes (8): A. The five-stage pipeline, B. The validation gate and its rejection taxonomy, C. Extraction as a structurally bounded model call, D. Read-back and the confirmation whitelist, E. Three independent enforcement mechanisms, F. The orchestrator as a declared state graph, G. A help agent that cannot write, III. System Architecture

### Community 91 - "LucidForm — Specification"
Cohesion: 0.15
Nodes (12): Non-negotiables, Committed values that differ from ground truth. The correctness invariant, not…, 1. Intent, 2. The gating contract — the thesis of the project, 3. Non-negotiables, 5. Rejection taxonomy, 6. Scope of this prototype, 7. Eval outputs (+4 more)

### Community 92 - "Persona"
Cohesion: 0.22
Nodes (6): _is_correct(), Is this proposed value the right answer? Compared after normalisation, using…, Persona, True when this persona has no value for an optional field., +91 98123 45607" and "9812345607" are the same answer. Judging a proposal on…, test_normalisation_is_applied_before_judging_a_proposal()

### Community 93 - "_Pages"
Cohesion: 0.31
Nodes (3): _Pages, One reportlab canvas per PDF page, drawn in PDF user space (origin bottom-left)., One character per box; if it does not fit, shrink across the whole span.

### Community 94 - "field_named"
Cohesion: 0.40
Nodes (5): field_named(), Index of the field the user named, by its declared aliases or label. Whole-…, parametrize, test_field_named(), test_field_named_does_not_guess()

### Community 96 - "Progress log"
Cohesion: 0.29
Nodes (6): 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5, 2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper, 2026-09-30 (night) · Shubh (+Claude) · Pre-push audit, 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs, 2026-10-01 — Review fixes LF-001..LF-010 (Yashvardhan, with Claude Code), Progress log

### Community 97 - "build_pin_directory.py"
Cohesion: 0.29
Nodes (6): csv, sys, main(), Path, Build lucidform/gate/data/pin_directory.json from the India Post pincode CSV.…, _title()

### Community 98 - "Live demo — 5 minutes, terminal only"
Cohesion: 0.40
Nodes (4): Backup commands (if the network is slow), Live demo — 5 minutes, terminal only, Script — what to type, and what to point out, The one-line pitch while it runs

### Community 99 - "Team guide"
Cohesion: 0.29
Nodes (7): 1. The idea in 60 seconds, 2. Who does what, 3. Setup, 4. The loop for every phase, 5. Saving tokens with graphify, 6. Rules nobody (human or AI) breaks, Team guide

### Community 100 - "AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate"
Cohesion: 0.40
Nodes (5): AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate, Invariants — never break these (the test suite enforces them), Run, What this is, Working rules for agents

### Community 101 - "LucidForm — Methodology"
Cohesion: 0.33
Nodes (5): LucidForm — Methodology, M7.1 Why replace a working loop, M7.2 Parity, not intuition, M7.3 No checkpoint-resume, M7. The orchestrator as a state graph

### Community 102 - "metrics.py"
Cohesion: 0.12
Nodes (19): FieldOutcome, load_sessions(), parse_session(), outcome(), _pct(), _personas(), Reduce session event logs to analysable tables. Reads the append-only JSONL…, Turn one log file into per-turn and per-field records. Turns are delimited by… (+11 more)

### Community 103 - "_whole_number"
Cohesion: 0.50
Nodes (3): LF-013 — A quote cut short inside a number defeats the digit check, The quote, widened to the whole run of digits it sits inside. A model can quote…, _whole_number()

### Community 104 - "test_a_failed_model_call_is_an_unclear_turn_not_a_crash"
Cohesion: 0.40
Nodes (3): FailingClient, parametrize, test_a_failed_model_call_is_an_unclear_turn_not_a_crash()

### Community 105 - "passing"
Cohesion: 0.50
Nodes (4): gate(), passing(), fixture, A candidate that has genuinely passed validation. Using a real verdict rather…

### Community 110 - "percentile"
Cohesion: 0.25
Nodes (7): percentile(), Any, Nearest-rank percentile. Deliberately not interpolated: with the sample sizes a…, Not interpolated. At prototype sample sizes an interpolated percentile reports…, Zero would read as an instantaneous stage rather than an unmeasured one., test_percentile_of_nothing_is_none_not_zero(), test_percentiles_are_values_that_actually_occurred()

### Community 115 - "answer.py"
Cohesion: 0.10
Nodes (21): Extraction clients (Gemini), hashlib, GeminiAnswerClient, _passages(), Answering a user's question about a field, grounded in retrieved passages. The…, GeminiEmbedder, Hit, Hybrid retrieval over the help corpus: dense embeddings + BM25, fused by rank.… (+13 more)

## Knowledge Gaps
- **182 isolated node(s):** `fs`, `path`, `{
  Document, Packer, Paragraph, TextRun, AlignmentType, SectionType, Table, TableRow,
  TableCell, WidthType, BorderStyle, ShadingType, LevelFormat,
}`, `ROOT`, `SRC` (+177 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 823 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Candidate` connect `Candidate` to `EventLog`, `test_formstate.py`, `SessionGraph`, `test_issues_phase1.py`, `test_confirm.py`, `cli.py`, `test_writer.py`, `asr_probe.py`, `test_issues_phase7.py`, `test_gate_crossfield.py`, `test_voice.py`, `probe`, `ExtractionOutcome`, `Status`, `ValidationGate`, `test_issues_phase3.py`, `LucidForm`, `graph.py`, `gate.py`, `test_gate.py`, `FormState`, `Extractor`, `models.py`, `III. System Architecture`, `LucidForm — Specification`, `AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate`, `passing`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `ValidationGate` connect `ValidationGate` to `EventLog`, `test_formstate.py`, `test_issues_phase1.py`, `test_confirm.py`, `cli.py`, `test_writer.py`, `test_extraction.py`, `asr_probe.py`, `FormSchema`, `test_issues_phase7.py`, `test_gate_crossfield.py`, `test_voice.py`, `test_session.py`, `Candidate`, `probe`, `Status`, `test_issues_phase3.py`, `FieldSpec`, `gate.py`, `test_gate.py`, `FormState`, `Extractor`, `models.py`, `passing`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M8. The help agent`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `ValidationGate` (e.g. with `asr_probe_cmd()` and `extract_cmd()`) actually correct?**
  _`ValidationGate` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Candidate` (e.g. with `Invariants — never break these (the test suite enforces them)` and `Conventions`) actually correct?**
  _`Candidate` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 46 inferred relationships involving `Status` (e.g. with `extract_cmd()` and `gate_check()`) actually correct?**
  _`Status` has 46 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `FormState` (e.g. with `run_cmd()` and `ReplayRun`) actually correct?**
  _`FormState` has 12 INFERRED edges - model-reasoned connections that need verification._