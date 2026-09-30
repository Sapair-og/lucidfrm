# Graph Report - LucidForm  (2026-09-30)

## Corpus Check
- 81 files · ~181,205 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 4, .example 1, .ini 1)

## Summary
- 1356 nodes · 2943 edges · 89 communities (69 shown, 20 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 282 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_gate_rules.py
- Event
- test_formstate.py
- test_readback.py
- LucidForm
- SessionResult
- test_i18n.py
- test_gate.py
- test_confirm.py
- test_gate_crossfield.py
- test_metrics.py
- cli.py
- FormState
- test_extraction.py
- ProbeSummary
- client.py
- What You Must Do When Invoked
- state.py
- parse_session
- pytest
- test_session.py
- Extraction
- test_voice.py
- test_checksums.py
- ValidationGate
- test_personas.py
- one_field
- test_schema_loader.py
- Title (pick one, or tell me to try again)
- test_adversarial.py
- .commit
- voice.py
- load
- Kind
- PersonaChannel
- Candidate
- Intent
- build
- Transcript
- loader.py
- EventLog
- FieldSpec
- aadhaar_valid
- get_settings
- percentile
- M0. System design
- graphify reference: extra exports and benchmark
- write_tables
- M2. The validation gate
- Settings
- Prompt for Claude Code — LucidForm Prototype
- test_llm_clients.py
- M3. The write path
- M4. Extraction
- M5. Orchestration and read-back
- LucidForm
- graphify reference: query, path, explain
- asr_probe.py
- make_client
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- pin_matches_state
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- LucidForm — Specification
- Purpose
- rules.py
- graphify reference: GitHub clone and cross-repo merge
- metrics.py
- LucidForm — Methodology
- parse_affirmation
- Aggregate
- .claude/CLAUDE.md
- extraction-spec.md
- UnauthorizedIssuer
- Reason
- ExtractionOutcome
- Puppet
- test_phone_country_and_trunk_prefixes_are_stripped
- parametrize
- PersonaError
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- _is_correct
- length_error
- passing
- uidai_faq_update.md

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 57 edges
2. `FormState` - 51 edges
3. `Candidate` - 50 edges
4. `Event` - 42 edges
5. `EventLog` - 40 edges
6. `Extraction` - 40 edges
7. `Status` - 38 edges
8. `load()` - 38 edges
9. `FieldSpec` - 36 edges
10. `Extractor` - 34 edges

## Surprising Connections (you probably didn't know these)
- `Three enforcement mechanisms` --references--> `ConfirmationReceipt`  [INFERRED]
  SPEC.md → lucidform/formstate/receipt.py
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

## Communities (89 total, 20 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.12
Nodes (20): normalize(), range_error(), field(), schema(), test_ambiguous_dates_resolve_day_first(), test_dates_normalize_to_iso_from_every_accepted_form(), test_enum_matching_is_case_and_space_insensitive_only(), test_full_width_digits_are_folded_to_ascii() (+12 more)

### Community 1 - "Event"
Cohesion: 0.08
Nodes (18): Event, _jsonable(), read_log(), log(), test_a_second_log_on_the_same_session_appends(), test_dataclass_payloads_are_serialised(), test_enums_inside_payloads_become_their_values(), test_latency_is_null_when_unmeasured_not_zero() (+10 more)

### Community 2 - "test_formstate.py"
Cohesion: 0.07
Nodes (27): SilentWriteBlocked, forge(), gate(), make(), state(), test_a_blocked_write_is_logged_as_an_event(), test_a_confirmed_value_is_written(), test_a_correction_still_requires_its_own_confirmation() (+19 more)

### Community 3 - "test_readback.py"
Cohesion: 0.09
Nodes (25): render(), render_value(), spell(), spell_email(), field(), render(), schema(), test_a_date_has_no_leading_zero_on_the_day() (+17 more)

### Community 4 - "LucidForm"
Cohesion: 0.15
Nodes (8): Commands, Conventions, Environment, graphify, LucidForm, Phase 3 notes, Phase 4 notes, Phase 5 notes

### Community 6 - "test_i18n.py"
Cohesion: 0.08
Nodes (16): available(), load(), MissingString, Strings, test_a_missing_key_raises_rather_than_falling_back(), test_a_missing_placeholder_raises_with_the_key_named(), test_an_unknown_language_fails_with_a_useful_message(), test_both_languages_are_available() (+8 more)

### Community 7 - "test_gate.py"
Cohesion: 0.09
Nodes (16): candidate(), gate(), schema(), test_a_pass_carries_the_exact_value_that_will_be_written(), test_a_rejection_carries_nothing_committable(), test_an_optional_field_still_rejects_an_empty_value(), test_an_unknown_field_is_an_error_not_a_pass(), test_every_report_records_the_candidate_it_judged() (+8 more)

### Community 8 - "test_confirm.py"
Cohesion: 0.13
Nodes (10): confirm(), normalize_utterance(), test_a_confirmation_issues_a_receipt(), test_a_denial_issues_no_receipt(), test_a_spoofed_confirmation_issues_no_receipt(), test_a_stale_report_issues_no_receipt(), test_apostrophe_forms_reduce_together(), test_filler_is_removed_but_content_is_not() (+2 more)

### Community 9 - "test_gate_crossfield.py"
Cohesion: 0.09
Nodes (20): check(), CrossFieldResult, pan_matches_surname(), pin_matches_confirmed_state(), _skipped(), _check(), test_a_check_with_an_unconfirmed_dependency_is_skipped_not_passed(), test_a_state_with_no_region_data_is_not_checked() (+12 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.06
Nodes (14): agg(), schema(), sessions(), test_a_question_and_the_answer_after_it_are_separate_turns(), test_nothing_wrong_was_committed(), test_offline_sessions_are_flagged_as_not_measuring_accuracy(), test_recall_and_false_positive_rate_are_both_reported(), test_the_caveat_survives_into_the_csv() (+6 more)

### Community 11 - "cli.py"
Cohesion: 0.13
Nodes (12): asr_probe_cmd(), extract_cmd(), _extraction_client(), make_form_cmd(), metrics_cmd(), personas_list(), personas_show(), replay_cmd() (+4 more)

### Community 12 - "FormState"
Cohesion: 0.08
Nodes (21): graphify reference: transcribe video and audio, Step 2.5 - Transcribe video / audio files (only if video files detected), FormState, export(), ExportError, read_back(), commit(), gate() (+13 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.10
Nodes (24): extractor(), gate(), replay(), schema(), test_a_decline_never_becomes_a_candidate(), test_a_loose_match_reports_no_span_rather_than_a_wrong_one(), test_a_question_never_becomes_a_candidate(), test_a_quote_from_the_utterance_grounds() (+16 more)

### Community 14 - "ProbeSummary"
Cohesion: 0.18
Nodes (7): is_simulated(), ProbeResult, ProbeSummary, report(), rows(), test_a_real_recogniser_would_not_be_labelled_simulated(), test_simulated_runs_are_labelled_as_not_being_measurements()

### Community 15 - "client.py"
Cohesion: 0.14
Nodes (3): AnthropicExtractionClient, ModelReply, ReplayClient

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

### Community 17 - "state.py"
Cohesion: 0.21
Nodes (4): ConfirmationReceipt, Affirmation, fingerprint(), 4. Data model

### Community 18 - "parse_session"
Cohesion: 0.15
Nodes (8): load_sessions(), parse_session(), _personas(), SessionMetrics, Turn, test_a_session_without_ground_truth_is_excluded_from_accuracy(), test_a_tampered_log_is_detected(), test_unscored_sessions_still_contribute_the_measures_that_need_no_truth()

### Community 19 - "pytest"
Cohesion: 0.15
Nodes (9): _imported_names(), _parse(), _python_files(), _rel(), test_decision_and_write_paths_import_no_model(), test_forbidden_import_detection_works(), test_private_form_state_is_not_touched_from_outside(), test_receipts_are_minted_only_by_the_confirmation_module() (+1 more)

### Community 20 - "test_session.py"
Cohesion: 0.12
Nodes (9): personas(), runs(), schema(), test_a_declined_optional_field_stays_empty(), test_a_question_is_handled_mid_session(), test_endless_questions_are_bounded(), test_out_of_enum_answers_are_re_asked_not_mapped(), test_the_gate_catches_the_homoglyph() (+1 more)

### Community 21 - "Extraction"
Cohesion: 0.11
Nodes (12): ScriptedClient, check(), clamp_confidence(), Grounding, locate(), _loose(), Extraction, test_a_model_reporting_impossible_confidence_is_clamped() (+4 more)

### Community 22 - "test_voice.py"
Cohesion: 0.15
Nodes (13): EchoRecognizer, SilentSynthesizer, personas(), schema(), test_an_empty_transcript_is_an_unusable_answer_not_a_hang_up(), test_asr_confidence_is_recorded_but_never_reaches_the_gate(), test_audio_events_are_logged_on_both_sides(), test_corrupted_identifiers_are_classified_and_offered_to_the_gate() (+5 more)

### Community 23 - "test_checksums.py"
Cohesion: 0.17
Nodes (10): corrupt_one_digit(), synthetic_aadhaar(), verhoeff_check_digit(), verhoeff_valid(), test_adjacent_transpositions_are_caught(), test_check_digit_completes_a_payload(), test_check_digit_rejects_non_numeric_payload(), test_corruption_helper_changes_exactly_one_digit() (+2 more)

### Community 25 - "test_personas.py"
Cohesion: 0.10
Nodes (8): personas(), schema(), test_email_addresses_use_a_reserved_domain(), test_every_persona_declares_a_synthetic_header(), test_everyone_is_an_adult(), test_ground_truth_covers_every_required_field(), test_optional_fields_may_be_declined_but_must_still_be_answerable(), test_pan_is_well_formed_and_agrees_with_the_surname()

### Community 26 - "one_field"
Cohesion: 0.14
Nodes (15): one_field(), test_a_confirmed_value_is_committed(), test_a_denied_readback_is_recorded_as_a_correction(), test_a_field_that_runs_out_of_attempts_is_abandoned_not_left_empty(), test_a_question_is_answered_and_does_not_count_as_an_attempt(), test_a_rejected_value_is_explained_in_the_gates_own_words(), test_a_spoofed_confirmation_does_not_commit(), test_declining_a_required_field_is_refused() (+7 more)

### Community 27 - "test_schema_loader.py"
Cohesion: 0.11
Nodes (9): built_pdf(), overlay(), schema(), test_a_field_missing_from_the_pdf_is_fatal(), test_cross_field_dependencies_are_declared(), test_enum_fields_carry_their_option_list(), test_every_field_has_a_plain_language_prompt_and_gloss(), test_max_length_comes_from_the_pdf_not_the_overlay() (+1 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.11
Nodes (18): A. Form representation, A. The five-stage pipeline, B. Synthetic data and its construction, B. The validation gate and its rejection taxonomy, C. Adversarial evaluation corpora, C. Extraction as a structurally bounded model call, D. Evaluation harness and its honesty constraints, D. Read-back and the confirmation whitelist (+10 more)

### Community 29 - "test_adversarial.py"
Cohesion: 0.13
Nodes (7): _candidate(), committed(), gate(), test_adversarial_case(), test_every_case_declares_why_it_exists(), test_the_suite_covers_every_reason_code_the_gate_can_emit(), test_the_suite_has_controls_in_the_categories_that_need_them()

### Community 30 - ".commit"
Cohesion: 0.15
Nodes (5): V. Algorithm and Pseudocode, CommitRecord, DeclineRecord, block(), _now()

### Community 31 - "voice.py"
Cohesion: 0.13
Nodes (4): FasterWhisperRecognizer, PiperSynthesizer, VoiceBackendMissing, test_asking_for_a_missing_backend_says_how_to_install_it()

### Community 32 - "load"
Cohesion: 0.17
Nodes (8): Gotchas, _inherited(), load(), load_overlay(), parse_acroform(), SchemaError, test_a_widget_with_no_overlay_entry_is_fatal(), test_missing_pdf_names_the_fix()

### Community 35 - "Candidate"
Cohesion: 0.11
Nodes (8): Candidate, Check, Status, ValidationReport, test_gate_never_raises_on_hostile_input(), test_no_receipt_is_issued_for_a_failed_validation(), test_a_pass_must_not_carry_a_reason(), test_a_rejection_must_carry_a_reason()

### Community 36 - "Intent"
Cohesion: 0.16
Nodes (6): Intent, _has_credentials(), test_a_decline_is_not_extracted_as_a_value(), test_a_question_is_not_extracted_as_a_value(), test_a_spoken_identifier_is_transcribed(), test_the_model_cannot_return_anything_outside_the_schema()

### Community 37 - "build"
Cohesion: 0.29
Nodes (4): build(), _clean_extraction(), write(), test_the_fixture_corpus_is_in_sync_with_its_generator()

### Community 38 - "Transcript"
Cohesion: 0.18
Nodes (4): CorruptingRecognizer, Transcript, test_a_perfect_recogniser_loses_nothing(), transcribe()

### Community 40 - "EventLog"
Cohesion: 0.14
Nodes (11): InputChannel, OutputChannel, EventLog, ReplayRun, run_persona(), ExtractionClient, Extractor, Session (+3 more)

### Community 41 - "FieldSpec"
Cohesion: 0.16
Nodes (7): build(), build_user_message(), FieldSpec, FieldType, test_enum_prompts_forbid_substituting_the_nearest_option(), test_prompt_carries_the_field_but_asks_for_no_judgement(), test_devanagari_digits_do_not_satisfy_the_numeric_patterns()

### Community 42 - "aadhaar_valid"
Cohesion: 0.20
Nodes (5): aadhaar_valid(), test_leading_zero_or_one_is_rejected(), test_non_digits_are_rejected_not_crashed(), test_wrong_length_is_rejected(), test_aadhaar_numbers_satisfy_verhoeff()

### Community 43 - "get_settings"
Cohesion: 0.22
Nodes (5): gate_check(), get_settings(), build(), _header(), _overlay()

### Community 44 - "percentile"
Cohesion: 0.25
Nodes (3): percentile(), test_percentile_of_nothing_is_none_not_zero(), test_percentiles_are_values_that_actually_occurred()

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

### Community 49 - "Settings"
Cohesion: 0.29
Nodes (3): Settings, test_sdk_key_variables_are_read_without_the_project_prefix(), test_the_default_provider_is_gemini_and_the_model_is_config()

### Community 50 - "Prompt for Claude Code — LucidForm Prototype"
Cohesion: 0.29
Nodes (6): Context, How I want you to work with me, Non-negotiable design constraint, Prompt for Claude Code — LucidForm Prototype, Scope for THIS prototype (deliberately small), What I need from you, in order

### Community 51 - "test_llm_clients.py"
Cohesion: 0.13
Nodes (14): GeminiExtractionClient, UnknownProvider, client_with(), fake_sdk(), FakeModels, rate_limited(), test_a_non_retryable_error_is_raised_immediately(), test_a_rate_limit_is_retried_with_backoff() (+6 more)

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

### Community 57 - "asr_probe.py"
Cohesion: 0.13
Nodes (10): SpeechRecognizer, SpeechSynthesizer, _category(), character_error_rate(), decode_spelled(), levenshtein(), probe(), test_character_error_rate_is_zero_for_an_exact_match() (+2 more)

### Community 59 - "M1. Implementation notes — instrumentation and corpus"
Cohesion: 0.33
Nodes (6): M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 62 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 63 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 64 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 65 - "LucidForm — Specification"
Cohesion: 0.17
Nodes (10): 1. Intent, 2. The gating contract — the thesis of the project, 3. Non-negotiables, 5. Rejection taxonomy, 6. Scope of this prototype, 7. Eval outputs, Check order, Commit invariant (+2 more)

### Community 66 - "Purpose"
Cohesion: 0.13
Nodes (6): Purpose, VoiceChannel, VoiceTurn, test_a_form_is_filled_over_the_voice_channel(), read_back(), test_the_module_imports_without_any_speech_library()

### Community 67 - "rules.py"
Cohesion: 0.18
Nodes (5): enum_error(), format_error(), parse_date(), strip_invisible(), test_format_errors_explain_themselves_in_plain_language()

### Community 69 - "metrics.py"
Cohesion: 0.20
Nodes (6): FieldOutcome, outcome(), _pct(), report(), _truth(), test_the_report_names_the_invariant()

### Community 71 - "parse_affirmation"
Cohesion: 0.16
Nodes (7): parse_affirmation(), _mint_as_issuer(), test_a_substring_parser_would_fail_this_suite(), test_affirmation_case(), test_the_helper_really_does_bypass_the_issuer_check(), test_the_receipt_refuses_a_failed_validation(), test_the_receipt_refuses_a_non_explicit_affirmation()

### Community 75 - "UnauthorizedIssuer"
Cohesion: 0.22
Nodes (4): Non-negotiables, _calling_module(), UnauthorizedIssuer, test_receipts_cannot_be_minted_outside_the_confirmation_module()

### Community 78 - "Reason"
Cohesion: 0.22
Nodes (4): Reason, test_replaying_an_out_of_enum_income_is_rejected_not_mapped(), test_check_order_covers_the_whole_taxonomy(), test_check_order_is_the_documented_sequence()

### Community 81 - "test_phone_country_and_trunk_prefixes_are_stripped"
Cohesion: 0.33
Nodes (3): test_pan_separators_and_case_are_reshaped(), test_phone_country_and_trunk_prefixes_are_stripped(), test_values_made_only_of_invisible_characters_become_empty()

### Community 82 - "parametrize"
Cohesion: 0.33
Nodes (3): test_every_field_is_resolved(), test_no_committed_value_differs_from_ground_truth(), test_no_write_was_blocked_during_a_normal_session()

### Community 84 - "Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms"
Cohesion: 0.50
Nodes (3): A: Form No. 93 – PAN Application Form for Individual (Being citizen of India), FAQ's on PAN, Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms

### Community 86 - "length_error"
Cohesion: 0.50
Nodes (3): length_error(), test_fixed_length_fields_require_an_exact_length(), test_free_text_fields_have_an_upper_bound_only()

## Knowledge Gaps
- **121 isolated node(s):** `graphify`, `Usage`, `What graphify is for`, `Step 0 - GitHub repos and multi-path merge (only if a URL or several paths)`, `Step 1 - Ensure graphify is installed` (+116 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 605 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FieldSpec` connect `FieldSpec` to `test_gate_rules.py`, `load`, `Candidate`, `Intent`, `rules.py`, `LucidForm`, `test_readback.py`, `EventLog`, `SessionResult`, `loader.py`, `client.py`, `ExtractionOutcome`, `What You Must Do When Invoked`, `state.py`, `length_error`, `ValidationGate`, `asr_probe.py`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Why does `Candidate` connect `Candidate` to `Event`, `test_formstate.py`, `LucidForm`, `test_gate.py`, `test_confirm.py`, `test_gate_crossfield.py`, `cli.py`, `FormState`, `state.py`, `test_voice.py`, `ValidationGate`, `Title (pick one, or tell me to try again)`, `test_adversarial.py`, `.commit`, `Intent`, `EventLog`, `get_settings`, `asr_probe.py`, `parse_affirmation`, `ExtractionOutcome`, `passing`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `LucidForm — Specification` connect `LucidForm — Specification` to `state.py`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `ValidationGate` (e.g. with `asr_probe_cmd()` and `extract_cmd()`) actually correct?**
  _`ValidationGate` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `FormState` (e.g. with `run_cmd()` and `ReplayRun`) actually correct?**
  _`FormState` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Candidate` (e.g. with `Conventions` and `A. The five-stage pipeline`) actually correct?**
  _`Candidate` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `Event` (e.g. with `VoiceChannel` and `parse_session()`) actually correct?**
  _`Event` has 27 INFERRED edges - model-reasoned connections that need verification._