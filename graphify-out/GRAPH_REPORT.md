# Graph Report - LucidForm  (2026-09-30)

## Corpus Check
- 103 files · ~230,444 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .jsonl 17, (none) 4, .example 1)

## Summary
- 1725 nodes · 3579 edges · 120 communities (84 shown, 36 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 215 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `580fb4c7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_gate_rules.py
- Event
- test_formstate.py
- test_readback.py
- build.js
- SessionGraph
- Strings
- test_confirm.py
- test_gate_crossfield.py
- test_metrics.py
- cli.py
- FormState
- test_extraction.py
- ProbeSummary
- parametrize
- What You Must Do When Invoked
- ValidationGate
- .commit
- test_no_silent_write.py
- crossfield.py
- Extraction
- test_voice.py
- test_personas.py
- PersonaChannel
- test_checksums.py
- test_session.py
- test_schema_loader.py
- Title (pick one, or tell me to try again)
- loader.py
- HelpAgent
- voice.py
- Transcript
- HelpIndex
- corpus.py
- Extractor
- test_extraction_live.py
- events.py
- EventLog
- Candidate
- answer.py
- test_help.py
- test_i18n.py
- load_all
- M0. System design
- graphify reference: extra exports and benchmark
- M2. The validation gate
- evaluate.py
- Prompt for Claude Code — LucidForm Prototype
- test_llm_clients.py
- M3. The write path
- M4. Extraction
- M5. Orchestration and read-back
- graphify reference: query, path, explain
- models.py
- render_value
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- Purpose
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- Aggregate
- parse_acroform
- graphify reference: GitHub clone and cross-repo merge
- LucidForm — Specification
- get_settings
- .claude/CLAUDE.md
- extraction-spec.md
- schema/__init__.py
- Status
- ScriptedClient
- Puppet
- Settings
- make_client
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- LucidForm
- README.md
- M8. The help agent
- uidai_faq_update.md
- percentile
- III. System Architecture
- LucidForm
- base.py
- write_tables
- AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate
- Progress log
- test_graph.py
- Live demo — 5 minutes, terminal only
- Team guide
- LucidForm — Methodology
- metrics.py
- .decline
- spell
- test_a_failed_model_call_is_an_unclear_turn_not_a_crash
- test_an_ambiguous_or_orphan_enum_name_is_fatal
- test_a_form_is_filled_over_the_voice_channel
- test_form_state_exposes_no_alternative_mutator
- gate
- test_a_blocked_write_is_logged_as_an_event
- test_a_widget_with_no_overlay_entry_is_fatal
- test_every_devanagari_option_name_is_one_the_hindi_prompt_says
- load_sessions
- test_max_length_comes_from_the_pdf_not_the_overlay
- parse_session
- test_the_blank_template_has_no_prefilled_values
- test_every_field_has_a_plain_language_prompt_and_gloss

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 56 edges
2. `Candidate` - 50 edges
3. `FormState` - 49 edges
4. `load()` - 44 edges
5. `get_settings()` - 44 edges
6. `EventLog` - 38 edges
7. `Event` - 37 edges
8. `read_log()` - 37 edges
9. `Status` - 34 edges
10. `load_all()` - 32 edges

## Surprising Connections (you probably didn't know these)
- `The guarantee is enforced, not promised` --references--> `ConfirmationReceipt`  [INFERRED]
  README.md → lucidform/formstate/receipt.py
- `Commit invariant` --references--> `SilentWriteBlocked`  [INFERRED]
  SPEC.md → lucidform/formstate/state.py
- `Conventions` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py
- `A. The five-stage pipeline` --references--> `Candidate`  [INFERRED]
  docs/paper-draft.md → lucidform/models.py
- `Three enforcement mechanisms` --references--> `ConfirmationReceipt`  [INFERRED]
  SPEC.md → lucidform/formstate/receipt.py

## Import Cycles
- None detected.

## Communities (120 total, 36 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.06
Nodes (35): enum_error(), format_error(), length_error(), normalize(), parse_date(), range_error(), strip_invisible(), _enum_field() (+27 more)

### Community 1 - "Event"
Cohesion: 0.14
Nodes (16): Event, read_log(), test_a_second_log_on_the_same_session_appends(), test_dataclass_payloads_are_serialised(), test_enums_inside_payloads_become_their_values(), test_latency_is_null_when_unmeasured_not_zero(), test_records_are_appended_never_overwritten(), test_session_end_closes_the_record() (+8 more)

### Community 2 - "test_formstate.py"
Cohesion: 0.08
Nodes (22): SilentWriteBlocked, forge(), make(), test_a_confirmed_value_is_written(), test_a_correction_still_requires_its_own_confirmation(), test_a_field_can_be_corrected_and_the_history_shows_both(), test_a_receipt_authorising_an_empty_value_is_refused(), test_a_receipt_carrying_another_candidates_verdict_is_refused() (+14 more)

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
Cohesion: 0.11
Nodes (6): _build(), _route(), SessionGraph, TurnState, FieldResult, SessionResult

### Community 6 - "Strings"
Cohesion: 0.14
Nodes (7): available(), MissingString, Strings, test_a_missing_placeholder_raises_with_the_key_named(), test_both_languages_are_available(), test_the_hindi_readback_frame_is_used_for_hindi(), test_the_readback_sentence_names_the_field_and_the_value()

### Community 8 - "test_confirm.py"
Cohesion: 0.07
Nodes (22): UnauthorizedIssuer, confirm(), normalize_utterance(), parse_affirmation(), gate(), _mint_as_issuer(), passing(), test_a_confirmation_issues_a_receipt() (+14 more)

### Community 9 - "test_gate_crossfield.py"
Cohesion: 0.12
Nodes (13): pan_matches_surname(), _check(), gate(), test_a_check_with_an_unconfirmed_dependency_is_skipped_not_passed(), test_an_empty_dependency_counts_as_unconfirmed(), test_cross_field_checks_read_only_committed_values(), test_pan_fifth_character_disagreeing_with_the_surname_fails(), test_pan_fifth_character_matching_the_surname_passes() (+5 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.07
Nodes (11): test_a_question_and_the_answer_after_it_are_separate_turns(), test_nothing_wrong_was_committed(), test_offline_sessions_are_flagged_as_not_measuring_accuracy(), test_recall_and_false_positive_rate_are_both_reported(), test_the_caveat_survives_into_the_csv(), test_the_gate_rejected_no_correct_value(), test_the_layers_account_for_every_wrong_value(), test_the_logs_are_internally_consistent() (+3 more)

### Community 11 - "cli.py"
Cohesion: 0.10
Nodes (17): asr_probe_cmd(), extract_cmd(), gate_check(), graph_cmd(), _help_agent(), help_ask(), help_eval(), make_form_cmd() (+9 more)

### Community 12 - "FormState"
Cohesion: 0.08
Nodes (20): graphify reference: transcribe video and audio, Step 2.5 - Transcribe video / audio files (only if video files detected), FormState, export(), ExportError, read_back(), commit(), gate() (+12 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.07
Nodes (27): extractor(), gate(), replay(), schema(), test_a_decline_never_becomes_a_candidate(), test_a_loose_match_reports_no_span_rather_than_a_wrong_one(), test_a_question_never_becomes_a_candidate(), test_a_quote_from_the_utterance_grounds() (+19 more)

### Community 14 - "ProbeSummary"
Cohesion: 0.18
Nodes (7): is_simulated(), ProbeResult, ProbeSummary, report(), rows(), test_a_real_recogniser_would_not_be_labelled_simulated(), test_simulated_runs_are_labelled_as_not_being_measurements()

### Community 15 - "parametrize"
Cohesion: 0.33
Nodes (3): test_every_field_is_resolved(), test_no_committed_value_differs_from_ground_truth(), test_no_write_was_blocked_during_a_normal_session()

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.06
Nodes (32): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+24 more)

### Community 17 - "ValidationGate"
Cohesion: 0.10
Nodes (4): ValidationGate, Check, committed(), gate()

### Community 18 - ".commit"
Cohesion: 0.20
Nodes (5): V. Algorithm and Pseudocode, CommitRecord, block(), Invariants every phase keeps, LucidForm — roadmap

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.12
Nodes (15): _help_violations(), _imported_names(), _parse(), _python_files(), _rel(), test_decision_and_write_paths_import_no_model(), test_forbidden_import_detection_works(), test_private_form_state_is_not_touched_from_outside() (+7 more)

### Community 20 - "crossfield.py"
Cohesion: 0.14
Nodes (10): check(), CrossFieldResult, pin_matches_confirmed_state(), _skipped(), pin_matches_state(), test_a_state_with_no_region_data_is_not_checked(), test_fields_without_a_cross_field_rule_return_nothing(), test_pin_in_the_right_postal_region_passes() (+2 more)

### Community 21 - "Extraction"
Cohesion: 0.18
Nodes (8): check(), clamp_confidence(), Grounding, locate(), _loose(), Extraction, test_a_model_reporting_impossible_confidence_is_clamped(), test_clamping_only_ever_lowers_confidence()

### Community 22 - "test_voice.py"
Cohesion: 0.12
Nodes (15): CorruptingRecognizer, EchoRecognizer, SilentSynthesizer, personas(), schema(), test_an_empty_transcript_is_an_unusable_answer_not_a_hang_up(), test_asr_confidence_is_recorded_but_never_reaches_the_gate(), test_audio_events_are_logged_on_both_sides() (+7 more)

### Community 23 - "test_personas.py"
Cohesion: 0.07
Nodes (9): PersonaError, test_a_persona_with_no_utterances_is_rejected(), test_aadhaar_numbers_satisfy_verhoeff(), test_email_addresses_use_a_reserved_domain(), test_every_persona_declares_a_synthetic_header(), test_everyone_is_an_adult(), test_ground_truth_covers_every_required_field(), test_optional_fields_may_be_declined_but_must_still_be_answerable() (+1 more)

### Community 25 - "test_checksums.py"
Cohesion: 0.12
Nodes (14): aadhaar_valid(), corrupt_one_digit(), synthetic_aadhaar(), verhoeff_check_digit(), verhoeff_valid(), test_adjacent_transpositions_are_caught(), test_check_digit_completes_a_payload(), test_check_digit_rejects_non_numeric_payload() (+6 more)

### Community 26 - "test_session.py"
Cohesion: 0.08
Nodes (24): one_field(), StubHelper, test_a_confirmed_value_is_committed(), test_a_declined_optional_field_stays_empty(), test_a_denied_readback_is_recorded_as_a_correction(), test_a_field_that_runs_out_of_attempts_is_abandoned_not_left_empty(), test_a_hang_up_at_the_read_back_ends_the_field_without_re_asking(), test_a_question_is_answered_and_does_not_count_as_an_attempt() (+16 more)

### Community 27 - "test_schema_loader.py"
Cohesion: 0.14
Nodes (5): built_pdf(), schema(), test_a_field_missing_from_the_pdf_is_fatal(), test_cross_field_dependencies_are_declared(), test_missing_pdf_names_the_fix()

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.15
Nodes (13): A. Form representation, B. Synthetic data and its construction, C. Adversarial evaluation corpora, D. Evaluation harness and its honesty constraints, E. Help-agent evaluation, I. Introduction, II. Related Work, IV. Methodology (+5 more)

### Community 29 - "loader.py"
Cohesion: 0.07
Nodes (14): _category(), character_error_rate(), decode_spelled(), levenshtein(), probe(), build(), build_user_message(), FieldSpec (+6 more)

### Community 30 - "HelpAgent"
Cohesion: 0.14
Nodes (6): AnswerClient, HelpAgent, HelpAnswer, _question_lines(), emit(), test_a_retrieval_failure_never_breaks_the_session()

### Community 31 - "voice.py"
Cohesion: 0.14
Nodes (4): FasterWhisperRecognizer, PiperSynthesizer, VoiceBackendMissing, test_asking_for_a_missing_backend_says_how_to_install_it()

### Community 32 - "Transcript"
Cohesion: 0.19
Nodes (5): SpeechRecognizer, SpeechSynthesizer, Transcript, test_a_perfect_recogniser_loses_nothing(), transcribe()

### Community 33 - "HelpIndex"
Cohesion: 0.14
Nodes (9): _corpus_digest(), Embedder, HashEmbedder, HelpIndex, _normalise(), tokenize(), index(), test_an_index_built_with_another_embedder_is_refused() (+1 more)

### Community 34 - "corpus.py"
Cohesion: 0.15
Nodes (12): help_build(), Chunk, _clean(), _flat(), _html_text(), load_chunks(), load_manifest(), _pdf_text() (+4 more)

### Community 35 - "Extractor"
Cohesion: 0.09
Nodes (9): AnthropicExtractionClient, ModelReply, ExtractionOutcome, Extractor, test_a_replay_corpus_miss_still_raises(), test_every_persona_utterance_has_a_recorded_response(), test_replaying_an_out_of_enum_income_is_rejected_not_mapped(), test_replaying_p02_pan_yields_the_homoglyph_the_gate_then_rejects() (+1 more)

### Community 36 - "test_extraction_live.py"
Cohesion: 0.13
Nodes (6): Intent, _has_credentials(), test_a_decline_is_not_extracted_as_a_value(), test_a_question_is_not_extracted_as_a_value(), test_a_spoken_identifier_is_transcribed(), test_the_model_cannot_return_anything_outside_the_schema()

### Community 38 - "EventLog"
Cohesion: 0.17
Nodes (5): EventLog, _jsonable(), log(), test_the_log_exposes_no_way_to_update_or_delete(), test_a_model_that_always_fails_ends_the_session_cleanly()

### Community 39 - "Candidate"
Cohesion: 0.12
Nodes (10): Invariants — never break these (the test suite enforces them), Non-negotiables, _calling_module(), ConfirmationReceipt, Candidate, 4. Data model, _candidate(), test_adversarial_case() (+2 more)

### Community 40 - "answer.py"
Cohesion: 0.11
Nodes (8): GeminiAnswerClient, _passages(), GeminiEmbedder, Hit, _hinted_delay(), json_config(), make_genai_client(), with_retries()

### Community 41 - "test_help.py"
Cohesion: 0.09
Nodes (15): HelpReply, ScriptedAnswerClient, reciprocal_rank_fusion(), agent(), chunks(), schema(), test_a_citation_to_a_passage_that_was_not_retrieved_falls_back(), test_a_cited_answer_is_spoken_with_its_source() (+7 more)

### Community 42 - "test_i18n.py"
Cohesion: 0.12
Nodes (11): load(), test_a_missing_key_raises_rather_than_falling_back(), test_an_unknown_language_fails_with_a_useful_message(), test_every_field_has_a_spoken_label_in_this_language(), test_every_language_has_the_same_keys(), test_every_schema_field_has_a_prompt_and_gloss_in_this_language(), test_hindi_strings_are_actually_devanagari(), test_no_string_is_empty() (+3 more)

### Community 43 - "load_all"
Cohesion: 0.11
Nodes (13): _extraction_client(), run_cmd(), load_all(), load_persona(), run_persona(), ReplayClient, Session, record() (+5 more)

### Community 45 - "M0. System design"
Cohesion: 0.20
Nodes (10): M0.1 Problem framing, M0.2 The five-stage pipeline, M0.3 Enforcing the constraint rather than asserting it, M0.4 Form representation: parser-assisted, human-verified schema, M0.5 Language selection, M0.6 Deferral of the voice channel, M0.7 Evaluation design, M0.8 Data (+2 more)

### Community 46 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 48 - "M2. The validation gate"
Cohesion: 0.22
Nodes (9): M2.1 Construction order, M2.2 Both directions are asserted, M2.3 Check ordering as a defined quantity, M2.4 Normalization reshapes but does not repair, M2.5 A script-dependent validation trap, M2.6 Cross-field checks and the confirmation dependency, M2.7 The validator does not interpret text, M2.8 Isolation (+1 more)

### Community 49 - "evaluate.py"
Cohesion: 0.11
Nodes (12): gold_matches(), load_set(), Row, run(), summarise(), write(), test_a_numbered_gold_label_matches_only_that_number(), row() (+4 more)

### Community 50 - "Prompt for Claude Code — LucidForm Prototype"
Cohesion: 0.29
Nodes (6): Context, How I want you to work with me, Non-negotiable design constraint, Prompt for Claude Code — LucidForm Prototype, Scope for THIS prototype (deliberately small), What I need from you, in order

### Community 51 - "test_llm_clients.py"
Cohesion: 0.15
Nodes (14): client_with(), fake_sdk(), FakeModels, rate_limited(), test_a_huge_retry_hint_is_capped(), test_a_non_retryable_error_is_raised_immediately(), test_a_rate_limit_is_retried_with_backoff(), test_a_rate_limit_retry_delay_hint_is_honoured() (+6 more)

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

### Community 57 - "models.py"
Cohesion: 0.14
Nodes (3): Affirmation, fingerprint(), ValidationReport

### Community 58 - "render_value"
Cohesion: 0.25
Nodes (4): render(), render_value(), spell_email(), test_the_decode_is_the_exact_inverse_of_the_read_back()

### Community 59 - "M1. Implementation notes — instrumentation and corpus"
Cohesion: 0.33
Nodes (6): M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 61 - "Purpose"
Cohesion: 0.13
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

### Community 66 - "parse_acroform"
Cohesion: 0.20
Nodes (6): Gotchas, _inherited(), load_overlay(), parse_acroform(), SchemaError, overlay()

### Community 70 - "LucidForm — Specification"
Cohesion: 0.15
Nodes (11): ReplayRun, 1. Intent, 2. The gating contract — the thesis of the project, 3. Non-negotiables, 5. Rejection taxonomy, 6. Scope of this prototype, 7. Eval outputs, Check order (+3 more)

### Community 72 - "get_settings"
Cohesion: 0.17
Nodes (7): get_settings(), build(), _header(), _overlay(), _blank_form_template(), personas(), schema()

### Community 75 - "schema/__init__.py"
Cohesion: 0.16
Nodes (5): build(), _clean_extraction(), write(), __iter__(), Persona

### Community 78 - "Status"
Cohesion: 0.08
Nodes (22): Reason, Status, candidate(), gate(), schema(), test_a_pass_carries_the_exact_value_that_will_be_written(), test_a_pass_must_not_carry_a_reason(), test_a_rejection_carries_nothing_committable() (+14 more)

### Community 82 - "Settings"
Cohesion: 0.27
Nodes (3): Settings, test_sdk_key_variables_are_read_without_the_project_prefix(), test_the_default_provider_is_gemini_and_the_model_is_config()

### Community 83 - "make_client"
Cohesion: 0.14
Nodes (7): ExtractionClient, GeminiExtractionClient, make_client(), UnknownProvider, extractor(), test_an_unknown_provider_is_refused(), test_the_factory_picks_the_configured_provider()

### Community 84 - "Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms"
Cohesion: 0.50
Nodes (3): A: Form No. 93 – PAN Application Form for Individual (Being citizen of India), FAQ's on PAN, Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms

### Community 85 - "LucidForm"
Cohesion: 0.20
Nodes (10): A real session, Documentation, How it works, LucidForm, Project layout, Quickstart, Results, Team (+2 more)

### Community 86 - "README.md"
Cohesion: 0.25
Nodes (4): Handing off to another AI, One-time setup, Per phase, Team workflow (5 people, each with their own AI assistant)

### Community 87 - "M8. The help agent"
Cohesion: 0.33
Nodes (6): M8.1 Scope: explanation, never a value, M8.2 Corpus and chunking, M8.3 Hybrid retrieval, M8.4 The citation check, M8.5 Evaluation, and what it does not measure, M8. The help agent

### Community 89 - "percentile"
Cohesion: 0.29
Nodes (3): percentile(), test_percentile_of_nothing_is_none_not_zero(), test_percentiles_are_values_that_actually_occurred()

### Community 90 - "III. System Architecture"
Cohesion: 0.25
Nodes (8): A. The five-stage pipeline, B. The validation gate and its rejection taxonomy, C. Extraction as a structurally bounded model call, D. Read-back and the confirmation whitelist, E. Three independent enforcement mechanisms, F. The orchestrator as a declared state graph, G. A help agent that cannot write, III. System Architecture

### Community 91 - "LucidForm"
Cohesion: 0.20
Nodes (7): Commands, Conventions, Environment, graphify, LucidForm, Phase 3 notes, Phase 4 notes

### Community 94 - "write_tables"
Cohesion: 0.29
Nodes (6): _write_csv(), write_tables(), test_all_tables_are_written(), test_the_fields_table_records_ground_truth_beside_what_was_committed(), test_the_summary_is_a_single_row(), test_the_turns_table_has_one_row_per_turn()

### Community 95 - "AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate"
Cohesion: 0.29
Nodes (6): AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate, Code map, Run, What this is, Working rules for agents, main()

### Community 96 - "Progress log"
Cohesion: 0.33
Nodes (5): 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5, 2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper, 2026-09-30 (night) · Shubh (+Claude) · Pre-push audit, 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs, Progress log

### Community 97 - "test_graph.py"
Cohesion: 0.29
Nodes (3): golden(), test_persona_sessions_match_the_pre_langgraph_loop(), test_the_graph_draws_as_mermaid_for_the_paper()

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
Cohesion: 0.16
Nodes (7): FieldOutcome, outcome(), _pct(), report(), _truth(), Turn, test_the_report_names_the_invariant()

### Community 104 - "spell"
Cohesion: 0.40
Nodes (4): spell(), test_spell_groups_evenly_and_keeps_the_remainder(), test_spell_ignores_whitespace_in_the_source_value(), test_spell_without_grouping()

### Community 115 - "load_sessions"
Cohesion: 0.22
Nodes (6): load_sessions(), SessionMetrics, agg(), schema(), sessions(), test_a_tampered_log_is_detected()

### Community 117 - "parse_session"
Cohesion: 0.19
Nodes (6): _is_correct(), parse_session(), _personas(), test_a_session_without_ground_truth_is_excluded_from_accuracy(), test_normalisation_is_applied_before_judging_a_proposal(), test_unscored_sessions_still_contribute_the_measures_that_need_no_truth()

## Knowledge Gaps
- **170 isolated node(s):** `Why`, `A real session`, `Results`, `Quickstart`, `Project layout` (+165 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 764 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M8. The help agent`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `FormState` connect `FormState` to `Event`, `test_formstate.py`, `events.py`, `EventLog`, `Candidate`, `.decline`, `load_all`, `cli.py`, `test_form_state_exposes_no_alternative_mutator`, `gate`, `.is_resolved`, `test_a_blocked_write_is_logged_as_an_event`, `test_a_form_is_filled_over_the_voice_channel`, `.commit`, `test_voice.py`, `models.py`, `test_session.py`, `loader.py`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Why does `Candidate` connect `Candidate` to `Event`, `test_formstate.py`, `Extractor`, `test_confirm.py`, `test_gate_crossfield.py`, `cli.py`, `FormState`, `Status`, `test_a_blocked_write_is_logged_as_an_event`, `ValidationGate`, `.commit`, `test_voice.py`, `models.py`, `III. System Architecture`, `LucidForm`, `loader.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ValidationGate` (e.g. with `Candidate` and `Check`) actually correct?**
  _`ValidationGate` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Candidate` (e.g. with `Invariants — never break these (the test suite enforces them)` and `Conventions`) actually correct?**
  _`Candidate` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `FormState` (e.g. with `Event` and `EventLog`) actually correct?**
  _`FormState` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Why`, `A real session`, `Results` to the rest of the system?**
  _170 weakly-connected nodes found - possible documentation gaps or missing edges._