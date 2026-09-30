# Graph Report - LucidForm  (2026-09-30)

## Corpus Check
- 103 files · ~229,903 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .jsonl 17, (none) 4, .example 1)

## Summary
- 1722 nodes · 3572 edges · 118 communities (78 shown, 40 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 214 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d74eac3e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_gate_rules.py
- EventLog
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
- ValidationGate
- .commit
- test_no_silent_write.py
- render
- Extraction
- test_voice.py
- test_personas.py
- Purpose
- test_checksums.py
- test_session.py
- test_schema_loader.py
- Title (pick one, or tell me to try again)
- test_adversarial.py
- HelpAgent
- voice.py
- test_a_form_is_filled_over_the_voice_channel
- HelpIndex
- corpus.py
- Extractor
- test_extraction_live.py
- loader.py
- extractor.py
- Status
- answer.py
- test_help.py
- load
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
- Kind
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- Aggregate
- load
- graphify reference: GitHub clone and cross-repo merge
- LucidForm — Specification
- get_settings
- .claude/CLAUDE.md
- extraction-spec.md
- graph.py
- test_gate.py
- ScriptedClient
- Puppet
- /graphify
- FormSchema
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- ReplayClient
- probe
- M8. The help agent
- uidai_faq_update.md
- report
- SessionResult
- LucidForm
- base.py
- write_tables
- aadhaar_valid
- Progress log
- test_graph.py
- Live demo — 5 minutes, terminal only
- verhoeff_valid
- LucidForm — Methodology
- metrics.py
- CorruptingRecognizer
- passing
- graphify reference: transcribe video and audio
- PersonaError
- test_form_state_exposes_no_alternative_mutator
- test_the_wrong_values_in_the_corpus_are_identified
- test_nothing_wrong_was_committed
- test_offline_sessions_are_flagged_as_not_measuring_accuracy
- test_the_caveat_survives_into_the_csv
- test_the_logs_are_internally_consistent
- test_a_tampered_log_is_detected
- test_turn_records_carry_both_confidence_figures
- test_normalisation_is_applied_before_judging_a_proposal

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 56 edges
2. `Candidate` - 50 edges
3. `FormState` - 49 edges
4. `get_settings()` - 44 edges
5. `load()` - 44 edges
6. `EventLog` - 38 edges
7. `Event` - 37 edges
8. `read_log()` - 37 edges
9. `Status` - 34 edges
10. `load_all()` - 32 edges

## Surprising Connections (you probably didn't know these)
- `Commit invariant` --references--> `SilentWriteBlocked`  [INFERRED]
  SPEC.md → lucidform/formstate/state.py
- `Conventions` --references--> `Candidate`  [INFERRED]
  CLAUDE.md → lucidform/models.py
- `A. The five-stage pipeline` --references--> `Candidate`  [INFERRED]
  docs/paper-draft.md → lucidform/models.py
- `Step 2.5 - Transcribe video / audio files (only if video files detected)` --references--> `export()`  [INFERRED]
  .claude/skills/graphify/references/transcribe.md → lucidform/formstate/writer.py
- `4. Data model` --references--> `FormState`  [INFERRED]
  SPEC.md → lucidform/formstate/state.py

## Import Cycles
- None detected.

## Communities (118 total, 40 thin omitted)

### Community 0 - "test_gate_rules.py"
Cohesion: 0.06
Nodes (35): enum_error(), format_error(), length_error(), normalize(), parse_date(), range_error(), strip_invisible(), _enum_field() (+27 more)

### Community 1 - "EventLog"
Cohesion: 0.06
Nodes (26): Event, EventLog, _jsonable(), read_log(), _is_correct(), parse_session(), Turn, log() (+18 more)

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

### Community 6 - "test_i18n.py"
Cohesion: 0.12
Nodes (8): available(), MissingString, Strings, test_a_missing_key_raises_rather_than_falling_back(), test_a_missing_placeholder_raises_with_the_key_named(), test_both_languages_are_available(), test_the_canonical_label_stays_english_for_the_pdf_and_logs(), test_the_greeting_explains_the_confirmation_step()

### Community 8 - "test_confirm.py"
Cohesion: 0.07
Nodes (22): UnauthorizedIssuer, Affirmation, fingerprint(), confirm(), normalize_utterance(), parse_affirmation(), _mint_as_issuer(), test_a_confirmation_issues_a_receipt() (+14 more)

### Community 9 - "test_gate_crossfield.py"
Cohesion: 0.09
Nodes (21): check(), CrossFieldResult, pan_matches_surname(), pin_matches_confirmed_state(), _skipped(), _check(), gate(), test_a_check_with_an_unconfirmed_dependency_is_skipped_not_passed() (+13 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.10
Nodes (8): agg(), schema(), sessions(), test_a_question_and_the_answer_after_it_are_separate_turns(), test_recall_and_false_positive_rate_are_both_reported(), test_the_gate_rejected_no_correct_value(), test_the_layers_account_for_every_wrong_value(), test_the_read_back_caught_what_the_gate_could_not()

### Community 11 - "cli.py"
Cohesion: 0.11
Nodes (13): asr_probe_cmd(), graph_cmd(), _help_agent(), help_ask(), help_eval(), make_form_cmd(), metrics_cmd(), personas_list() (+5 more)

### Community 12 - "FormState"
Cohesion: 0.09
Nodes (19): FormState, export(), ExportError, read_back(), commit(), gate(), schema(), template() (+11 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.08
Nodes (25): extractor(), gate(), replay(), schema(), test_a_decline_never_becomes_a_candidate(), test_a_loose_match_reports_no_span_rather_than_a_wrong_one(), test_a_question_never_becomes_a_candidate(), test_a_quote_from_the_utterance_grounds() (+17 more)

### Community 14 - "ProbeSummary"
Cohesion: 0.20
Nodes (6): is_simulated(), ProbeResult, ProbeSummary, report(), rows(), test_a_real_recogniser_would_not_be_labelled_simulated()

### Community 15 - "parametrize"
Cohesion: 0.33
Nodes (3): test_every_field_is_resolved(), test_no_committed_value_differs_from_ground_truth(), test_no_write_was_blocked_during_a_normal_session()

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.14
Nodes (14): Part A - Structural extraction for code files, Part C - Merge AST + semantic into final extraction, Step 0 - GitHub repos and multi-path merge (only if a URL or several paths), Step 1 - Ensure graphify is installed, Step 2.5 - Video and audio (only if video files detected), Step 2 - Detect files, Step 3 - Extract entities and relationships, Step 4.5 - Graph health check (read-only integrity gate) (+6 more)

### Community 18 - ".commit"
Cohesion: 0.15
Nodes (5): V. Algorithm and Pseudocode, CommitRecord, DeclineRecord, block(), _now()

### Community 19 - "test_no_silent_write.py"
Cohesion: 0.12
Nodes (15): _help_violations(), _imported_names(), _parse(), _python_files(), _rel(), test_decision_and_write_paths_import_no_model(), test_forbidden_import_detection_works(), test_private_form_state_is_not_touched_from_outside() (+7 more)

### Community 20 - "render"
Cohesion: 0.40
Nodes (3): render(), test_the_hindi_readback_frame_is_used_for_hindi(), test_the_readback_sentence_names_the_field_and_the_value()

### Community 21 - "Extraction"
Cohesion: 0.18
Nodes (8): check(), clamp_confidence(), Grounding, locate(), _loose(), Extraction, test_a_model_reporting_impossible_confidence_is_clamped(), test_clamping_only_ever_lowers_confidence()

### Community 22 - "test_voice.py"
Cohesion: 0.12
Nodes (16): EchoRecognizer, SilentSynthesizer, VoiceChannel, personas(), schema(), test_an_empty_transcript_is_an_unusable_answer_not_a_hang_up(), test_asr_confidence_is_recorded_but_never_reaches_the_gate(), test_audio_events_are_logged_on_both_sides() (+8 more)

### Community 23 - "test_personas.py"
Cohesion: 0.09
Nodes (9): pin_matches_state(), test_a_persona_with_no_utterances_is_rejected(), test_email_addresses_use_a_reserved_domain(), test_every_persona_declares_a_synthetic_header(), test_everyone_is_an_adult(), test_ground_truth_covers_every_required_field(), test_optional_fields_may_be_declined_but_must_still_be_answerable(), test_pan_is_well_formed_and_agrees_with_the_surname() (+1 more)

### Community 24 - "Purpose"
Cohesion: 0.14
Nodes (4): Phase 4 notes, Purpose, PersonaChannel, Turn

### Community 25 - "test_checksums.py"
Cohesion: 0.24
Nodes (5): corrupt_one_digit(), verhoeff_check_digit(), test_check_digit_completes_a_payload(), test_check_digit_rejects_non_numeric_payload(), test_corruption_helper_changes_exactly_one_digit()

### Community 26 - "test_session.py"
Cohesion: 0.07
Nodes (25): one_field(), StubHelper, test_a_confirmed_value_is_committed(), test_a_declined_optional_field_stays_empty(), test_a_denied_readback_is_recorded_as_a_correction(), test_a_field_that_runs_out_of_attempts_is_abandoned_not_left_empty(), test_a_hang_up_at_the_read_back_ends_the_field_without_re_asking(), test_a_question_is_answered_and_does_not_count_as_an_attempt() (+17 more)

### Community 27 - "test_schema_loader.py"
Cohesion: 0.08
Nodes (11): built_pdf(), overlay(), schema(), test_a_field_missing_from_the_pdf_is_fatal(), test_a_widget_with_no_overlay_entry_is_fatal(), test_cross_field_dependencies_are_declared(), test_every_devanagari_option_name_is_one_the_hindi_prompt_says(), test_every_field_has_a_plain_language_prompt_and_gloss() (+3 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.09
Nodes (21): A. Form representation, A. The five-stage pipeline, B. Synthetic data and its construction, B. The validation gate and its rejection taxonomy, C. Adversarial evaluation corpora, C. Extraction as a structurally bounded model call, D. Evaluation harness and its honesty constraints, D. Read-back and the confirmation whitelist (+13 more)

### Community 29 - "test_adversarial.py"
Cohesion: 0.12
Nodes (7): _candidate(), committed(), gate(), test_adversarial_case(), test_every_case_declares_why_it_exists(), test_the_suite_covers_every_reason_code_the_gate_can_emit(), test_the_suite_has_controls_in_the_categories_that_need_them()

### Community 30 - "HelpAgent"
Cohesion: 0.18
Nodes (5): AnswerClient, HelpAgent, HelpAnswer, _question_lines(), emit()

### Community 31 - "voice.py"
Cohesion: 0.11
Nodes (6): FasterWhisperRecognizer, PiperSynthesizer, SpeechRecognizer, SpeechSynthesizer, VoiceBackendMissing, test_asking_for_a_missing_backend_says_how_to_install_it()

### Community 32 - "test_a_form_is_filled_over_the_voice_channel"
Cohesion: 0.22
Nodes (5): Transcript, test_a_form_is_filled_over_the_voice_channel(), read_back(), test_a_perfect_recogniser_loses_nothing(), transcribe()

### Community 33 - "HelpIndex"
Cohesion: 0.14
Nodes (9): _corpus_digest(), Embedder, HashEmbedder, HelpIndex, _normalise(), tokenize(), index(), test_an_index_built_with_another_embedder_is_refused() (+1 more)

### Community 34 - "corpus.py"
Cohesion: 0.15
Nodes (12): help_build(), Chunk, _clean(), _flat(), _html_text(), load_chunks(), load_manifest(), _pdf_text() (+4 more)

### Community 35 - "Extractor"
Cohesion: 0.11
Nodes (8): ModelReply, ExtractionOutcome, Extractor, test_a_replay_corpus_miss_still_raises(), test_every_persona_utterance_has_a_recorded_response(), test_replaying_an_out_of_enum_income_is_rejected_not_mapped(), test_replaying_p02_pan_yields_the_homoglyph_the_gate_then_rejects(), test_replaying_p03_pan_yields_a_question_then_a_value()

### Community 36 - "test_extraction_live.py"
Cohesion: 0.11
Nodes (10): build(), _clean_extraction(), write(), Intent, _has_credentials(), test_a_decline_is_not_extracted_as_a_value(), test_a_question_is_not_extracted_as_a_value(), test_a_spoken_identifier_is_transcribed() (+2 more)

### Community 38 - "extractor.py"
Cohesion: 0.27
Nodes (3): build(), build_user_message(), FieldSpec

### Community 39 - "Status"
Cohesion: 0.09
Nodes (14): Invariants — never break these (the test suite enforces them), Gotchas, Non-negotiables, _calling_module(), ConfirmationReceipt, Status, ValidationReport, 2. The gating contract — the thesis of the project (+6 more)

### Community 40 - "answer.py"
Cohesion: 0.11
Nodes (8): GeminiAnswerClient, _passages(), GeminiEmbedder, Hit, _hinted_delay(), json_config(), make_genai_client(), with_retries()

### Community 41 - "test_help.py"
Cohesion: 0.08
Nodes (16): HelpReply, ScriptedAnswerClient, reciprocal_rank_fusion(), agent(), chunks(), schema(), test_a_citation_to_a_passage_that_was_not_retrieved_falls_back(), test_a_cited_answer_is_spoken_with_its_source() (+8 more)

### Community 42 - "load"
Cohesion: 0.15
Nodes (8): load(), test_an_unknown_language_fails_with_a_useful_message(), test_every_field_has_a_spoken_label_in_this_language(), test_every_language_has_the_same_keys(), test_every_schema_field_has_a_prompt_and_gloss_in_this_language(), test_hindi_strings_are_actually_devanagari(), test_no_string_is_empty(), test_placeholders_match_across_languages()

### Community 43 - "load_all"
Cohesion: 0.14
Nodes (11): run_cmd(), load_sessions(), _personas(), load_all(), load_persona(), run_persona(), Session, record() (+3 more)

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
Cohesion: 0.06
Nodes (24): Settings, AnthropicExtractionClient, GeminiExtractionClient, make_client(), UnknownProvider, extractor(), client_with(), fake_sdk() (+16 more)

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

### Community 58 - "render_value"
Cohesion: 0.18
Nodes (7): render_value(), spell(), spell_email(), test_spell_groups_evenly_and_keeps_the_remainder(), test_spell_ignores_whitespace_in_the_source_value(), test_spell_without_grouping(), test_the_decode_is_the_exact_inverse_of_the_read_back()

### Community 59 - "M1. Implementation notes — instrumentation and corpus"
Cohesion: 0.33
Nodes (6): M1.1 Form structure is read from the document, not asserted, M1.2 The blank template carries no default values, M1.3 Instrumentation precedes the pipeline, M1.4 Corpus construction and its self-consistency checks, M1.5 The safety property is a test, not a claim, M1. Implementation notes — instrumentation and corpus

### Community 60 - "M6. Measurement"
Cohesion: 0.33
Nodes (6): M6.1 Analysis is separated from collection, M6.2 Which measures require ground truth, M6.3 The layered result, M6.4 Recall is reported with its false-positive rate, M6.5 Figures that are not measurements, M6. Measurement

### Community 61 - "Kind"
Cohesion: 0.15
Nodes (3): Kind, ConsoleChannel, VoiceTurn

### Community 62 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 63 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 64 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 66 - "load"
Cohesion: 0.14
Nodes (9): gate_check(), schema_show(), _inherited(), load(), load_overlay(), parse_acroform(), SchemaError, test_an_ambiguous_or_orphan_enum_name_is_fatal() (+1 more)

### Community 70 - "LucidForm — Specification"
Cohesion: 0.05
Nodes (34): AGENTS.md — handoff for any AI agent (Claude, Codex, Cursor, Gemini…) or new teammate, Code map, Run, What this is, Working rules for agents, Handing off to another AI, One-time setup, Per phase (+26 more)

### Community 72 - "get_settings"
Cohesion: 0.17
Nodes (7): get_settings(), build(), _header(), _overlay(), _blank_form_template(), personas(), schema()

### Community 75 - "graph.py"
Cohesion: 0.20
Nodes (8): Part B - Semantic extraction (parallel subagents), _build(), edges(), node_names(), _route(), _structure(), _Stub, test_the_graph_has_the_pipeline_stages_as_nodes()

### Community 78 - "test_gate.py"
Cohesion: 0.08
Nodes (19): Reason, candidate(), gate(), schema(), test_a_pass_carries_the_exact_value_that_will_be_written(), test_a_rejection_carries_nothing_committable(), test_an_optional_field_still_rejects_an_empty_value(), test_an_unknown_field_is_an_error_not_a_pass() (+11 more)

### Community 79 - "ScriptedClient"
Cohesion: 0.29
Nodes (3): ScriptedClient, test_a_question_is_logged_too(), test_extraction_is_logged_with_both_confidence_figures()

### Community 82 - "/graphify"
Cohesion: 0.17
Nodes (11): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, PowerShell 5.1: Vertical scrolling stops working (+3 more)

### Community 84 - "Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms"
Cohesion: 0.50
Nodes (3): A: Form No. 93 – PAN Application Form for Individual (Being citizen of India), FAQ's on PAN, Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms

### Community 85 - "ReplayClient"
Cohesion: 0.17
Nodes (6): extract_cmd(), _extraction_client(), ReplayClient, personas(), runs(), schema()

### Community 86 - "probe"
Cohesion: 0.18
Nodes (6): _category(), character_error_rate(), decode_spelled(), levenshtein(), probe(), test_character_error_rate_is_zero_for_an_exact_match()

### Community 87 - "M8. The help agent"
Cohesion: 0.33
Nodes (6): M8.1 Scope: explanation, never a value, M8.2 Corpus and chunking, M8.3 Hybrid retrieval, M8.4 The citation check, M8.5 Evaluation, and what it does not measure, M8. The help agent

### Community 89 - "report"
Cohesion: 0.18
Nodes (6): _pct(), percentile(), report(), test_percentile_of_nothing_is_none_not_zero(), test_percentiles_are_values_that_actually_occurred(), test_the_report_names_the_invariant()

### Community 91 - "LucidForm"
Cohesion: 0.20
Nodes (7): Commands, Conventions, Environment, graphify, LucidForm, Phase 3 notes, Phase 5 notes

### Community 94 - "write_tables"
Cohesion: 0.22
Nodes (7): SessionMetrics, _write_csv(), write_tables(), test_all_tables_are_written(), test_the_fields_table_records_ground_truth_beside_what_was_committed(), test_the_summary_is_a_single_row(), test_the_turns_table_has_one_row_per_turn()

### Community 95 - "aadhaar_valid"
Cohesion: 0.24
Nodes (6): aadhaar_valid(), synthetic_aadhaar(), test_generated_numbers_are_valid(), test_leading_zero_or_one_is_rejected(), test_wrong_length_is_rejected(), test_aadhaar_numbers_satisfy_verhoeff()

### Community 96 - "Progress log"
Cohesion: 0.33
Nodes (5): 2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5, 2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper, 2026-09-30 (night) · Shubh (+Claude) · Pre-push audit, 2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs, Progress log

### Community 97 - "test_graph.py"
Cohesion: 0.20
Nodes (4): golden(), test_commit_is_reachable_only_through_confirm(), test_persona_sessions_match_the_pre_langgraph_loop(), test_the_graph_draws_as_mermaid_for_the_paper()

### Community 98 - "Live demo — 5 minutes, terminal only"
Cohesion: 0.40
Nodes (4): Backup commands (if the network is slow), Live demo — 5 minutes, terminal only, Script — what to type, and what to point out, The one-line pitch while it runs

### Community 99 - "verhoeff_valid"
Cohesion: 0.22
Nodes (4): verhoeff_valid(), test_adjacent_transpositions_are_caught(), test_every_single_digit_substitution_is_caught(), test_non_digits_are_rejected_not_crashed()

### Community 101 - "LucidForm — Methodology"
Cohesion: 0.33
Nodes (5): LucidForm — Methodology, M7.1 Why replace a working loop, M7.2 Parity, not intuition, M7.3 No checkpoint-resume, M7. The orchestrator as a state graph

### Community 102 - "metrics.py"
Cohesion: 0.29
Nodes (3): FieldOutcome, outcome(), _truth()

## Knowledge Gaps
- **169 isolated node(s):** `2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5`, `2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs`, `2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper`, `2026-09-30 (night) · Shubh (+Claude) · Pre-push audit`, `M7.1 Why replace a working loop` (+164 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 766 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M8. The help agent`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Why does `Candidate` connect `Candidate` to `EventLog`, `test_confirm.py`, `test_gate_crossfield.py`, `cli.py`, `FormState`, `ValidationGate`, `.commit`, `test_voice.py`, `Title (pick one, or tell me to try again)`, `test_adversarial.py`, `Extractor`, `loader.py`, `extractor.py`, `Status`, `models.py`, `load`, `test_gate.py`, `probe`, `LucidForm`, `passing`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `LucidForm — Specification` connect `LucidForm — Specification` to `Status`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ValidationGate` (e.g. with `Candidate` and `Check`) actually correct?**
  _`ValidationGate` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Candidate` (e.g. with `Invariants — never break these (the test suite enforces them)` and `Conventions`) actually correct?**
  _`Candidate` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `FormState` (e.g. with `Event` and `EventLog`) actually correct?**
  _`FormState` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `2026-09-06 → 2026-09-07 · Shubh (+Claude) · Phases 0–5`, `2026-09-30 · Shubh (+Claude) · Gemini, LangGraph, help agent, safety test, team docs`, `2026-09-30 (evening) · Shubh (+Claude) · Phases 7–8: live evaluation + paper` to the rest of the system?**
  _169 weakly-connected nodes found - possible documentation gaps or missing edges._