# Graph Report - LucidForm  (2026-09-30)

## Corpus Check
- 100 files · ~224,900 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 16 file(s) not represented in the graph (top: .jsonl 9, (none) 4, .example 1)

## Summary
- 1634 nodes · 3453 edges · 94 communities (70 shown, 24 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 244 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7ec6d221`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_gate_rules.py
- Event
- Candidate
- test_readback.py
- index.py
- SessionGraph
- load
- test_confirm.py
- test_gate_crossfield.py
- test_metrics.py
- cli.py
- FormState
- test_extraction.py
- asr_probe.py
- parametrize
- What You Must Do When Invoked
- crossfield.py
- Row
- pytest
- AnswerClient
- Extraction
- test_voice.py
- test_personas.py
- ValidationGate
- test_checksums.py
- test_session.py
- load
- Title (pick one, or tell me to try again)
- test_adversarial.py
- .answer
- voice.py
- index
- HashEmbedder
- corpus.py
- HelpIndex
- Intent
- loader.py
- FieldSpec
- models.py
- GeminiEmbedder
- test_help.py
- test_i18n.py
- replay.py
- .commit
- M0. System design
- graphify reference: extra exports and benchmark
- M2. The validation gate
- answer.py
- Prompt for Claude Code — LucidForm Prototype
- test_llm_clients.py
- M3. The write path
- M4. Extraction
- M5. Orchestration and read-back
- graphify reference: query, path, explain
- test_a_form_is_filled_over_the_voice_channel
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- Purpose
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- PersonaChannel
- MissingString
- graphify reference: GitHub clone and cross-repo merge
- LucidForm — Specification
- get_settings
- .claude/CLAUDE.md
- extraction-spec.md
- Status
- Extractor
- Puppet
- percentile
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- i18n/__init__.py
- M8. The help agent
- uidai_faq_update.md
- metrics.py
- Progress log
- Live demo — 5 minutes, terminal only
- LucidForm — Methodology

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 55 edges
2. `Candidate` - 52 edges
3. `FormState` - 48 edges
4. `load()` - 43 edges
5. `Event` - 40 edges
6. `get_settings()` - 40 edges
7. `EventLog` - 38 edges
8. `Status` - 36 edges
9. `FieldSpec` - 35 edges
10. `Extraction` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Conventions` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py
- `A. The five-stage pipeline` --references--> `Candidate`  [INFERRED]
  docs/paper-draft.md → lucidform/models.py
- `Commit invariant` --references--> `SilentWriteBlocked`  [INFERRED]
  SPEC.md → lucidform/formstate/state.py
- `Three enforcement mechanisms` --references--> `ConfirmationReceipt`  [INFERRED]
  SPEC.md → lucidform/formstate/receipt.py
- `Non-negotiables` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py

## Import Cycles
- None detected.

## Communities (94 total, 24 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.06
Nodes (32): enum_error(), format_error(), length_error(), normalize(), parse_date(), range_error(), strip_invisible(), field() (+24 more)

### Community 1 - "Event"
Cohesion: 0.07
Nodes (21): Event, EventLog, _jsonable(), read_log(), log(), test_a_second_log_on_the_same_session_appends(), test_dataclass_payloads_are_serialised(), test_enums_inside_payloads_become_their_values() (+13 more)

### Community 2 - "Candidate"
Cohesion: 0.07
Nodes (28): SilentWriteBlocked, Candidate, forge(), gate(), make(), state(), test_a_blocked_write_is_logged_as_an_event(), test_a_confirmed_value_is_written() (+20 more)

### Community 3 - "test_readback.py"
Cohesion: 0.08
Nodes (26): render(), render_value(), spell(), spell_email(), field(), render(), schema(), test_a_date_has_no_leading_zero_on_the_day() (+18 more)

### Community 4 - "index.py"
Cohesion: 0.24
Nodes (4): Hit, reciprocal_rank_fusion(), tokenize(), test_reciprocal_rank_fusion_rewards_agreement()

### Community 5 - "SessionGraph"
Cohesion: 0.07
Nodes (16): _build(), edges(), mermaid(), node_names(), _route(), SessionGraph, _structure(), _Stub (+8 more)

### Community 6 - "load"
Cohesion: 0.15
Nodes (8): load(), test_an_unknown_language_fails_with_a_useful_message(), test_every_field_has_a_spoken_label_in_this_language(), test_every_language_has_the_same_keys(), test_every_schema_field_has_a_prompt_and_gloss_in_this_language(), test_hindi_strings_are_actually_devanagari(), test_no_string_is_empty(), test_placeholders_match_across_languages()

### Community 8 - "test_confirm.py"
Cohesion: 0.07
Nodes (20): UnauthorizedIssuer, confirm(), normalize_utterance(), gate(), _mint_as_issuer(), passing(), test_a_confirmation_issues_a_receipt(), test_a_denial_issues_no_receipt() (+12 more)

### Community 9 - "test_gate_crossfield.py"
Cohesion: 0.12
Nodes (13): pan_matches_surname(), _check(), gate(), test_a_check_with_an_unconfirmed_dependency_is_skipped_not_passed(), test_an_empty_dependency_counts_as_unconfirmed(), test_cross_field_checks_read_only_committed_values(), test_pan_fifth_character_disagreeing_with_the_surname_fails(), test_pan_fifth_character_matching_the_surname_passes() (+5 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.05
Nodes (22): agg(), runs(), schema(), sessions(), test_a_question_and_the_answer_after_it_are_separate_turns(), test_a_tampered_log_is_detected(), test_all_tables_are_written(), test_normalisation_is_applied_before_judging_a_proposal() (+14 more)

### Community 11 - "cli.py"
Cohesion: 0.09
Nodes (17): asr_probe_cmd(), extract_cmd(), _extraction_client(), gate_check(), graph_cmd(), _help_agent(), help_ask(), help_build() (+9 more)

### Community 12 - "FormState"
Cohesion: 0.08
Nodes (21): graphify reference: transcribe video and audio, Step 2.5 - Transcribe video / audio files (only if video files detected), FormState, export(), ExportError, read_back(), commit(), gate() (+13 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.08
Nodes (27): Reason, extractor(), gate(), replay(), schema(), test_a_decline_never_becomes_a_candidate(), test_a_loose_match_reports_no_span_rather_than_a_wrong_one(), test_a_question_never_becomes_a_candidate() (+19 more)

### Community 14 - "asr_probe.py"
Cohesion: 0.10
Nodes (15): _category(), character_error_rate(), decode_spelled(), is_simulated(), levenshtein(), probe(), ProbeResult, ProbeSummary (+7 more)

### Community 15 - "parametrize"
Cohesion: 0.33
Nodes (3): test_every_field_is_resolved(), test_no_committed_value_differs_from_ground_truth(), test_no_write_was_blocked_during_a_normal_session()

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

### Community 17 - "crossfield.py"
Cohesion: 0.19
Nodes (8): check(), CrossFieldResult, pin_matches_confirmed_state(), _skipped(), test_a_state_with_no_region_data_is_not_checked(), test_fields_without_a_cross_field_rule_return_nothing(), test_pin_in_the_right_postal_region_passes(), test_pin_in_the_wrong_postal_region_fails()

### Community 18 - "Row"
Cohesion: 0.38
Nodes (4): Row, summarise(), test_scoring_counts_hits_answers_and_refusals(), row()

### Community 19 - "pytest"
Cohesion: 0.13
Nodes (13): _imported_names(), _parse(), _python_files(), _rel(), test_decision_and_write_paths_import_no_model(), test_forbidden_import_detection_works(), test_private_form_state_is_not_touched_from_outside(), test_receipts_are_minted_only_by_the_confirmation_module() (+5 more)

### Community 21 - "Extraction"
Cohesion: 0.14
Nodes (10): check(), clamp_confidence(), Grounding, locate(), _loose(), Extraction, test_a_model_reporting_impossible_confidence_is_clamped(), test_a_reply_that_does_not_fit_the_schema_is_an_error_not_a_fallback() (+2 more)

### Community 22 - "test_voice.py"
Cohesion: 0.10
Nodes (15): InputChannel, OutputChannel, CorruptingRecognizer, EchoRecognizer, SilentSynthesizer, personas(), schema(), test_an_empty_transcript_is_an_unusable_answer_not_a_hang_up() (+7 more)

### Community 23 - "test_personas.py"
Cohesion: 0.08
Nodes (10): pin_matches_state(), test_a_persona_with_no_utterances_is_rejected(), test_aadhaar_numbers_satisfy_verhoeff(), test_email_addresses_use_a_reserved_domain(), test_every_persona_declares_a_synthetic_header(), test_everyone_is_an_adult(), test_ground_truth_covers_every_required_field(), test_optional_fields_may_be_declined_but_must_still_be_answerable() (+2 more)

### Community 25 - "test_checksums.py"
Cohesion: 0.13
Nodes (14): aadhaar_valid(), corrupt_one_digit(), synthetic_aadhaar(), verhoeff_check_digit(), verhoeff_valid(), test_adjacent_transpositions_are_caught(), test_check_digit_completes_a_payload(), test_check_digit_rejects_non_numeric_payload() (+6 more)

### Community 26 - "test_session.py"
Cohesion: 0.09
Nodes (23): one_field(), test_a_confirmed_value_is_committed(), test_a_declined_optional_field_stays_empty(), test_a_denied_readback_is_recorded_as_a_correction(), test_a_field_that_runs_out_of_attempts_is_abandoned_not_left_empty(), test_a_hang_up_at_the_read_back_ends_the_field_without_re_asking(), test_a_question_is_answered_and_does_not_count_as_an_attempt(), test_a_question_is_answered_by_the_help_agent_and_never_becomes_a_value() (+15 more)

### Community 27 - "load"
Cohesion: 0.07
Nodes (17): _inherited(), load(), load_overlay(), parse_acroform(), SchemaError, built_pdf(), overlay(), schema() (+9 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.09
Nodes (21): A. Form representation, A. The five-stage pipeline, B. Synthetic data and its construction, B. The validation gate and its rejection taxonomy, C. Adversarial evaluation corpora, C. Extraction as a structurally bounded model call, D. Evaluation harness and its honesty constraints, D. Read-back and the confirmation whitelist (+13 more)

### Community 29 - "test_adversarial.py"
Cohesion: 0.11
Nodes (8): _candidate(), committed(), gate(), test_adversarial_case(), test_every_case_declares_why_it_exists(), test_gate_never_raises_on_hostile_input(), test_the_suite_covers_every_reason_code_the_gate_can_emit(), test_the_suite_has_controls_in_the_categories_that_need_them()

### Community 30 - ".answer"
Cohesion: 0.20
Nodes (5): HelpAnswer, _passages(), _question_lines(), emit(), StubHelper

### Community 31 - "voice.py"
Cohesion: 0.10
Nodes (6): FasterWhisperRecognizer, PiperSynthesizer, SpeechRecognizer, SpeechSynthesizer, VoiceBackendMissing, test_asking_for_a_missing_backend_says_how_to_install_it()

### Community 32 - "index"
Cohesion: 0.50
Nodes (3): chunks(), index(), schema()

### Community 33 - "HashEmbedder"
Cohesion: 0.22
Nodes (5): _corpus_digest(), HashEmbedder, _normalise(), test_an_index_built_with_another_embedder_is_refused(), test_the_index_round_trips_through_disk()

### Community 34 - "corpus.py"
Cohesion: 0.18
Nodes (10): _clean(), _flat(), _html_text(), load_chunks(), load_manifest(), _pdf_text(), _read(), _slug() (+2 more)

### Community 35 - "HelpIndex"
Cohesion: 0.29
Nodes (3): Chunk, Embedder, HelpIndex

### Community 36 - "Intent"
Cohesion: 0.17
Nodes (7): Intent, extractor(), _has_credentials(), test_a_decline_is_not_extracted_as_a_value(), test_a_question_is_not_extracted_as_a_value(), test_a_spoken_identifier_is_transcribed(), test_the_model_cannot_return_anything_outside_the_schema()

### Community 37 - "loader.py"
Cohesion: 0.11
Nodes (5): build(), _clean_extraction(), write(), __iter__(), Persona

### Community 38 - "FieldSpec"
Cohesion: 0.13
Nodes (6): build(), build_user_message(), FieldSpec, FormSchema, test_enum_prompts_forbid_substituting_the_nearest_option(), test_prompt_carries_the_field_but_asks_for_no_judgement()

### Community 39 - "models.py"
Cohesion: 0.10
Nodes (11): Invariants — never break these (the test suite enforces them), Gotchas, Non-negotiables, _calling_module(), ConfirmationReceipt, Affirmation, fingerprint(), ValidationReport (+3 more)

### Community 41 - "test_help.py"
Cohesion: 0.09
Nodes (12): HelpReply, ScriptedAnswerClient, agent(), test_a_citation_to_a_passage_that_was_not_retrieved_falls_back(), test_a_cited_answer_is_spoken_with_its_source(), test_a_model_failure_never_breaks_the_session(), test_an_unanswerable_question_falls_back_and_says_so(), test_an_uncited_answer_falls_back() (+4 more)

### Community 42 - "test_i18n.py"
Cohesion: 0.19
Nodes (5): Strings, test_a_missing_key_raises_rather_than_falling_back(), test_a_missing_placeholder_raises_with_the_key_named(), test_the_canonical_label_stays_english_for_the_pdf_and_logs(), test_the_greeting_explains_the_confirmation_step()

### Community 43 - "replay.py"
Cohesion: 0.13
Nodes (10): ReplayRun, run_persona(), ReplayClient, Session, main(), record(), _scrub(), personas() (+2 more)

### Community 44 - ".commit"
Cohesion: 0.15
Nodes (5): V. Algorithm and Pseudocode, CommitRecord, DeclineRecord, block(), _now()

### Community 45 - "M0. System design"
Cohesion: 0.20
Nodes (10): M0.1 Problem framing, M0.2 The five-stage pipeline, M0.3 Enforcing the constraint rather than asserting it, M0.4 Form representation: parser-assisted, human-verified schema, M0.5 Language selection, M0.6 Deferral of the voice channel, M0.7 Evaluation design, M0.8 Data (+2 more)

### Community 46 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 48 - "M2. The validation gate"
Cohesion: 0.22
Nodes (9): M2.1 Construction order, M2.2 Both directions are asserted, M2.3 Check ordering as a defined quantity, M2.4 Normalization reshapes but does not repair, M2.5 A script-dependent validation trap, M2.6 Cross-field checks and the confirmation dependency, M2.7 The validator does not interpret text, M2.8 Isolation (+1 more)

### Community 49 - "answer.py"
Cohesion: 0.15
Nodes (8): help_eval(), default_index_dir(), GeminiAnswerClient, HelpAgent, load_agent(), load_set(), run(), write()

### Community 50 - "Prompt for Claude Code — LucidForm Prototype"
Cohesion: 0.29
Nodes (6): Context, How I want you to work with me, Non-negotiable design constraint, Prompt for Claude Code — LucidForm Prototype, Scope for THIS prototype (deliberately small), What I need from you, in order

### Community 51 - "test_llm_clients.py"
Cohesion: 0.05
Nodes (23): Settings, AnthropicExtractionClient, ExtractionClient, GeminiExtractionClient, make_client(), ModelReply, UnknownProvider, json_config() (+15 more)

### Community 52 - "M3. The write path"
Cohesion: 0.29
Nodes (7): M3.1 Three mechanisms, and what each actually covers, M3.2 Testing each precondition in isolation, M3.3 Affirmation parsing, and why it is a whitelist, M3.4 Adversarial evaluation of the confirmation step, M3.5 Corrections, declines, and the distinction between them, M3.6 Export, M3. The write path

### Community 53 - "M4. Extraction"
Cohesion: 0.29
Nodes (7): M4.1 The model's output is bounded by a schema, not by instruction, M4.2 Intent is separated from value, M4.3 Two deterministic checks on the model's output, M4.4 What the offline corpus can and cannot measure, M4.5 The extractor does not repair, M4.6 Live testing, M4. Extraction

### Community 54 - "M5. Orchestration and read-back"
Cohesion: 0.29
Nodes (7): M5.1 The orchestrator makes no judgements, M5.2 Read-back as an audibility problem, M5.3 Read-back detects a class of error nothing else can, M5.4 Asking for an explanation is not a failed attempt, M5.5 The simulated user, M5.6 Localisation of what the user hears, M5. Orchestration and read-back

### Community 56 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 57 - "test_a_form_is_filled_over_the_voice_channel"
Cohesion: 0.22
Nodes (5): Transcript, test_a_form_is_filled_over_the_voice_channel(), read_back(), test_a_perfect_recogniser_loses_nothing(), transcribe()

### Community 59 - "M1. Implementation notes — instrumentation and corpus"
Cohesion: 0.33
Nodes (6): M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 61 - "Purpose"
Cohesion: 0.11
Nodes (6): Kind, Purpose, ConsoleChannel, VoiceChannel, VoiceTurn, test_the_module_imports_without_any_speech_library()

### Community 62 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 63 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 64 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 65 - "PersonaChannel"
Cohesion: 0.06
Nodes (11): Commands, Conventions, Environment, graphify, LucidForm, Phase 3 notes, Phase 4 notes, Phase 5 notes (+3 more)

### Community 70 - "LucidForm — Specification"
Cohesion: 0.05
Nodes (35): AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate, Code map, Run, What this is, Working rules for agents, Handing off to another AI, One-time setup, Per phase (+27 more)

### Community 72 - "get_settings"
Cohesion: 0.18
Nodes (7): get_settings(), build(), _header(), _overlay(), personas(), schema(), test_the_extended_set_is_present_and_separate()

### Community 78 - "Status"
Cohesion: 0.10
Nodes (19): Status, candidate(), gate(), schema(), test_a_pass_carries_the_exact_value_that_will_be_written(), test_a_pass_must_not_carry_a_reason(), test_a_rejection_carries_nothing_committable(), test_a_rejection_must_carry_a_reason() (+11 more)

### Community 79 - "Extractor"
Cohesion: 0.13
Nodes (7): ScriptedClient, ExtractionOutcome, Extractor, test_a_question_is_logged_too(), test_every_persona_utterance_has_a_recorded_response(), test_extraction_is_logged_with_both_confidence_figures(), test_replaying_p03_pan_yields_a_question_then_a_value()

### Community 83 - "percentile"
Cohesion: 0.29
Nodes (3): percentile(), test_percentile_of_nothing_is_none_not_zero(), test_percentiles_are_values_that_actually_occurred()

### Community 84 - "Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms"
Cohesion: 0.50
Nodes (3): A: Form No. 93 – PAN Application Form for Individual (Being citizen of India), FAQ's on PAN, Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms

### Community 87 - "M8. The help agent"
Cohesion: 0.33
Nodes (6): M8.1 Scope: explanation, never a value, M8.2 Corpus and chunking, M8.3 Hybrid retrieval, M8.4 The citation check, M8.5 Evaluation, and what it does not measure, M8. The help agent

### Community 89 - "metrics.py"
Cohesion: 0.12
Nodes (15): metrics_cmd(), FieldOutcome, _is_correct(), load_sessions(), parse_session(), outcome(), _pct(), _personas() (+7 more)

### Community 96 - "Progress log"
Cohesion: 0.50
Nodes (3): 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5, 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs, Progress log

### Community 98 - "Live demo — 5 minutes, terminal only"
Cohesion: 0.40
Nodes (4): Backup commands (if the network is slow), Live demo — 5 minutes, terminal only, Script — what to type, and what to point out, The one-line pitch while it runs

### Community 101 - "LucidForm — Methodology"
Cohesion: 0.33
Nodes (5): LucidForm — Methodology, M7.1 Why replace a working loop, M7.2 Parity, not intuition, M7.3 No checkpoint-resume, M7. The orchestrator as a state graph

## Knowledge Gaps
- **147 isolated node(s):** `Commands`, `Environment`, `Phase 3 notes`, `graphify`, `M7.1 Why replace a working loop` (+142 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 721 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Candidate` connect `Candidate` to `PersonaChannel`, `Event`, `FieldSpec`, `models.py`, `test_confirm.py`, `test_gate_crossfield.py`, `cli.py`, `FormState`, `.commit`, `asr_probe.py`, `Extractor`, `Status`, `test_voice.py`, `ValidationGate`, `Title (pick one, or tell me to try again)`, `test_adversarial.py`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M8. The help agent`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Why does `LucidForm — Specification` connect `LucidForm — Specification` to `models.py`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ValidationGate` (e.g. with `Candidate` and `Check`) actually correct?**
  _`ValidationGate` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `Candidate` (e.g. with `Invariants — never break these (the test suite enforces them)` and `Conventions`) actually correct?**
  _`Candidate` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `FormState` (e.g. with `Event` and `EventLog`) actually correct?**
  _`FormState` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Event` (e.g. with `VoiceChannel` and `Extractor`) actually correct?**
  _`Event` has 24 INFERRED edges - model-reasoned connections that need verification._