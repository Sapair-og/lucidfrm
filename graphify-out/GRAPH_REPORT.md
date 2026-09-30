# Graph Report - LucidForm  (2026-09-30)

## Corpus Check
- 92 files · ~216,194 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .example 1, .jsonl 1)

## Summary
- 1559 nodes · 3348 edges · 101 communities (72 shown, 29 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 253 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2fdd934e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_gate_rules.py
- Event
- Candidate
- test_readback.py
- LucidForm
- SessionGraph
- test_i18n.py
- Status
- test_confirm.py
- test_gate_crossfield.py
- test_metrics.py
- cli.py
- FormState
- test_extraction.py
- asr_probe.py
- parametrize
- What You Must Do When Invoked
- ConfirmationReceipt
- parse_session
- test_no_silent_write.py
- Purpose
- Extraction
- test_voice.py
- test_personas.py
- ValidationGate
- test_checksums.py
- test_session.py
- test_schema_loader.py
- Title (pick one, or tell me to try again)
- test_adversarial.py
- answer.py
- voice.py
- loader.py
- test_help.py
- corpus.py
- Chunk
- Intent
- load_all
- .answer
- models.py
- GeminiEmbedder
- FieldSpec
- confirm
- run_persona
- with_retries
- M0. System design
- graphify reference: extra exports and benchmark
- write_tables
- M2. The validation gate
- aadhaar_valid
- Prompt for Claude Code — LucidForm Prototype
- test_llm_clients.py
- M3. The write path
- M4. Extraction
- M5. Orchestration and read-back
- LucidForm
- graphify reference: query, path, explain
- run_cmd
- metrics.py
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- graph.py
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- PersonaChannel
- .emit
- Aggregate
- graphify reference: GitHub clone and cross-repo merge
- LucidForm — Specification
- LucidForm — Methodology
- get_settings
- .claude/CLAUDE.md
- extraction-spec.md
- gate
- candidate
- Extractor
- Puppet
- test_a_declined_optional_field_stays_empty
- index.py
- test_a_question_is_handled_mid_session
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- PersonaError
- _is_correct
- pytest
- uidai_faq_update.md
- percentile
- test_the_gate_catches_the_homoglyph
- ScriptedClient
- test_the_readback_catches_what_nothing_else_could
- test_out_of_enum_answers_are_re_asked_not_mapped
- StubHelper
- test_a_form_is_filled_over_the_voice_channel
- test_the_session_log_identifies_which_client_produced_it
- test_form_state_exposes_no_alternative_mutator

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 55 edges
2. `Candidate` - 51 edges
3. `FormState` - 48 edges
4. `Event` - 41 edges
5. `load()` - 41 edges
6. `EventLog` - 38 edges
7. `Status` - 36 edges
8. `Extraction` - 35 edges
9. `read_log()` - 35 edges
10. `FieldSpec` - 34 edges

## Surprising Connections (you probably didn't know these)
- `Conventions` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py
- `Three enforcement mechanisms` --references--> `ConfirmationReceipt`  [INFERRED]
  SPEC.md → lucidform/formstate/receipt.py
- `Commit invariant` --references--> `SilentWriteBlocked`  [INFERRED]
  SPEC.md → lucidform/formstate/state.py
- `A. The five-stage pipeline` --references--> `Candidate`  [INFERRED]
  docs/paper-draft.md → lucidform/models.py
- `Non-negotiables` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py

## Import Cycles
- None detected.

## Communities (101 total, 29 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.07
Nodes (33): enum_error(), format_error(), length_error(), normalize(), parse_date(), range_error(), strip_invisible(), FieldType (+25 more)

### Community 1 - "Event"
Cohesion: 0.13
Nodes (16): Event, read_log(), log(), test_a_second_log_on_the_same_session_appends(), test_dataclass_payloads_are_serialised(), test_enums_inside_payloads_become_their_values(), test_latency_is_null_when_unmeasured_not_zero(), test_records_are_appended_never_overwritten() (+8 more)

### Community 2 - "Candidate"
Cohesion: 0.08
Nodes (24): SilentWriteBlocked, Candidate, make(), test_a_blocked_write_is_logged_as_an_event(), test_a_confirmed_value_is_written(), test_a_correction_still_requires_its_own_confirmation(), test_a_field_can_be_corrected_and_the_history_shows_both(), test_a_receipt_authorising_an_empty_value_is_refused() (+16 more)

### Community 3 - "test_readback.py"
Cohesion: 0.09
Nodes (25): render(), render_value(), spell(), spell_email(), field(), render(), schema(), test_a_date_has_no_leading_zero_on_the_day() (+17 more)

### Community 4 - "LucidForm"
Cohesion: 0.18
Nodes (8): Commands, Conventions, Environment, graphify, LucidForm, Non-negotiables, Phase 3 notes, _calling_module()

### Community 5 - "SessionGraph"
Cohesion: 0.13
Nodes (4): SessionGraph, TurnState, FieldResult, SessionResult

### Community 6 - "test_i18n.py"
Cohesion: 0.06
Nodes (16): available(), load(), MissingString, Strings, test_a_missing_key_raises_rather_than_falling_back(), test_a_missing_placeholder_raises_with_the_key_named(), test_an_unknown_language_fails_with_a_useful_message(), test_both_languages_are_available() (+8 more)

### Community 7 - "Status"
Cohesion: 0.13
Nodes (11): Status, gate(), schema(), test_a_pass_carries_the_exact_value_that_will_be_written(), test_a_pass_must_not_carry_a_reason(), test_a_rejection_carries_nothing_committable(), test_a_rejection_must_carry_a_reason(), test_check_order_covers_the_whole_taxonomy() (+3 more)

### Community 8 - "test_confirm.py"
Cohesion: 0.09
Nodes (15): UnauthorizedIssuer, normalize_utterance(), parse_affirmation(), gate(), _mint_as_issuer(), passing(), test_a_substring_parser_would_fail_this_suite(), test_affirmation_case() (+7 more)

### Community 9 - "test_gate_crossfield.py"
Cohesion: 0.07
Nodes (23): check(), CrossFieldResult, pan_matches_surname(), pin_matches_confirmed_state(), _skipped(), pin_matches_state(), _check(), gate() (+15 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.06
Nodes (14): agg(), schema(), sessions(), test_a_question_and_the_answer_after_it_are_separate_turns(), test_nothing_wrong_was_committed(), test_offline_sessions_are_flagged_as_not_measuring_accuracy(), test_recall_and_false_positive_rate_are_both_reported(), test_the_caveat_survives_into_the_csv() (+6 more)

### Community 11 - "cli.py"
Cohesion: 0.13
Nodes (10): asr_probe_cmd(), gate_check(), graph_cmd(), help_ask(), make_form_cmd(), metrics_cmd(), personas_list(), personas_show() (+2 more)

### Community 12 - "FormState"
Cohesion: 0.06
Nodes (24): graphify reference: transcribe video and audio, Step 2.5 - Transcribe video / audio files (only if video files detected), CommitRecord, DeclineRecord, FormState, _now(), export(), ExportError (+16 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.11
Nodes (22): extractor(), gate(), replay(), schema(), test_a_decline_never_becomes_a_candidate(), test_a_loose_match_reports_no_span_rather_than_a_wrong_one(), test_a_question_never_becomes_a_candidate(), test_a_quote_from_the_utterance_grounds() (+14 more)

### Community 14 - "asr_probe.py"
Cohesion: 0.09
Nodes (15): _category(), character_error_rate(), decode_spelled(), is_simulated(), levenshtein(), probe(), ProbeResult, ProbeSummary (+7 more)

### Community 15 - "parametrize"
Cohesion: 0.33
Nodes (3): test_every_field_is_resolved(), test_no_committed_value_differs_from_ground_truth(), test_no_write_was_blocked_during_a_normal_session()

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (25): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+17 more)

### Community 17 - "ConfirmationReceipt"
Cohesion: 0.12
Nodes (9): Gotchas, V. Algorithm and Pseudocode, ConfirmationReceipt, block(), Affirmation, fingerprint(), ValidationReport, 4. Data model (+1 more)

### Community 18 - "parse_session"
Cohesion: 0.15
Nodes (8): load_sessions(), parse_session(), _personas(), SessionMetrics, Turn, test_a_session_without_ground_truth_is_excluded_from_accuracy(), test_a_tampered_log_is_detected(), test_unscored_sessions_still_contribute_the_measures_that_need_no_truth()

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.13
Nodes (13): _imported_names(), _parse(), _python_files(), _rel(), test_decision_and_write_paths_import_no_model(), test_forbidden_import_detection_works(), test_private_form_state_is_not_touched_from_outside(), test_receipts_are_minted_only_by_the_confirmation_module() (+5 more)

### Community 20 - "Purpose"
Cohesion: 0.10
Nodes (6): InputChannel, Kind, OutputChannel, Purpose, ConsoleChannel, VoiceTurn

### Community 21 - "Extraction"
Cohesion: 0.14
Nodes (10): check(), clamp_confidence(), Grounding, locate(), _loose(), Extraction, test_a_model_reporting_impossible_confidence_is_clamped(), test_a_reply_that_does_not_fit_the_schema_is_an_error_not_a_fallback() (+2 more)

### Community 22 - "test_voice.py"
Cohesion: 0.13
Nodes (15): EchoRecognizer, SilentSynthesizer, VoiceChannel, personas(), schema(), test_an_empty_transcript_is_an_unusable_answer_not_a_hang_up(), test_asr_confidence_is_recorded_but_never_reaches_the_gate(), test_audio_events_are_logged_on_both_sides() (+7 more)

### Community 23 - "test_personas.py"
Cohesion: 0.10
Nodes (8): personas(), schema(), test_email_addresses_use_a_reserved_domain(), test_every_persona_declares_a_synthetic_header(), test_everyone_is_an_adult(), test_ground_truth_covers_every_required_field(), test_optional_fields_may_be_declined_but_must_still_be_answerable(), test_pan_is_well_formed_and_agrees_with_the_surname()

### Community 25 - "test_checksums.py"
Cohesion: 0.16
Nodes (10): corrupt_one_digit(), synthetic_aadhaar(), verhoeff_check_digit(), verhoeff_valid(), test_adjacent_transpositions_are_caught(), test_check_digit_completes_a_payload(), test_check_digit_rejects_non_numeric_payload(), test_corruption_helper_changes_exactly_one_digit() (+2 more)

### Community 26 - "test_session.py"
Cohesion: 0.13
Nodes (18): one_field(), test_a_confirmed_value_is_committed(), test_a_denied_readback_is_recorded_as_a_correction(), test_a_field_that_runs_out_of_attempts_is_abandoned_not_left_empty(), test_a_hang_up_at_the_read_back_ends_the_field_without_re_asking(), test_a_question_is_answered_and_does_not_count_as_an_attempt(), test_a_question_is_answered_by_the_help_agent_and_never_becomes_a_value(), test_a_rejected_value_is_explained_in_the_gates_own_words() (+10 more)

### Community 27 - "test_schema_loader.py"
Cohesion: 0.09
Nodes (11): built_pdf(), overlay(), schema(), test_a_field_missing_from_the_pdf_is_fatal(), test_a_widget_with_no_overlay_entry_is_fatal(), test_cross_field_dependencies_are_declared(), test_enum_fields_carry_their_option_list(), test_every_field_has_a_plain_language_prompt_and_gloss() (+3 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.11
Nodes (18): A. Form representation, A. The five-stage pipeline, B. Synthetic data and its construction, B. The validation gate and its rejection taxonomy, C. Adversarial evaluation corpora, C. Extraction as a structurally bounded model call, D. Evaluation harness and its honesty constraints, D. Read-back and the confirmation whitelist (+10 more)

### Community 29 - "test_adversarial.py"
Cohesion: 0.12
Nodes (8): _candidate(), committed(), gate(), test_adversarial_case(), test_every_case_declares_why_it_exists(), test_gate_never_raises_on_hostile_input(), test_the_suite_covers_every_reason_code_the_gate_can_emit(), test_the_suite_has_controls_in_the_categories_that_need_them()

### Community 30 - "answer.py"
Cohesion: 0.20
Nodes (8): AnswerClient, default_index_dir(), HelpAgent, load_agent(), _corpus_digest(), HelpIndex, test_an_index_built_with_another_embedder_is_refused(), test_the_index_round_trips_through_disk()

### Community 31 - "voice.py"
Cohesion: 0.08
Nodes (10): CorruptingRecognizer, FasterWhisperRecognizer, PiperSynthesizer, SpeechRecognizer, SpeechSynthesizer, Transcript, VoiceBackendMissing, test_a_perfect_recogniser_loses_nothing() (+2 more)

### Community 32 - "loader.py"
Cohesion: 0.24
Nodes (5): _inherited(), load(), load_overlay(), parse_acroform(), SchemaError

### Community 33 - "test_help.py"
Cohesion: 0.09
Nodes (15): HelpReply, ScriptedAnswerClient, reciprocal_rank_fusion(), agent(), chunks(), schema(), test_a_citation_to_a_passage_that_was_not_retrieved_falls_back(), test_a_cited_answer_is_spoken_with_its_source() (+7 more)

### Community 34 - "corpus.py"
Cohesion: 0.16
Nodes (11): help_build(), _clean(), _flat(), _html_text(), load_chunks(), load_manifest(), _pdf_text(), _read() (+3 more)

### Community 35 - "Chunk"
Cohesion: 0.24
Nodes (3): Chunk, Embedder, index()

### Community 36 - "Intent"
Cohesion: 0.10
Nodes (11): build(), _clean_extraction(), write(), Intent, extractor(), _has_credentials(), test_a_decline_is_not_extracted_as_a_value(), test_a_question_is_not_extracted_as_a_value() (+3 more)

### Community 37 - "load_all"
Cohesion: 0.29
Nodes (4): __iter__(), load_all(), load_persona(), Persona

### Community 38 - ".answer"
Cohesion: 0.25
Nodes (4): HelpAnswer, _passages(), _question_lines(), emit()

### Community 39 - "models.py"
Cohesion: 0.12
Nodes (3): EventLog, Check, Reason

### Community 41 - "FieldSpec"
Cohesion: 0.15
Nodes (6): build(), build_user_message(), FieldSpec, FormSchema, test_enum_prompts_forbid_substituting_the_nearest_option(), test_prompt_carries_the_field_but_asks_for_no_judgement()

### Community 42 - "confirm"
Cohesion: 0.17
Nodes (7): confirm(), test_a_confirmation_issues_a_receipt(), test_a_denial_issues_no_receipt(), test_a_spoofed_confirmation_issues_no_receipt(), test_a_stale_report_issues_no_receipt(), test_no_receipt_is_issued_for_a_failed_validation(), test_the_receipt_records_what_the_user_actually_said()

### Community 43 - "run_persona"
Cohesion: 0.13
Nodes (9): run_persona(), ReplayClient, main(), record(), _scrub(), runs(), personas(), runs() (+1 more)

### Community 44 - "with_retries"
Cohesion: 0.28
Nodes (3): GeminiAnswerClient, json_config(), with_retries()

### Community 45 - "M0. System design"
Cohesion: 0.20
Nodes (10): M0.1 Problem framing, M0.2 The five-stage pipeline, M0.3 Enforcing the constraint rather than asserting it, M0.4 Form representation: parser-assisted, human-verified schema, M0.5 Language selection, M0.6 Deferral of the voice channel, M0.7 Evaluation design, M0.8 Data (+2 more)

### Community 46 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 47 - "write_tables"
Cohesion: 0.29
Nodes (6): _write_csv(), write_tables(), test_all_tables_are_written(), test_the_fields_table_records_ground_truth_beside_what_was_committed(), test_the_summary_is_a_single_row(), test_the_turns_table_has_one_row_per_turn()

### Community 48 - "M2. The validation gate"
Cohesion: 0.22
Nodes (9): M2.1 Construction order, M2.2 Both directions are asserted, M2.3 Check ordering as a defined quantity, M2.4 Normalization reshapes but does not repair, M2.5 A script-dependent validation trap, M2.6 Cross-field checks and the confirmation dependency, M2.7 The validator does not interpret text, M2.8 Isolation (+1 more)

### Community 49 - "aadhaar_valid"
Cohesion: 0.20
Nodes (5): aadhaar_valid(), test_leading_zero_or_one_is_rejected(), test_non_digits_are_rejected_not_crashed(), test_wrong_length_is_rejected(), test_aadhaar_numbers_satisfy_verhoeff()

### Community 50 - "Prompt for Claude Code — LucidForm Prototype"
Cohesion: 0.29
Nodes (6): Context, How I want you to work with me, Non-negotiable design constraint, Prompt for Claude Code — LucidForm Prototype, Scope for THIS prototype (deliberately small), What I need from you, in order

### Community 51 - "test_llm_clients.py"
Cohesion: 0.08
Nodes (19): Settings, AnthropicExtractionClient, GeminiExtractionClient, make_client(), UnknownProvider, client_with(), fake_sdk(), FakeModels (+11 more)

### Community 52 - "M3. The write path"
Cohesion: 0.29
Nodes (7): M3.1 Three mechanisms, and what each actually covers, M3.2 Testing each precondition in isolation, M3.3 Affirmation parsing, and why it is a whitelist, M3.4 Adversarial evaluation of the confirmation step, M3.5 Corrections, declines, and the distinction between them, M3.6 Export, M3. The write path

### Community 53 - "M4. Extraction"
Cohesion: 0.29
Nodes (7): M4.1 The model's output is bounded by a schema, not by instruction, M4.2 Intent is separated from value, M4.3 Two deterministic checks on the model's output, M4.4 What the offline corpus can and cannot measure, M4.5 The extractor does not repair, M4.6 Live testing, M4. Extraction

### Community 54 - "M5. Orchestration and read-back"
Cohesion: 0.29
Nodes (7): M5.1 The orchestrator makes no judgements, M5.2 Read-back as an audibility problem, M5.3 Read-back detects a class of error nothing else can, M5.4 Asking for an explanation is not a failed attempt, M5.5 The simulated user, M5.6 Localisation of what the user hears, M5. Orchestration and read-back

### Community 55 - "LucidForm"
Cohesion: 0.29
Nodes (7): First results, Layout, LucidForm, Run, Setup, Status, The pipeline

### Community 56 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 57 - "run_cmd"
Cohesion: 0.17
Nodes (6): extract_cmd(), _extraction_client(), _help_agent(), replay_cmd(), run_cmd(), Session

### Community 58 - "metrics.py"
Cohesion: 0.20
Nodes (6): FieldOutcome, outcome(), _pct(), report(), _truth(), test_the_report_names_the_invariant()

### Community 59 - "M1. Implementation notes — instrumentation and corpus"
Cohesion: 0.33
Nodes (6): M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 61 - "graph.py"
Cohesion: 0.18
Nodes (8): Part B - Semantic extraction (parallel subagents), _build(), edges(), node_names(), _route(), _structure(), _Stub, test_the_graph_has_the_pipeline_stages_as_nodes()

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
Cohesion: 0.16
Nodes (3): Phase 4 notes, PersonaChannel, Turn

### Community 70 - "LucidForm — Specification"
Cohesion: 0.15
Nodes (11): ReplayRun, 1. Intent, 2. The gating contract — the thesis of the project, 3. Non-negotiables, 5. Rejection taxonomy, 6. Scope of this prototype, 7. Eval outputs, Check order (+3 more)

### Community 72 - "get_settings"
Cohesion: 0.19
Nodes (4): get_settings(), build(), _header(), _overlay()

### Community 78 - "candidate"
Cohesion: 0.12
Nodes (9): candidate(), test_an_optional_field_still_rejects_an_empty_value(), test_an_unknown_field_is_an_error_not_a_pass(), test_every_report_records_the_candidate_it_judged(), test_every_report_records_the_checks_it_ran(), test_structural_failure_outranks_low_confidence(), test_the_clock_is_injectable(), test_the_first_failing_check_wins() (+1 more)

### Community 79 - "Extractor"
Cohesion: 0.10
Nodes (8): ExtractionClient, ModelReply, ExtractionOutcome, Extractor, test_every_persona_utterance_has_a_recorded_response(), test_replaying_an_out_of_enum_income_is_rejected_not_mapped(), test_replaying_p02_pan_yields_the_homoglyph_the_gate_then_rejects(), test_replaying_p03_pan_yields_a_question_then_a_value()

### Community 82 - "index.py"
Cohesion: 0.17
Nodes (4): HashEmbedder, Hit, _normalise(), tokenize()

### Community 84 - "Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms"
Cohesion: 0.50
Nodes (3): A: Form No. 93 – PAN Application Form for Individual (Being citizen of India), FAQ's on PAN, Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms

### Community 87 - "pytest"
Cohesion: 0.20
Nodes (4): golden(), test_commit_is_reachable_only_through_confirm(), test_persona_sessions_match_the_pre_langgraph_loop(), test_the_graph_draws_as_mermaid_for_the_paper()

### Community 89 - "percentile"
Cohesion: 0.25
Nodes (3): percentile(), test_percentile_of_nothing_is_none_not_zero(), test_percentiles_are_values_that_actually_occurred()

## Knowledge Gaps
- **121 isolated node(s):** `Commands`, `Environment`, `Phase 3 notes`, `graphify`, `For /graphify add and --watch` (+116 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 679 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LucidForm — Specification` connect `LucidForm — Specification` to `ConfirmationReceipt`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `4. Data model` connect `ConfirmationReceipt` to `FieldSpec`, `Candidate`, `FormState`, `LucidForm — Specification`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Why does `Candidate` connect `Candidate` to `Event`, `LucidForm`, `.check`, `models.py`, `test_confirm.py`, `Status`, `confirm`, `cli.py`, `FormState`, `test_gate_crossfield.py`, `asr_probe.py`, `Extractor`, `candidate`, `ConfirmationReceipt`, `test_voice.py`, `ValidationGate`, `Title (pick one, or tell me to try again)`, `test_adversarial.py`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ValidationGate` (e.g. with `Candidate` and `Check`) actually correct?**
  _`ValidationGate` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Candidate` (e.g. with `Conventions` and `Non-negotiables`) actually correct?**
  _`Candidate` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `FormState` (e.g. with `Event` and `EventLog`) actually correct?**
  _`FormState` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `Event` (e.g. with `VoiceChannel` and `parse_session()`) actually correct?**
  _`Event` has 25 INFERRED edges - model-reasoned connections that need verification._