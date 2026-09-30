# Graph Report - LucidForm  (2026-10-01)

## Corpus Check
- 115 files · ~266,288 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .jsonl 17, (none) 4, .example 1)

## Summary
- 1922 nodes · 4323 edges · 110 communities (99 shown, 11 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 405 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `131d96ce`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_gate_rules.py
- Event
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
- asr_probe.py
- IV. Methodology
- What You Must Do When Invoked
- ValidationGate
- state.py
- test_no_silent_write.py
- test_gate_crossfield.py
- rules.py
- test_voice.py
- test_personas.py
- models.py
- aadhaar_valid
- test_session.py
- test_schema_loader.py
- Title (pick one, or tell me to try again)
- test_adversarial.py
- .answer
- voice.py
- VoiceChannel
- index.py
- corpus.py
- ExtractionOutcome
- test_extraction_live.py
- events.py
- test_issues_phase2.py
- test_issues_phase5.py
- answer.py
- test_help.py
- test_i18n.py
- grounding.py
- test_form_state_exposes_no_alternative_mutator
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
- loader.py
- LucidForm
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- PersonaChannel
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- Aggregate
- run_persona
- Purpose
- graphify reference: GitHub clone and cross-repo merge
- build_official_layout.py
- graphify reference: transcribe video and audio
- suggest.py
- make_form.py
- .claude/CLAUDE.md
- extraction-spec.md
- Persona
- test_gate.py
- test_issues_phase4.py
- EventLog
- FieldSpec
- parametrize
- passing
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- LucidForm
- Team workflow (5 people, each with their own AI assistant)
- M8. The help agent
- uidai_faq_update.md
- ConfirmationReceipt
- III. System Architecture
- LucidForm — Specification
- verhoeff_valid
- HelpIndex
- _Pages
- README.md
- Progress log
- Reason
- Live demo — 5 minutes, terminal only
- Team guide
- AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate
- LucidForm — Methodology
- metrics.py
- pytest
- test_a_failed_model_call_is_an_unclear_turn_not_a_crash
- decode_spelled
- test_a_form_is_filled_over_the_voice_channel
- PersonaError
- checksums.py

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 73 edges
2. `Candidate` - 67 edges
3. `Status` - 63 edges
4. `FormState` - 61 edges
5. `EventLog` - 48 edges
6. `Extraction` - 48 edges
7. `load()` - 48 edges
8. `get_settings()` - 47 edges
9. `Event` - 47 edges
10. `Extractor` - 45 edges

## Surprising Connections (you probably didn't know these)
- `The guarantee is enforced, not promised` --references--> `ConfirmationReceipt`  [INFERRED]
  README.md → lucidform/formstate/receipt.py
- `Commit invariant` --references--> `SilentWriteBlocked`  [INFERRED]
  SPEC.md → lucidform/formstate/state.py
- `Step 2.5 - Transcribe video / audio files (only if video files detected)` --references--> `export()`  [INFERRED]
  .claude/skills/graphify/references/transcribe.md → lucidform/formstate/writer.py
- `Conventions` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py
- `A. The five-stage pipeline` --references--> `Candidate`  [INFERRED]
  docs/paper-draft.md → lucidform/models.py

## Import Cycles
- None detected.

## Communities (110 total, 11 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.09
Nodes (42): normalize(), range_error(), Canonical form of a value: what gets read back, and what gets committed. The…, Well-formed, but outside the permitted domain., _enum_field(), field(), fixture, parametrize (+34 more)

### Community 1 - "Event"
Cohesion: 0.12
Nodes (29): Event, str, Read one session log. Used by metrics and by tests; never by the pipeline., read_log(), log(), fixture, The event log is the evaluation substrate, so its guarantees are tested.…, Null means "not applicable"; zero would mean "instantaneous". Conflating them… (+21 more)

### Community 2 - "Candidate"
Cohesion: 0.07
Nodes (48): RuntimeError, A write was attempted that did not satisfy the commit invariant. Raised, never…, SilentWriteBlocked, Candidate, A proposed value. Explicitly *not* a form value. Frozen: a receipt is bound to…, forge(), gate(), make() (+40 more)

### Community 3 - "test_readback.py"
Cohesion: 0.15
Nodes (26): field(), fixture, Read-back rendering: can the user actually check this by ear? For a user who…, A listener can check "example dot invalid" without hearing it letter by letter,…, Spelling a name the user just said would be tedious and no clearer., Presentation differs; the value does not. If rendering altered the value, the…, AKQPS3417M" spoken as a word is an unpronounceable noise that no listener can…, A synthesiser reading "3417" says "three thousand four hundred and seventeen",… (+18 more)

### Community 4 - "build.js"
Cohesion: 0.08
Nodes (33): docx, ref_fs, ref_path, authorsTable(), body(), bodyBlocks(), COL_W, doc (+25 more)

### Community 5 - "SessionGraph"
Cohesion: 0.06
Nodes (32): Orchestrator (LangGraph), LF-006 — Session ends incomplete, no final review, langgraph_graph, _build(), edges(), field_named(), mermaid(), node_names() (+24 more)

### Community 6 - "MissingString"
Cohesion: 0.40
Nodes (4): KeyError, MissingString, A string key is absent from the requested language's table., Look up a key and fill in its placeholders.

### Community 7 - "test_issues_phase1.py"
Cohesion: 0.16
Nodes (22): check(), Ground an extraction against the utterance it claims to come from. Only value-…, FieldType, `str.isdigit()` and `\\d` both accept these. The rules must not. This is the…, test_devanagari_digits_do_not_satisfy_the_numeric_patterns(), _extraction(), _gate(), fixture (+14 more)

### Community 8 - "test_confirm.py"
Cohesion: 0.07
Nodes (40): RuntimeError, The confirmation receipt: the capability that authorises a write. A receipt is…, A receipt was constructed outside the confirmation module., UnauthorizedIssuer, fingerprint(), Bind a receipt to one exact candidate and one exact committed value. The unit…, confirm(), normalize_utterance() (+32 more)

### Community 9 - "readback.py"
Cohesion: 0.15
Nodes (15): Rendering a validated value so a person can check it by ear. This is the last…, The value, as it should be heard., The full read-back sentence. `template` comes from the string table so the…, Render a value character by character, digits as words. Letters are upper-cased…, Emails are spoken with 'at' and 'dot', and the local part spelled out. The…, render(), render_value(), spell() (+7 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.05
Nodes (39): write_tables(), agg(), fixture, The measures, and the guards on how they may be read. Every number reported in…, Six deliberate errors are planted across the three personas., The headline table must balance. A wrong value is stopped by the gate, stopped…, The correctness invariant. A defect, not a finding., The evidence that the read-back is a stage rather than a courtesy. These are… (+31 more)

### Community 11 - "cli.py"
Cohesion: 0.10
Nodes (41): command, asr_probe_cmd(), extract_cmd(), _extraction_client(), gate_check(), graph_cmd(), _help_agent(), help_ask() (+33 more)

### Community 12 - "FormState"
Cohesion: 0.10
Nodes (35): FormState, Committed or explicitly declined -- either way, we are done asking., Confirmed values for one form-filling session., Read-only view. Handing out the dict itself would be a second write path, since…, export(), Path, Read the filled values out of an exported PDF. Used by the tests to verify that…, Write the confirmed values into a copy of the blank form. The template is never… (+27 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.08
Nodes (45): Returns extractions handed to it. For tests that need one exact reply., ScriptedClient, Extraction, Intent, BaseModel, str, What the user was doing, not what they said., The model's entire permitted output. (+37 more)

### Community 14 - "asr_probe.py"
Cohesion: 0.12
Nodes (19): _category(), character_error_rate(), is_simulated(), levenshtein(), probe(), ProbeResult, ProbeSummary, Path (+11 more)

### Community 15 - "IV. Methodology"
Cohesion: 0.33
Nodes (6): A. Form representation, B. Synthetic data and its construction, C. Adversarial evaluation corpora, D. Evaluation harness and its honesty constraints, E. Help-agent evaluation, IV. Methodology

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

### Community 17 - "ValidationGate"
Cohesion: 0.12
Nodes (6): date, Deterministic accept/reject on a single candidate value., Validate one candidate against the schema and confirmed values. `committed`…, ValidationGate, Check, One executed validation check. Recorded whether it passed or failed, so the log…

### Community 18 - "state.py"
Cohesion: 0.14
Nodes (11): Personas and live evaluation, LF-008 — "I don't have a PAN" skips a required field, CommitRecord, DeclineRecord, block(), _now(), Form state: the single write path. This module is the first of the three…, Write a confirmed value. The sole mutator of form state. Every precondition is… (+3 more)

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.12
Nodes (28): ast, Module, _help_violations(), _imported_names(), _parse(), parametrize, Path, _python_files() (+20 more)

### Community 20 - "test_gate_crossfield.py"
Cohesion: 0.06
Nodes (54): LF-003 — PIN / city / state mismatch accepted, check(), _city_agrees(), city_matches_pin_and_state(), CrossFieldResult, doc_number_matches_type(), _or(), pan_matches_surname() (+46 more)

### Community 21 - "rules.py"
Cohesion: 0.12
Nodes (20): LF-002 — Weak Aadhaar validation, enum_error(), format_error(), is_placeholder_number(), parse_date(), placeholder_error(), date, Normalization and single-field rules. Pure functions over strings, with no… (+12 more)

### Community 22 - "test_voice.py"
Cohesion: 0.13
Nodes (22): CorruptingRecognizer, EchoRecognizer, Returns text handed to it. Lets the channel be tested without audio., Applies documented speech-recognition error patterns, deterministically. **This…, Writes a valid but silent WAV. Exercises the file path without a voice., SilentSynthesizer, personas(), fixture (+14 more)

### Community 23 - "test_personas.py"
Cohesion: 0.11
Nodes (14): The synthetic corpus must be internally consistent. Accuracy is measured…, The form states an 18-year minimum, and the gate enforces it., A persona who has no email still has to say so out loud. An empty ground truth…, .invalid is reserved by RFC 2606 and can never resolve. A synthetic corpus that…, The data provenance claim in METHODOLOGY M0.8 is only true if the files…, A persona that cannot answer a required field would abandon it mid-run, which…, PAN's fifth character is the surname's first letter. This is the cross-field…, test_email_addresses_use_a_reserved_domain() (+6 more)

### Community 24 - "models.py"
Cohesion: 0.20
Nodes (7): datetime, The validation gate. Stage 4 of the pipeline, and the component the project's…, Core types shared across the pipeline. Deliberately free of I/O and of any…, ValidationReport, test_a_pass_must_not_carry_a_reason(), test_a_rejection_must_carry_a_reason(), uuid

### Community 25 - "aadhaar_valid"
Cohesion: 0.24
Nodes (10): aadhaar_valid(), Structural + checksum validity of a 12-digit Aadhaar number. The first digit is…, Generate a checksum-valid but entirely fabricated Aadhaar number. Used only to…, synthetic_aadhaar(), Issued Aadhaar numbers never begin with 0 or 1. Treated as part of validity…, test_generated_numbers_are_valid(), test_leading_zero_or_one_is_rejected(), test_wrong_length_is_rejected() (+2 more)

### Community 26 - "test_session.py"
Cohesion: 0.08
Nodes (45): Kind, What sort of thing is being said, for channels that present them differently., test_form_60_is_not_committed_without_yes(), test_session_rejects_the_shortened_aadhaar(), test_offered_band_denied_is_not_saved(), test_offered_band_needs_a_yes(), test_only_one_suggestion_per_utterance(), one_field() (+37 more)

### Community 27 - "test_schema_loader.py"
Cohesion: 0.07
Nodes (26): built_pdf(), overlay(), fixture, parametrize, Round-trip: the generator writes the AcroForm, the loader reads it back.…, A field the PDF does not have must raise, not be skipped. A silently dropped…, One spoken name for two options would make the gate choose for the user., Conversely, a PDF widget nothing validates must raise. (+18 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.25
Nodes (8): I. Introduction, II. Related Work, References, Title (pick one, or tell me to try again), V. Algorithm and Pseudocode, VI. Results, VII. Discussion, VIII. Conclusion and Future Work

### Community 29 - "test_adversarial.py"
Cohesion: 0.11
Nodes (15): _candidate(), committed(), gate(), fixture, parametrize, The adversarial suite -- the evidence for the safety claim. Every case in…, Every code in the taxonomy needs at least one case. An unexercised reason code…, A rejection-only category cannot distinguish a gate from a brick wall. The… (+7 more)

### Community 30 - ".answer"
Cohesion: 0.22
Nodes (6): HelpAnswer, _passages(), _question_lines(), emit(), FAQ pages where a question is a line ending in '?' followed by its answer., StubHelper

### Community 31 - "voice.py"
Cohesion: 0.11
Nodes (16): FasterWhisperRecognizer, PiperSynthesizer, Path, Protocol, RuntimeError, The voice channel: speech in, speech out, pipeline unchanged. Phase 7 of the…, Local speech synthesis via Piper. Invoked as a subprocess rather than through a…, A speech backend was requested but is not installed. (+8 more)

### Community 32 - "VoiceChannel"
Cohesion: 0.24
Nodes (6): One audio exchange, retained for the transcript and for error analysis., Speech in, speech out, over the same protocols as the console. Audio input is…, VoiceChannel, VoiceTurn, The gate must stay installable and testable without a gigabyte of model…, test_the_module_imports_without_any_speech_library()

### Community 33 - "index.py"
Cohesion: 0.10
Nodes (19): Help agent (RAG), hashlib, Embedder, HashEmbedder, Hit, _normalise(), Protocol, Hybrid retrieval over the help corpus: dense embeddings + BM25, fused by rank.… (+11 more)

### Community 34 - "corpus.py"
Cohesion: 0.16
Nodes (16): html, help_build(), Chunk the official sources and embed them (a few minutes on the free tier)., _clean(), _flat(), _html_text(), load_chunks(), load_manifest() (+8 more)

### Community 36 - "test_extraction_live.py"
Cohesion: 0.11
Nodes (16): enum, Settings. Model id is config, never hardcoded -- the extraction-accuracy sweep…, The shape the model is allowed to reply in. This schema is a safety boundary,…, os, pydantic, pydantic_settings, extractor(), _has_credentials() (+8 more)

### Community 37 - "events.py"
Cohesion: 0.09
Nodes (26): contextlib, csv, dataclasses, functools, json, Text channels: a console for a person, and a persona for the replay driver.…, Append-only session event log -- the evaluation substrate. One record per…, Synthetic persona loading. A persona is a fabricated user: ground-truth field… (+18 more)

### Community 38 - "test_issues_phase2.py"
Cohesion: 0.23
Nodes (12): _gate(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-003: PIN / city / state consistency. The…, schema(), test_correct_pairs_pass(), test_directory_lookup(), test_known_city_in_another_state_is_caught() (+4 more)

### Community 39 - "test_issues_phase5.py"
Cohesion: 0.10
Nodes (24): _drawn(), _gate(), official(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-001: filling the official CKYC form., (text, x, y_from_top) for every string drawn on the page, via pypdf., Characters drawn inside one row of boxes, left to right. (+16 more)

### Community 40 - "answer.py"
Cohesion: 0.13
Nodes (14): Extraction clients (Gemini), GeminiAnswerClient, Answering a user's question about a field, grounded in retrieved passages. The…, GeminiEmbedder, `gemini-embedding-001`, with the asymmetric document/query task types., _hinted_delay(), json_config(), make_genai_client() (+6 more)

### Community 41 - "test_help.py"
Cohesion: 0.09
Nodes (22): HelpReply, BaseModel, The model's entire permitted output., Returns the replies handed to it; an Exception in the list is raised., ScriptedAnswerClient, The help agent: answers a user's question about a field from official…, agent(), chunks() (+14 more)

### Community 42 - "test_i18n.py"
Cohesion: 0.10
Nodes (26): available(), load(), The system's own wording, in one language., Strings, LucidForm -- accessibility-first form assistant. The LLM never writes a form…, parametrize, String tables. A missing key must fail loudly. Falling back to another language…, The read-back names the field, so an English label inside a Hindi read-back is… (+18 more)

### Community 43 - "grounding.py"
Cohesion: 0.09
Nodes (27): Decisions (approved 2026-09-30), ISSUES.md — known problems, root causes, and fixes, LF-001 — Can't fill the official CKYC form, LF-004 — Email only syntax-checked, LF-007 — Model silently drops/changes digits, LF-009 — Near-miss answers get no suggestion, LF-010 — A valid option the model was unsure of is re-asked blindly, LF-011 — Follow-ups (open) (+19 more)

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
Cohesion: 0.11
Nodes (20): help_eval(), Run the help agent over the 30-question set + 6 controls (live)., default_index_dir(), gold_matches(), load_set(), Path, A numbered gold ("RBI KYC FAQ, Q1") must equal the label -- a substring test…, Row (+12 more)

### Community 50 - "Prompt for Claude Code — LucidForm Prototype"
Cohesion: 0.29
Nodes (6): Context, How I want you to work with me, Non-negotiable design constraint, Prompt for Claude Code — LucidForm Prototype, Scope for THIS prototype (deliberately small), What I need from you, in order

### Community 51 - "test_llm_clients.py"
Cohesion: 0.05
Nodes (37): BaseSettings, Path, Settings, AnthropicExtractionClient, ExtractionClient, GeminiExtractionClient, make_client(), ModelReply (+29 more)

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
Cohesion: 0.12
Nodes (19): io, _address(), export_official(), date, Path, Write confirmed values onto the official CKYC form (ISSUES.md LF-001). The…, Greedy word wrap into lines of the given box counts; the last line takes the…, split_name() (+11 more)

### Community 56 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 57 - "loader.py"
Cohesion: 0.22
Nodes (16): _build(), _inherited(), load_official(), load_overlay(), parse_acroform(), Any, Path, RuntimeError (+8 more)

### Community 58 - "LucidForm"
Cohesion: 0.14
Nodes (12): Commands, Conventions, Environment, graphify, LucidForm, Non-negotiables, Paper, Phase 3 notes (+4 more)

### Community 59 - "M1. Implementation notes — instrumentation and corpus"
Cohesion: 0.33
Nodes (6): M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 61 - "PersonaChannel"
Cohesion: 0.16
Nodes (7): Phase 4 notes, PersonaChannel, Agree only if the value read back matches ground truth., One exchange, kept for the transcript., A simulated user, driven by a persona's script. Implements both protocols: it…, Turn, What to call this field out loud. An English label inside a Hindi read-back is…

### Community 62 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 63 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 64 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 65 - "Aggregate"
Cohesion: 0.14
Nodes (6): Phase 5 notes, Aggregate, True if no session called a real model., Figures that must not be read as results, given how they were produced. Printed…, Of the wrong values proposed, how many did the gate reject?, Of the correct values proposed, how many did the gate wrongly reject? The…

### Community 66 - "run_persona"
Cohesion: 0.14
Nodes (17): Path, ReplayRun, run_persona(), Path, Replays recorded model responses from disk, keyed by field and utterance. Lets…, ReplayClient, tempfile, main() (+9 more)

### Community 67 - "Purpose"
Cohesion: 0.12
Nodes (11): InputChannel, OutputChannel, Purpose, Protocol, str, The boundary between the pipeline and however the user is actually talking. The…, Why the system is listening. The user does not see this; the channel does., State a validated value for confirmation. `value` is the exact string that will… (+3 more)

### Community 69 - "build_official_layout.py"
Cohesion: 0.24
Nodes (15): collections, pdfplumber, cells(), date_slot(), main(), address_block(), doc_numbers(), name_row() (+7 more)

### Community 71 - "suggest.py"
Cohesion: 0.23
Nodes (11): difflib, LF-005 — Income band not derived from an amount, amount_band(), _email(), email_typo(), parse_amount(), Suggestions for a rejected value (ISSUES.md LF-005, LF-009, LF-004). A…, Rupees per year stated in `text`, or None if it holds no clear amount. "45… (+3 more)

### Community 72 - "make_form.py"
Cohesion: 0.21
Nodes (11): Canvas, build(), _header(), _overlay(), Path, Generate the target fillable PDF (AcroForm). The prototype's form reproduces…, reportlab_lib_colors, reportlab_lib_pagesizes (+3 more)

### Community 75 - "Persona"
Cohesion: 0.19
Nodes (10): build(), _clean_extraction(), Any, Path, Build the offline extraction fixture corpus. python -m lucidform.eval.fixtures…, The straightforward case: the value was stated and heard correctly., write(), __iter__() (+2 more)

### Community 78 - "test_gate.py"
Cohesion: 0.09
Nodes (29): candidate(), gate(), fixture, Gate-level invariants: the contract the rest of the pipeline relies on. Phase 2…, A rejection must not colour the next verdict. The gate is used in a loop over…, Construction order and instance identity must not matter., A value failing several checks reports the earliest one. Deterministic…, Otherwise a malformed value would be reported as a confidence problem, hiding… (+21 more)

### Community 79 - "test_issues_phase4.py"
Cohesion: 0.16
Nodes (12): fixture, Regression tests for docs/ISSUES.md LF-006: revisit missing fields, final…, schema(), test_a_hedged_yes_does_not_approve(), test_a_missing_field_is_asked_again_before_the_end(), test_an_unclear_review_reply_asks_again(), test_change_a_field_at_the_review(), test_changing_then_giving_nothing_keeps_the_confirmed_value() (+4 more)

### Community 80 - "EventLog"
Cohesion: 0.12
Nodes (19): EventLog, _jsonable(), Any, Path, Time a stage and emit once it completes. Mutate the yielded dict to attach the…, Append-only JSONL writer for one session., Extractor, Session (+11 more)

### Community 81 - "FieldSpec"
Cohesion: 0.14
Nodes (11): build(), build_user_message(), The extraction prompt. Built per field, from the schema the form parser…, Return (system, user) for one extraction., length_error(), Wrong size. Returns a human-readable detail, or None if the size is fine., FieldSpec, One form field: structure from the PDF, semantics from the YAML overlay.… (+3 more)

### Community 82 - "parametrize"
Cohesion: 0.33
Nodes (6): parametrize, The correctness invariant. Not a finding -- a build failure. Any entry here…, A blocked write here would mean a defect upstream, not a caught attack --…, test_every_field_is_resolved(), test_no_committed_value_differs_from_ground_truth(), test_no_write_was_blocked_during_a_normal_session()

### Community 83 - "passing"
Cohesion: 0.50
Nodes (4): gate(), passing(), fixture, A candidate that has genuinely passed validation. Using a real verdict rather…

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
Cohesion: 0.18
Nodes (11): Invariants — never break these (the test suite enforces them), Gotchas, ConfirmationReceipt, True if this receipt authorises writing exactly this value., Proof that one specific candidate was validated and explicitly affirmed.…, Affirmation, The user's response to a read-back. `explicit` is True only for an unambiguous,…, 2. The gating contract — the thesis of the project (+3 more)

### Community 90 - "III. System Architecture"
Cohesion: 0.25
Nodes (8): A. The five-stage pipeline, B. The validation gate and its rejection taxonomy, C. Extraction as a structurally bounded model call, D. Read-back and the confirmation whitelist, E. Three independent enforcement mechanisms, F. The orchestrator as a declared state graph, G. A help agent that cannot write, III. System Architecture

### Community 91 - "LucidForm — Specification"
Cohesion: 0.22
Nodes (8): Committed values that differ from ground truth. The correctness invariant, not…, 1. Intent, 3. Non-negotiables, 5. Rejection taxonomy, 6. Scope of this prototype, 7. Eval outputs, Check order, LucidForm — Specification

### Community 92 - "verhoeff_valid"
Cohesion: 0.20
Nodes (10): True if `digits` (including its trailing check digit) satisfies Verhoeff., verhoeff_valid(), parametrize, The realistic error: one digit misheard or mistyped. Exhaustive over all 12…, Two neighbouring digits swapped -- the classic dictation error. This is the…, Whitespace-separated and letter-bearing input reaches this function in practice…, test_adjacent_transpositions_are_caught(), test_corruption_helper_changes_exactly_one_digit() (+2 more)

### Community 93 - "HelpIndex"
Cohesion: 0.14
Nodes (14): AnswerClient, HelpAgent, load_agent(), Protocol, The live help agent, or None if no index has been built yet., Chunk, _corpus_digest(), HelpIndex (+6 more)

### Community 94 - "_Pages"
Cohesion: 0.31
Nodes (3): _Pages, One reportlab canvas per PDF page, drawn in PDF user space (origin bottom-left)., One character per box; if it does not fit, shrink across the whole span.

### Community 96 - "Progress log"
Cohesion: 0.29
Nodes (6): 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5, 2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper, 2026-09-30 (night) · Shubh (+Claude) · Pre-push audit, 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs, 2026-10-01 — Review fixes LF-001..LF-010 (Yashvardhan, with Claude Code), Progress log

### Community 97 - "Reason"
Cohesion: 0.22
Nodes (9): str, Closed rejection taxonomy. Every rejection carries exactly one. Each member…, Reason, About three lakh" must not become "1-5 Lakh" inside the extractor., test_replaying_an_out_of_enum_income_is_rejected_not_mapped(), An unreachable reason code would be a column in the results table that always…, Pinned deliberately. The reported reason distribution shifts if this changes,…, test_check_order_covers_the_whole_taxonomy() (+1 more)

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
Cohesion: 0.08
Nodes (29): FieldOutcome, _is_correct(), load_sessions(), parse_session(), outcome(), _pct(), percentile(), _personas() (+21 more)

### Community 103 - "pytest"
Cohesion: 0.22
Nodes (7): Check digit for a payload that does not yet carry one., verhoeff_check_digit(), pytest, Session setup shared by the whole suite. The blank KYC template…, Verhoeff checksum, and the synthetic-data generator built on it. Aadhaar uses…, test_check_digit_completes_a_payload(), test_check_digit_rejects_non_numeric_payload()

### Community 104 - "test_a_failed_model_call_is_an_unclear_turn_not_a_crash"
Cohesion: 0.40
Nodes (3): FailingClient, parametrize, test_a_failed_model_call_is_an_unclear_turn_not_a_crash()

### Community 105 - "decode_spelled"
Cohesion: 0.33
Nodes (6): decode_spelled(), Turn a spelled-out transcript back into a value. The exact inverse of…, The round trip only measures anything if these two agree., oh" for zero and "for" for four are transcription artefacts, not mistakes the…, test_homophones_are_decoded_as_the_digit_they_sound_like(), test_the_decode_is_the_exact_inverse_of_the_read_back()

### Community 106 - "test_a_form_is_filled_over_the_voice_channel"
Cohesion: 0.22
Nodes (8): What the recogniser heard. `confidence` is the recogniser's own estimate where…, Transcript, Guard on the probe itself. If the round trip corrupted values even with a…, The Phase 7 claim, asserted. The orchestrator, gate, confirmation step, and…, test_a_form_is_filled_over_the_voice_channel(), read_back(), test_a_perfect_recogniser_loses_nothing(), transcribe()

### Community 108 - "PersonaError"
Cohesion: 0.40
Nodes (5): PersonaError, RuntimeError, A persona is internally inconsistent. Always fatal. A persona whose ground…, The loader must refuse a persona the replay driver could not run., test_a_persona_with_no_utterances_is_rejected()

### Community 109 - "checksums.py"
Cohesion: 0.50
Nodes (4): corrupt_one_digit(), Checksum primitives for the validation gate. Pure functions over strings. No…, Change exactly one digit, producing a checksum-invalid variant. The single-…, Random

## Knowledge Gaps
- **181 isolated node(s):** `fs`, `path`, `{
  Document, Packer, Paragraph, TextRun, AlignmentType, SectionType, Table, TableRow,
  TableCell, WidthType, BorderStyle, ShadingType, LevelFormat,
}`, `ROOT`, `SRC` (+176 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 806 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M8. The help agent`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `Candidate` connect `Candidate` to `Event`, `SessionGraph`, `test_issues_phase1.py`, `test_confirm.py`, `cli.py`, `FormState`, `asr_probe.py`, `ValidationGate`, `state.py`, `test_gate_crossfield.py`, `test_voice.py`, `models.py`, `test_adversarial.py`, `ExtractionOutcome`, `events.py`, `test_issues_phase2.py`, `test_issues_phase5.py`, `Status`, `LucidForm`, `test_gate.py`, `EventLog`, `passing`, `ConfirmationReceipt`, `III. System Architecture`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `FieldSpec` connect `FieldSpec` to `test_gate_rules.py`, `readback.py`, `asr_probe.py`, `ValidationGate`, `rules.py`, `models.py`, `.answer`, `ExtractionOutcome`, `events.py`, `answer.py`, `test_llm_clients.py`, `FormSchema`, `loader.py`, `PersonaChannel`, `suggest.py`, `EventLog`, `ConfirmationReceipt`, `HelpIndex`, `AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate`, `decode_spelled`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `ValidationGate` (e.g. with `asr_probe_cmd()` and `extract_cmd()`) actually correct?**
  _`ValidationGate` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Candidate` (e.g. with `Invariants — never break these (the test suite enforces them)` and `Conventions`) actually correct?**
  _`Candidate` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 45 inferred relationships involving `Status` (e.g. with `extract_cmd()` and `gate_check()`) actually correct?**
  _`Status` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `FormState` (e.g. with `run_cmd()` and `ReplayRun`) actually correct?**
  _`FormState` has 12 INFERRED edges - model-reasoned connections that need verification._