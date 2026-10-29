# Files and processing steps

The figure's numbered Python scripts name processing stages. They are not a promise that one numbered box equals one source file.

| Figure step | Source functions | What is produced |
|---|---|---|
| A1-1 | `nova_cli.a1_request` | One model request containing the general prompt and separate exercise/offer blocks |
| A1 interpretation | `common1225.api` with `prompts/A1_Final.txt` | The model's structured interpretation |
| A1-2 | `runtime/app/a1/backend/interpretation.finalize`, `Scorer.for_empirica` | Checked terms, table-derived values, totals and messages |
| A2-1 job | `a2_extract.retrieval_text`, `stream._catalog`, `a2_extract.extract` | Retrieved issue definitions/options and the model request |
| A2 interpretation job | `prompts/A2_Interpretation.txt` plus `frozen/A2_Reading_Rules.json` | One Luna interpretation |
| A2-2 job | `a2_custom_rules.customize`, `a2_finalize.finalize` | Fitted interpretation, rule trace, and shared numerical scoring |
| A2-T1 tutorial | `stream._llm_extract_once` | The tutorial request and first interpretation |
| A2-T2 tutorial | `stream.llm_extract`, `_dense_offer_signal` | Whether the existing optional completeness read is made |
| A2-T3 tutorial | `stream.llm_extract`, `stream.score` | Merged interpretation, findings, and tutorial scoring |

## Exact instruction files

- `prompts/A1_Final.txt`: the same general prompt for A1-low and A1-high in both exercises.
- `prompts/A2_Interpretation.txt`: the concise fitted-job A2 interpretation prompt.
- `frozen/A2_Reading_Rules.json`: job-specific guidance sent in that same A2 request.
- `a2_custom_rules.py`: the fitted job Python interpretation rules, unchanged from the selected evaluated source.
- `prompts/A2_Tutorial_Standard.txt`: the literal existing standard tutorial instructions extracted from a saved request.
- `prompts/A2_Tutorial_Completeness.txt`: the literal existing second-pass instructions, also extracted from a saved request.
- `validation/Reference.txt`: instructions for drafting independent tutorial references.
- `validation/Checklist_Review.txt`: the final tutorial checklist-review instructions. Low-cost and advanced review use these same instructions, with different model/reasoning settings.
- `validation/Reference_Correction.txt`: the independent-reference instructions plus the reference-repair rules.
- `validation/Reference_Format.json` and `validation/Checklist_Format.json`: output schemas for those evaluation tasks.

The full model-facing job data are `frozen/A1_Exercise.json`, `frozen/A1_Scoring_Definitions.json`, and `frozen/Role_Materials.json`. The table used for numerical lookup is `frozen/Scoring_Table.json`; the requested A1 response schema is `frozen/SOURCE_FIRST_FORMAT.json`. Tutorial counterparts are in `frozen/tutorial/`.

## Historical source retained in the runtime

The frozen runtime contains older prompt files and routing code needed for traceability and imports. They are not automatically the selected experiment. The authoritative current A1 prompt is the top-level `prompts/A1_Final.txt`, not the older runtime prompt. The selected job A2 uses one Luna call, not the dormant Nano-to-Luna option in `scorer_routing.py`.

## Private data and keys

No participant-level benchmark, original offer, answer key, review workbook, API key or billing database is in this repository. The phrase dictionary is fitted matching configuration with origin annotations removed, not a table of participant observations. The private handoff maps the original records for authorized researchers.
