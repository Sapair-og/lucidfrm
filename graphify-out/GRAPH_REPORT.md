# Graph Report - LucidForm  (2026-09-30)

## Corpus Check
- 103 files · ~228,058 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .jsonl 17, (none) 4, .example 1)

## Summary
- 1675 nodes · 3511 edges · 103 communities (78 shown, 25 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 244 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0df3b02a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FieldSpec
- Event
- Candidate
- test_readback.py
- build.js
- SessionGraph
- test_i18n.py
- test_confirm.py
- test_gate_crossfield.py
- test_metrics.py
- cli.py
- FormState
- test_extraction.py
- ProbeSummary
- parametrize
- What You Must Do When Invoked
- load_all
- test_session.py
- test_no_silent_write.py
- readback.py
- grounding.py
- test_voice.py
- test_personas.py
- EventLog
- test_checksums.py
- one_field
- test_schema_loader.py
- Title (pick one, or tell me to try again)
- pytest
- answer.py
- voice.py
- probe
- HashEmbedder
- corpus.py
- VoiceChannel
- events.py
- loader.py
- build
- models.py
- with_retries
- test_help.py
- load
- run_persona
- parse_acroform
- M0. System design
- graphify reference: extra exports and benchmark
- M2. The validation gate
- Row
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
- _check
- graphify reference: GitHub clone and cross-repo merge
- index.py
- LucidForm — Specification
- report
- make_form.py
- .claude/CLAUDE.md
- extraction-spec.md
- Extraction
- ValidationGate
- Extractor
- Puppet
- ScriptedClient
- Chunk
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- GeminiEmbedder
- character_error_rate
- M8. The help agent
- uidai_faq_update.md
- metrics.py
- test_a_question_is_answered_by_the_help_agent_and_never_becomes_a_value
- PersonaError
- test_the_model_has_no_field_in_which_to_request_a_write
- test_a_reply_that_does_not_fit_the_schema_is_an_error_not_a_fallback
- Progress log
- Live demo — 5 minutes, terminal only
- LucidForm — Methodology

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 55 edges
2. `Candidate` - 52 edges
3. `FormState` - 48 edges
4. `load()` - 43 edges
5. `get_settings()` - 42 edges
6. `Event` - 40 edges
7. `EventLog` - 38 edges
8. `Status` - 36 edges
9. `FieldSpec` - 35 edges
10. `Extraction` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Commit invariant` --references--> `SilentWriteBlocked`  [INFERRED]
  SPEC.md → lucidform/formstate/state.py
- `Conventions` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py
- `A. The five-stage pipeline` --references--> `Candidate`  [INFERRED]
  docs/paper-draft.md → lucidform/models.py
- `Three enforcement mechanisms` --references--> `ConfirmationReceipt`  [INFERRED]
  SPEC.md → lucidform/formstate/receipt.py
- `Code map` --references--> `FieldSpec`  [INFERRED]
  AGENTS.md → lucidform/models.py

## Import Cycles
- None detected.

## Communities (103 total, 25 thin omitted)

### Community 0 - "FieldSpec"
Cohesion: 0.06
Nodes (37): _category(), decode_spelled(), enum_error(), format_error(), length_error(), normalize(), parse_date(), range_error() (+29 more)

### Community 1 - "Event"
Cohesion: 0.16
Nodes (15): Event, read_log(), test_a_second_log_on_the_same_session_appends(), test_dataclass_payloads_are_serialised(), test_enums_inside_payloads_become_their_values(), test_latency_is_null_when_unmeasured_not_zero(), test_records_are_appended_never_overwritten(), test_session_end_closes_the_record() (+7 more)

### Community 2 - "Candidate"
Cohesion: 0.07
Nodes (27): SilentWriteBlocked, Candidate, forge(), gate(), make(), state(), test_a_blocked_write_is_logged_as_an_event(), test_a_confirmed_value_is_written() (+19 more)

### Community 3 - "test_readback.py"
Cohesion: 0.15
Nodes (16): field(), render(), schema(), test_a_date_has_no_leading_zero_on_the_day(), test_a_date_is_spoken_readably_not_as_stored(), test_a_mobile_number_is_grouped_too(), test_a_pan_is_spelled_out_not_pronounced(), test_an_aadhaar_is_grouped_so_it_can_be_held_in_memory() (+8 more)

### Community 4 - "build.js"
Cohesion: 0.08
Nodes (31): docx, authorsTable(), body(), bodyBlocks(), COL_W, doc, {
  Document, Packer, Paragraph, TextRun, AlignmentType, SectionType, Table, TableRow,
  TableCell, WidthType, BorderStyle, ShadingType, LevelFormat,
}, fs (+23 more)

### Community 5 - "SessionGraph"
Cohesion: 0.08
Nodes (11): _build(), node_names(), _route(), SessionGraph, _structure(), _Stub, TurnState, FieldResult (+3 more)

### Community 6 - "test_i18n.py"
Cohesion: 0.12
Nodes (8): available(), MissingString, Strings, test_a_missing_key_raises_rather_than_falling_back(), test_a_missing_placeholder_raises_with_the_key_named(), test_both_languages_are_available(), test_the_canonical_label_stays_english_for_the_pdf_and_logs(), test_the_greeting_explains_the_confirmation_step()

### Community 8 - "test_confirm.py"
Cohesion: 0.07
Nodes (22): UnauthorizedIssuer, confirm(), normalize_utterance(), parse_affirmation(), gate(), _mint_as_issuer(), passing(), test_a_confirmation_issues_a_receipt() (+14 more)

### Community 9 - "test_gate_crossfield.py"
Cohesion: 0.11
Nodes (16): check(), CrossFieldResult, pan_matches_surname(), pin_matches_confirmed_state(), _skipped(), gate(), test_a_check_with_an_unconfirmed_dependency_is_skipped_not_passed(), test_a_state_with_no_region_data_is_not_checked() (+8 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.06
Nodes (20): write_tables(), agg(), runs(), schema(), sessions(), test_a_question_and_the_answer_after_it_are_separate_turns(), test_all_tables_are_written(), test_nothing_wrong_was_committed() (+12 more)

### Community 11 - "cli.py"
Cohesion: 0.10
Nodes (22): asr_probe_cmd(), extract_cmd(), _extraction_client(), gate_check(), graph_cmd(), _help_agent(), help_ask(), help_eval() (+14 more)

### Community 12 - "FormState"
Cohesion: 0.08
Nodes (21): graphify reference: transcribe video and audio, Step 2.5 - Transcribe video / audio files (only if video files detected), FormState, export(), ExportError, read_back(), commit(), gate() (+13 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.11
Nodes (22): extractor(), gate(), replay(), schema(), test_a_decline_never_becomes_a_candidate(), test_a_loose_match_reports_no_span_rather_than_a_wrong_one(), test_a_question_never_becomes_a_candidate(), test_a_quote_from_the_utterance_grounds() (+14 more)

### Community 14 - "ProbeSummary"
Cohesion: 0.19
Nodes (6): is_simulated(), ProbeResult, ProbeSummary, report(), test_a_real_recogniser_would_not_be_labelled_simulated(), test_simulated_runs_are_labelled_as_not_being_measurements()

### Community 15 - "parametrize"
Cohesion: 0.33
Nodes (3): test_every_field_is_resolved(), test_no_committed_value_differs_from_ground_truth(), test_no_write_was_blocked_during_a_normal_session()

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (28): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+20 more)

### Community 17 - "load_all"
Cohesion: 0.15
Nodes (9): build(), _clean_extraction(), write(), __iter__(), load_all(), load_persona(), Persona, test_normalisation_is_applied_before_judging_a_proposal() (+1 more)

### Community 18 - "test_session.py"
Cohesion: 0.12
Nodes (9): personas(), runs(), schema(), test_a_declined_optional_field_stays_empty(), test_a_question_is_handled_mid_session(), test_out_of_enum_answers_are_re_asked_not_mapped(), test_the_gate_catches_the_homoglyph(), test_the_readback_catches_what_nothing_else_could() (+1 more)

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.12
Nodes (14): test_keyword_questions_retrieve_their_source(), _imported_names(), _parse(), _python_files(), _rel(), test_decision_and_write_paths_import_no_model(), test_forbidden_import_detection_works(), test_private_form_state_is_not_touched_from_outside() (+6 more)

### Community 20 - "readback.py"
Cohesion: 0.13
Nodes (10): render(), render_value(), spell(), spell_email(), test_spell_groups_evenly_and_keeps_the_remainder(), test_spell_ignores_whitespace_in_the_source_value(), test_spell_without_grouping(), test_the_hindi_readback_frame_is_used_for_hindi() (+2 more)

### Community 21 - "grounding.py"
Cohesion: 0.22
Nodes (7): check(), clamp_confidence(), Grounding, locate(), _loose(), test_a_model_reporting_impossible_confidence_is_clamped(), test_clamping_only_ever_lowers_confidence()

### Community 22 - "test_voice.py"
Cohesion: 0.16
Nodes (11): EchoRecognizer, SilentSynthesizer, personas(), schema(), test_an_empty_transcript_is_an_unusable_answer_not_a_hang_up(), test_asr_confidence_is_recorded_but_never_reaches_the_gate(), test_audio_events_are_logged_on_both_sides(), test_no_audio_ends_the_field_rather_than_being_read_as_consent() (+3 more)

### Community 23 - "test_personas.py"
Cohesion: 0.08
Nodes (10): pin_matches_state(), test_a_persona_with_no_utterances_is_rejected(), test_aadhaar_numbers_satisfy_verhoeff(), test_email_addresses_use_a_reserved_domain(), test_every_persona_declares_a_synthetic_header(), test_everyone_is_an_adult(), test_ground_truth_covers_every_required_field(), test_optional_fields_may_be_declined_but_must_still_be_answerable() (+2 more)

### Community 24 - "EventLog"
Cohesion: 0.20
Nodes (4): EventLog, _jsonable(), log(), test_the_log_exposes_no_way_to_update_or_delete()

### Community 25 - "test_checksums.py"
Cohesion: 0.12
Nodes (14): aadhaar_valid(), corrupt_one_digit(), synthetic_aadhaar(), verhoeff_check_digit(), verhoeff_valid(), test_adjacent_transpositions_are_caught(), test_check_digit_completes_a_payload(), test_check_digit_rejects_non_numeric_payload() (+6 more)

### Community 26 - "one_field"
Cohesion: 0.14
Nodes (13): one_field(), test_a_confirmed_value_is_committed(), test_a_denied_readback_is_recorded_as_a_correction(), test_a_field_that_runs_out_of_attempts_is_abandoned_not_left_empty(), test_a_hang_up_at_the_read_back_ends_the_field_without_re_asking(), test_a_rejected_value_is_explained_in_the_gates_own_words(), test_a_spoofed_confirmation_does_not_commit(), test_declining_a_required_field_is_refused() (+5 more)

### Community 27 - "test_schema_loader.py"
Cohesion: 0.08
Nodes (11): built_pdf(), overlay(), schema(), test_a_field_missing_from_the_pdf_is_fatal(), test_a_widget_with_no_overlay_entry_is_fatal(), test_an_ambiguous_or_orphan_enum_name_is_fatal(), test_cross_field_dependencies_are_declared(), test_enum_fields_carry_their_option_list() (+3 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.09
Nodes (21): A. Form representation, A. The five-stage pipeline, B. Synthetic data and its construction, B. The validation gate and its rejection taxonomy, C. Adversarial evaluation corpora, C. Extraction as a structurally bounded model call, D. Evaluation harness and its honesty constraints, D. Read-back and the confirmation whitelist (+13 more)

### Community 29 - "pytest"
Cohesion: 0.11
Nodes (8): _candidate(), committed(), gate(), test_adversarial_case(), test_every_case_declares_why_it_exists(), test_gate_never_raises_on_hostile_input(), test_the_suite_covers_every_reason_code_the_gate_can_emit(), test_the_suite_has_controls_in_the_categories_that_need_them()

### Community 30 - "answer.py"
Cohesion: 0.16
Nodes (7): AnswerClient, HelpAgent, HelpAnswer, _passages(), _question_lines(), emit(), HelpIndex

### Community 31 - "voice.py"
Cohesion: 0.11
Nodes (6): FasterWhisperRecognizer, PiperSynthesizer, SpeechRecognizer, SpeechSynthesizer, VoiceBackendMissing, test_asking_for_a_missing_backend_says_how_to_install_it()

### Community 32 - "probe"
Cohesion: 0.19
Nodes (7): CorruptingRecognizer, Transcript, probe(), test_a_perfect_recogniser_loses_nothing(), transcribe(), test_corrupted_identifiers_are_classified_and_offered_to_the_gate(), test_the_probe_runs_end_to_end_without_any_model()

### Community 33 - "HashEmbedder"
Cohesion: 0.16
Nodes (6): _corpus_digest(), Embedder, HashEmbedder, _normalise(), test_an_index_built_with_another_embedder_is_refused(), test_the_index_round_trips_through_disk()

### Community 34 - "corpus.py"
Cohesion: 0.16
Nodes (11): help_build(), _clean(), _flat(), _html_text(), load_chunks(), load_manifest(), _pdf_text(), _read() (+3 more)

### Community 35 - "VoiceChannel"
Cohesion: 0.22
Nodes (4): Kind, VoiceChannel, VoiceTurn, test_the_module_imports_without_any_speech_library()

### Community 36 - "events.py"
Cohesion: 0.11
Nodes (7): Intent, extractor(), _has_credentials(), test_a_decline_is_not_extracted_as_a_value(), test_a_question_is_not_extracted_as_a_value(), test_a_spoken_identifier_is_transcribed(), test_the_model_cannot_return_anything_outside_the_schema()

### Community 37 - "loader.py"
Cohesion: 0.10
Nodes (3): rows(), run(), FormSchema

### Community 38 - "build"
Cohesion: 0.29
Nodes (4): build(), build_user_message(), test_enum_prompts_forbid_substituting_the_nearest_option(), test_prompt_carries_the_field_but_asks_for_no_judgement()

### Community 39 - "models.py"
Cohesion: 0.08
Nodes (12): Invariants — never break these (the test suite enforces them), Non-negotiables, V. Algorithm and Pseudocode, _calling_module(), ConfirmationReceipt, CommitRecord, DeclineRecord, block() (+4 more)

### Community 40 - "with_retries"
Cohesion: 0.28
Nodes (3): GeminiAnswerClient, json_config(), with_retries()

### Community 41 - "test_help.py"
Cohesion: 0.11
Nodes (10): HelpReply, ScriptedAnswerClient, agent(), test_a_citation_to_a_passage_that_was_not_retrieved_falls_back(), test_a_cited_answer_is_spoken_with_its_source(), test_a_model_failure_never_breaks_the_session(), test_an_unanswerable_question_falls_back_and_says_so(), test_an_uncited_answer_falls_back() (+2 more)

### Community 42 - "load"
Cohesion: 0.15
Nodes (8): load(), test_an_unknown_language_fails_with_a_useful_message(), test_every_field_has_a_spoken_label_in_this_language(), test_every_language_has_the_same_keys(), test_every_schema_field_has_a_prompt_and_gloss_in_this_language(), test_hindi_strings_are_actually_devanagari(), test_no_string_is_empty(), test_placeholders_match_across_languages()

### Community 43 - "run_persona"
Cohesion: 0.12
Nodes (9): ReplayRun, run_persona(), ReplayClient, main(), record(), _scrub(), golden(), test_persona_sessions_match_the_pre_langgraph_loop() (+1 more)

### Community 44 - "parse_acroform"
Cohesion: 0.20
Nodes (5): _inherited(), load_overlay(), parse_acroform(), SchemaError, test_max_length_comes_from_the_pdf_not_the_overlay()

### Community 45 - "M0. System design"
Cohesion: 0.20
Nodes (10): M0.1 Problem framing, M0.2 The five-stage pipeline, M0.3 Enforcing the constraint rather than asserting it, M0.4 Form representation: parser-assisted, human-verified schema, M0.5 Language selection, M0.6 Deferral of the voice channel, M0.7 Evaluation design, M0.8 Data (+2 more)

### Community 46 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 48 - "M2. The validation gate"
Cohesion: 0.22
Nodes (9): M2.1 Construction order, M2.2 Both directions are asserted, M2.3 Check ordering as a defined quantity, M2.4 Normalization reshapes but does not repair, M2.5 A script-dependent validation trap, M2.6 Cross-field checks and the confirmation dependency, M2.7 The validator does not interpret text, M2.8 Isolation (+1 more)

### Community 49 - "Row"
Cohesion: 0.20
Nodes (7): load_set(), Row, summarise(), write(), test_every_gold_label_exists_in_the_corpus(), test_scoring_counts_hits_answers_and_refusals(), row()

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

### Community 56 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 59 - "M1. Implementation notes — instrumentation and corpus"
Cohesion: 0.33
Nodes (6): M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 61 - "Purpose"
Cohesion: 0.12
Nodes (4): InputChannel, OutputChannel, Purpose, ConsoleChannel

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
Nodes (12): Commands, Conventions, Environment, Gotchas, graphify, LucidForm, Phase 3 notes, Phase 4 notes (+4 more)

### Community 66 - "_check"
Cohesion: 0.22
Nodes (5): _check(), test_an_empty_dependency_counts_as_unconfirmed(), test_skipping_lets_the_value_through_but_records_the_skip(), test_structural_failures_are_reported_before_cross_field_ones(), test_the_same_value_is_rejected_once_the_dependency_is_confirmed()

### Community 69 - "index.py"
Cohesion: 0.22
Nodes (4): Hit, reciprocal_rank_fusion(), tokenize(), test_reciprocal_rank_fusion_rewards_agreement()

### Community 70 - "LucidForm — Specification"
Cohesion: 0.05
Nodes (35): AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate, Code map, Run, What this is, Working rules for agents, Handing off to another AI, One-time setup, Per phase (+27 more)

### Community 71 - "report"
Cohesion: 0.18
Nodes (6): _pct(), percentile(), report(), test_percentile_of_nothing_is_none_not_zero(), test_percentiles_are_values_that_actually_occurred(), test_the_report_names_the_invariant()

### Community 72 - "make_form.py"
Cohesion: 0.19
Nodes (4): build(), _header(), _overlay(), _blank_form_template()

### Community 75 - "Extraction"
Cohesion: 0.20
Nodes (5): Extraction, test_a_question_is_answered_and_does_not_count_as_an_attempt(), test_declining_an_optional_field_is_recorded_not_committed(), test_endless_questions_are_bounded(), test_the_explanation_is_the_fields_own_gloss()

### Community 78 - "ValidationGate"
Cohesion: 0.05
Nodes (25): ValidationGate, Check, Reason, Status, ValidationReport, candidate(), gate(), schema() (+17 more)

### Community 79 - "Extractor"
Cohesion: 0.10
Nodes (8): ExtractionClient, ModelReply, ExtractionOutcome, Extractor, test_every_persona_utterance_has_a_recorded_response(), test_replaying_an_out_of_enum_income_is_rejected_not_mapped(), test_replaying_p02_pan_yields_the_homoglyph_the_gate_then_rejects(), test_replaying_p03_pan_yields_a_question_then_a_value()

### Community 82 - "ScriptedClient"
Cohesion: 0.25
Nodes (3): ScriptedClient, test_a_question_is_logged_too(), test_extraction_is_logged_with_both_confidence_figures()

### Community 83 - "Chunk"
Cohesion: 0.25
Nodes (4): Chunk, chunks(), index(), schema()

### Community 84 - "Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms"
Cohesion: 0.50
Nodes (3): A: Form No. 93 – PAN Application Form for Individual (Being citizen of India), FAQ's on PAN, Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms

### Community 86 - "character_error_rate"
Cohesion: 0.40
Nodes (3): character_error_rate(), levenshtein(), test_character_error_rate_is_zero_for_an_exact_match()

### Community 87 - "M8. The help agent"
Cohesion: 0.33
Nodes (6): M8.1 Scope: explanation, never a value, M8.2 Corpus and chunking, M8.3 Hybrid retrieval, M8.4 The citation check, M8.5 Evaluation, and what it does not measure, M8. The help agent

### Community 89 - "metrics.py"
Cohesion: 0.11
Nodes (13): FieldOutcome, _is_correct(), load_sessions(), parse_session(), outcome(), _personas(), SessionMetrics, _truth() (+5 more)

### Community 96 - "Progress log"
Cohesion: 0.40
Nodes (4): 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5, 2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper, 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs, Progress log

### Community 98 - "Live demo — 5 minutes, terminal only"
Cohesion: 0.40
Nodes (4): Backup commands (if the network is slow), Live demo — 5 minutes, terminal only, Script — what to type, and what to point out, The one-line pitch while it runs

### Community 101 - "LucidForm — Methodology"
Cohesion: 0.40
Nodes (5): LucidForm — Methodology, M7.1 Why replace a working loop, M7.2 Parity, not intuition, M7.3 No checkpoint-resume, M7. The orchestrator as a state graph

## Knowledge Gaps
- **168 isolated node(s):** `M7.1 Why replace a working loop`, `M7.2 Parity, not intuition`, `M7.3 No checkpoint-resume`, `For /graphify add and --watch`, `For /graphify query` (+163 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 747 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `LucidForm — Specification`, `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M8. The help agent`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `Candidate` connect `Candidate` to `probe`, `PersonaChannel`, `Event`, `_check`, `events.py`, `loader.py`, `models.py`, `test_confirm.py`, `test_gate_crossfield.py`, `cli.py`, `FormState`, `ValidationGate`, `Extractor`, `test_voice.py`, `Title (pick one, or tell me to try again)`, `pytest`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `FormState` connect `FormState` to `Event`, `Candidate`, `loader.py`, `SessionGraph`, `models.py`, `run_persona`, `cli.py`, `test_session.py`, `test_voice.py`, `EventLog`, `test_a_form_is_filled_over_the_voice_channel`, `one_field`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ValidationGate` (e.g. with `Candidate` and `Check`) actually correct?**
  _`ValidationGate` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `Candidate` (e.g. with `Invariants — never break these (the test suite enforces them)` and `Conventions`) actually correct?**
  _`Candidate` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `FormState` (e.g. with `Event` and `EventLog`) actually correct?**
  _`FormState` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `M7.1 Why replace a working loop`, `M7.2 Parity, not intuition`, `M7.3 No checkpoint-resume` to the rest of the system?**
  _168 weakly-connected nodes found - possible documentation gaps or missing edges._