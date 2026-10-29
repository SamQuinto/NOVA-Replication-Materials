# Flowchart and implementation consistency

The edited Word figure is the text authority. Only the two approved headings and final-output bullets were changed. The other Word cells were compared before and after editing and left unchanged.

| Figure box | Executable implementation | What passes onward |
| --- | --- | --- |
| Python script A1-1 | `A1-1.py`, `prepare_request` | One JSON request with all active issue definitions |
| Advanced LLM | `nova_cli.py` calls `common1225.api` once | Structured interpretation, not assigned points |
| Python script A1-2 | `A1-2.py`, `score_interpretation` | Checked terms, researcher-defined scores and findings |
| Python script A2-1 | `A2-1.py`, `a2_extract.build_request` | One JSON request with retrieved issue definitions and reading rules |
| Economical LLM | `nova_cli.py` calls `common1225.api` once | Structured interpretation from Luna |
| Python script A2-2 | `A2-2.py`, `a2_finalize.finalize`, `a2_custom_rules.customize` | Fitted, checked and scored offer |

The LLM selects interpretations. A2's initial Python stage retrieves candidates; it does not decide each final interpretation by itself. Neither model call decides the assigned point values. Supporting quotations are checked, but a matching quotation does not prove semantic correctness.

The scoring table supplied to A1's model means the complete set of active definitions and options. Python retains the numerical scoring fields. Some role narratives mention illustrative points. Do not claim that every numerical point weight is included in the model-facing table or that the model never sees valuation information.

A valid complete offer may include unscored ideas. A clarification response can retain valid partial terms but withhold the final total. The revised last-box wording permits both cases. The server-side response can include both role totals; a participant interface should display only the values intended for that role.

The main diagram describes the current job A2 configuration: one Luna call, not an escalating Nano-to-Luna chain. Tutorial A2 remains a separate existing path and may make an additional Luna read. The evaluator and reference-review models are not live scoring stages.

The frozen agreement metadata has historical inconsistent flags: both a nonnegative-party flag and strict-positive comparison fields appear. The researcher's stated study rule was nonnegative scores. This release preserves the frozen historical files and scoring parity rather than silently changing experiment settings. The diagram ends with scoring output, not final agreement acceptance; do not use it as evidence that an agreement threshold is fully configured. Agreement decisions require a separately consistent deployment configuration.
