# Graph Report - LucidForm  (2026-09-30)

## Corpus Check
- 92 files · ~215,751 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .example 1, .jsonl 1)

## Summary
- 1535 nodes · 3373 edges · 81 communities (70 shown, 11 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 309 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2bb5570d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FieldSpec
- Event
- Candidate
- test_readback.py
- PersonaChannel
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
- test_session.py
- What You Must Do When Invoked
- models.py
- metrics.py
- pytest
- Purpose
- Extraction
- test_voice.py
- i18n/__init__.py
- ValidationGate
- test_personas.py
- one_field
- test_schema_loader.py
- Title (pick one, or tell me to try again)
- test_adversarial.py
- .commit
- voice.py
- personas
- test_help.py
- corpus.py
- HelpIndex
- Intent
- fixtures.py
- answer.py
- loader.py
- index.py
- build
- readback.py
- UnauthorizedIssuer
- with_retries
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
- .emit
- GeminiEmbedder
- M1. Implementation notes — instrumentation and corpus
- M6. Measurement
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- VoiceChannel
- Aggregate
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- LucidForm — Methodology
- Settings
- .claude/CLAUDE.md
- extraction-spec.md
- Reason
- Extractor
- Kind
- Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms
- personas.py
- uidai_faq_update.md
- 2. The gating contract — the thesis of the project

## God Nodes (most connected - your core abstractions)
1. `ValidationGate` - 57 edges
2. `FormState` - 51 edges
3. `Candidate` - 50 edges
4. `Event` - 46 edges
5. `Extraction` - 41 edges
6. `load()` - 41 edges
7. `EventLog` - 40 edges
8. `Status` - 38 edges
9. `FieldSpec` - 38 edges
10. `read_log()` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Three enforcement mechanisms` --references--> `ConfirmationReceipt`  [INFERRED]
  SPEC.md → lucidform/formstate/receipt.py
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

## Communities (81 total, 11 thin omitted)

### Community 0 - "FieldSpec"
Cohesion: 0.06
Nodes (34): enum_error(), format_error(), length_error(), normalize(), parse_date(), range_error(), strip_invisible(), FieldSpec (+26 more)

### Community 1 - "Event"
Cohesion: 0.13
Nodes (16): Event, read_log(), log(), test_a_second_log_on_the_same_session_appends(), test_dataclass_payloads_are_serialised(), test_enums_inside_payloads_become_their_values(), test_latency_is_null_when_unmeasured_not_zero(), test_records_are_appended_never_overwritten() (+8 more)

### Community 2 - "Candidate"
Cohesion: 0.07
Nodes (28): SilentWriteBlocked, Candidate, forge(), gate(), make(), state(), test_a_blocked_write_is_logged_as_an_event(), test_a_confirmed_value_is_written() (+20 more)

### Community 3 - "test_readback.py"
Cohesion: 0.15
Nodes (16): field(), render(), schema(), test_a_date_has_no_leading_zero_on_the_day(), test_a_date_is_spoken_readably_not_as_stored(), test_a_mobile_number_is_grouped_too(), test_a_pan_is_spelled_out_not_pronounced(), test_an_aadhaar_is_grouped_so_it_can_be_held_in_memory() (+8 more)

### Community 4 - "PersonaChannel"
Cohesion: 0.06
Nodes (19): Commands, Conventions, Environment, graphify, LucidForm, Non-negotiables, Phase 3 notes, Phase 4 notes (+11 more)

### Community 5 - "SessionGraph"
Cohesion: 0.06
Nodes (19): _build(), edges(), mermaid(), node_names(), _route(), SessionGraph, _structure(), _Stub (+11 more)

### Community 6 - "test_i18n.py"
Cohesion: 0.11
Nodes (13): load(), Strings, test_a_missing_key_raises_rather_than_falling_back(), test_a_missing_placeholder_raises_with_the_key_named(), test_an_unknown_language_fails_with_a_useful_message(), test_every_field_has_a_spoken_label_in_this_language(), test_every_language_has_the_same_keys(), test_every_schema_field_has_a_prompt_and_gloss_in_this_language() (+5 more)

### Community 7 - "Status"
Cohesion: 0.11
Nodes (17): Status, candidate(), test_a_pass_carries_the_exact_value_that_will_be_written(), test_a_pass_must_not_carry_a_reason(), test_a_rejection_carries_nothing_committable(), test_a_rejection_must_carry_a_reason(), test_an_optional_field_still_rejects_an_empty_value(), test_an_unknown_field_is_an_error_not_a_pass() (+9 more)

### Community 8 - "test_confirm.py"
Cohesion: 0.08
Nodes (15): confirm(), normalize_utterance(), gate(), passing(), test_a_confirmation_issues_a_receipt(), test_a_denial_issues_no_receipt(), test_a_spoofed_confirmation_issues_no_receipt(), test_a_stale_report_issues_no_receipt() (+7 more)

### Community 9 - "test_gate_crossfield.py"
Cohesion: 0.10
Nodes (17): check(), CrossFieldResult, pan_matches_surname(), pin_matches_confirmed_state(), _skipped(), pin_matches_state(), test_a_check_with_an_unconfirmed_dependency_is_skipped_not_passed(), test_a_state_with_no_region_data_is_not_checked() (+9 more)

### Community 10 - "test_metrics.py"
Cohesion: 0.06
Nodes (15): agg(), runs(), schema(), sessions(), test_a_question_and_the_answer_after_it_are_separate_turns(), test_nothing_wrong_was_committed(), test_offline_sessions_are_flagged_as_not_measuring_accuracy(), test_recall_and_false_positive_rate_are_both_reported() (+7 more)

### Community 11 - "cli.py"
Cohesion: 0.10
Nodes (21): asr_probe_cmd(), extract_cmd(), _extraction_client(), gate_check(), graph_cmd(), _help_agent(), help_ask(), make_form_cmd() (+13 more)

### Community 12 - "FormState"
Cohesion: 0.08
Nodes (19): FormState, export(), ExportError, read_back(), commit(), gate(), schema(), template() (+11 more)

### Community 13 - "test_extraction.py"
Cohesion: 0.11
Nodes (22): extractor(), gate(), replay(), schema(), test_a_decline_never_becomes_a_candidate(), test_a_loose_match_reports_no_span_rather_than_a_wrong_one(), test_a_question_never_becomes_a_candidate(), test_a_quote_from_the_utterance_grounds() (+14 more)

### Community 14 - "asr_probe.py"
Cohesion: 0.09
Nodes (15): _category(), character_error_rate(), decode_spelled(), is_simulated(), levenshtein(), probe(), ProbeResult, ProbeSummary (+7 more)

### Community 15 - "test_session.py"
Cohesion: 0.09
Nodes (13): personas(), runs(), schema(), test_a_declined_optional_field_stays_empty(), test_a_question_is_handled_mid_session(), test_endless_questions_are_bounded(), test_every_field_is_resolved(), test_no_committed_value_differs_from_ground_truth() (+5 more)

### Community 16 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

### Community 17 - "models.py"
Cohesion: 0.12
Nodes (7): ConfirmationReceipt, Affirmation, fingerprint(), ValidationReport, parse_affirmation(), 4. Data model, test_receipts_cannot_be_minted_outside_the_confirmation_module()

### Community 18 - "metrics.py"
Cohesion: 0.08
Nodes (17): FieldOutcome, _is_correct(), load_sessions(), parse_session(), outcome(), _pct(), _personas(), report() (+9 more)

### Community 19 - "pytest"
Cohesion: 0.15
Nodes (9): _imported_names(), _parse(), _python_files(), _rel(), test_decision_and_write_paths_import_no_model(), test_forbidden_import_detection_works(), test_private_form_state_is_not_touched_from_outside(), test_receipts_are_minted_only_by_the_confirmation_module() (+1 more)

### Community 20 - "Purpose"
Cohesion: 0.15
Nodes (4): Purpose, ConsoleChannel, test_a_form_is_filled_over_the_voice_channel(), read_back()

### Community 21 - "Extraction"
Cohesion: 0.11
Nodes (12): ScriptedClient, check(), clamp_confidence(), Grounding, locate(), _loose(), Extraction, test_a_model_reporting_impossible_confidence_is_clamped() (+4 more)

### Community 22 - "test_voice.py"
Cohesion: 0.16
Nodes (11): CorruptingRecognizer, EchoRecognizer, SilentSynthesizer, test_an_empty_transcript_is_an_unusable_answer_not_a_hang_up(), test_asr_confidence_is_recorded_but_never_reaches_the_gate(), test_audio_events_are_logged_on_both_sides(), test_corrupted_identifiers_are_classified_and_offered_to_the_gate(), test_no_audio_ends_the_field_rather_than_being_read_as_consent() (+3 more)

### Community 23 - "i18n/__init__.py"
Cohesion: 0.18
Nodes (3): available(), MissingString, test_both_languages_are_available()

### Community 24 - "ValidationGate"
Cohesion: 0.11
Nodes (4): ValidationGate, gate(), gate(), schema()

### Community 25 - "test_personas.py"
Cohesion: 0.06
Nodes (23): aadhaar_valid(), corrupt_one_digit(), synthetic_aadhaar(), verhoeff_check_digit(), verhoeff_valid(), test_adjacent_transpositions_are_caught(), test_check_digit_completes_a_payload(), test_check_digit_rejects_non_numeric_payload() (+15 more)

### Community 26 - "one_field"
Cohesion: 0.13
Nodes (16): one_field(), test_a_confirmed_value_is_committed(), test_a_denied_readback_is_recorded_as_a_correction(), test_a_field_that_runs_out_of_attempts_is_abandoned_not_left_empty(), test_a_hang_up_at_the_read_back_ends_the_field_without_re_asking(), test_a_question_is_answered_and_does_not_count_as_an_attempt(), test_a_rejected_value_is_explained_in_the_gates_own_words(), test_a_spoofed_confirmation_does_not_commit() (+8 more)

### Community 27 - "test_schema_loader.py"
Cohesion: 0.05
Nodes (19): Gotchas, _inherited(), load_overlay(), parse_acroform(), SchemaError, build(), _header(), _overlay() (+11 more)

### Community 28 - "Title (pick one, or tell me to try again)"
Cohesion: 0.10
Nodes (19): A. Form representation, A. The five-stage pipeline, B. Synthetic data and its construction, B. The validation gate and its rejection taxonomy, C. Adversarial evaluation corpora, C. Extraction as a structurally bounded model call, D. Evaluation harness and its honesty constraints, D. Read-back and the confirmation whitelist (+11 more)

### Community 29 - "test_adversarial.py"
Cohesion: 0.12
Nodes (8): _candidate(), committed(), gate(), test_adversarial_case(), test_every_case_declares_why_it_exists(), test_gate_never_raises_on_hostile_input(), test_the_suite_covers_every_reason_code_the_gate_can_emit(), test_the_suite_has_controls_in_the_categories_that_need_them()

### Community 30 - ".commit"
Cohesion: 0.17
Nodes (4): CommitRecord, DeclineRecord, block(), _now()

### Community 31 - "voice.py"
Cohesion: 0.09
Nodes (9): FasterWhisperRecognizer, PiperSynthesizer, SpeechRecognizer, SpeechSynthesizer, Transcript, VoiceBackendMissing, test_a_perfect_recogniser_loses_nothing(), transcribe() (+1 more)

### Community 33 - "test_help.py"
Cohesion: 0.09
Nodes (15): HelpReply, ScriptedAnswerClient, reciprocal_rank_fusion(), agent(), chunks(), schema(), test_a_citation_to_a_passage_that_was_not_retrieved_falls_back(), test_a_cited_answer_is_spoken_with_its_source() (+7 more)

### Community 34 - "corpus.py"
Cohesion: 0.16
Nodes (11): help_build(), _clean(), _flat(), _html_text(), load_chunks(), load_manifest(), _pdf_text(), _read() (+3 more)

### Community 35 - "HelpIndex"
Cohesion: 0.20
Nodes (7): Chunk, _corpus_digest(), Embedder, HelpIndex, index(), test_an_index_built_with_another_embedder_is_refused(), test_the_index_round_trips_through_disk()

### Community 36 - "Intent"
Cohesion: 0.12
Nodes (7): Intent, extractor(), _has_credentials(), test_a_decline_is_not_extracted_as_a_value(), test_a_question_is_not_extracted_as_a_value(), test_a_spoken_identifier_is_transcribed(), test_the_model_cannot_return_anything_outside_the_schema()

### Community 37 - "fixtures.py"
Cohesion: 0.27
Nodes (4): build(), _clean_extraction(), write(), test_the_fixture_corpus_is_in_sync_with_its_generator()

### Community 38 - "answer.py"
Cohesion: 0.16
Nodes (7): AnswerClient, HelpAgent, HelpAnswer, _passages(), _question_lines(), emit(), Hit

### Community 39 - "loader.py"
Cohesion: 0.14
Nodes (5): InputChannel, OutputChannel, EventLog, Session, test_the_fakes_satisfy_the_channel_protocols()

### Community 40 - "index.py"
Cohesion: 0.18
Nodes (3): HashEmbedder, _normalise(), tokenize()

### Community 41 - "build"
Cohesion: 0.29
Nodes (4): build(), build_user_message(), test_enum_prompts_forbid_substituting_the_nearest_option(), test_prompt_carries_the_field_but_asks_for_no_judgement()

### Community 42 - "readback.py"
Cohesion: 0.15
Nodes (9): render(), render_value(), spell(), spell_email(), test_spell_groups_evenly_and_keeps_the_remainder(), test_spell_ignores_whitespace_in_the_source_value(), test_spell_without_grouping(), test_the_hindi_readback_frame_is_used_for_hindi() (+1 more)

### Community 43 - "UnauthorizedIssuer"
Cohesion: 0.17
Nodes (6): _calling_module(), UnauthorizedIssuer, _mint_as_issuer(), test_the_helper_really_does_bypass_the_issuer_check(), test_the_receipt_refuses_a_failed_validation(), test_the_receipt_refuses_a_non_explicit_affirmation()

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

### Community 49 - "_check"
Cohesion: 0.22
Nodes (5): _check(), test_an_empty_dependency_counts_as_unconfirmed(), test_skipping_lets_the_value_through_but_records_the_skip(), test_structural_failures_are_reported_before_cross_field_ones(), test_the_same_value_is_rejected_once_the_dependency_is_confirmed()

### Community 50 - "Prompt for Claude Code — LucidForm Prototype"
Cohesion: 0.29
Nodes (6): Context, How I want you to work with me, Non-negotiable design constraint, Prompt for Claude Code — LucidForm Prototype, Scope for THIS prototype (deliberately small), What I need from you, in order

### Community 51 - "test_llm_clients.py"
Cohesion: 0.11
Nodes (16): AnthropicExtractionClient, GeminiExtractionClient, make_client(), UnknownProvider, client_with(), fake_sdk(), FakeModels, rate_limited() (+8 more)

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

### Community 66 - "VoiceChannel"
Cohesion: 0.24
Nodes (3): VoiceChannel, VoiceTurn, test_the_module_imports_without_any_speech_library()

### Community 67 - "Aggregate"
Cohesion: 0.11
Nodes (4): Aggregate, percentile(), test_percentile_of_nothing_is_none_not_zero(), test_percentiles_are_values_that_actually_occurred()

### Community 72 - "Settings"
Cohesion: 0.29
Nodes (3): Settings, test_sdk_key_variables_are_read_without_the_project_prefix(), test_the_default_provider_is_gemini_and_the_model_is_config()

### Community 78 - "Reason"
Cohesion: 0.15
Nodes (4): Check, Reason, test_check_order_covers_the_whole_taxonomy(), test_check_order_is_the_documented_sequence()

### Community 79 - "Extractor"
Cohesion: 0.08
Nodes (9): ExtractionClient, ModelReply, ReplayClient, ExtractionOutcome, Extractor, test_every_persona_utterance_has_a_recorded_response(), test_replaying_an_out_of_enum_income_is_rejected_not_mapped(), test_replaying_p02_pan_yields_the_homoglyph_the_gate_then_rejects() (+1 more)

### Community 80 - "Kind"
Cohesion: 0.15
Nodes (4): Kind, Puppet, StubHelper, test_a_question_is_answered_by_the_help_agent_and_never_becomes_a_value()

### Community 84 - "Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms"
Cohesion: 0.50
Nodes (3): A: Form No. 93 – PAN Application Form for Individual (Being citizen of India), FAQ's on PAN, Form No. 93/94/95/96 - Frequently Asked Questions (FAQs) on PAN Forms

### Community 85 - "personas.py"
Cohesion: 0.17
Nodes (4): __iter__(), Persona, PersonaError, test_a_persona_with_no_utterances_is_rejected()

### Community 96 - "2. The gating contract — the thesis of the project"
Cohesion: 0.67
Nodes (3): 2. The gating contract — the thesis of the project, Commit invariant, Three enforcement mechanisms

## Knowledge Gaps
- **121 isolated node(s):** `graphify`, `Usage`, `What graphify is for`, `Step 0 - GitHub repos and multi-path merge (only if a URL or several paths)`, `Step 1 - Ensure graphify is installed` (+116 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 659 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `4. Data model` connect `models.py` to `FieldSpec`, `Candidate`, `FormState`, `PersonaChannel`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Why does `LucidForm — Specification` connect `PersonaChannel` to `2. The gating contract — the thesis of the project`, `models.py`, `LucidForm — Methodology`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Why does `LucidForm — Methodology` connect `LucidForm — Methodology` to `M0. System design`, `M2. The validation gate`, `M3. The write path`, `M4. Extraction`, `M5. Orchestration and read-back`, `M1. Implementation notes — instrumentation and corpus`, `M6. Measurement`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `ValidationGate` (e.g. with `asr_probe_cmd()` and `extract_cmd()`) actually correct?**
  _`ValidationGate` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `FormState` (e.g. with `run_cmd()` and `ReplayRun`) actually correct?**
  _`FormState` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Candidate` (e.g. with `Conventions` and `A. The five-stage pipeline`) actually correct?**
  _`Candidate` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Event` (e.g. with `VoiceChannel` and `parse_session()`) actually correct?**
  _`Event` has 30 INFERRED edges - model-reasoned connections that need verification._