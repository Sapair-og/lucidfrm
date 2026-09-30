# Graph Report - LucidForm  (2026-09-30)

## Corpus Check
- 92 files · ~215,751 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .example 1, .jsonl 1)

## Summary
- 1551 nodes · 3334 edges · 101 communities (78 shown, 23 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 252 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8a5ffed6`
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
- crossfield.py
- test_metrics.py
- cli.py
- FormState
- test_extraction.py
- ProbeSummary
- parametrize
- /graphify
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
- load
- Title (pick one, or tell me to try again)
- test_adversarial.py
- state.py
- voice.py
- probe
- test_help.py
- corpus.py
- HelpIndex
- Intent
- load_all
- HelpAgent
- GeminiEmbedder
- build
- models.py
- run_persona
- answer.py
- M0. System design
- graphify reference: extra exports and benchmark
- write_tables
- M2. The validation gate
- _check
- Prompt for Claude Code — LucidForm Prototype
- test_llm_clients.py
- M3. The write path
- M4. Extraction
- M5. Orchestration and read-back
- LucidForm
- graphify reference: query, path, explain
- session.py
- metrics.py
- LucidForm — Methodology
- M6. Measurement
- graph.py
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- PersonaChannel
- VoiceChannel
- Aggregate
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- LucidForm — Specification
- test_gate_crossfield.py
- get_settings
- .claude/CLAUDE.md
- extraction-spec.md
- What You Must Do When Invoked
- Reason
- Extractor
- Puppet
- range_error
- index.py
- Path
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- PersonaError
- FormSchema
- pytest
- uidai_faq_update.md
- percentile
- Step 3 - Extract entities and relationships
- ScriptedClient
- check
- strip_invisible
- HelpAnswer
- test_a_form_is_filled_over_the_voice_channel
- length_error
- gate
- test_form_state_exposes_no_alternative_mutator
- test_devanagari_digits_do_not_satisfy_the_numeric_patterns

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 55 edges
2. `Candidate` - 50 edges
3. `FormState` - 48 edges
4. `Event` - 41 edges
5. `load()` - 41 edges
6. `EventLog` - 38 edges
7. `Status` - 36 edges
8. `Extraction` - 35 edges
9. `read_log()` - 35 edges
10. `get_settings()` - 34 edges

## Surprising Connections (you probably didn't know these)
- `Commit invariant` --references--> `SilentWriteBlocked`  [INFERRED]
  SPEC.md → lucidform/formstate/state.py
- `Conventions` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py
- `A. The five-stage pipeline` --references--> `Candidate`  [INFERRED]
  docs/paper-draft.md → lucidform/models.py
- `Step 2.5 - Transcribe video / audio files (only if video files detected)` --references--> `export()`  [INFERRED]
  .claude/skills/graphify/references/transcribe.md → lucidform/formstate/writer.py
- `4. Data model` --references--> `FieldSpec`  [INFERRED]
  SPEC.md → lucidform/models.py

## Import Cycles
- None detected.

## Communities (101 total, 23 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.12
Nodes (21): normalize(), field(), schema(), test_ambiguous_dates_resolve_day_first(), test_dates_normalize_to_iso_from_every_accepted_form(), test_enum_matching_is_case_and_space_insensitive_only(), test_fixed_length_fields_require_an_exact_length(), test_full_width_digits_are_folded_to_ascii() (+13 more)

### Community 1 - "Event"
Cohesion: 0.08
Nodes (20): Event, EventLog, _jsonable(), read_log(), log(), test_a_second_log_on_the_same_session_appends(), test_dataclass_payloads_are_serialised(), test_enums_inside_payloads_become_their_values() (+12 more)

### Community 2 - "Candidate"
Cohesion: 0.07
Nodes (26): SilentWriteBlocked, Candidate, forge(), gate(), make(), state(), test_a_blocked_write_is_logged_as_an_event(), test_a_confirmed_value_is_written() (+18 more)

### Community 3 - "test_readback.py"
Cohesion: 0.08
Nodes (26): render(), render_value(), spell(), spell_email(), field(), render(), schema(), test_a_date_has_no_leading_zero_on_the_day() (+18 more)

### Community 4 - "LucidForm"
Cohesion: 0.15
Nodes (8): Commands, Conventions, Environment, graphify, LucidForm, Phase 3 notes, Phase 4 notes, Phase 5 notes

### Community 6 - "test_i18n.py"
Cohesion: 0.06
Nodes (16): available(), load(), MissingString, Strings, test_a_missing_key_raises_rather_than_falling_back(), test_a_missing_placeholder_raises_with_the_key_named(), test_an_unknown_language_fails_with_a_useful_message(), test_both_languages_are_available() (+8 more)

### Community 7 - "Status"
Cohesion: 0.15
Nodes (13): Status, candidate(), test_a_pass_carries_the_exact_value_that_will_be_written(), test_a_pass_must_not_carry_a_reason(), test_a_rejection_carries_nothing_committable(), test_a_rejection_must_carry_a_reason(), test_an_unknown_field_is_an_error_not_a_pass(), test_every_report_records_the_candidate_it_judged() (+5 more)

### Community 8 - "test_confirm.py"
Cohesion: 0.07
Nodes (22): UnauthorizedIssuer, confirm(), normalize_utterance(), parse_affirmation(), gate(), _mint_as_issuer(), passing(), test_a_confirmation_issues_a_receipt() (+14 more)

### Community 9 - "crossfield.py"
Cohesion: 0.17
Nodes (8): CrossFieldResult, pin_matches_confirmed_state(), _skipped(), pin_matches_state(), test_a_state_with_no_region_data_is_not_checked(), test_pin_in_the_right_postal_region_passes(), test_pin_in_the_wrong_postal_region_fails(), test_pin_agrees_with_state()

### Community 10 - "test_metrics.py"
Cohesion: 0.06
Nodes (14): agg(), schema(), sessions(), test_a_question_and_the_answer_after_it_are_separate_turns(), test_nothing_wrong_was_committed(), test_offline_sessions_are_flagged_as_not_measuring_accuracy(), test_recall_and_false_positive_rate_are_both_reported(), test_the_caveat_survives_into_the_csv() (+6 more)

### Community 11 - "cli.py"
Cohesion: 0.08
Nodes (17): asr_probe_cmd(), extract_cmd(), _extraction_client(), gate_check(), graph_cmd(), _help_agent(), help_ask(), help_build() (+9 more)

### Community 12 - "FormState"
Cohesion: 0.09
Nodes (19): FormState, export(), ExportError, read_back(), commit(), gate(), schema(), template() (+11 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.10
Nodes (24): extractor(), gate(), replay(), schema(), test_a_decline_never_becomes_a_candidate(), test_a_loose_match_reports_no_span_rather_than_a_wrong_one(), test_a_question_never_becomes_a_candidate(), test_a_quote_from_the_utterance_grounds() (+16 more)

### Community 14 - "ProbeSummary"
Cohesion: 0.20
Nodes (6): is_simulated(), ProbeResult, ProbeSummary, report(), rows(), test_a_real_recogniser_would_not_be_labelled_simulated()

### Community 15 - "parametrize"
Cohesion: 0.33
Nodes (3): test_every_field_is_resolved(), test_no_committed_value_differs_from_ground_truth(), test_no_write_was_blocked_during_a_normal_session()

### Community 16 - "/graphify"
Cohesion: 0.17
Nodes (11): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, PowerShell 5.1: Vertical scrolling stops working (+3 more)

### Community 17 - "ConfirmationReceipt"
Cohesion: 0.13
Nodes (10): Gotchas, _calling_module(), ConfirmationReceipt, Affirmation, fingerprint(), ValidationReport, 2. The gating contract — the thesis of the project, 4. Data model (+2 more)

### Community 18 - "parse_session"
Cohesion: 0.18
Nodes (7): load_sessions(), parse_session(), _personas(), SessionMetrics, Turn, test_a_tampered_log_is_detected(), test_unscored_sessions_still_contribute_the_measures_that_need_no_truth()

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.16
Nodes (9): _imported_names(), _parse(), _python_files(), _rel(), test_decision_and_write_paths_import_no_model(), test_forbidden_import_detection_works(), test_private_form_state_is_not_touched_from_outside(), test_receipts_are_minted_only_by_the_confirmation_module() (+1 more)

### Community 20 - "Purpose"
Cohesion: 0.13
Nodes (5): InputChannel, Kind, OutputChannel, Purpose, ConsoleChannel

### Community 21 - "Extraction"
Cohesion: 0.14
Nodes (10): check(), clamp_confidence(), Grounding, locate(), _loose(), Extraction, test_a_model_reporting_impossible_confidence_is_clamped(), test_a_reply_that_does_not_fit_the_schema_is_an_error_not_a_fallback() (+2 more)

### Community 22 - "test_voice.py"
Cohesion: 0.16
Nodes (10): EchoRecognizer, SilentSynthesizer, personas(), schema(), test_an_empty_transcript_is_an_unusable_answer_not_a_hang_up(), test_asr_confidence_is_recorded_but_never_reaches_the_gate(), test_audio_events_are_logged_on_both_sides(), test_the_channel_speaks_everything_it_is_given() (+2 more)

### Community 23 - "test_personas.py"
Cohesion: 0.09
Nodes (9): personas(), schema(), test_aadhaar_numbers_satisfy_verhoeff(), test_email_addresses_use_a_reserved_domain(), test_every_persona_declares_a_synthetic_header(), test_everyone_is_an_adult(), test_ground_truth_covers_every_required_field(), test_optional_fields_may_be_declined_but_must_still_be_answerable() (+1 more)

### Community 24 - "ValidationGate"
Cohesion: 0.11
Nodes (3): ValidationGate, Check, test_two_gates_agree()

### Community 25 - "test_checksums.py"
Cohesion: 0.12
Nodes (14): aadhaar_valid(), corrupt_one_digit(), synthetic_aadhaar(), verhoeff_check_digit(), verhoeff_valid(), test_adjacent_transpositions_are_caught(), test_check_digit_completes_a_payload(), test_check_digit_rejects_non_numeric_payload() (+6 more)

### Community 26 - "test_session.py"
Cohesion: 0.08
Nodes (24): one_field(), test_a_confirmed_value_is_committed(), test_a_declined_optional_field_stays_empty(), test_a_denied_readback_is_recorded_as_a_correction(), test_a_field_that_runs_out_of_attempts_is_abandoned_not_left_empty(), test_a_hang_up_at_the_read_back_ends_the_field_without_re_asking(), test_a_question_is_answered_and_does_not_count_as_an_attempt(), test_a_question_is_answered_by_the_help_agent_and_never_becomes_a_value() (+16 more)

### Community 27 - "load"
Cohesion: 0.08
Nodes (16): _inherited(), load(), load_overlay(), parse_acroform(), SchemaError, built_pdf(), overlay(), schema() (+8 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.11
Nodes (18): A. Form representation, A. The five-stage pipeline, B. Synthetic data and its construction, B. The validation gate and its rejection taxonomy, C. Adversarial evaluation corpora, C. Extraction as a structurally bounded model call, D. Evaluation harness and its honesty constraints, D. Read-back and the confirmation whitelist (+10 more)

### Community 29 - "test_adversarial.py"
Cohesion: 0.12
Nodes (8): _candidate(), committed(), gate(), test_adversarial_case(), test_every_case_declares_why_it_exists(), test_gate_never_raises_on_hostile_input(), test_the_suite_covers_every_reason_code_the_gate_can_emit(), test_the_suite_has_controls_in_the_categories_that_need_them()

### Community 30 - "state.py"
Cohesion: 0.15
Nodes (5): V. Algorithm and Pseudocode, CommitRecord, DeclineRecord, block(), _now()

### Community 31 - "voice.py"
Cohesion: 0.14
Nodes (4): FasterWhisperRecognizer, PiperSynthesizer, VoiceBackendMissing, test_asking_for_a_missing_backend_says_how_to_install_it()

### Community 32 - "probe"
Cohesion: 0.13
Nodes (10): CorruptingRecognizer, Transcript, character_error_rate(), probe(), test_a_perfect_recogniser_loses_nothing(), transcribe(), test_character_error_rate_is_zero_for_an_exact_match(), test_corrupted_identifiers_are_classified_and_offered_to_the_gate() (+2 more)

### Community 33 - "test_help.py"
Cohesion: 0.09
Nodes (13): HelpReply, ScriptedAnswerClient, agent(), chunks(), schema(), test_a_citation_to_a_passage_that_was_not_retrieved_falls_back(), test_a_cited_answer_is_spoken_with_its_source(), test_a_model_failure_never_breaks_the_session() (+5 more)

### Community 34 - "corpus.py"
Cohesion: 0.18
Nodes (10): _clean(), _flat(), _html_text(), load_chunks(), load_manifest(), _pdf_text(), _read(), _slug() (+2 more)

### Community 35 - "HelpIndex"
Cohesion: 0.22
Nodes (7): Chunk, _corpus_digest(), Embedder, HelpIndex, index(), test_an_index_built_with_another_embedder_is_refused(), test_the_index_round_trips_through_disk()

### Community 36 - "Intent"
Cohesion: 0.17
Nodes (7): Intent, extractor(), _has_credentials(), test_a_decline_is_not_extracted_as_a_value(), test_a_question_is_not_extracted_as_a_value(), test_a_spoken_identifier_is_transcribed(), test_the_model_cannot_return_anything_outside_the_schema()

### Community 37 - "load_all"
Cohesion: 0.15
Nodes (8): run_cmd(), build(), _clean_extraction(), write(), __iter__(), load_all(), load_persona(), Persona

### Community 38 - "HelpAgent"
Cohesion: 0.18
Nodes (5): AnswerClient, HelpAgent, _passages(), _question_lines(), emit()

### Community 40 - "GeminiEmbedder"
Cohesion: 0.20
Nodes (3): GeminiEmbedder, HashEmbedder, _normalise()

### Community 41 - "build"
Cohesion: 0.33
Nodes (3): build(), build_user_message(), test_prompt_carries_the_field_but_asks_for_no_judgement()

### Community 42 - "models.py"
Cohesion: 0.12
Nodes (7): _category(), decode_spelled(), levenshtein(), enum_error(), FieldSpec, FieldType, test_homophones_are_decoded_as_the_digit_they_sound_like()

### Community 43 - "run_persona"
Cohesion: 0.13
Nodes (9): run_persona(), ReplayClient, main(), record(), _scrub(), runs(), personas(), runs() (+1 more)

### Community 44 - "answer.py"
Cohesion: 0.25
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

### Community 49 - "_check"
Cohesion: 0.22
Nodes (5): _check(), test_an_empty_dependency_counts_as_unconfirmed(), test_skipping_lets_the_value_through_but_records_the_skip(), test_structural_failures_are_reported_before_cross_field_ones(), test_the_same_value_is_rejected_once_the_dependency_is_confirmed()

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

### Community 57 - "session.py"
Cohesion: 0.17
Nodes (3): FieldResult, Session, SessionResult

### Community 58 - "metrics.py"
Cohesion: 0.20
Nodes (6): FieldOutcome, outcome(), _pct(), report(), _truth(), test_the_report_names_the_invariant()

### Community 59 - "LucidForm — Methodology"
Cohesion: 0.22
Nodes (7): LucidForm — Methodology, M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 61 - "graph.py"
Cohesion: 0.23
Nodes (6): _build(), node_names(), _route(), _structure(), _Stub, test_the_graph_has_the_pipeline_stages_as_nodes()

### Community 62 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 63 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 64 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 66 - "VoiceChannel"
Cohesion: 0.21
Nodes (4): VoiceChannel, VoiceTurn, test_no_audio_ends_the_field_rather_than_being_read_as_consent(), test_the_module_imports_without_any_speech_library()

### Community 70 - "LucidForm — Specification"
Cohesion: 0.18
Nodes (9): Non-negotiables, ReplayRun, 1. Intent, 3. Non-negotiables, 5. Rejection taxonomy, 6. Scope of this prototype, 7. Eval outputs, Check order (+1 more)

### Community 71 - "test_gate_crossfield.py"
Cohesion: 0.23
Nodes (7): pan_matches_surname(), gate(), test_a_check_with_an_unconfirmed_dependency_is_skipped_not_passed(), test_pan_fifth_character_disagreeing_with_the_surname_fails(), test_pan_fifth_character_matching_the_surname_passes(), test_single_word_names_use_that_word_as_the_surname(), test_surname_matching_is_case_insensitive()

### Community 72 - "get_settings"
Cohesion: 0.27
Nodes (4): get_settings(), build(), _header(), _overlay()

### Community 75 - "What You Must Do When Invoked"
Cohesion: 0.18
Nodes (11): Step 0 - GitHub repos and multi-path merge (only if a URL or several paths), Step 1 - Ensure graphify is installed, Step 2.5 - Video and audio (only if video files detected), Step 2 - Detect files, Step 4.5 - Graph health check (read-only integrity gate), Step 4 - Build graph, cluster, analyze, generate outputs, Step 5 - Label communities, Step 6 - Generate Obsidian vault (opt-in) + HTML (+3 more)

### Community 78 - "Reason"
Cohesion: 0.15
Nodes (6): Reason, test_an_optional_field_still_rejects_an_empty_value(), test_check_order_covers_the_whole_taxonomy(), test_check_order_is_the_documented_sequence(), test_structural_failure_outranks_low_confidence(), test_the_first_failing_check_wins()

### Community 79 - "Extractor"
Cohesion: 0.10
Nodes (8): ExtractionClient, ModelReply, ExtractionOutcome, Extractor, test_every_persona_utterance_has_a_recorded_response(), test_replaying_an_out_of_enum_income_is_rejected_not_mapped(), test_replaying_p02_pan_yields_the_homoglyph_the_gate_then_rejects(), test_replaying_p03_pan_yields_a_question_then_a_value()

### Community 81 - "range_error"
Cohesion: 0.20
Nodes (5): format_error(), parse_date(), range_error(), test_format_errors_explain_themselves_in_plain_language(), test_the_age_boundary_is_exact()

### Community 82 - "index.py"
Cohesion: 0.24
Nodes (4): Hit, reciprocal_rank_fusion(), tokenize(), test_reciprocal_rank_fusion_rewards_agreement()

### Community 84 - "Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms"
Cohesion: 0.50
Nodes (3): A: Form No. 93 – PAN Application Form for Individual (Being citizen of India), FAQ's on PAN, Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms

### Community 86 - "FormSchema"
Cohesion: 0.22
Nodes (3): _is_correct(), FormSchema, test_normalisation_is_applied_before_judging_a_proposal()

### Community 87 - "pytest"
Cohesion: 0.22
Nodes (3): golden(), test_persona_sessions_match_the_pre_langgraph_loop(), test_the_graph_draws_as_mermaid_for_the_paper()

### Community 89 - "percentile"
Cohesion: 0.25
Nodes (3): percentile(), test_percentile_of_nothing_is_none_not_zero(), test_percentiles_are_values_that_actually_occurred()

### Community 90 - "Step 3 - Extract entities and relationships"
Cohesion: 0.29
Nodes (6): Part A - Structural extraction for code files, Part B - Semantic extraction (parallel subagents), Part C - Merge AST + semantic into final extraction, Step 3 - Extract entities and relationships, edges(), test_commit_is_reachable_only_through_confirm()

### Community 92 - "check"
Cohesion: 0.40
Nodes (3): check(), test_cross_field_checks_read_only_committed_values(), test_fields_without_a_cross_field_rule_return_nothing()

## Knowledge Gaps
- **121 isolated node(s):** `For /graphify add and --watch`, `For /graphify query`, `For the commit hook and native CLAUDE.md integration`, `For --update and --cluster-only`, `Honesty Rules` (+116 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 675 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LucidForm — Specification` connect `LucidForm — Specification` to `ConfirmationReceipt`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `4. Data model` connect `ConfirmationReceipt` to `Candidate`, `FormState`, `models.py`, `LucidForm — Specification`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `Candidate` connect `Candidate` to `probe`, `Event`, `LucidForm`, `Status`, `test_confirm.py`, `test_gate_crossfield.py`, `models.py`, `cli.py`, `FormState`, `Extractor`, `ConfirmationReceipt`, `_check`, `test_voice.py`, `ValidationGate`, `Title (pick one, or tell me to try again)`, `test_adversarial.py`, `state.py`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `ValidationGate` (e.g. with `Candidate` and `Check`) actually correct?**
  _`ValidationGate` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Candidate` (e.g. with `Conventions` and `A. The five-stage pipeline`) actually correct?**
  _`Candidate` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `FormState` (e.g. with `Event` and `EventLog`) actually correct?**
  _`FormState` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `Event` (e.g. with `VoiceChannel` and `parse_session()`) actually correct?**
  _`Event` has 25 INFERRED edges - model-reasoned connections that need verification._