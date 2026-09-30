# Graph Report - LucidForm  (2026-09-30)

## Corpus Check
- 112 files · ~255,873 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .jsonl 17, (none) 4, .example 1)

## Summary
- 1844 nodes · 4108 edges · 108 communities (98 shown, 10 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 396 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3bfeaee0`
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
- readback.py
- test_metrics.py
- cli.py
- test_writer.py
- test_extraction.py
- asr_probe.py
- IV. Methodology
- What You Must Do When Invoked
- ValidationGate
- .commit
- test_no_silent_write.py
- test_gate_crossfield.py
- FieldSpec
- test_voice.py
- test_personas.py
- models.py
- test_checksums.py
- test_session.py
- test_schema_loader.py
- Title (pick one, or tell me to try again)
- test_adversarial.py
- HelpAgent
- voice.py
- Kind
- HelpIndex
- corpus.py
- Extractor
- Intent
- loader.py
- test_issues_phase2.py
- GeminiEmbedder
- answer.py
- test_help.py
- test_i18n.py
- grounding.py
- FormState
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
- parse_acroform
- test_the_readback_sentence_names_the_field_and_the_value
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- PersonaChannel
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- LucidForm
- run_persona
- base.py
- graphify reference: GitHub clone and cross-repo merge
- evaluate.py
- export
- suggest.py
- make_form.py
- .claude/CLAUDE.md
- extraction-spec.md
- load_all
- test_gate.py
- test_issues_phase4.py
- EventLog
- build
- parametrize
- passing
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- LucidForm
- Team workflow (5 people, each with their own AI assistant)
- M8. The help agent
- uidai_faq_update.md
- .decline
- III. System Architecture
- gate
- config.py
- ScriptedAnswerClient
- load_overlay
- README.md
- Progress log
- load_set
- Live demo — 5 minutes, terminal only
- Team guide
- spell
- LucidForm — Methodology
- metrics.py
- pytest
- test_a_failed_model_call_is_an_unclear_turn_not_a_crash
- test_an_ambiguous_or_orphan_enum_name_is_fatal
- test_a_form_is_filled_over_the_voice_channel

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 68 edges
2. `Candidate` - 63 edges
3. `Status` - 58 edges
4. `FormState` - 57 edges
5. `Extraction` - 48 edges
6. `load()` - 48 edges
7. `Event` - 47 edges
8. `EventLog` - 46 edges
9. `get_settings()` - 44 edges
10. `FieldSpec` - 44 edges

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

## Communities (108 total, 10 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.09
Nodes (44): normalize(), range_error(), Canonical form of a value: what gets read back, and what gets committed. The…, Well-formed, but outside the permitted domain., _enum_field(), field(), fixture, parametrize (+36 more)

### Community 1 - "Event"
Cohesion: 0.14
Nodes (25): Event, str, Read one session log. Used by metrics and by tests; never by the pipeline., read_log(), The event log is the evaluation substrate, so its guarantees are tested.…, Null means "not applicable"; zero would mean "instantaneous". Conflating them…, Hindi utterances must not be mangled into escapes. The logs are read by a human…, Not a swallowed error -- a logged finding (SPEC.md section 2). (+17 more)

### Community 2 - "test_formstate.py"
Cohesion: 0.09
Nodes (32): forge(), make(), The single write path, and every way of getting round it that I could think of.…, The fingerprint is recomputed at the write site, not trusted. Constructed by…, A passing verdict on one value must not authorise another. `confirm()` refuses…, The check the pipeline actually relies on: there is nothing to pass in., End to end: "yes I know that's wrong" must leave the form untouched., Handing out the underlying dict would be a second write path, since a caller… (+24 more)

### Community 3 - "test_readback.py"
Cohesion: 0.14
Nodes (27): field(), fixture, Read-back rendering: can the user actually check this by ear? For a user who…, A listener can check "example dot invalid" without hearing it letter by letter,…, Spelling a name the user just said would be tedious and no clearer., Presentation differs; the value does not. If rendering altered the value, the…, AKQPS3417M" spoken as a word is an unpronounceable noise that no listener can…, A synthesiser reading "3417" says "three thousand four hundred and seventeen",… (+19 more)

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
Cohesion: 0.15
Nodes (23): check(), Ground an extraction against the utterance it claims to come from. Only value-…, FieldType, str, `str.isdigit()` and `\\d` both accept these. The rules must not. This is the…, test_devanagari_digits_do_not_satisfy_the_numeric_patterns(), _extraction(), _gate() (+15 more)

### Community 8 - "test_confirm.py"
Cohesion: 0.07
Nodes (37): RuntimeError, A receipt was constructed outside the confirmation module., UnauthorizedIssuer, confirm(), normalize_utterance(), parse_affirmation(), Read-back confirmation: deciding whether the user actually said yes. This…, Lowercase, strip punctuation and filler, collapse whitespace. Apostrophes… (+29 more)

### Community 9 - "readback.py"
Cohesion: 0.16
Nodes (13): decode_spelled(), Turn a spelled-out transcript back into a value. The exact inverse of…, Rendering a validated value so a person can check it by ear. This is the last…, The value, as it should be heard., The full read-back sentence. `template` comes from the string table so the…, Emails are spoken with 'at' and 'dot', and the local part spelled out. The…, render(), render_value() (+5 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.05
Nodes (36): write_tables(), tempfile, agg(), fixture, The measures, and the guards on how they may be read. Every number reported in…, Six deliberate errors are planted across the three personas., The headline table must balance. A wrong value is stopped by the gate, stopped…, The correctness invariant. A defect, not a finding. (+28 more)

### Community 11 - "cli.py"
Cohesion: 0.09
Nodes (46): command, asr_probe_cmd(), extract_cmd(), _extraction_client(), gate_check(), graph_cmd(), _help_agent(), help_ask() (+38 more)

### Community 12 - "test_writer.py"
Cohesion: 0.12
Nodes (27): ExportError, Path, RuntimeError, Read the filled values out of an exported PDF. Used by the tests to verify that…, The export could not be performed. Never partially completed., read_back(), commit(), gate() (+19 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.08
Nodes (44): Help agent (RAG), Closed rejection taxonomy. Every rejection carries exactly one. Each member…, Reason, extractor(), gate(), fixture, Stage 3: utterance to candidate. No network. Every test here runs against a…, Belt and braces: intent says value, but there is none to propose. (+36 more)

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
Cohesion: 0.13
Nodes (6): date, Deterministic accept/reject on a single candidate value., Validate one candidate against the schema and confirmed values. `committed`…, ValidationGate, Check, One executed validation check. Recorded whether it passed or failed, so the log…

### Community 18 - ".commit"
Cohesion: 0.15
Nodes (11): AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate, Code map, Invariants — never break these (the test suite enforces them), Run, What this is, Working rules for agents, LF-008 — "I don't have a PAN" skips a required field, CommitRecord (+3 more)

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.12
Nodes (28): ast, Module, _help_violations(), _imported_names(), _parse(), parametrize, Path, _python_files() (+20 more)

### Community 20 - "test_gate_crossfield.py"
Cohesion: 0.07
Nodes (53): LF-003 — PIN / city / state mismatch accepted, check(), _city_agrees(), city_matches_pin_and_state(), CrossFieldResult, _or(), pan_matches_surname(), pin_matches_confirmed_state() (+45 more)

### Community 21 - "FieldSpec"
Cohesion: 0.10
Nodes (22): LF-002 — Weak Aadhaar validation, enum_error(), format_error(), is_placeholder_number(), length_error(), parse_date(), placeholder_error(), date (+14 more)

### Community 22 - "test_voice.py"
Cohesion: 0.12
Nodes (23): CorruptingRecognizer, EchoRecognizer, Returns text handed to it. Lets the channel be tested without audio., Applies documented speech-recognition error patterns, deterministically. **This…, Writes a valid but silent WAV. Exercises the file path without a voice., SilentSynthesizer, personas(), fixture (+15 more)

### Community 23 - "test_personas.py"
Cohesion: 0.10
Nodes (17): personas(), fixture, The synthetic corpus must be internally consistent. Accuracy is measured…, The form states an 18-year minimum, and the gate enforces it., A persona who has no email still has to say so out loud. An empty ground truth…, .invalid is reserved by RFC 2606 and can never resolve. A synthetic corpus that…, The data provenance claim in METHODOLOGY M0.8 is only true if the files…, A persona that cannot answer a required field would abandon it mid-run, which… (+9 more)

### Community 24 - "models.py"
Cohesion: 0.13
Nodes (17): datetime, enum, _calling_module(), ConfirmationReceipt, The confirmation receipt: the capability that authorises a write. A receipt is…, True if this receipt authorises writing exactly this value., The first module on the stack that is not this one. Walked rather than indexed…, Proof that one specific candidate was validated and explicitly affirmed.… (+9 more)

### Community 25 - "test_checksums.py"
Cohesion: 0.10
Nodes (29): aadhaar_valid(), corrupt_one_digit(), Checksum primitives for the validation gate. Pure functions over strings. No…, True if `digits` (including its trailing check digit) satisfies Verhoeff., Check digit for a payload that does not yet carry one., Structural + checksum validity of a 12-digit Aadhaar number. The first digit is…, Generate a checksum-valid but entirely fabricated Aadhaar number. Used only to…, Change exactly one digit, producing a checksum-invalid variant. The single-… (+21 more)

### Community 26 - "test_session.py"
Cohesion: 0.08
Nodes (47): Extraction, BaseModel, The model's entire permitted output., test_declining_pan_offers_form_60_and_commits_on_yes(), test_form_60_is_not_committed_without_yes(), test_session_rejects_the_shortened_aadhaar(), test_offered_band_denied_is_not_saved(), test_offered_band_needs_a_yes() (+39 more)

### Community 27 - "test_schema_loader.py"
Cohesion: 0.10
Nodes (16): Round-trip: the generator writes the AcroForm, the loader reads it back.…, A field the PDF does not have must raise, not be skipped. A silently dropped…, Conversely, a PDF widget nothing validates must raise., The error should tell you the command to run, not just fail., The rule in CLAUDE.md, enforced: declared names are the prompt's own words., An unfilled template must not carry a default for any field. A pre-selected…, The two cross-field checks must have their inputs wired up., The system exists to explain fields, so an unexplained field is a bug. Checked… (+8 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.25
Nodes (8): I. Introduction, II. Related Work, References, Title (pick one, or tell me to try again), V. Algorithm and Pseudocode, VI. Results, VII. Discussion, VIII. Conclusion and Future Work

### Community 29 - "test_adversarial.py"
Cohesion: 0.11
Nodes (15): _candidate(), committed(), gate(), fixture, parametrize, The adversarial suite -- the evidence for the safety claim. Every case in…, Every code in the taxonomy needs at least one case. An unexercised reason code…, A rejection-only category cannot distinguish a gate from a brick wall. The… (+7 more)

### Community 30 - "HelpAgent"
Cohesion: 0.16
Nodes (8): AnswerClient, HelpAgent, HelpAnswer, Protocol, _question_lines(), emit(), FAQ pages where a question is a line ending in '?' followed by its answer., StubHelper

### Community 31 - "voice.py"
Cohesion: 0.09
Nodes (21): FasterWhisperRecognizer, PiperSynthesizer, Path, Protocol, RuntimeError, The voice channel: speech in, speech out, pipeline unchanged. Phase 7 of the…, Local speech synthesis via Piper. Invoked as a subprocess rather than through a…, A speech backend was requested but is not installed. (+13 more)

### Community 32 - "Kind"
Cohesion: 0.14
Nodes (12): Kind, Purpose, str, Why the system is listening. The user does not see this; the channel does., What sort of thing is being said, for channels that present them differently., ConsoleChannel, Text channels: a console for a person, and a persona for the replay driver.…, A real person at a terminal. Output is prefixed by kind rather than coloured… (+4 more)

### Community 33 - "HelpIndex"
Cohesion: 0.14
Nodes (14): Chunk, _corpus_digest(), Embedder, HashEmbedder, HelpIndex, _normalise(), Path, Protocol (+6 more)

### Community 34 - "corpus.py"
Cohesion: 0.18
Nodes (14): html, _clean(), _flat(), _html_text(), load_chunks(), load_manifest(), _pdf_text(), Path (+6 more)

### Community 35 - "Extractor"
Cohesion: 0.18
Nodes (8): ExtractionOutcome, Extractor, Everything stage 3 produced, including the parts that did not become a value., Otherwise the Phase 5 replay driver stalls partway through a session., A missing fixture is a broken corpus, not a model failure -- it must be loud., test_a_replay_corpus_miss_still_raises(), test_every_persona_utterance_has_a_recorded_response(), test_replaying_p03_pan_yields_a_question_then_a_value()

### Community 36 - "Intent"
Cohesion: 0.15
Nodes (15): Intent, str, The shape the model is allowed to reply in. This schema is a safety boundary,…, What the user was doing, not what they said., os, extractor(), _has_credentials(), fixture (+7 more)

### Community 37 - "loader.py"
Cohesion: 0.13
Nodes (19): contextlib, dataclasses, json, Append-only session event log -- the evaluation substrate. One record per…, Run a persona through the whole pipeline, headlessly. This is the driver every…, ExtractionClient, Protocol, Model clients for the extraction layer. The extractor talks to a small protocol… (+11 more)

### Community 38 - "test_issues_phase2.py"
Cohesion: 0.23
Nodes (12): _gate(), fixture, parametrize, Regression tests for docs/ISSUES.md LF-003: PIN / city / state consistency. The…, schema(), test_correct_pairs_pass(), test_directory_lookup(), test_known_city_in_another_state_is_caught() (+4 more)

### Community 40 - "answer.py"
Cohesion: 0.13
Nodes (18): Extraction clients (Gemini), hashlib, GeminiAnswerClient, _passages(), Answering a user's question about a field, grounded in retrieved passages. The…, Hit, Hybrid retrieval over the help corpus: dense embeddings + BM25, fused by rank.…, _hinted_delay() (+10 more)

### Community 41 - "test_help.py"
Cohesion: 0.10
Nodes (22): HelpReply, BaseModel, The model's entire permitted output., reciprocal_rank_fusion(), The help agent: answers a user's question about a field from official…, agent(), chunks(), fixture (+14 more)

### Community 42 - "test_i18n.py"
Cohesion: 0.10
Nodes (26): available(), load(), The system's own wording, in one language., Strings, LucidForm -- accessibility-first form assistant. The LLM never writes a form…, parametrize, String tables. A missing key must fail loudly. Falling back to another language…, The read-back names the field, so an English label inside a Hindi read-back is… (+18 more)

### Community 43 - "grounding.py"
Cohesion: 0.15
Nodes (19): LF-007 — Model silently drops/changes digits, clamp_confidence(), digits_agree(), Grounding, locate(), _loose(), Deterministic checks on the model's output, performed without the model. The…, The digit string a quote spells out, or None if it cannot be read that way. (+11 more)

### Community 44 - "FormState"
Cohesion: 0.12
Nodes (9): FormState, Committed or explicitly declined -- either way, we are done asking., Confirmed values for one form-filling session., Read-only view. Handing out the dict itself would be a second write path, since…, The absence of an API is the enforcement. A `set` or `update` added for…, The whole point of requiring confirmation before a cross-field check. Once the…, test_committed_values_become_context_for_later_cross_field_checks(), test_form_state_exposes_no_alternative_mutator() (+1 more)

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
Cohesion: 0.06
Nodes (34): BaseSettings, Path, Settings, AnthropicExtractionClient, GeminiExtractionClient, make_client(), ModelReply, An extraction provider was named that this build has no client for. (+26 more)

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
Cohesion: 0.21
Nodes (13): RuntimeError, A write was attempted that did not satisfy the commit invariant. Raised, never…, SilentWriteBlocked, Candidate, A proposed value. Explicitly *not* a form value. Frozen: a receipt is bound to…, The central case. A held receipt must not authorise a value it was not issued…, SPEC.md section 2: a blocked write is a research finding, and a non-zero count…, test_a_blocked_write_is_logged_as_an_event() (+5 more)

### Community 56 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 57 - "parse_acroform"
Cohesion: 0.20
Nodes (11): Gotchas, _inherited(), parse_acroform(), Any, RuntimeError, The parsed form and the overlay disagree. Always fatal., Read a field attribute, following /Parent. AcroForm attributes are inheritable:…, Structure only. Returns {acroform_name: {widget, max_length, options}}. Reads… (+3 more)

### Community 59 - "M1. Implementation notes — instrumentation and corpus"
Cohesion: 0.33
Nodes (6): M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 61 - "PersonaChannel"
Cohesion: 0.21
Nodes (5): PersonaChannel, Agree only if the value read back matches ground truth., One exchange, kept for the transcript., A simulated user, driven by a persona's script. Implements both protocols: it…, Turn

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
Cohesion: 0.05
Nodes (30): Commands, Conventions, Environment, graphify, LucidForm, Non-negotiables, Paper, Phase 3 notes (+22 more)

### Community 66 - "run_persona"
Cohesion: 0.17
Nodes (12): Path, run_persona(), Path, Replays recorded model responses from disk, keyed by field and utterance. Lets…, ReplayClient, main(), record(), _scrub() (+4 more)

### Community 67 - "base.py"
Cohesion: 0.21
Nodes (7): InputChannel, OutputChannel, Protocol, The boundary between the pipeline and however the user is actually talking. The…, State a validated value for confirmation. `value` is the exact string that will…, Return what the user said, or None if there is nothing further. None means the…, test_the_fakes_satisfy_the_channel_protocols()

### Community 69 - "evaluate.py"
Cohesion: 0.15
Nodes (11): collections, csv, Measure the help agent against the hand-written question set. Four numbers,…, String table loading. Keys are looked up strictly. A missing key raises rather…, sys, time, main(), Path (+3 more)

### Community 70 - "export"
Cohesion: 0.22
Nodes (8): graphify reference: transcribe video and audio, Step 2.5 - Transcribe video / audio files (only if video files detected), export(), A one-page PDF carrying a large diagonal watermark., Write the confirmed values into a copy of the blank form. The template is never…, _stamp_page(), Every field of a real persona, through the whole pipeline and out., test_a_fully_completed_form_round_trips()

### Community 71 - "suggest.py"
Cohesion: 0.13
Nodes (17): difflib, Decisions (approved 2026-09-30), ISSUES.md — known problems, root causes, and fixes, LF-001 — Can't fill the official CKYC form, LF-004 — Email only syntax-checked, LF-005 — Income band not derived from an amount, LF-009 — Near-miss answers get no suggestion, Summary (+9 more)

### Community 72 - "make_form.py"
Cohesion: 0.27
Nodes (9): Canvas, build(), _header(), _overlay(), Path, Generate the target fillable PDF (AcroForm). The prototype's form reproduces…, reportlab_lib_colors, reportlab_lib_pagesizes (+1 more)

### Community 75 - "load_all"
Cohesion: 0.12
Nodes (22): build(), _clean_extraction(), Any, Path, Build the offline extraction fixture corpus. python -m lucidform.eval.fixtures…, The straightforward case: the value was stated and heard correctly., write(), _personas() (+14 more)

### Community 78 - "test_gate.py"
Cohesion: 0.08
Nodes (35): candidate(), gate(), fixture, Gate-level invariants: the contract the rest of the pipeline relies on. Phase 2…, A rejection must not colour the next verdict. The gate is used in a loop over…, Construction order and instance identity must not matter., An unreachable reason code would be a column in the results table that always…, Pinned deliberately. The reported reason distribution shifts if this changes,… (+27 more)

### Community 79 - "test_issues_phase4.py"
Cohesion: 0.11
Nodes (17): Returns extractions handed to it. For tests that need one exact reply., ScriptedClient, Session, test_a_question_is_logged_too(), test_state_is_proposed_from_the_pin_and_needs_a_yes(), Regression tests for docs/ISSUES.md LF-006: revisit missing fields, final…, test_a_hedged_yes_does_not_approve(), test_a_missing_field_is_asked_again_before_the_end() (+9 more)

### Community 80 - "EventLog"
Cohesion: 0.18
Nodes (12): EventLog, _jsonable(), Any, Path, Time a stage and emit once it completes. Mutate the yielded dict to attach the…, Append-only JSONL writer for one session., log(), fixture (+4 more)

### Community 81 - "build"
Cohesion: 0.29
Nodes (7): build(), build_user_message(), The extraction prompt. Built per field, from the schema the form parser…, Return (system, user) for one extraction., The prompt must not move validation into the model. A prompt saying "only…, test_enum_prompts_forbid_substituting_the_nearest_option(), test_prompt_carries_the_field_but_asks_for_no_judgement()

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

### Community 89 - ".decline"
Cohesion: 0.29
Nodes (5): Personas and live evaluation, DeclineRecord, _now(), Record that the user chose not to answer an optional field. Writes no value.…, An optional field the user chose not to answer. Recorded distinctly from an…

### Community 90 - "III. System Architecture"
Cohesion: 0.25
Nodes (8): A. The five-stage pipeline, B. The validation gate and its rejection taxonomy, C. Extraction as a structurally bounded model call, D. Read-back and the confirmation whitelist, E. Three independent enforcement mechanisms, F. The orchestrator as a declared state graph, G. A help agent that cannot write, III. System Architecture

### Community 91 - "gate"
Cohesion: 0.67
Nodes (3): gate(), fixture, state()

### Community 92 - "config.py"
Cohesion: 0.29
Nodes (5): functools, Settings. Model id is config, never hardcoded -- the extraction-accuracy sweep…, Network checks the gate may be given, but never performs itself (ISSUES.md…, pydantic, pydantic_settings

### Community 93 - "ScriptedAnswerClient"
Cohesion: 0.29
Nodes (4): Returns the replies handed to it; an Exception in the list is raised., ScriptedAnswerClient, The embedding call is a live API call too; it sits inside the fallback., test_a_retrieval_failure_never_breaks_the_session()

### Community 94 - "load_overlay"
Cohesion: 0.33
Nodes (6): load_overlay(), Path, built_pdf(), overlay(), fixture, schema()

### Community 96 - "Progress log"
Cohesion: 0.33
Nodes (5): 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5, 2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper, 2026-09-30 (night) · Shubh (+Claude) · Pre-push audit, 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs, Progress log

### Community 97 - "load_set"
Cohesion: 0.40
Nodes (5): load_set(), Path, write(), A gold label that matches nothing would score a correct retrieval as a miss., test_every_gold_label_exists_in_the_corpus()

### Community 98 - "Live demo — 5 minutes, terminal only"
Cohesion: 0.40
Nodes (4): Backup commands (if the network is slow), Live demo — 5 minutes, terminal only, Script — what to type, and what to point out, The one-line pitch while it runs

### Community 99 - "Team guide"
Cohesion: 0.29
Nodes (7): 1. The idea in 60 seconds, 2. Who does what, 3. Setup, 4. The loop for every phase, 5. Saving tokens with graphify, 6. Rules nobody (human or AI) breaks, Team guide

### Community 100 - "spell"
Cohesion: 0.40
Nodes (5): Render a value character by character, digits as words. Letters are upper-cased…, spell(), test_spell_groups_evenly_and_keeps_the_remainder(), test_spell_ignores_whitespace_in_the_source_value(), test_spell_without_grouping()

### Community 101 - "LucidForm — Methodology"
Cohesion: 0.33
Nodes (5): LucidForm — Methodology, M7.1 Why replace a working loop, M7.2 Parity, not intuition, M7.3 No checkpoint-resume, M7. The orchestrator as a state graph

### Community 102 - "metrics.py"
Cohesion: 0.07
Nodes (32): FieldOutcome, _is_correct(), load_sessions(), parse_session(), outcome(), _pct(), percentile(), Any (+24 more)

### Community 103 - "pytest"
Cohesion: 0.40
Nodes (4): pytest, _blank_form_template(), fixture, Session setup shared by the whole suite. The blank KYC template…

### Community 104 - "test_a_failed_model_call_is_an_unclear_turn_not_a_crash"
Cohesion: 0.40
Nodes (3): FailingClient, parametrize, test_a_failed_model_call_is_an_unclear_turn_not_a_crash()

### Community 105 - "test_an_ambiguous_or_orphan_enum_name_is_fatal"
Cohesion: 0.50
Nodes (4): parametrize, One spoken name for two options would make the gate choose for the user., test_an_ambiguous_or_orphan_enum_name_is_fatal(), test_malformed_enum_names_are_fatal()

### Community 106 - "test_a_form_is_filled_over_the_voice_channel"
Cohesion: 0.50
Nodes (3): The Phase 7 claim, asserted. The orchestrator, gate, confirmation step, and…, test_a_form_is_filled_over_the_voice_channel(), read_back()

## Knowledge Gaps
- **179 isolated node(s):** `fs`, `path`, `{
  Document, Packer, Paragraph, TextRun, AlignmentType, SectionType, Table, TableRow,
  TableCell, WidthType, BorderStyle, ShadingType, LevelFormat,
}`, `ROOT`, `SRC` (+174 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 781 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M8. The help agent`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `FieldSpec` connect `FieldSpec` to `test_gate_rules.py`, `LucidForm`, `Extractor`, `loader.py`, `suggest.py`, `answer.py`, `readback.py`, `cli.py`, `asr_probe.py`, `test_issues_phase4.py`, `build`, `.commit`, `test_llm_clients.py`, `ValidationGate`, `models.py`, `HelpAgent`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `Candidate` connect `Candidate` to `Event`, `test_formstate.py`, `SessionGraph`, `test_issues_phase1.py`, `test_confirm.py`, `cli.py`, `test_writer.py`, `asr_probe.py`, `ValidationGate`, `.commit`, `test_gate_crossfield.py`, `test_voice.py`, `models.py`, `test_adversarial.py`, `Extractor`, `loader.py`, `test_issues_phase2.py`, `FormState`, `Status`, `LucidForm`, `test_gate.py`, `passing`, `III. System Architecture`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `ValidationGate` (e.g. with `asr_probe_cmd()` and `extract_cmd()`) actually correct?**
  _`ValidationGate` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Candidate` (e.g. with `Invariants — never break these (the test suite enforces them)` and `Conventions`) actually correct?**
  _`Candidate` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `Status` (e.g. with `extract_cmd()` and `gate_check()`) actually correct?**
  _`Status` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `FormState` (e.g. with `run_cmd()` and `ReplayRun`) actually correct?**
  _`FormState` has 11 INFERRED edges - model-reasoned connections that need verification._