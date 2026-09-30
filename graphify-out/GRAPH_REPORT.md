# Graph Report - LucidForm  (2026-10-01)

## Corpus Check
- 116 files · ~267,580 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .jsonl 17, (none) 4, .example 1)

## Summary
- 1936 nodes · 4358 edges · 126 communities (109 shown, 17 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 406 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9d852948`
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
- render_value
- test_metrics.py
- cli.py
- FormState
- test_extraction.py
- asr_probe.py
- IV. Methodology
- What You Must Do When Invoked
- ValidationGate
- .commit
- test_no_silent_write.py
- test_gate_crossfield.py
- rules.py
- test_voice.py
- test_personas.py
- Candidate
- aadhaar_valid
- test_session.py
- test_schema_loader.py
- Title (pick one, or tell me to try again)
- test_adversarial.py
- answer.py
- voice.py
- VoiceChannel
- index.py
- corpus.py
- Extractor
- Intent
- models.py
- test_issues_phase2.py
- test_issues_phase5.py
- client.py
- test_help.py
- test_i18n.py
- Extraction
- Settings
- M0. System design
- graphify reference: extra exports and benchmark
- Status
- M2. The validation gate
- evaluate.py
- Prompt for Claude Code — LucidForm Prototype
- test_llm_clients.py
- M3. The write path
- M4. Extraction
- M5. Orchestration and read-back
- official_writer.py
- graphify reference: query, path, explain
- loader.py
- Non-negotiables
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- PersonaChannel
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- graph.py
- golden_sessions.py
- Purpose
- graphify reference: GitHub clone and cross-repo merge
- build_official_layout.py
- Session
- suggest.py
- make_form.py
- .claude/CLAUDE.md
- extraction-spec.md
- load_all
- test_gate.py
- test_issues_phase4.py
- EventLog
- FieldSpec
- parametrize
- ModelReply
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- LucidForm
- Team workflow (5 people, each with their own AI assistant)
- M8. The help agent
- uidai_faq_update.md
- ConfirmationReceipt
- III. System Architecture
- LucidForm — Specification
- verhoeff_valid
- ScriptedAnswerClient
- _Pages
- README.md
- Progress log
- json
- Live demo — 5 minutes, terminal only
- Team guide
- AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate
- LucidForm — Methodology
- metrics.py
- pytest
- test_a_failed_model_call_is_an_unclear_turn_not_a_crash
- digits_agree
- test_a_form_is_filled_over_the_voice_channel
- PersonaError
- checksums.py
- percentile
- make_client
- test_phone_country_and_trunk_prefixes_are_stripped
- runs
- ExtractionClient
- GeminiEmbedder
- _enum_field
- test_a_huge_retry_hint_is_capped
- test_devanagari_digits_do_not_satisfy_the_numeric_patterns
- test_the_layers_account_for_every_wrong_value
- test_nothing_wrong_was_committed
- test_the_read_back_caught_what_the_gate_could_not
- test_the_gate_rejected_no_correct_value
- test_recall_and_false_positive_rate_are_both_reported
- test_a_tampered_log_is_detected
- test_turn_records_carry_both_confidence_figures

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

## Communities (126 total, 17 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.11
Nodes (34): normalize(), range_error(), Canonical form of a value: what gets read back, and what gets committed. The…, Well-formed, but outside the permitted domain., field(), fixture, Normalization and single-field rules. The adversarial suite checks verdicts.…, The user said a number; the system cannot be sure which one it heard.… (+26 more)

### Community 1 - "Event"
Cohesion: 0.13
Nodes (27): Event, str, Read one session log. Used by metrics and by tests; never by the pipeline., read_log(), The event log is the evaluation substrate, so its guarantees are tested.…, Null means "not applicable"; zero would mean "instantaneous". Conflating them…, Hindi utterances must not be mangled into escapes. The logs are read by a human…, Not a swallowed error -- a logged finding (SPEC.md section 2). (+19 more)

### Community 2 - "test_formstate.py"
Cohesion: 0.07
Nodes (49): block(), RuntimeError, A write was attempted that did not satisfy the commit invariant. Raised, never…, SilentWriteBlocked, forge(), gate(), make(), fixture (+41 more)

### Community 3 - "test_readback.py"
Cohesion: 0.12
Nodes (31): Render a value character by character, digits as words. Letters are upper-cased…, spell(), field(), fixture, Read-back rendering: can the user actually check this by ear? For a user who…, A listener can check "example dot invalid" without hearing it letter by letter,…, Spelling a name the user just said would be tedious and no clearer., Presentation differs; the value does not. If rendering altered the value, the… (+23 more)

### Community 4 - "build.js"
Cohesion: 0.08
Nodes (33): docx, ref_fs, ref_path, authorsTable(), body(), bodyBlocks(), COL_W, doc (+25 more)

### Community 5 - "SessionGraph"
Cohesion: 0.07
Nodes (26): Orchestrator (LangGraph), Decisions (approved 2026-09-30), ISSUES.md — known problems, root causes, and fixes, LF-001 — Can't fill the official CKYC form, LF-004 — Email only syntax-checked, LF-006 — Session ends incomplete, no final review, LF-008 — "I don't have a PAN" skips a required field, LF-009 — Near-miss answers get no suggestion (+18 more)

### Community 6 - "MissingString"
Cohesion: 0.40
Nodes (4): KeyError, MissingString, A string key is absent from the requested language's table., Look up a key and fill in its placeholders.

### Community 7 - "test_issues_phase1.py"
Cohesion: 0.17
Nodes (21): check(), Ground an extraction against the utterance it claims to come from. Only value-…, FieldType, str, _extraction(), _gate(), fixture, parametrize (+13 more)

### Community 8 - "test_confirm.py"
Cohesion: 0.09
Nodes (28): RuntimeError, A receipt was constructed outside the confirmation module., UnauthorizedIssuer, normalize_utterance(), parse_affirmation(), Lowercase, strip punctuation and filler, collapse whitespace. Apostrophes…, Decide whether an utterance is an explicit confirmation. Returns an…, gate() (+20 more)

### Community 9 - "render_value"
Cohesion: 0.18
Nodes (11): The value, as it should be heard., The full read-back sentence. `template` comes from the string table so the…, Emails are spoken with 'at' and 'dot', and the local part spelled out. The…, render(), render_value(), spell_email(), A read-back that omits which field it is about cannot be checked -- the user…, test_the_hindi_readback_frame_is_used_for_hindi() (+3 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.09
Nodes (17): The measures, and the guards on how they may be read. Every number reported in…, Six deliberate errors are planted across the three personas., The circularity warning must travel with the number., A row lifted out of the CSV into a paper still carries the warning., So a reader can audit the accuracy figure rather than trusting it., Every commit agrees with the validation verdict in the same turn. Unreachable…, A turn is delimited by the ask, not by the logged turn index. An explanation…, test_a_question_and_the_answer_after_it_are_separate_turns() (+9 more)

### Community 11 - "cli.py"
Cohesion: 0.10
Nodes (43): command, asr_probe_cmd(), extract_cmd(), _extraction_client(), gate_check(), graph_cmd(), _help_agent(), help_ask() (+35 more)

### Community 12 - "FormState"
Cohesion: 0.09
Nodes (37): graphify reference: transcribe video and audio, Step 2.5 - Transcribe video / audio files (only if video files detected), FormState, Committed or explicitly declined -- either way, we are done asking., Confirmed values for one form-filling session., Read-only view. Handing out the dict itself would be a second write path, since…, export(), Path (+29 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.09
Nodes (37): Help agent (RAG), extractor(), gate(), fixture, Stage 3: utterance to candidate. No network. Every test here runs against a…, Belt and braces: intent says value, but there is none to propose., A value the model did not take from what the user said. This is the…, End to end: grounding failure reaches a rejection with a reason. (+29 more)

### Community 14 - "asr_probe.py"
Cohesion: 0.11
Nodes (21): _category(), character_error_rate(), decode_spelled(), is_simulated(), levenshtein(), probe(), ProbeResult, ProbeSummary (+13 more)

### Community 15 - "IV. Methodology"
Cohesion: 0.33
Nodes (6): A. Form representation, B. Synthetic data and its construction, C. Adversarial evaluation corpora, D. Evaluation harness and its honesty constraints, E. Help-agent evaluation, IV. Methodology

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (29): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+21 more)

### Community 17 - "ValidationGate"
Cohesion: 0.15
Nodes (3): date, Deterministic accept/reject on a single candidate value., ValidationGate

### Community 18 - ".commit"
Cohesion: 0.29
Nodes (5): Code map, CommitRecord, _now(), Write a confirmed value. The sole mutator of form state. Every precondition is…, One entry in the append-only history of what was written and why.

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.12
Nodes (28): ast, Module, _help_violations(), _imported_names(), _parse(), parametrize, Path, _python_files() (+20 more)

### Community 20 - "test_gate_crossfield.py"
Cohesion: 0.06
Nodes (54): LF-003 — PIN / city / state mismatch accepted, check(), _city_agrees(), city_matches_pin_and_state(), CrossFieldResult, doc_number_matches_type(), _or(), pan_matches_surname() (+46 more)

### Community 21 - "rules.py"
Cohesion: 0.12
Nodes (20): LF-002 — Weak Aadhaar validation, enum_error(), format_error(), is_placeholder_number(), length_error(), parse_date(), placeholder_error(), date (+12 more)

### Community 22 - "test_voice.py"
Cohesion: 0.11
Nodes (26): CorruptingRecognizer, EchoRecognizer, PiperSynthesizer, Local speech synthesis via Piper. Invoked as a subprocess rather than through a…, Returns text handed to it. Lets the channel be tested without audio., Applies documented speech-recognition error patterns, deterministically. **This…, Writes a valid but silent WAV. Exercises the file path without a voice., SilentSynthesizer (+18 more)

### Community 23 - "test_personas.py"
Cohesion: 0.11
Nodes (14): The synthetic corpus must be internally consistent. Accuracy is measured…, The form states an 18-year minimum, and the gate enforces it., A persona who has no email still has to say so out loud. An empty ground truth…, .invalid is reserved by RFC 2606 and can never resolve. A synthetic corpus that…, The data provenance claim in METHODOLOGY M0.8 is only true if the files…, A persona that cannot answer a required field would abandon it mid-run, which…, PAN's fifth character is the surname's first letter. This is the cross-field…, test_email_addresses_use_a_reserved_domain() (+6 more)

### Community 24 - "Candidate"
Cohesion: 0.12
Nodes (17): Validate one candidate against the schema and confirmed values. `committed`…, Candidate, Check, A proposed value. Explicitly *not* a form value. Frozen: a receipt is bound to…, One executed validation check. Recorded whether it passed or failed, so the log…, confirm(), Parse the user's response and, if it is a yes, issue a receipt. This is the…, The case the whole design exists for. (+9 more)

### Community 25 - "aadhaar_valid"
Cohesion: 0.24
Nodes (10): aadhaar_valid(), Structural + checksum validity of a 12-digit Aadhaar number. The first digit is…, Generate a checksum-valid but entirely fabricated Aadhaar number. Used only to…, synthetic_aadhaar(), Issued Aadhaar numbers never begin with 0 or 1. Treated as part of validity…, test_generated_numbers_are_valid(), test_leading_zero_or_one_is_rejected(), test_wrong_length_is_rejected() (+2 more)

### Community 26 - "test_session.py"
Cohesion: 0.06
Nodes (56): Kind, str, What sort of thing is being said, for channels that present them differently., test_session_rejects_the_shortened_aadhaar(), test_offered_band_denied_is_not_saved(), test_offered_band_needs_a_yes(), test_only_one_suggestion_per_utterance(), fixture (+48 more)

### Community 27 - "test_schema_loader.py"
Cohesion: 0.07
Nodes (26): built_pdf(), overlay(), fixture, parametrize, Round-trip: the generator writes the AcroForm, the loader reads it back.…, A field the PDF does not have must raise, not be skipped. A silently dropped…, One spoken name for two options would make the gate choose for the user., Conversely, a PDF widget nothing validates must raise. (+18 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.25
Nodes (8): I. Introduction, II. Related Work, References, Title (pick one, or tell me to try again), V. Algorithm and Pseudocode, VI. Results, VII. Discussion, VIII. Conclusion and Future Work

### Community 29 - "test_adversarial.py"
Cohesion: 0.11
Nodes (15): _candidate(), committed(), gate(), fixture, parametrize, The adversarial suite -- the evidence for the safety claim. Every case in…, Every code in the taxonomy needs at least one case. An unexercised reason code…, A rejection-only category cannot distinguish a gate from a brick wall. The… (+7 more)

### Community 30 - "answer.py"
Cohesion: 0.14
Nodes (12): AnswerClient, HelpAgent, HelpAnswer, _passages(), Protocol, Answering a user's question about a field, grounded in retrieved passages. The…, _question_lines(), emit() (+4 more)

### Community 31 - "voice.py"
Cohesion: 0.10
Nodes (18): FasterWhisperRecognizer, Path, Protocol, RuntimeError, The voice channel: speech in, speech out, pipeline unchanged. Phase 7 of the…, A speech backend was requested but is not installed., What the recogniser heard. `confidence` is the recogniser's own estimate where…, Local speech recognition via faster-whisper (CTranslate2). Local and pinned… (+10 more)

### Community 32 - "VoiceChannel"
Cohesion: 0.24
Nodes (6): One audio exchange, retained for the transcript and for error analysis., Speech in, speech out, over the same protocols as the console. Audio input is…, VoiceChannel, VoiceTurn, The gate must stay installable and testable without a gigabyte of model…, test_the_module_imports_without_any_speech_library()

### Community 33 - "index.py"
Cohesion: 0.12
Nodes (18): hashlib, Chunk, _corpus_digest(), Embedder, HashEmbedder, HelpIndex, _normalise(), Path (+10 more)

### Community 34 - "corpus.py"
Cohesion: 0.16
Nodes (16): html, help_build(), Chunk the official sources and embed them (a few minutes on the free tier)., _clean(), _flat(), _html_text(), load_chunks(), load_manifest() (+8 more)

### Community 35 - "Extractor"
Cohesion: 0.12
Nodes (12): ExtractionOutcome, Extractor, Everything stage 3 produced, including the parts that did not become a value., The corpus's job in one test: an error the extractor faithfully reproduces,…, About three lakh" must not become "1-5 Lakh" inside the extractor., Otherwise the Phase 5 replay driver stalls partway through a session., A missing fixture is a broken corpus, not a model failure -- it must be loud., test_a_replay_corpus_miss_still_raises() (+4 more)

### Community 36 - "Intent"
Cohesion: 0.15
Nodes (15): Intent, str, The shape the model is allowed to reply in. This schema is a safety boundary,…, What the user was doing, not what they said., os, extractor(), _has_credentials(), fixture (+7 more)

### Community 37 - "models.py"
Cohesion: 0.16
Nodes (16): contextlib, dataclasses, datetime, enum, The boundary between the pipeline and however the user is actually talking. The…, Append-only session event log -- the evaluation substrate. One record per…, Stage 3: an utterance becomes a candidate. A candidate is a *proposal*. Nothing…, The confirmation receipt: the capability that authorises a write. A receipt is… (+8 more)

### Community 38 - "test_issues_phase2.py"
Cohesion: 0.23
Nodes (12): _gate(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-003: PIN / city / state consistency. The…, schema(), test_correct_pairs_pass(), test_directory_lookup(), test_known_city_in_another_state_is_caught() (+4 more)

### Community 39 - "test_issues_phase5.py"
Cohesion: 0.10
Nodes (25): Greedy word wrap into lines of the given box counts; the last line takes the…, wrap(), _drawn(), _gate(), official(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-001: filling the official CKYC form. (+17 more)

### Community 40 - "client.py"
Cohesion: 0.16
Nodes (13): Extraction clients (Gemini), GeminiExtractionClient, Model clients for the extraction layer. The extractor talks to a small protocol…, The Gemini client, held to the same contract as the Anthropic one. The reply is…, GeminiAnswerClient, _hinted_delay(), json_config(), make_genai_client() (+5 more)

### Community 41 - "test_help.py"
Cohesion: 0.10
Nodes (22): HelpReply, BaseModel, The model's entire permitted output., reciprocal_rank_fusion(), The help agent: answers a user's question about a field from official…, agent(), chunks(), fixture (+14 more)

### Community 42 - "test_i18n.py"
Cohesion: 0.10
Nodes (26): available(), load(), The system's own wording, in one language., Strings, LucidForm -- accessibility-first form assistant. The LLM never writes a form…, parametrize, String tables. A missing key must fail loudly. Falling back to another language…, The read-back names the field, so an English label inside a Hindi read-back is… (+18 more)

### Community 43 - "Extraction"
Cohesion: 0.11
Nodes (23): clamp_confidence(), Grounding, locate(), _loose(), Deterministic checks on the model's output, performed without the model. The…, Confidence the pipeline will actually use. The model reports its own…, Find the quote in the utterance and return its span. Spans are reported against…, Extraction (+15 more)

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
Cohesion: 0.30
Nodes (13): Status, _gate(), fixture, Regression tests for docs/ISSUES.md LF-004 (email), LF-005 (income), LF-009…, schema(), test_a_suggestion_never_rides_on_a_pass(), test_domain_without_mail_is_rejected(), test_income_rejected_but_band_offered() (+5 more)

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
Cohesion: 0.19
Nodes (13): client_with(), fake_sdk(), FakeModels, rate_limited(), Provider selection and the Gemini extraction client, offline. The Gemini client…, test_a_non_retryable_error_is_raised_immediately(), test_a_rate_limit_is_retried_with_backoff(), test_a_reply_is_parsed_into_the_schema() (+5 more)

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
Cohesion: 0.17
Nodes (15): io, _address(), export_official(), date, Path, Write confirmed values onto the official CKYC form (ISSUES.md LF-001). The…, split_name(), ExportError (+7 more)

### Community 56 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 57 - "loader.py"
Cohesion: 0.20
Nodes (17): Gotchas, _build(), _inherited(), load_official(), load_overlay(), parse_acroform(), Any, Path (+9 more)

### Community 58 - "Non-negotiables"
Cohesion: 0.50
Nodes (3): Non-negotiables, _calling_module(), The first module on the stack that is not this one. Walked rather than indexed…

### Community 59 - "M1. Implementation notes — instrumentation and corpus"
Cohesion: 0.33
Nodes (6): M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 61 - "PersonaChannel"
Cohesion: 0.05
Nodes (28): Commands, Conventions, Environment, graphify, LucidForm, Paper, Personas and live evaluation, Phase 3 notes (+20 more)

### Community 62 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 63 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 64 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 65 - "graph.py"
Cohesion: 0.22
Nodes (7): langgraph_graph, node_names(), The conversation as a LangGraph state machine. Same stages, same decisions,…, _structure(), _Stub, Rendering a validated value so a person can check it by ear. This is the last…, test_the_graph_has_the_pipeline_stages_as_nodes()

### Community 66 - "golden_sessions.py"
Cohesion: 0.15
Nodes (14): Path, Replays recorded model responses from disk, keyed by field and utterance. Lets…, ReplayClient, tempfile, main(), Record what a persona session does, minus what legitimately varies per run. The…, record(), _scrub() (+6 more)

### Community 67 - "Purpose"
Cohesion: 0.22
Nodes (5): Purpose, Why the system is listening. The user does not see this; the channel does., Return what the user said, or None if there is nothing further. None means the…, ConsoleChannel, A real person at a terminal. Output is prefixed by kind rather than coloured…

### Community 69 - "build_official_layout.py"
Cohesion: 0.24
Nodes (15): collections, pdfplumber, cells(), date_slot(), main(), address_block(), doc_numbers(), name_row() (+7 more)

### Community 70 - "Session"
Cohesion: 0.29
Nodes (6): InputChannel, OutputChannel, Protocol, State a validated value for confirmation. `value` is the exact string that will…, Session, test_the_fakes_satisfy_the_channel_protocols()

### Community 71 - "suggest.py"
Cohesion: 0.18
Nodes (14): difflib, LF-005 — Income band not derived from an amount, amount_band(), _email(), email_typo(), parse_amount(), Suggestions for a rejected value (ISSUES.md LF-005, LF-009, LF-004). A…, Rupees per year stated in `text`, or None if it holds no clear amount. "45… (+6 more)

### Community 72 - "make_form.py"
Cohesion: 0.12
Nodes (17): Canvas, functools, String table loading. Keys are looked up strictly. A missing key raises rather…, email_domain_ok(), Network checks the gate may be given, but never performs itself (ISSUES.md…, True if the domain publishes a mail server (MX), False if it cannot receive…, build(), _header() (+9 more)

### Community 75 - "load_all"
Cohesion: 0.12
Nodes (22): Settings. Model id is config, never hardcoded -- the extraction-accuracy sweep…, build(), _clean_extraction(), Any, Path, Build the offline extraction fixture corpus. python -m lucidform.eval.fixtures…, The straightforward case: the value was stated and heard correctly., write() (+14 more)

### Community 78 - "test_gate.py"
Cohesion: 0.08
Nodes (37): Closed rejection taxonomy. Every rejection carries exactly one. Each member…, Reason, candidate(), gate(), fixture, Gate-level invariants: the contract the rest of the pipeline relies on. Phase 2…, A rejection must not colour the next verdict. The gate is used in a loop over…, Construction order and instance identity must not matter. (+29 more)

### Community 79 - "test_issues_phase4.py"
Cohesion: 0.11
Nodes (19): Returns extractions handed to it. For tests that need one exact reply., ScriptedClient, test_a_question_is_logged_too(), test_state_is_proposed_from_the_pin_and_needs_a_yes(), fixture, Regression tests for docs/ISSUES.md LF-006: revisit missing fields, final…, schema(), test_a_hedged_yes_does_not_approve() (+11 more)

### Community 80 - "EventLog"
Cohesion: 0.17
Nodes (12): EventLog, _jsonable(), Any, Path, Time a stage and emit once it completes. Mutate the yielded dict to attach the…, Append-only JSONL writer for one session., log(), fixture (+4 more)

### Community 81 - "FieldSpec"
Cohesion: 0.19
Nodes (8): build(), build_user_message(), The extraction prompt. Built per field, from the schema the form parser…, Return (system, user) for one extraction., FieldSpec, One form field: structure from the PDF, semantics from the YAML overlay.…, The prompt must not move validation into the model. A prompt saying "only…, test_prompt_carries_the_field_but_asks_for_no_judgement()

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

### Community 89 - "ConfirmationReceipt"
Cohesion: 0.19
Nodes (10): Invariants — never break these (the test suite enforces them), ConfirmationReceipt, True if this receipt authorises writing exactly this value., Proof that one specific candidate was validated and explicitly affirmed.…, Affirmation, The user's response to a read-back. `explicit` is True only for an unambiguous,…, ValidationReport, Read-back confirmation: deciding whether the user actually said yes. This… (+2 more)

### Community 90 - "III. System Architecture"
Cohesion: 0.25
Nodes (8): A. The five-stage pipeline, B. The validation gate and its rejection taxonomy, C. Extraction as a structurally bounded model call, D. Read-back and the confirmation whitelist, E. Three independent enforcement mechanisms, F. The orchestrator as a declared state graph, G. A help agent that cannot write, III. System Architecture

### Community 91 - "LucidForm — Specification"
Cohesion: 0.17
Nodes (11): Committed values that differ from ground truth. The correctness invariant, not…, 1. Intent, 2. The gating contract — the thesis of the project, 3. Non-negotiables, 5. Rejection taxonomy, 6. Scope of this prototype, 7. Eval outputs, Check order (+3 more)

### Community 92 - "verhoeff_valid"
Cohesion: 0.20
Nodes (10): True if `digits` (including its trailing check digit) satisfies Verhoeff., verhoeff_valid(), parametrize, The realistic error: one digit misheard or mistyped. Exhaustive over all 12…, Two neighbouring digits swapped -- the classic dictation error. This is the…, Whitespace-separated and letter-bearing input reaches this function in practice…, test_adjacent_transpositions_are_caught(), test_corruption_helper_changes_exactly_one_digit() (+2 more)

### Community 93 - "ScriptedAnswerClient"
Cohesion: 0.29
Nodes (4): Returns the replies handed to it; an Exception in the list is raised., ScriptedAnswerClient, The embedding call is a live API call too; it sits inside the fallback., test_a_retrieval_failure_never_breaks_the_session()

### Community 94 - "_Pages"
Cohesion: 0.31
Nodes (3): _Pages, One reportlab canvas per PDF page, drawn in PDF user space (origin bottom-left)., One character per box; if it does not fit, shrink across the whole span.

### Community 96 - "Progress log"
Cohesion: 0.29
Nodes (6): 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5, 2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper, 2026-09-30 (night) · Shubh (+Claude) · Pre-push audit, 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs, 2026-10-01 — Review fixes LF-001..LF-010 (Yashvardhan, with Claude Code), Progress log

### Community 97 - "json"
Cohesion: 0.29
Nodes (6): csv, json, main(), Path, Build lucidform/gate/data/pin_directory.json from the India Post pincode CSV.…, _title()

### Community 98 - "Live demo — 5 minutes, terminal only"
Cohesion: 0.40
Nodes (4): Backup commands (if the network is slow), Live demo — 5 minutes, terminal only, Script — what to type, and what to point out, The one-line pitch while it runs

### Community 99 - "Team guide"
Cohesion: 0.29
Nodes (7): 1. The idea in 60 seconds, 2. Who does what, 3. Setup, 4. The loop for every phase, 5. Saving tokens with graphify, 6. Rules nobody (human or AI) breaks, Team guide

### Community 100 - "AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate"
Cohesion: 0.40
Nodes (4): AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate, Run, What this is, Working rules for agents

### Community 101 - "LucidForm — Methodology"
Cohesion: 0.33
Nodes (5): LucidForm — Methodology, M7.1 Why replace a working loop, M7.2 Parity, not intuition, M7.3 No checkpoint-resume, M7. The orchestrator as a state graph

### Community 102 - "metrics.py"
Cohesion: 0.10
Nodes (25): FieldOutcome, _is_correct(), load_sessions(), parse_session(), outcome(), _pct(), _personas(), Path (+17 more)

### Community 103 - "pytest"
Cohesion: 0.22
Nodes (7): Check digit for a payload that does not yet carry one., verhoeff_check_digit(), pytest, Session setup shared by the whole suite. The blank KYC template…, Verhoeff checksum, and the synthetic-data generator built on it. Aadhaar uses…, test_check_digit_completes_a_payload(), test_check_digit_rejects_non_numeric_payload()

### Community 104 - "test_a_failed_model_call_is_an_unclear_turn_not_a_crash"
Cohesion: 0.40
Nodes (3): FailingClient, parametrize, test_a_failed_model_call_is_an_unclear_turn_not_a_crash()

### Community 105 - "digits_agree"
Cohesion: 0.29
Nodes (8): LF-007 — Model silently drops/changes digits, digits_agree(), The digit string a quote spells out, or None if it cannot be read that way., None when consistent or not checkable; a failed Grounding otherwise., spoken_digits(), _strip_phone_prefix(), test_compound_number_words_skip_the_check(), test_oh_is_zero_only_where_letters_cannot_occur()

### Community 106 - "test_a_form_is_filled_over_the_voice_channel"
Cohesion: 0.50
Nodes (3): The Phase 7 claim, asserted. The orchestrator, gate, confirmation step, and…, test_a_form_is_filled_over_the_voice_channel(), read_back()

### Community 108 - "PersonaError"
Cohesion: 0.40
Nodes (5): PersonaError, RuntimeError, A persona is internally inconsistent. Always fatal. A persona whose ground…, The loader must refuse a persona the replay driver could not run., test_a_persona_with_no_utterances_is_rejected()

### Community 109 - "checksums.py"
Cohesion: 0.50
Nodes (4): corrupt_one_digit(), Checksum primitives for the validation gate. Pure functions over strings. No…, Change exactly one digit, producing a checksum-invalid variant. The single-…, Random

### Community 110 - "percentile"
Cohesion: 0.25
Nodes (7): percentile(), Any, Nearest-rank percentile. Deliberately not interpolated: with the sample sizes a…, Not interpolated. At prototype sample sizes an interpolated percentile reports…, Zero would read as an instantaneous stage rather than an unmeasured one., test_percentile_of_nothing_is_none_not_zero(), test_percentiles_are_values_that_actually_occurred()

### Community 111 - "make_client"
Cohesion: 0.33
Nodes (7): make_client(), An extraction provider was named that this build has no client for., The live extraction client for `provider`, or for the configured one., UnknownProvider, test_an_unknown_provider_is_refused(), test_the_factory_picks_the_configured_provider(), ValueError

### Community 112 - "test_phone_country_and_trunk_prefixes_are_stripped"
Cohesion: 0.33
Nodes (6): parametrize, Otherwise they are non-empty to a length check and blank to the user, who would…, Reshaping: the subscriber number is unchanged, only the prefix goes., test_pan_separators_and_case_are_reshaped(), test_phone_country_and_trunk_prefixes_are_stripped(), test_values_made_only_of_invisible_characters_become_empty()

### Community 113 - "runs"
Cohesion: 0.33
Nodes (6): agg(), fixture, Three real sessions, recorded into a scratch directory., runs(), schema(), sessions()

### Community 114 - "ExtractionClient"
Cohesion: 0.40
Nodes (3): ExtractionClient, Protocol, Anything that can turn a prompt into an `Extraction`.

### Community 116 - "_enum_field"
Cohesion: 0.50
Nodes (4): _enum_field(), U+095B (precomposed ज़) is NFKC-decomposed in the value; the name must be too., test_a_declared_name_does_not_leak_across_options(), test_a_declared_name_is_compared_after_the_same_unicode_normalisation()

### Community 117 - "test_a_huge_retry_hint_is_capped"
Cohesion: 0.50
Nodes (3): test_a_huge_retry_hint_is_capped(), test_a_rate_limit_retry_delay_hint_is_honoured(), call()

## Knowledge Gaps
- **181 isolated node(s):** `fs`, `path`, `{
  Document, Packer, Paragraph, TextRun, AlignmentType, SectionType, Table, TableRow,
  TableCell, WidthType, BorderStyle, ShadingType, LevelFormat,
}`, `ROOT`, `SRC` (+176 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 809 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M8. The help agent`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `Candidate` connect `Candidate` to `Event`, `test_formstate.py`, `SessionGraph`, `test_issues_phase1.py`, `test_confirm.py`, `cli.py`, `FormState`, `asr_probe.py`, `ValidationGate`, `.commit`, `test_gate_crossfield.py`, `test_voice.py`, `test_adversarial.py`, `Extractor`, `models.py`, `test_issues_phase2.py`, `test_issues_phase5.py`, `Status`, `Non-negotiables`, `PersonaChannel`, `graph.py`, `test_gate.py`, `ConfirmationReceipt`, `III. System Architecture`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `FormState` connect `FormState` to `Event`, `test_formstate.py`, `models.py`, `Session`, `test_issues_phase2.py`, `test_issues_phase5.py`, `test_a_form_is_filled_over_the_voice_channel`, `load_all`, `cli.py`, `test_issues_phase4.py`, `EventLog`, `.commit`, `test_voice.py`, `official_writer.py`, `Candidate`, `ConfirmationReceipt`, `test_session.py`, `PersonaChannel`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `ValidationGate` (e.g. with `asr_probe_cmd()` and `extract_cmd()`) actually correct?**
  _`ValidationGate` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Candidate` (e.g. with `Invariants — never break these (the test suite enforces them)` and `Conventions`) actually correct?**
  _`Candidate` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 45 inferred relationships involving `Status` (e.g. with `extract_cmd()` and `gate_check()`) actually correct?**
  _`Status` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `FormState` (e.g. with `run_cmd()` and `ReplayRun`) actually correct?**
  _`FormState` has 12 INFERRED edges - model-reasoned connections that need verification._