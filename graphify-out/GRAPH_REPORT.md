# Graph Report - LucidForm  (2026-09-30)

## Corpus Check
- 109 files · ~253,854 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .jsonl 17, (none) 4, .example 1)

## Summary
- 1809 nodes · 4017 edges · 99 communities (90 shown, 9 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 386 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `72459bf7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FieldSpec
- Event
- Candidate
- test_readback.py
- build.js
- SessionGraph
- i18n/__init__.py
- test_issues_phase1.py
- test_confirm.py
- decode_spelled
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
- crossfield.py
- test_voice.py
- test_personas.py
- models.py
- test_checksums.py
- test_session.py
- loader.py
- Title (pick one, or tell me to try again)
- test_adversarial.py
- HelpAgent
- voice.py
- Purpose
- HelpIndex
- corpus.py
- ExtractionOutcome
- events.py
- EventLog
- Status
- answer.py
- with_retries
- test_help.py
- test_i18n.py
- golden_sessions.py
- graph.py
- M0. System design
- graphify reference: extra exports and benchmark
- client.py
- M2. The validation gate
- evaluate.py
- Prompt for Claude Code — LucidForm Prototype
- test_llm_clients.py
- M3. The write path
- M4. Extraction
- M5. Orchestration and read-back
- Settings
- graphify reference: query, path, explain
- VoiceChannel
- render_value
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- Kind
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- LucidForm
- ReplayClient
- base.py
- graphify reference: GitHub clone and cross-repo merge
- build_pin_directory.py
- LucidForm — Specification
- ISSUES.md — known problems, root causes, and fixes
- get_settings
- .claude/CLAUDE.md
- extraction-spec.md
- load_all
- test_gate.py
- test_issues_phase4.py
- .emit
- AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate
- parametrize
- passing
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- LucidForm
- Team workflow (5 people, each with their own AI assistant)
- M8. The help agent
- uidai_faq_update.md
- test_a_huge_retry_hint_is_capped
- III. System Architecture
- gate
- README.md
- Progress log
- Live demo — 5 minutes, terminal only
- Team guide
- LucidForm — Methodology
- metrics.py

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 65 edges
2. `Candidate` - 60 edges
3. `FormState` - 57 edges
4. `Status` - 50 edges
5. `Extraction` - 48 edges
6. `Event` - 47 edges
7. `load()` - 47 edges
8. `EventLog` - 46 edges
9. `get_settings()` - 44 edges
10. `Extractor` - 43 edges

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

## Communities (99 total, 9 thin omitted)

### Community 0 - "FieldSpec"
Cohesion: 0.05
Nodes (68): LF-002 — Weak Aadhaar validation, enum_error(), format_error(), is_placeholder_number(), length_error(), normalize(), parse_date(), placeholder_error() (+60 more)

### Community 1 - "Event"
Cohesion: 0.11
Nodes (31): Event, str, Read one session log. Used by metrics and by tests; never by the pipeline., read_log(), log(), fixture, The event log is the evaluation substrate, so its guarantees are tested.…, Null means "not applicable"; zero would mean "instantaneous". Conflating them… (+23 more)

### Community 2 - "Candidate"
Cohesion: 0.08
Nodes (45): RuntimeError, A write was attempted that did not satisfy the commit invariant. Raised, never…, SilentWriteBlocked, Candidate, A proposed value. Explicitly *not* a form value. Frozen: a receipt is bound to…, forge(), make(), The single write path, and every way of getting round it that I could think of.… (+37 more)

### Community 3 - "test_readback.py"
Cohesion: 0.12
Nodes (31): Render a value character by character, digits as words. Letters are upper-cased…, spell(), field(), fixture, Read-back rendering: can the user actually check this by ear? For a user who…, A listener can check "example dot invalid" without hearing it letter by letter,…, Spelling a name the user just said would be tedious and no clearer., Presentation differs; the value does not. If rendering altered the value, the… (+23 more)

### Community 4 - "build.js"
Cohesion: 0.08
Nodes (33): docx, ref_fs, ref_path, authorsTable(), body(), bodyBlocks(), COL_W, doc (+25 more)

### Community 5 - "SessionGraph"
Cohesion: 0.10
Nodes (13): Orchestrator (LangGraph), LF-006 — Session ends incomplete, no final review, field_named(), Runs one `Session` through the graph. Holds the stateful collaborators., Index of the field the user named, by its declared aliases or label. Whole-…, SessionGraph, TurnState, FieldResult (+5 more)

### Community 6 - "i18n/__init__.py"
Cohesion: 0.20
Nodes (8): functools, KeyError, available(), MissingString, String table loading. Keys are looked up strictly. A missing key raises rather…, A string key is absent from the requested language's table., Look up a key and fill in its placeholders., test_both_languages_are_available()

### Community 7 - "test_issues_phase1.py"
Cohesion: 0.09
Nodes (39): LF-007 — Model silently drops/changes digits, check(), clamp_confidence(), digits_agree(), Grounding, locate(), _loose(), Deterministic checks on the model's output, performed without the model. The… (+31 more)

### Community 8 - "test_confirm.py"
Cohesion: 0.07
Nodes (36): RuntimeError, A receipt was constructed outside the confirmation module., UnauthorizedIssuer, confirm(), normalize_utterance(), parse_affirmation(), Lowercase, strip punctuation and filler, collapse whitespace. Apostrophes…, Decide whether an utterance is an explicit confirmation. Returns an… (+28 more)

### Community 9 - "decode_spelled"
Cohesion: 0.33
Nodes (6): decode_spelled(), Turn a spelled-out transcript back into a value. The exact inverse of…, The round trip only measures anything if these two agree., oh" for zero and "for" for four are transcription artefacts, not mistakes the…, test_homophones_are_decoded_as_the_digit_they_sound_like(), test_the_decode_is_the_exact_inverse_of_the_read_back()

### Community 10 - "test_metrics.py"
Cohesion: 0.06
Nodes (33): agg(), fixture, The measures, and the guards on how they may be read. Every number reported in…, Six deliberate errors are planted across the three personas., The headline table must balance. A wrong value is stopped by the gate, stopped…, The correctness invariant. A defect, not a finding., The evidence that the read-back is a stage rather than a courtesy. These are…, A false positive is a real user told their correct answer is wrong. (+25 more)

### Community 11 - "cli.py"
Cohesion: 0.09
Nodes (38): command, asr_probe_cmd(), extract_cmd(), _extraction_client(), gate_check(), graph_cmd(), _help_agent(), help_ask() (+30 more)

### Community 12 - "FormState"
Cohesion: 0.06
Nodes (51): Personas and live evaluation, graphify reference: transcribe video and audio, Step 2.5 - Transcribe video / audio files (only if video files detected), DeclineRecord, FormState, _now(), Committed or explicitly declined -- either way, we are done asking., Record that the user chose not to answer an optional field. Writes no value.… (+43 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.05
Nodes (53): Help agent (RAG), build(), build_user_message(), The extraction prompt. Built per field, from the schema the form parser…, Return (system, user) for one extraction., extractor(), FailingClient, gate() (+45 more)

### Community 14 - "asr_probe.py"
Cohesion: 0.12
Nodes (19): _category(), character_error_rate(), is_simulated(), levenshtein(), probe(), ProbeResult, ProbeSummary, Path (+11 more)

### Community 15 - "IV. Methodology"
Cohesion: 0.33
Nodes (6): A. Form representation, B. Synthetic data and its construction, C. Adversarial evaluation corpora, D. Evaluation harness and its honesty constraints, E. Help-agent evaluation, IV. Methodology

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (25): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+17 more)

### Community 17 - "ValidationGate"
Cohesion: 0.11
Nodes (8): date, Deterministic accept/reject on a single candidate value., Validate one candidate against the schema and confirmed values. `committed`…, ValidationGate, Check, One executed validation check. Recorded whether it passed or failed, so the log…, gate(), fixture

### Community 18 - ".commit"
Cohesion: 0.25
Nodes (6): LF-008 — "I don't have a PAN" skips a required field, V. Algorithm and Pseudocode, CommitRecord, block(), Write a confirmed value. The sole mutator of form state. Every precondition is…, One entry in the append-only history of what was written and why.

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.12
Nodes (28): ast, Module, _help_violations(), _imported_names(), _parse(), parametrize, Path, _python_files() (+20 more)

### Community 20 - "test_gate_crossfield.py"
Cohesion: 0.10
Nodes (27): check(), pan_matches_surname(), Run the cross-field check for a field, if it has one., A PAN's fifth character is the first letter of the holder's surname. This is a…, _check(), Cross-field checks, and the discipline around when they may run. The rules…, The value passes -- there is nothing to contradict yet -- but the log must show…, The dependency guard defers a check; it does not waive it. (+19 more)

### Community 21 - "crossfield.py"
Cohesion: 0.15
Nodes (25): LF-003 — PIN / city / state mismatch accepted, _city_agrees(), city_matches_pin_and_state(), CrossFieldResult, _or(), pin_matches_confirmed_state(), Cross-field consistency checks. These catch the values that are individually…, The confirmed city, if the directory knows it, must be in the PIN's or state's… (+17 more)

### Community 22 - "test_voice.py"
Cohesion: 0.13
Nodes (22): CorruptingRecognizer, EchoRecognizer, Returns text handed to it. Lets the channel be tested without audio., Applies documented speech-recognition error patterns, deterministically. **This…, Writes a valid but silent WAV. Exercises the file path without a voice., SilentSynthesizer, personas(), fixture (+14 more)

### Community 23 - "test_personas.py"
Cohesion: 0.08
Nodes (22): PersonaError, RuntimeError, A persona is internally inconsistent. Always fatal. A persona whose ground…, personas(), fixture, The synthetic corpus must be internally consistent. Accuracy is measured…, The form states an 18-year minimum, and the gate enforces it., A persona who has no email still has to say so out loud. An empty ground truth… (+14 more)

### Community 24 - "models.py"
Cohesion: 0.15
Nodes (16): dataclasses, datetime, ConfirmationReceipt, The confirmation receipt: the capability that authorises a write. A receipt is…, True if this receipt authorises writing exactly this value., Proof that one specific candidate was validated and explicitly affirmed.…, Form state: the single write path. This module is the first of the three…, Affirmation (+8 more)

### Community 25 - "test_checksums.py"
Cohesion: 0.10
Nodes (30): aadhaar_valid(), corrupt_one_digit(), Checksum primitives for the validation gate. Pure functions over strings. No…, True if `digits` (including its trailing check digit) satisfies Verhoeff., Check digit for a payload that does not yet carry one., Structural + checksum validity of a 12-digit Aadhaar number. The first digit is…, Generate a checksum-valid but entirely fabricated Aadhaar number. Used only to…, Change exactly one digit, producing a checksum-invalid variant. The single-… (+22 more)

### Community 26 - "test_session.py"
Cohesion: 0.08
Nodes (49): Extraction, Intent, BaseModel, str, What the user was doing, not what they said., The model's entire permitted output., test_declining_pan_offers_form_60_and_commits_on_yes(), test_form_60_is_not_committed_without_yes() (+41 more)

### Community 27 - "loader.py"
Cohesion: 0.06
Nodes (41): Gotchas, _inherited(), load(), load_overlay(), parse_acroform(), Any, Path, RuntimeError (+33 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.29
Nodes (7): I. Introduction, II. Related Work, References, Title (pick one, or tell me to try again), VI. Results, VII. Discussion, VIII. Conclusion and Future Work

### Community 29 - "test_adversarial.py"
Cohesion: 0.11
Nodes (15): _candidate(), committed(), gate(), fixture, parametrize, The adversarial suite -- the evidence for the safety claim. Every case in…, Every code in the taxonomy needs at least one case. An unexercised reason code…, A rejection-only category cannot distinguish a gate from a brick wall. The… (+7 more)

### Community 30 - "HelpAgent"
Cohesion: 0.13
Nodes (10): AnswerClient, HelpAgent, HelpAnswer, Protocol, _question_lines(), emit(), FAQ pages where a question is a line ending in '?' followed by its answer., The embedding call is a live API call too; it sits inside the fallback. (+2 more)

### Community 31 - "voice.py"
Cohesion: 0.09
Nodes (21): FasterWhisperRecognizer, PiperSynthesizer, Path, Protocol, RuntimeError, The voice channel: speech in, speech out, pipeline unchanged. Phase 7 of the…, Local speech synthesis via Piper. Invoked as a subprocess rather than through a…, A speech backend was requested but is not installed. (+13 more)

### Community 32 - "Purpose"
Cohesion: 0.17
Nodes (8): Purpose, str, Why the system is listening. The user does not see this; the channel does., ConsoleChannel, A real person at a terminal. Output is prefixed by kind rather than coloured…, The Phase 7 claim, asserted. The orchestrator, gate, confirmation step, and…, test_a_form_is_filled_over_the_voice_channel(), read_back()

### Community 33 - "HelpIndex"
Cohesion: 0.14
Nodes (14): Chunk, _corpus_digest(), Embedder, HashEmbedder, HelpIndex, _normalise(), Path, Protocol (+6 more)

### Community 34 - "corpus.py"
Cohesion: 0.18
Nodes (14): html, _clean(), _flat(), _html_text(), load_chunks(), load_manifest(), _pdf_text(), Path (+6 more)

### Community 36 - "events.py"
Cohesion: 0.11
Nodes (17): contextlib, enum, Append-only session event log -- the evaluation substrate. One record per…, The shape the model is allowed to reply in. This schema is a safety boundary,…, os, pydantic, extractor(), _has_credentials() (+9 more)

### Community 37 - "EventLog"
Cohesion: 0.16
Nodes (19): EventLog, Append-only JSONL writer for one session., Path, Run a persona through the whole pipeline, headlessly. This is the driver every…, ReplayRun, run_persona(), ExtractionClient, Protocol (+11 more)

### Community 38 - "Status"
Cohesion: 0.19
Nodes (16): The validation gate. Stage 4 of the pipeline, and the component the project's…, Status, About three lakh" must not become "1-5 Lakh" inside the extractor., test_replaying_an_out_of_enum_income_is_rejected_not_mapped(), _gate(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-003: PIN / city / state consistency. The… (+8 more)

### Community 39 - "answer.py"
Cohesion: 0.16
Nodes (12): hashlib, _passages(), Answering a user's question about a field, grounded in retrieved passages. The…, GeminiEmbedder, Hit, Hybrid retrieval over the help corpus: dense embeddings + BM25, fused by rank.…, `gemini-embedding-001`, with the asymmetric document/query task types., reciprocal_rank_fusion() (+4 more)

### Community 40 - "with_retries"
Cohesion: 0.14
Nodes (13): Extraction clients (Gemini), GeminiExtractionClient, The Gemini client, held to the same contract as the Anthropic one. The reply is…, GeminiAnswerClient, _hinted_delay(), json_config(), make_genai_client(), Shared plumbing for Gemini calls: the client, retries, schema-constrained JSON.… (+5 more)

### Community 41 - "test_help.py"
Cohesion: 0.09
Nodes (22): HelpReply, BaseModel, The model's entire permitted output., Returns the replies handed to it; an Exception in the list is raised., ScriptedAnswerClient, The help agent: answers a user's question about a field from official…, agent(), chunks() (+14 more)

### Community 42 - "test_i18n.py"
Cohesion: 0.11
Nodes (24): load(), The system's own wording, in one language., Strings, LucidForm -- accessibility-first form assistant. The LLM never writes a form…, parametrize, String tables. A missing key must fail loudly. Falling back to another language…, The read-back names the field, so an English label inside a Hindi read-back is…, `label` is the identifier used in the document and the results table; only what… (+16 more)

### Community 43 - "golden_sessions.py"
Cohesion: 0.15
Nodes (14): json, tempfile, main(), Record what a persona session does, minus what legitimately varies per run. The…, record(), _scrub(), golden(), fixture (+6 more)

### Community 44 - "graph.py"
Cohesion: 0.18
Nodes (12): Part B - Semantic extraction (parallel subagents), langgraph_graph, _build(), edges(), node_names(), The conversation as a LangGraph state machine. Same stages, same decisions,…, _route(), _structure() (+4 more)

### Community 45 - "M0. System design"
Cohesion: 0.20
Nodes (10): M0.1 Problem framing, M0.2 The five-stage pipeline, M0.3 Enforcing the constraint rather than asserting it, M0.4 Form representation: parser-assisted, human-verified schema, M0.5 Language selection, M0.6 Deferral of the voice channel, M0.7 Evaluation design, M0.8 Data (+2 more)

### Community 46 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 47 - "client.py"
Cohesion: 0.19
Nodes (10): AnthropicExtractionClient, make_client(), Model clients for the extraction layer. The extractor talks to a small protocol…, An extraction provider was named that this build has no client for., The live extraction client for `provider`, or for the configured one., The real client. Uses the SDK's structured-output helper, so the response is…, UnknownProvider, test_an_unknown_provider_is_refused() (+2 more)

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

### Community 55 - "Settings"
Cohesion: 0.27
Nodes (5): BaseSettings, Path, Settings, test_sdk_key_variables_are_read_without_the_project_prefix(), test_the_default_provider_is_gemini_and_the_model_is_config()

### Community 56 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 57 - "VoiceChannel"
Cohesion: 0.24
Nodes (6): One audio exchange, retained for the transcript and for error analysis., Speech in, speech out, over the same protocols as the console. Audio input is…, VoiceChannel, VoiceTurn, The gate must stay installable and testable without a gigabyte of model…, test_the_module_imports_without_any_speech_library()

### Community 58 - "render_value"
Cohesion: 0.22
Nodes (9): The value, as it should be heard., The full read-back sentence. `template` comes from the string table so the…, Emails are spoken with 'at' and 'dot', and the local part spelled out. The…, render(), render_value(), spell_email(), A read-back that omits which field it is about cannot be checked -- the user…, test_the_hindi_readback_frame_is_used_for_hindi() (+1 more)

### Community 59 - "M1. Implementation notes — instrumentation and corpus"
Cohesion: 0.33
Nodes (6): M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 61 - "Kind"
Cohesion: 0.10
Nodes (13): Kind, What sort of thing is being said, for channels that present them differently., PersonaChannel, Text channels: a console for a person, and a persona for the replay driver.…, Agree only if the value read back matches ground truth., One exchange, kept for the transcript., A simulated user, driven by a persona's script. Implements both protocols: it…, Turn (+5 more)

### Community 62 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 63 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 64 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 65 - "LucidForm"
Cohesion: 0.07
Nodes (17): Commands, Conventions, Environment, graphify, LucidForm, Paper, Phase 3 notes, Phase 4 notes (+9 more)

### Community 66 - "ReplayClient"
Cohesion: 0.22
Nodes (5): ModelReply, Path, Replays recorded model responses from disk, keyed by field and utterance. Lets…, One model response, plus what it cost., ReplayClient

### Community 67 - "base.py"
Cohesion: 0.22
Nodes (6): InputChannel, OutputChannel, Protocol, The boundary between the pipeline and however the user is actually talking. The…, State a validated value for confirmation. `value` is the exact string that will…, Return what the user said, or None if there is nothing further. None means the…

### Community 69 - "build_pin_directory.py"
Cohesion: 0.25
Nodes (7): collections, csv, main(), Path, Build lucidform/gate/data/pin_directory.json from the India Post pincode CSV.…, _title(), yaml

### Community 70 - "LucidForm — Specification"
Cohesion: 0.12
Nodes (14): Non-negotiables, Committed values that differ from ground truth. The correctness invariant, not…, _calling_module(), The first module on the stack that is not this one. Walked rather than indexed…, 1. Intent, 2. The gating contract — the thesis of the project, 3. Non-negotiables, 5. Rejection taxonomy (+6 more)

### Community 71 - "ISSUES.md — known problems, root causes, and fixes"
Cohesion: 0.25
Nodes (7): Decisions (approved 2026-09-30), ISSUES.md — known problems, root causes, and fixes, LF-001 — Can't fill the official CKYC form, LF-004 — Email only syntax-checked, LF-005 — Income band not derived from an amount, LF-009 — Near-miss answers get no suggestion, Summary

### Community 72 - "get_settings"
Cohesion: 0.15
Nodes (17): Canvas, get_settings(), Settings. Model id is config, never hardcoded -- the extraction-accuracy sweep…, build(), _header(), _overlay(), Path, Generate the target fillable PDF (AcroForm). The prototype's form reproduces… (+9 more)

### Community 75 - "load_all"
Cohesion: 0.16
Nodes (16): Fill in the form by conversation. With no --persona, prompts you at the…, run_cmd(), build(), _clean_extraction(), Any, Path, Build the offline extraction fixture corpus. python -m lucidform.eval.fixtures…, The straightforward case: the value was stated and heard correctly. (+8 more)

### Community 78 - "test_gate.py"
Cohesion: 0.08
Nodes (37): Closed rejection taxonomy. Every rejection carries exactly one. Each member…, Reason, candidate(), gate(), fixture, Gate-level invariants: the contract the rest of the pipeline relies on. Phase 2…, A rejection must not colour the next verdict. The gate is used in a loop over…, Construction order and instance identity must not matter. (+29 more)

### Community 79 - "test_issues_phase4.py"
Cohesion: 0.20
Nodes (13): Returns extractions handed to it. For tests that need one exact reply., ScriptedClient, The reported and the clamped value are both recorded. The gap between them is…, test_a_question_is_logged_too(), test_extraction_is_logged_with_both_confidence_figures(), Regression tests for docs/ISSUES.md LF-006: revisit missing fields, final…, test_a_hedged_yes_does_not_approve(), test_a_missing_field_is_asked_again_before_the_end() (+5 more)

### Community 80 - ".emit"
Cohesion: 0.39
Nodes (4): _jsonable(), Any, Path, Time a stage and emit once it completes. Mutate the yielded dict to attach the…

### Community 81 - "AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate"
Cohesion: 0.33
Nodes (6): AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate, Code map, Invariants — never break these (the test suite enforces them), Run, What this is, Working rules for agents

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

### Community 89 - "test_a_huge_retry_hint_is_capped"
Cohesion: 0.50
Nodes (3): test_a_huge_retry_hint_is_capped(), test_a_rate_limit_retry_delay_hint_is_honoured(), call()

### Community 90 - "III. System Architecture"
Cohesion: 0.25
Nodes (8): A. The five-stage pipeline, B. The validation gate and its rejection taxonomy, C. Extraction as a structurally bounded model call, D. Read-back and the confirmation whitelist, E. Three independent enforcement mechanisms, F. The orchestrator as a declared state graph, G. A help agent that cannot write, III. System Architecture

### Community 91 - "gate"
Cohesion: 0.67
Nodes (3): gate(), fixture, state()

### Community 96 - "Progress log"
Cohesion: 0.33
Nodes (5): 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5, 2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper, 2026-09-30 (night) · Shubh (+Claude) · Pre-push audit, 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs, Progress log

### Community 98 - "Live demo — 5 minutes, terminal only"
Cohesion: 0.40
Nodes (4): Backup commands (if the network is slow), Live demo — 5 minutes, terminal only, Script — what to type, and what to point out, The one-line pitch while it runs

### Community 99 - "Team guide"
Cohesion: 0.29
Nodes (7): 1. The idea in 60 seconds, 2. Who does what, 3. Setup, 4. The loop for every phase, 5. Saving tokens with graphify, 6. Rules nobody (human or AI) breaks, Team guide

### Community 101 - "LucidForm — Methodology"
Cohesion: 0.33
Nodes (5): LucidForm — Methodology, M7.1 Why replace a working loop, M7.2 Parity, not intuition, M7.3 No checkpoint-resume, M7. The orchestrator as a state graph

### Community 102 - "metrics.py"
Cohesion: 0.07
Nodes (35): FieldOutcome, _is_correct(), load_sessions(), parse_session(), outcome(), _pct(), percentile(), _personas() (+27 more)

## Knowledge Gaps
- **180 isolated node(s):** `fs`, `path`, `{
  Document, Packer, Paragraph, TextRun, AlignmentType, SectionType, Table, TableRow,
  TableCell, WidthType, BorderStyle, ShadingType, LevelFormat,
}`, `ROOT`, `SRC` (+175 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 774 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Candidate` connect `Candidate` to `Event`, `SessionGraph`, `test_issues_phase1.py`, `test_confirm.py`, `cli.py`, `FormState`, `asr_probe.py`, `ValidationGate`, `.commit`, `test_gate_crossfield.py`, `test_voice.py`, `models.py`, `test_adversarial.py`, `ExtractionOutcome`, `EventLog`, `Status`, `graph.py`, `LucidForm`, `LucidForm — Specification`, `test_gate.py`, `AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate`, `passing`, `III. System Architecture`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `FieldSpec` connect `FieldSpec` to `LucidForm`, `ReplayClient`, `ExtractionOutcome`, `EventLog`, `Status`, `answer.py`, `decode_spelled`, `test_extraction.py`, `asr_probe.py`, `AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate`, `ValidationGate`, `models.py`, `render_value`, `loader.py`, `HelpAgent`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M8. The help agent`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `ValidationGate` (e.g. with `asr_probe_cmd()` and `extract_cmd()`) actually correct?**
  _`ValidationGate` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Candidate` (e.g. with `Invariants — never break these (the test suite enforces them)` and `Conventions`) actually correct?**
  _`Candidate` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `FormState` (e.g. with `run_cmd()` and `ReplayRun`) actually correct?**
  _`FormState` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 34 inferred relationships involving `Status` (e.g. with `extract_cmd()` and `gate_check()`) actually correct?**
  _`Status` has 34 INFERRED edges - model-reasoned connections that need verification._