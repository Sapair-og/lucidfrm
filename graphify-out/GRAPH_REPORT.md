# Graph Report - LucidForm  (2026-10-01)

## Corpus Check
- 116 files · ~268,042 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .jsonl 17, (none) 4, .example 1)

## Summary
- 1943 nodes · 4377 edges · 119 communities (100 shown, 19 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 411 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `36cc7ef5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_gate_rules.py
- EventLog
- Candidate
- test_readback.py
- build.js
- SessionGraph
- MissingString
- test_issues_phase1.py
- test_confirm.py
- readback.py
- test_metrics.py
- cli.py
- FormState
- test_extraction.py
- ProbeSummary
- IV. Methodology
- What You Must Do When Invoked
- ValidationGate
- .commit
- test_no_silent_write.py
- test_gate_crossfield.py
- rules.py
- test_voice.py
- test_personas.py
- voice.py
- PersonaChannel
- test_session.py
- load
- Title (pick one, or tell me to try again)
- test_adversarial.py
- answer.py
- probe
- VoiceChannel
- index.py
- corpus.py
- ExtractionOutcome
- pytest
- range_error
- test_issues_phase2.py
- test_issues_phase5.py
- with_retries
- test_help.py
- test_i18n.py
- write_tables
- Settings
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
- FormSchema
- graphify reference: query, path, explain
- Reason
- LucidForm
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- Aggregate
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- decode_spelled
- run_persona
- Purpose
- graphify reference: GitHub clone and cross-repo merge
- build_official_layout.py
- Extractor
- character_error_rate
- get_settings
- .claude/CLAUDE.md
- extraction-spec.md
- loader.py
- test_gate.py
- test_issues_phase4.py
- length_error
- FieldSpec
- parametrize
- ModelReply
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- LucidForm
- Team workflow (5 people, each with their own AI assistant)
- M8. The help agent
- uidai_faq_update.md
- models.py
- III. System Architecture
- LucidForm — Specification
- test_the_canonical_label_stays_english_for_the_pdf_and_logs
- ScriptedAnswerClient
- test_the_wrong_values_in_the_corpus_are_identified
- README.md
- Progress log
- evaluate.py
- Live demo — 5 minutes, terminal only
- Team guide
- AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate
- LucidForm — Methodology
- metrics.py
- test_the_caveat_survives_into_the_csv
- test_a_failed_model_call_is_an_unclear_turn_not_a_crash
- test_a_question_and_the_answer_after_it_are_separate_turns
- test_a_form_is_filled_over_the_voice_channel
- percentile
- make_client
- strip_invisible
- GeminiEmbedder
- _enum_field
- test_devanagari_digits_do_not_satisfy_the_numeric_patterns
- test_the_layers_account_for_every_wrong_value
- test_nothing_wrong_was_committed
- test_the_gate_rejected_no_correct_value
- test_recall_and_false_positive_rate_are_both_reported
- test_a_tampered_log_is_detected

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 73 edges
2. `Candidate` - 67 edges
3. `Status` - 63 edges
4. `FormState` - 61 edges
5. `Extraction` - 49 edges
6. `load()` - 49 edges
7. `EventLog` - 48 edges
8. `get_settings()` - 47 edges
9. `Event` - 47 edges
10. `Extractor` - 45 edges

## Surprising Connections (you probably didn't know these)
- `The guarantee is enforced, not promised` --references--> `ConfirmationReceipt`  [INFERRED]
  README.md → lucidform/formstate/receipt.py
- `Commit invariant` --references--> `SilentWriteBlocked`  [INFERRED]
  SPEC.md → lucidform/formstate/state.py
- `Conventions` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py
- `A. The five-stage pipeline` --references--> `Candidate`  [INFERRED]
  docs/paper-draft.md → lucidform/models.py
- `Phase 4 notes` --references--> `PersonaChannel`  [INFERRED]
  CLAUDE.md → lucidform/channels/text.py

## Import Cycles
- None detected.

## Communities (119 total, 19 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.15
Nodes (26): normalize(), Canonical form of a value: what gets read back, and what gets committed. The…, field(), fixture, Normalization and single-field rules. The adversarial suite checks verdicts.…, The user said a number; the system cannot be sure which one it heard.…, NFKC folding, so a full-width digit cannot slip past an ASCII range., Reshaping: the subscriber number is unchanged, only the prefix goes. (+18 more)

### Community 1 - "EventLog"
Cohesion: 0.07
Nodes (48): contextlib, Event, EventLog, _jsonable(), Any, Path, str, Append-only session event log -- the evaluation substrate. One record per… (+40 more)

### Community 2 - "Candidate"
Cohesion: 0.07
Nodes (49): RuntimeError, A write was attempted that did not satisfy the commit invariant. Raised, never…, SilentWriteBlocked, Candidate, A proposed value. Explicitly *not* a form value. Frozen: a receipt is bound to…, forge(), gate(), make() (+41 more)

### Community 3 - "test_readback.py"
Cohesion: 0.15
Nodes (26): field(), fixture, Read-back rendering: can the user actually check this by ear? For a user who…, A listener can check "example dot invalid" without hearing it letter by letter,…, Spelling a name the user just said would be tedious and no clearer., Presentation differs; the value does not. If rendering altered the value, the…, AKQPS3417M" spoken as a word is an unpronounceable noise that no listener can…, A synthesiser reading "3417" says "three thousand four hundred and seventeen",… (+18 more)

### Community 4 - "build.js"
Cohesion: 0.08
Nodes (33): docx, ref_fs, ref_path, authorsTable(), body(), bodyBlocks(), COL_W, doc (+25 more)

### Community 5 - "SessionGraph"
Cohesion: 0.06
Nodes (30): Orchestrator (LangGraph), LF-006 — Session ends incomplete, no final review, langgraph_graph, _build(), edges(), field_named(), mermaid(), node_names() (+22 more)

### Community 6 - "MissingString"
Cohesion: 0.40
Nodes (4): KeyError, MissingString, A string key is absent from the requested language's table., Look up a key and fill in its placeholders.

### Community 7 - "test_issues_phase1.py"
Cohesion: 0.05
Nodes (63): difflib, Decisions (approved 2026-09-30), ISSUES.md — known problems, root causes, and fixes, LF-004 — Email only syntax-checked, LF-005 — Income band not derived from an amount, LF-007 — Model silently drops/changes digits, LF-009 — Near-miss answers get no suggestion, LF-010 — A valid option the model was unsure of is re-asked blindly (+55 more)

### Community 8 - "test_confirm.py"
Cohesion: 0.07
Nodes (40): RuntimeError, A receipt was constructed outside the confirmation module., UnauthorizedIssuer, confirm(), normalize_utterance(), parse_affirmation(), Lowercase, strip punctuation and filler, collapse whitespace. Apostrophes…, Decide whether an utterance is an explicit confirmation. Returns an… (+32 more)

### Community 9 - "readback.py"
Cohesion: 0.15
Nodes (15): Rendering a validated value so a person can check it by ear. This is the last…, The value, as it should be heard., The full read-back sentence. `template` comes from the string table so the…, Render a value character by character, digits as words. Letters are upper-cased…, Emails are spoken with 'at' and 'dot', and the local part spelled out. The…, render(), render_value(), spell() (+7 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.12
Nodes (13): agg(), fixture, The measures, and the guards on how they may be read. Every number reported in…, The evidence that the read-back is a stage rather than a courtesy. These are…, The circularity warning must travel with the number., Every commit agrees with the validation verdict in the same turn. Unreachable…, The gap between reported and clamped confidence is itself a measure., schema() (+5 more)

### Community 11 - "cli.py"
Cohesion: 0.09
Nodes (41): command, asr_probe_cmd(), extract_cmd(), _extraction_client(), gate_check(), graph_cmd(), _help_agent(), help_ask() (+33 more)

### Community 12 - "FormState"
Cohesion: 0.08
Nodes (40): graphify reference: transcribe video and audio, Step 2.5 - Transcribe video / audio files (only if video files detected), FormState, Committed or explicitly declined -- either way, we are done asking., Confirmed values for one form-filling session., Read-only view. Handing out the dict itself would be a second write path, since…, export(), ExportError (+32 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.07
Nodes (49): Help agent (RAG), Extraction, Intent, BaseModel, str, What the user was doing, not what they said., The model's entire permitted output., extractor() (+41 more)

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
Cohesion: 0.11
Nodes (8): date, Deterministic accept/reject on a single candidate value., Validate one candidate against the schema and confirmed values. `committed`…, ValidationGate, Check, One executed validation check. Recorded whether it passed or failed, so the log…, test_a_valid_option_the_model_was_unsure_of_is_offered(), test_an_ambiguous_date_is_still_not_offered()

### Community 18 - ".commit"
Cohesion: 0.14
Nodes (10): Personas and live evaluation, LF-008 — "I don't have a PAN" skips a required field, CommitRecord, DeclineRecord, block(), _now(), Write a confirmed value. The sole mutator of form state. Every precondition is…, Record that the user chose not to answer an optional field. Writes no value.… (+2 more)

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.12
Nodes (28): ast, Module, _help_violations(), _imported_names(), _parse(), parametrize, Path, _python_files() (+20 more)

### Community 20 - "test_gate_crossfield.py"
Cohesion: 0.06
Nodes (58): LF-003 — PIN / city / state mismatch accepted, functools, check(), _city_agrees(), city_matches_pin_and_state(), CrossFieldResult, doc_number_matches_type(), _or() (+50 more)

### Community 21 - "rules.py"
Cohesion: 0.18
Nodes (13): LF-002 — Weak Aadhaar validation, enum_error(), format_error(), is_placeholder_number(), placeholder_error(), Normalization and single-field rules. Pure functions over strings, with no…, Right size, wrong shape. Returns a detail, or None if the shape is fine., All one digit, or a straight run up or down (wrapping 9->0). Such numbers pass… (+5 more)

### Community 22 - "test_voice.py"
Cohesion: 0.15
Nodes (20): EchoRecognizer, Returns text handed to it. Lets the channel be tested without audio., Writes a valid but silent WAV. Exercises the file path without a voice., SilentSynthesizer, personas(), fixture, The voice channel, and the claim it exists to test. Every test here runs…, A voice session's log must record what was said and what was heard, or an error… (+12 more)

### Community 23 - "test_personas.py"
Cohesion: 0.05
Nodes (49): PersonaError, RuntimeError, A persona is internally inconsistent. Always fatal. A persona whose ground…, aadhaar_valid(), corrupt_one_digit(), Checksum primitives for the validation gate. Pure functions over strings. No…, True if `digits` (including its trailing check digit) satisfies Verhoeff., Check digit for a payload that does not yet carry one. (+41 more)

### Community 24 - "voice.py"
Cohesion: 0.13
Nodes (13): FasterWhisperRecognizer, PiperSynthesizer, RuntimeError, The voice channel: speech in, speech out, pipeline unchanged. Phase 7 of the…, Local speech synthesis via Piper. Invoked as a subprocess rather than through a…, A speech backend was requested but is not installed., Local speech recognition via faster-whisper (CTranslate2). Local and pinned…, VoiceBackendMissing (+5 more)

### Community 25 - "PersonaChannel"
Cohesion: 0.21
Nodes (5): PersonaChannel, Agree only if the value read back matches ground truth., One exchange, kept for the transcript., A simulated user, driven by a persona's script. Implements both protocols: it…, Turn

### Community 26 - "test_session.py"
Cohesion: 0.07
Nodes (52): Kind, What sort of thing is being said, for channels that present them differently., test_form_60_is_not_committed_without_yes(), test_session_rejects_the_shortened_aadhaar(), test_offered_band_denied_is_not_saved(), test_offered_band_needs_a_yes(), test_only_one_suggestion_per_utterance(), fixture (+44 more)

### Community 27 - "load"
Cohesion: 0.06
Nodes (46): LF-001 — Can't fill the official CKYC form, _build(), _inherited(), load(), load_official(), load_overlay(), parse_acroform(), Any (+38 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.25
Nodes (8): I. Introduction, II. Related Work, References, Title (pick one, or tell me to try again), V. Algorithm and Pseudocode, VI. Results, VII. Discussion, VIII. Conclusion and Future Work

### Community 29 - "test_adversarial.py"
Cohesion: 0.11
Nodes (15): _candidate(), committed(), gate(), fixture, parametrize, The adversarial suite -- the evidence for the safety claim. Every case in…, Every code in the taxonomy needs at least one case. An unexercised reason code…, A rejection-only category cannot distinguish a gate from a brick wall. The… (+7 more)

### Community 30 - "answer.py"
Cohesion: 0.14
Nodes (12): AnswerClient, HelpAgent, HelpAnswer, _passages(), Protocol, Answering a user's question about a field, grounded in retrieved passages. The…, _question_lines(), emit() (+4 more)

### Community 31 - "probe"
Cohesion: 0.13
Nodes (15): CorruptingRecognizer, Path, Protocol, Applies documented speech-recognition error patterns, deterministically. **This…, What the recogniser heard. `confidence` is the recogniser's own estimate where…, SpeechRecognizer, SpeechSynthesizer, Transcript (+7 more)

### Community 32 - "VoiceChannel"
Cohesion: 0.24
Nodes (6): One audio exchange, retained for the transcript and for error analysis., Speech in, speech out, over the same protocols as the console. Audio input is…, VoiceChannel, VoiceTurn, The gate must stay installable and testable without a gigabyte of model…, test_the_module_imports_without_any_speech_library()

### Community 33 - "index.py"
Cohesion: 0.11
Nodes (20): hashlib, Chunk, _corpus_digest(), Embedder, HashEmbedder, HelpIndex, _normalise(), Path (+12 more)

### Community 34 - "corpus.py"
Cohesion: 0.18
Nodes (14): html, _clean(), _flat(), _html_text(), load_chunks(), load_manifest(), _pdf_text(), Path (+6 more)

### Community 36 - "pytest"
Cohesion: 0.12
Nodes (13): enum, The shape the model is allowed to reply in. This schema is a safety boundary,…, os, pytest, Session setup shared by the whole suite. The blank KYC template…, _has_credentials(), The one test that calls a real model. Skipped unless credentials exist.…, The failure mode with the worst consequence, checked against the real model. (+5 more)

### Community 37 - "range_error"
Cohesion: 0.18
Nodes (12): parse_date(), date, range_error(), Well-formed, but outside the permitted domain., Parse an accepted date input. Returns None if it is not a real date. Rejects…, Someone turning 18 today is 18. Someone turning 18 tomorrow is not. An off-by-…, Already reported as a format error -- reporting it twice would mean the reason…, test_future_dates_are_out_of_range() (+4 more)

### Community 38 - "test_issues_phase2.py"
Cohesion: 0.23
Nodes (12): _gate(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-003: PIN / city / state consistency. The…, schema(), test_correct_pairs_pass(), test_directory_lookup(), test_known_city_in_another_state_is_caught() (+4 more)

### Community 39 - "test_issues_phase5.py"
Cohesion: 0.08
Nodes (29): _address(), _Pages, Greedy word wrap into lines of the given box counts; the last line takes the…, One reportlab canvas per PDF page, drawn in PDF user space (origin bottom-left)., One character per box; if it does not fit, shrink across the whole span., split_name(), wrap(), _drawn() (+21 more)

### Community 40 - "with_retries"
Cohesion: 0.18
Nodes (10): _hinted_delay(), json_config(), Shared plumbing for Gemini calls: the client, retries, schema-constrained JSON.…, Seconds from a google.rpc.RetryInfo detail on a 429, if the server sent one., Run `call`, retrying rate limits, transient server errors and transport…, with_retries(), test_a_huge_retry_hint_is_capped(), test_a_rate_limit_retry_delay_hint_is_honoured() (+2 more)

### Community 41 - "test_help.py"
Cohesion: 0.09
Nodes (23): HelpReply, BaseModel, The model's entire permitted output., load_set(), The help agent: answers a user's question about a field from official…, agent(), chunks(), fixture (+15 more)

### Community 42 - "test_i18n.py"
Cohesion: 0.10
Nodes (25): available(), load(), String table loading. Keys are looked up strictly. A missing key raises rather…, The system's own wording, in one language., Strings, LucidForm -- accessibility-first form assistant. The LLM never writes a form…, parametrize, String tables. A missing key must fail loudly. Falling back to another language… (+17 more)

### Community 43 - "write_tables"
Cohesion: 0.25
Nodes (9): Any, Path, _write_csv(), write_tables(), So a reader can audit the accuracy figure rather than trusting it., test_all_tables_are_written(), test_the_fields_table_records_ground_truth_beside_what_was_committed(), test_the_summary_is_a_single_row() (+1 more)

### Community 44 - "Settings"
Cohesion: 0.23
Nodes (5): BaseSettings, Path, Settings, test_sdk_key_variables_are_read_without_the_project_prefix(), test_the_default_provider_is_gemini_and_the_model_is_config()

### Community 45 - "M0. System design"
Cohesion: 0.20
Nodes (10): M0.1 Problem framing, M0.2 The five-stage pipeline, M0.3 Enforcing the constraint rather than asserting it, M0.4 Form representation: parser-assisted, human-verified schema, M0.5 Language selection, M0.6 Deferral of the voice channel, M0.7 Evaluation design, M0.8 Data (+2 more)

### Community 46 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 47 - "Status"
Cohesion: 0.24
Nodes (16): Status, _gate(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-004 (email), LF-005 (income), LF-009…, schema(), test_a_suggestion_never_rides_on_a_pass(), test_amount_band() (+8 more)

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
Cohesion: 0.23
Nodes (12): client_with(), fake_sdk(), FakeModels, rate_limited(), Provider selection and the Gemini extraction client, offline. The Gemini client…, test_a_non_retryable_error_is_raised_immediately(), test_a_rate_limit_is_retried_with_backoff(), test_a_reply_is_parsed_into_the_schema() (+4 more)

### Community 52 - "M3. The write path"
Cohesion: 0.29
Nodes (7): M3.1 Three mechanisms, and what each actually covers, M3.2 Testing each precondition in isolation, M3.3 Affirmation parsing, and why it is a whitelist, M3.4 Adversarial evaluation of the confirmation step, M3.5 Corrections, declines, and the distinction between them, M3.6 Export, M3. The write path

### Community 53 - "M4. Extraction"
Cohesion: 0.29
Nodes (7): M4.1 The model's output is bounded by a schema, not by instruction, M4.2 Intent is separated from value, M4.3 Two deterministic checks on the model's output, M4.4 What the offline corpus can and cannot measure, M4.5 The extractor does not repair, M4.6 Live testing, M4. Extraction

### Community 54 - "M5. Orchestration and read-back"
Cohesion: 0.29
Nodes (7): M5.1 The orchestrator makes no judgements, M5.2 Read-back as an audibility problem, M5.3 Read-back detects a class of error nothing else can, M5.4 Asking for an explanation is not a failed attempt, M5.5 The simulated user, M5.6 Localisation of what the user hears, M5. Orchestration and read-back

### Community 55 - "FormSchema"
Cohesion: 0.14
Nodes (13): io, Settings. Model id is config, never hardcoded -- the extraction-accuracy sweep…, export_official(), date, Path, Write confirmed values onto the official CKYC form (ISSUES.md LF-001). The…, Export confirmed values into the AcroForm PDF. The exporter is deliberately…, A one-page PDF carrying a large diagonal watermark. (+5 more)

### Community 56 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 57 - "Reason"
Cohesion: 0.22
Nodes (9): str, Closed rejection taxonomy. Every rejection carries exactly one. Each member…, Reason, About three lakh" must not become "1-5 Lakh" inside the extractor., test_replaying_an_out_of_enum_income_is_rejected_not_mapped(), An unreachable reason code would be a column in the results table that always…, Pinned deliberately. The reported reason distribution shifts if this changes,…, test_check_order_covers_the_whole_taxonomy() (+1 more)

### Community 58 - "LucidForm"
Cohesion: 0.13
Nodes (13): Commands, Conventions, Environment, Gotchas, graphify, LucidForm, Non-negotiables, Paper (+5 more)

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

### Community 66 - "run_persona"
Cohesion: 0.14
Nodes (17): Path, run_persona(), Path, Replays recorded model responses from disk, keyed by field and utterance. Lets…, ReplayClient, main(), Record what a persona session does, minus what legitimately varies per run. The…, record() (+9 more)

### Community 67 - "Purpose"
Cohesion: 0.20
Nodes (6): Purpose, str, Why the system is listening. The user does not see this; the channel does., Return what the user said, or None if there is nothing further. None means the…, ConsoleChannel, A real person at a terminal. Output is prefixed by kind rather than coloured…

### Community 69 - "build_official_layout.py"
Cohesion: 0.24
Nodes (15): collections, pdfplumber, cells(), date_slot(), main(), address_block(), doc_numbers(), name_row() (+7 more)

### Community 70 - "Extractor"
Cohesion: 0.11
Nodes (17): InputChannel, OutputChannel, Protocol, The boundary between the pipeline and however the user is actually talking. The…, State a validated value for confirmation. `value` is the exact string that will…, Extractor, The conversation: one field at a time, through all five stages. This module is…, Session (+9 more)

### Community 71 - "character_error_rate"
Cohesion: 0.40
Nodes (5): character_error_rate(), levenshtein(), Edit distance. Implemented rather than imported to avoid a dependency in a…, Edit distance normalised by reference length, case- and space-insensitive., test_character_error_rate_is_zero_for_an_exact_match()

### Community 72 - "get_settings"
Cohesion: 0.17
Nodes (15): Canvas, get_settings(), build(), _header(), _overlay(), Path, Generate the target fillable PDF (AcroForm). The prototype's form reproduces…, reportlab_lib_colors (+7 more)

### Community 75 - "loader.py"
Cohesion: 0.11
Nodes (24): dataclasses, json, Text channels: a console for a person, and a persona for the replay driver.…, Does an identifier survive being spoken and heard? METHODOLOGY M0.5 asserts…, build(), _clean_extraction(), Any, Path (+16 more)

### Community 78 - "test_gate.py"
Cohesion: 0.09
Nodes (31): candidate(), gate(), fixture, Gate-level invariants: the contract the rest of the pipeline relies on. Phase 2…, A rejection must not colour the next verdict. The gate is used in a loop over…, Construction order and instance identity must not matter., A value failing several checks reports the earliest one. Deterministic…, Otherwise a malformed value would be reported as a confidence problem, hiding… (+23 more)

### Community 79 - "test_issues_phase4.py"
Cohesion: 0.13
Nodes (15): Returns extractions handed to it. For tests that need one exact reply., ScriptedClient, test_state_is_proposed_from_the_pin_and_needs_a_yes(), fixture, Regression tests for docs/ISSUES.md LF-006: revisit missing fields, final…, schema(), test_a_hedged_yes_does_not_approve(), test_a_missing_field_is_asked_again_before_the_end() (+7 more)

### Community 80 - "length_error"
Cohesion: 0.50
Nodes (4): length_error(), Wrong size. Returns a human-readable detail, or None if the size is fine., test_fixed_length_fields_require_an_exact_length(), test_free_text_fields_have_an_upper_bound_only()

### Community 81 - "FieldSpec"
Cohesion: 0.14
Nodes (11): Phase 4 notes, build(), build_user_message(), The extraction prompt. Built per field, from the schema the form parser…, Return (system, user) for one extraction., FieldSpec, What to call this field out loud. An English label inside a Hindi read-back is…, One form field: structure from the PDF, semantics from the YAML overlay.… (+3 more)

### Community 82 - "parametrize"
Cohesion: 0.33
Nodes (6): parametrize, The correctness invariant. Not a finding -- a build failure. Any entry here…, A blocked write here would mean a defect upstream, not a caught attack --…, test_every_field_is_resolved(), test_no_committed_value_differs_from_ground_truth(), test_no_write_was_blocked_during_a_normal_session()

### Community 83 - "ModelReply"
Cohesion: 0.22
Nodes (4): AnthropicExtractionClient, ModelReply, One model response, plus what it cost., The real client. Uses the SDK's structured-output helper, so the response is…

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
Cohesion: 0.12
Nodes (19): Invariants — never break these (the test suite enforces them), datetime, ConfirmationReceipt, The confirmation receipt: the capability that authorises a write. A receipt is…, True if this receipt authorises writing exactly this value., Proof that one specific candidate was validated and explicitly affirmed.…, Form state: the single write path. This module is the first of the three…, The validation gate. Stage 4 of the pipeline, and the component the project's… (+11 more)

### Community 90 - "III. System Architecture"
Cohesion: 0.25
Nodes (8): A. The five-stage pipeline, B. The validation gate and its rejection taxonomy, C. Extraction as a structurally bounded model call, D. Read-back and the confirmation whitelist, E. Three independent enforcement mechanisms, F. The orchestrator as a declared state graph, G. A help agent that cannot write, III. System Architecture

### Community 91 - "LucidForm — Specification"
Cohesion: 0.20
Nodes (9): Committed values that differ from ground truth. The correctness invariant, not…, ReplayRun, 1. Intent, 3. Non-negotiables, 5. Rejection taxonomy, 6. Scope of this prototype, 7. Eval outputs, Check order (+1 more)

### Community 93 - "ScriptedAnswerClient"
Cohesion: 0.29
Nodes (4): Returns the replies handed to it; an Exception in the list is raised., ScriptedAnswerClient, The embedding call is a live API call too; it sits inside the fallback., test_a_retrieval_failure_never_breaks_the_session()

### Community 96 - "Progress log"
Cohesion: 0.29
Nodes (6): 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5, 2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper, 2026-09-30 (night) · Shubh (+Claude) · Pre-push audit, 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs, 2026-10-01 — Review fixes LF-001..LF-010 (Yashvardhan, with Claude Code), Progress log

### Community 97 - "evaluate.py"
Cohesion: 0.18
Nodes (11): csv, Path, Measure the help agent against the hand-written question set. Four numbers,…, write(), re, sys, main(), Path (+3 more)

### Community 98 - "Live demo — 5 minutes, terminal only"
Cohesion: 0.40
Nodes (4): Backup commands (if the network is slow), Live demo — 5 minutes, terminal only, Script — what to type, and what to point out, The one-line pitch while it runs

### Community 99 - "Team guide"
Cohesion: 0.29
Nodes (7): 1. The idea in 60 seconds, 2. Who does what, 3. Setup, 4. The loop for every phase, 5. Saving tokens with graphify, 6. Rules nobody (human or AI) breaks, Team guide

### Community 100 - "AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate"
Cohesion: 0.33
Nodes (5): AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate, Code map, Run, What this is, Working rules for agents

### Community 101 - "LucidForm — Methodology"
Cohesion: 0.33
Nodes (5): LucidForm — Methodology, M7.1 Why replace a working loop, M7.2 Parity, not intuition, M7.3 No checkpoint-resume, M7. The orchestrator as a state graph

### Community 102 - "metrics.py"
Cohesion: 0.12
Nodes (19): metrics_cmd(), Reduce session logs to CSV tables and print the headline figures., FieldOutcome, _is_correct(), load_sessions(), outcome(), _pct(), _personas() (+11 more)

### Community 104 - "test_a_failed_model_call_is_an_unclear_turn_not_a_crash"
Cohesion: 0.40
Nodes (3): FailingClient, parametrize, test_a_failed_model_call_is_an_unclear_turn_not_a_crash()

### Community 106 - "test_a_form_is_filled_over_the_voice_channel"
Cohesion: 0.50
Nodes (3): The Phase 7 claim, asserted. The orchestrator, gate, confirmation step, and…, test_a_form_is_filled_over_the_voice_channel(), read_back()

### Community 110 - "percentile"
Cohesion: 0.29
Nodes (6): percentile(), Nearest-rank percentile. Deliberately not interpolated: with the sample sizes a…, Not interpolated. At prototype sample sizes an interpolated percentile reports…, Zero would read as an instantaneous stage rather than an unmeasured one., test_percentile_of_nothing_is_none_not_zero(), test_percentiles_are_values_that_actually_occurred()

### Community 111 - "make_client"
Cohesion: 0.21
Nodes (12): Extraction clients (Gemini), GeminiExtractionClient, make_client(), An extraction provider was named that this build has no client for., The live extraction client for `provider`, or for the configured one., The Gemini client, held to the same contract as the Anthropic one. The reply is…, UnknownProvider, extractor() (+4 more)

### Community 112 - "strip_invisible"
Cohesion: 0.40
Nodes (5): Remove characters that render as nothing, then collapse whitespace., strip_invisible(), parametrize, Otherwise they are non-empty to a length check and blank to the user, who would…, test_values_made_only_of_invisible_characters_become_empty()

### Community 115 - "GeminiEmbedder"
Cohesion: 0.20
Nodes (5): GeminiAnswerClient, GeminiEmbedder, `gemini-embedding-001`, with the asymmetric document/query task types., make_genai_client(), The one place credentials for Gemini are resolved.

### Community 116 - "_enum_field"
Cohesion: 0.50
Nodes (4): _enum_field(), U+095B (precomposed ज़) is NFKC-decomposed in the value; the name must be too., test_a_declared_name_does_not_leak_across_options(), test_a_declared_name_is_compared_after_the_same_unicode_normalisation()

## Knowledge Gaps
- **181 isolated node(s):** `fs`, `path`, `{
  Document, Packer, Paragraph, TextRun, AlignmentType, SectionType, Table, TableRow,
  TableCell, WidthType, BorderStyle, ShadingType, LevelFormat,
}`, `ROOT`, `SRC` (+176 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 811 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Candidate` connect `Candidate` to `EventLog`, `SessionGraph`, `test_issues_phase1.py`, `test_confirm.py`, `cli.py`, `FormState`, `ValidationGate`, `.commit`, `test_gate_crossfield.py`, `test_voice.py`, `test_adversarial.py`, `probe`, `ExtractionOutcome`, `test_issues_phase2.py`, `test_issues_phase5.py`, `Status`, `LucidForm`, `Extractor`, `loader.py`, `test_gate.py`, `models.py`, `III. System Architecture`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M8. The help agent`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `FormState` connect `FormState` to `EventLog`, `run_persona`, `Candidate`, `Extractor`, `test_issues_phase2.py`, `test_issues_phase5.py`, `test_a_form_is_filled_over_the_voice_channel`, `loader.py`, `cli.py`, `test_issues_phase4.py`, `.commit`, `test_voice.py`, `FormSchema`, `models.py`, `test_session.py`, `LucidForm — Specification`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `ValidationGate` (e.g. with `asr_probe_cmd()` and `extract_cmd()`) actually correct?**
  _`ValidationGate` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Candidate` (e.g. with `Invariants — never break these (the test suite enforces them)` and `Conventions`) actually correct?**
  _`Candidate` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 45 inferred relationships involving `Status` (e.g. with `extract_cmd()` and `gate_check()`) actually correct?**
  _`Status` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `FormState` (e.g. with `run_cmd()` and `ReplayRun`) actually correct?**
  _`FormState` has 12 INFERRED edges - model-reasoned connections that need verification._