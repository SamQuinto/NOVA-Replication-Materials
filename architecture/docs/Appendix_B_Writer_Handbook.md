# NOVA technical architecture and implementation

## What this handbook is for

This handbook gives an appendix writer the details needed to explain NOVA without reconstructing old conversations. The complete single-file handoff is `LLM_Architecture_Dump.txt` at the architecture-folder root. All implementation paths in that file are relative to this folder, wherever it is placed. Participant-level evidence remains private and is not embedded in the public handoff.

The key distinction is simple. The language model decides **what the negotiator proposed**. Python scripts decide **what that interpreted proposal is worth under the researcher's scoring table**. A perfectly formed JSON response can still misunderstand an offer, so the second step does not remove the need to validate the first.

The current labels are A1 for the general-prompt, stronger-model architecture and A2 for the lower-cost, exercise-customized architecture. Earlier project records used these labels the other way around. Do not combine older accuracy tables with the current names without checking their configuration.

## A suggested structure for Appendix B

1. Explain the shared interpretation-and-scoring flow.
2. Describe the files the researcher prepares and the objects created at run time.
3. Walk through A1, including its single model call and subsequent Python checks.
4. Walk through the fitted A2 job scorer, including issue selection and custom rules.
5. Explain the separate existing A2 tutorial path and its optional completeness call.
6. Explain numerical scoring, missing details, new ideas, and role-specific display.
7. Describe how an exercise can be changed and what must be validated again.
8. Close with practical replication instructions and the limits of the evaluation.

Use the manuscript's final appendix lettering. This package does not renumber the manuscript. Detailed validation belongs wherever the final manuscript places that material, even though enough information is included here to explain the implementation correctly.

## The shared flow

A negotiator types an offer. The application supplies the offer text and the negotiator's recorded role. It can also supply a previous offer as context. The request includes instructions, role materials, and the relevant view of the scoring table. The language model returns a structured interpretation. Python checks the returned choices against the configured exercise, looks up the values for each role, and prepares a scored response or a useful request for clarification.

Consider a synthetic example: “Salary 52k; work-expense budget 8 grand; start 1 May; 35 vacation days.” The model should identify the named issues and normalize the stated quantities. It should not invent health insurance or a company car just because these would be plausible employment terms. Python then evaluates the interpreted values using the table. It does not ask the model to decide how many points a salary or vacation allowance deserves.

The exercise information matters. “35 days” might be annual leave in one exercise and an implementation deadline in another. A1 is designed to obtain these meanings and conventions from the files, rather than embedding the job exercise's issue names and numerical defaults in its general prompt. This is an intended design advantage, not proof that it will transfer perfectly to every exercise.

## Files, text blocks, and JSON objects are different things

The researcher prepares files on the server. The Python runner reads those files and puts their contents into an API request. The model is not browsing the researcher's computer, opening a OneDrive path, or following a hyperlink to fetch a scoring table.

JSON is a structured text format. It can be saved in a `.json` file, but it can also exist only in memory as part of a request or response. An “Interpretation (JSON)” box in a figure therefore does not mean the application must create a separate disk file at every step.

For A1, one request contains several named text blocks. There is still one interpretation call. Four developer-message blocks and one user-message block are not five separate model calls, and the response schema is not a second prompt asking another model to score the result.

| Object | Where it comes from | What it contains | What happens to it |
|---|---|---|---|
| Current offer | Negotiator and application | Original text and recorded proposer role | Sent in the changing user-message object |
| Previous offer | Application, when available | Earlier text that may help resolve an explicit reference | Sent as context; not permission to copy all earlier terms |
| Exercise information | Researcher file | Exercise title, roles, required issues, and outside-table policy | Added to the request as named data |
| Role materials | Researcher file | Narrative context about the negotiators and exercise | Added as context, not as extra proposed terms |
| Scoring-table definitions | Derived from the scoring table | Issue meanings, option labels, units, domains, defaults and aliases | Read by the model to interpret offers |
| Full numerical scoring table | Researcher file | The configured options or scoring functions and each role's scores | Used by Python to assign scores |
| General prompt | Text file | Instructions for interpreting words and handling uncertainty | Sent to the model |
| Response format | JSON-schema file or schema object | Allowed fields, types and issue-name boundaries | Supplied through the API's structured-output setting |
| Interpretation | Model response | Selected issues/options, quotes, questions and unpriced ideas | Checked by Python |
| Scored offer | Python result | Valid terms, role-specific values, totals where appropriate, and messages | Adapted for the interface and recorded |

The model-facing table removes numerical point-weight fields. However, role narratives may describe example points, and the model can receive those narratives. Do not say that the model never sees any valuation information. The accurate claim is that Python, not a model-generated point estimate, determines the scored result.

## A1 step by step

### Python script A1 1 prepares one request

The runner reads `prompts/A1_Final.txt`. It reads the exercise information, all active issue/option definitions, role materials, and output schema from the selected exercise folder. It combines those contents with the current offer, proposer role, and optional previous-offer text.

The request uses the following names consistently:

- `EXERCISE_INFORMATION`
- `SCORING_TABLE`
- `ROLE_MATERIALS`
- `CURRENT_OFFER`, with `proposer_role` and `text`
- `PREVIOUS_OFFER`, with `text`

The JSON response format is supplied in the request's `text.format` setting. The public runner preserves the evaluated layout: the general prompt comes first, followed by the stable exercise blocks, followed by the changing offer object. This arrangement also allows repeated prefixes to benefit from provider-side caching.

All active issue definitions and available choices are included. No researcher chooses the offer's issues by hand, and this A1 path does not use an initial low-cost model to shortlist issues. The advanced model selects the issues and options during interpretation.

The figure label “Python script A1-1” now corresponds to the actual runnable file `A1-1.py`. Its `prepare_request` function is called by `nova_cli.py`. The other numbered boxes likewise correspond to `A1-2.py`, `A2-1.py` and `A2-2.py`.

### The advanced LLM interprets the offer

The evaluated model is OpenAI `gpt-6.1-sol`, with either low or high reasoning effort. Both settings use the same general prompt and exercise inputs. The latest main spreadsheet omits extra-high at the researcher's request. Extra-high records exist historically but must not be mixed into the selected three-configuration comparison.

The model's job is to read the words naturally, identify supported issues, choose the matching options or normalized values, and provide source quotations. It should tolerate ordinary spelling mistakes, shorthand, lists, and varied punctuation. It should ask about a genuinely missing essential detail, retain an unrepresentable idea without points, and avoid introducing an optional issue the negotiator did not propose.

“Reasoning effort” is an API setting, not an extra reviewer call. The returned interpretation does not contain the model's private internal reasoning. It contains the structured result, supporting quotes, and brief interpretation notes requested by the schema.

### The returned interpretation is JSON

The main fields are:

| Field | Meaning |
|---|---|
| `pairs` | Proposed issue and option/value selections |
| `source_text` within a pair | Words copied from the offer supporting that selection |
| `from_previous_offer` | Whether a retained term came from explicitly referenced prior context |
| `ambiguities` | An issue, supporting words, and a short clarification question |
| `novel_terms` | Meaningful ideas the scoring table cannot represent |
| `unsupported_terms` | Other explicitly recognized material that was not priced |
| `offer_intent` | Whether the text is an offer, genuinely uncertain, or not an offer |
| `explicit_reference` | Current wording that refers to earlier terms |
| `interpretation_notes` | Brief explanation of useful normalization or context |

An illustrative pair would be `{"issue":"Salary","option":"52000","source_text":"Salary 52k","from_previous_offer":false}`. This is an example of the object, not an archived participant response.

### Python script A1 2 checks and scores the interpretation

The generic `interpretation.finalize` function is the important boundary. It checks that the configured exercise has two roles and that the proposer role is valid. It checks known issue names and duplicate choices. It checks whether the source quotation appears in the appropriate current or previous text. A prior quotation is permitted only when a valid explicit reference supports inheritance.

For each accepted pair, `offer_engine.score_pair` normalizes the option and obtains the configured value for the proposer and the other role. Non-finite values and invalid choices are not assigned arbitrary points. Python records a finding and requests clarification instead. It also checks for missing required issues, inappropriate outside-table terms under a fixed-issue policy, and a genuinely non-offer input.

If no blocking finding remains, the generic path sums the issue values. If clarification is needed, it retains the valid partial interpretation but does not present a final complete-offer total in the same way as an accepted complete package. The adapter prepares the fields expected by the interface.

This is not a second semantic model. A quoted phrase can still be misunderstood, so quote checking alone cannot establish that an issue or option is correct. It is a useful constraint, not an independent proof of meaning.

## The fitted A2 job scorer step by step

### Python script A2 1 selects possible issues and prepares the request

A2 uses the exercise's issue names, aliases and fitted wording vocabulary to retrieve likely relevant entries before the model sees the table. The three required job issues remain available. Retrieval supplements the text with a close spelling match when there is a clear single vocabulary match. It does not supply a missing numerical value.

The researcher designs the scoring table and reading rules. The researcher does not manually select the issue set separately for every participant offer. Python performs the candidate retrieval, and the LLM chooses among the supported issues and options it receives.

`A2-1.py` calls `a2_extract.build_request`. The helper's `retrieval_text` and the existing stream module's `_catalog` prepare the selected definitions and choices. The prepared request combines the current offer, previous-offer context, proposer role, selected scoring-table entries, role materials, and `frozen/A2_Reading_Rules.json`. The general A2 interpretation instructions are in `prompts/A2_Interpretation.txt`. The API call happens after this preparation step, through the runner and shared API client.

The reading-rules JSON is part of the same request. It is not a second call, a hidden trained model, or a separate negotiator message.

### The economical LLM returns the interpretation

The latest evaluated job configuration uses `gpt-5.6-luna` at low reasoning. It makes one interpretation call. The model sees the retrieved issue entries and exact allowed issue names, quotes the supporting words, and returns an interpretation in JSON.

Do not use the old Nano-to-Luna figure for this configuration. Earlier code retains an escalation option, but its presence in an archived module does not mean it was used in the reported final job evaluation.

### Python script A2 2 applies the fitted rules and scores the result

`A2-2.py` calls `a2_finalize.finalize`, which converts the extraction to the shared validation format and calls `a2_custom_rules.customize`. The custom rules are intentionally exercise-specific. They identify recurrent wording and interpretation problems, change supported pairs, retain unclear ideas or add a relevant question, and record which rule fired.

The final job scorer does not simply rerun every old lexical rejection rule after the model. The refined path removed the older second lexical parser from this step. It then uses the shared evidence/domain checks and numerical lookup. This matters because a correctly interpreted phrase should not be thrown away just because a second regular expression failed to anticipate its wording.

The resulting object includes a `custom_rule_trace`. This makes a repair inspectable: a reader can see the rule name, issue and source wording rather than receiving an unexplained altered score.

The job exercise's A2 result is fitted development evidence. Its final deterministic rules were applied to saved model interpretations. That is valid evidence that the saved interpretations can be handled by the final rules. It is not a fresh untouched holdout proving that every future model response will be correct.

## What customization means in practice

Customization here means editing prompts, reading guidance, vocabulary, or deterministic interpretation rules. It is **not** fine-tuning a model's weights. No model fine-tuning is established by these records.

The job reading rules are grouped by problem: units and shorthand; reference anchors versus hard limits; relative allowances; dates; exact amounts and alternatives; benefit defaults; who performs a duty; staged changes and contingencies; explicit references to prior offers; reasonable idea coverage; company publicity; unmatched ideas; neighboring issue scope; incomplete headings; and exact evidence.

The Python file contains the actual fitted rules. Examples below are synthetic illustrations of their purpose, not new validation findings:

| Problem | Illustrative wording | Intended handling |
|---|---|---|
| Attached units or typos | “0days remote” | Read zero weekly remote days, not a missing number |
| A usual allowance is explicitly changed | “five more vacation days than usual” | Apply the exercise's stated usual value, not an invented baseline |
| A later total replaces an initial amount | “Salary 45k, becoming 50k after six months' probation” | Use the defined staged-total convention, retain probation, and avoid double-counting a pay rise |
| Related but different issues | “A training budget of $800” | Match the professional-development budget, not automatic training-program participation |
| Direction of a duty | “We will help with the recruitment fair” | Use the proposer's role and the exercise's duty definitions |
| Unpriced imaginative request | “Put an aquarium in the interview room” | Retain the proposal without inventing a salary or office allowance |
| A prior package is explicitly retained | “Keep the rest, but change salary to 52k” | Carry only the terms covered by that reference and apply the stated change |

A useful development workflow is to record the failure, identify its broader cause, decide the intended handling, change the smallest appropriate component, and add contrasting tests. If a repair handles “no remote days,” also test positive days, negation, attached units, a different issue order, and a request about a different issue. A fix should not award a feature merely because its keyword appeared inside a different request.

Before publishing a rule, ask whether it depends on a participant/case identifier. The fitted rule files operate on text, role, prior context and exercise definitions, not validation row IDs. This does not eliminate overfitting: a rule can still be very closely fitted to wording seen during development.

## The existing A2 tutorial path is separate

The tutorial is a community-event venue negotiation. Its table has nine issues: Venue fee, Event date, Closing time, Projector, Cleanup, Cancellation notice, Setup access, Door staffing, and Food and refreshments. The first three are required. The internal `Candidate` slot is the Organizer and `Recruiter` slot is the Venue Manager. These are interface role identifiers, not job-offer roles in this exercise.

The as-is tutorial comparison used the existing `stream.llm_extract` and `stream.score` functions with Luna at low reasoning. It did not apply the job-specific `a2_custom_rules.py` patch to tutorial inputs. The existing tutorial path can make a second Luna call when `_dense_offer_signal` identifies a dense offer. The second call is an independent completeness read of the same original offer and relevant context, not a reviewer that sees and edits the first answer. Python merges the two interpretations and notes disagreements.

The literal standard and completeness prompts are saved separately. The legacy tutorial prompt still contains some job-specific examples and instructions inherited from the shared code. That is part of the as-is implementation, not a recommended clean generic prompt. The new figures must not suggest that this path is identical to the fitted one-call job A2 scorer.

The 731-input tutorial run found weaknesses in that existing path: omitted or unnecessarily queried fees and times, missed early access or refreshments, and an unrelated “NDA” acknowledgement in some inputs. Report the observed results rather than borrowing the fitted job scorer's 100% development figure. No tutorial scorer was tuned on the new test during this comparison.

## Numerical scoring and feasibility

For discrete issues, Python retrieves the score assigned to the chosen option. For numerical issues, it follows the exercise's declared interpolation, extrapolation and permitted domain. A reference scoring anchor is not automatically a proposal limit. A date is parsed as a date, not passed blindly into a floating-point currency calculation.

The job exercise deliberately permits continuous values for several issues. Some are bounded by meaningful constraints, such as no more than five remote working days in a five-day working week or 365 vacation days in a year. Others can extend beyond scoring anchors. Do not generalize this to “there are no limits on anything.”

The job starting-date convention and post-September failure rule are exercise choices. They are not universal properties of NOVA. Read their exact implementation from the frozen table and scoring code before describing their numerical curve. A good architecture explanation distinguishes interpretation, numerical valuation, submission eligibility, and agreement acceptance; these need not be the same rule.

The researcher previously clarified that agreement at zero can be valid. Some archived scenario material still contains positive-threshold submission or acceptance wording. Do not claim that every historical application path implements the same zero rule. Inspect the actual `proposal_rules`, `agreement_rules`, and frontend behavior for the deployment being described. This replication release does not change those rules.

## What a negotiator sees

The scored object can contain internal information for both roles so the server can prepare each person's private display. That does not mean the proposer should see the other role's private score. The experimental application controls which fields are displayed to whom.

For the tutorial review workbook, “Scorer Output” collects the saved breakdown, findings and unpriced terms, including partial breakdowns that an older rejection display may hide. It is not a screenshot reconstruction of what Empirica displayed. A writer should not infer the exact participant interface from these internal review cells alone.

## Accuracy and what it does not mean

The selected primary measure checks two error types. Type A is a meaningful idea missed, or a clear supported choice left unscored without a genuine reason. Useful clarification can pass when a necessary detail is missing, choices conflict, a value cannot be represented, or the parties in the proposal are genuinely unclear. Acknowledgement without points can pass for an idea the table cannot represent. Type B is a genuinely unproposed issue added, whether priced or raised as an optional issue in a question or acknowledgement. Required-issue reminders are permitted.

A wrong option, quantity, provider or value on an issue that was genuinely raised is a separate mapping check. It is not automatically Type B. Consequently, high A/B accuracy must not be described as complete verification of all numerical scores or mappings. The tutorial's additional mapping flags are provisional and have not had the same assistant review as the A/B labels.

The initial 1,000-case benchmark and its older accuracy tables were part of development. The selected current job table has 1,225 inputs, and the new tutorial table has 731 retained inputs. Do not add old overlapping samples together or call them an independent combined holdout. The private files preserve their source history.

## The selected results

| Exercise | Configuration | Primary passes | Type A | Type B | Estimated API cost per 1,000 offers | Mean API scoring time |
|---|---|---:|---:|---:|---:|---:|
| Job development set | A1-low | 1,224/1,225 | 1 | 0 | US$5.74–5.79 | 4.45 s |
| Job development set | A1-high | 1,225/1,225 | 0 | 0 | US$9.51–9.58 | 10.16 s |
| Job fitted evaluation | A2 | 1,225/1,225 | 0 | 0 | US$2.39–2.90 | 3.81 s |
| New tutorial inputs | A1-low | 730/731 | 1 | 0 | US$2.95–2.99 | 4.20 s |
| New tutorial inputs | A1-high | 730/731 | 1 | 0 | US$7.02–7.06 | 12.09 s |
| New tutorial inputs | Existing A2 tutorial path | 579/731 | 146 | 9 | US$0.74–0.82 | 3.77 s |

Tutorial A1 accuracy is 99.86%, with an offer-level Wilson 95% interval of 99.23%–99.98%. Tutorial A2 accuracy is 79.21%, with interval 76.12%–81.99%. Three tutorial A2 inputs have both A and B errors, so the error columns must not simply be added to count failed inputs.

The tutorial inputs came from 134 participants. Repeated and related submissions remain after exact/formatting-only deduplication, so offer-level confidence intervals are not participant-cluster-adjusted population estimates. The job set deliberately retained duplicate human offers; only 1,089 role/text/context requests were distinct in the archived run. Its headline counts describe all 1,225 retained input records.

## Cost and time should be reported with assumptions

A request is billed for tokens rather than for an offer as such. Estimate its cost from uncached input tokens, cached input tokens, and output tokens using the selected rate card. Output usage can include reasoning tokens billed by the provider. Sum all calls needed to score that input; a two-call tutorial A2 input is not a one-call cost.

To obtain cost per 1,000 offers, sum the per-input scoring costs, divide by the number of retained inputs, and multiply by 1,000. Keep reference-key and evaluator-model costs separate from scoring costs. Count an actual call once when reporting total experimental spend, even if its identical response was reused in more than one retained record. The tutorial per-offer estimate prices fourteen reused A2 calls normally, so it does not assume free application-level response reuse in production.

The tutorial run used standard per-million-token rates of US$2 input, US$0.10 cached input, US$10 output for Sol, and US$0.20 input, US$0.02 cached input, US$1.20 output for Luna. The upper estimate treats uncached input as potentially subject to a 1.25 cache-write rate. Actual account invoices were not reconciled here. Historical main-run cost summaries use their archived accounting assumptions; do not silently treat every historical estimate as an invoice or a uniformly repriced comparison.

Provider-side caching is different from omitting data from the request. The full definitions are still included. Repeated stable prefixes may be processed at a lower cached-input rate. The main A1 run had very high observed cache usage; its costs should not be generalized to a study where every request changes the stable exercise data or caching does not occur. A no-cache sensitivity analysis is more informative than promising a universal per-offer price.

The reported mean scoring time sums measured API-response durations for each input. It excludes dispatch pacing, queue time and local Python/file operations. It is not a promise about end-to-end participant waiting time in production. A stronger model or higher reasoning setting can cost more and take longer without improving the observed A/B result.

## Replication and release boundaries

The public repository has three useful modes: request preview without a key; offline scoring of a saved or synthetic interpretation; and a deliberately requested live API call. The first two do not require paid inference. A fresh API run can produce different wording and interpretations, so exact response reproducibility is not guaranteed by a prompt file alone.

The numerical scoring and aggregation on fixed inputs can be reproduced deterministically. The semantic judgments behind the accuracy labels are model-assisted and assistant-reviewed, not independent human ground truth. A researcher can inspect the actual offers, responses and Y/N classifications in the private workbook, change a flag, and recompute the summary. That is different from asking a model to regenerate the offers or silently resampling an incorrect answer until it passes.

The public package is separate from Joshua's deployment package. It does not replace the canonical Empirica folder or change the study frontend, treatments, server, role materials or API key. The frozen source modules are retained for traceability; the portable runner adds paths, request preview and explicit live-call control. These packaging changes need offline parity checks before claiming they preserve the evaluated behavior.

Do not publish private offer tables, full validation keys, billing databases, API credentials, or participant identifiers. Synthetic examples and aggregate results are sufficient for the public code walkthrough. Researchers seeking participant-level replication need an authorized private-data route.

## A writing checklist

- Use “scoring table,” “issue,” and “option” consistently.
- Say “Python script” for a processing step. The four main numbered labels now have matching runnable files. Explain their supporting functions separately rather than treating every imported helper as another model call.
- Make it clear who selects issues at each stage: Python retrieves candidates for A2; the LLM selects the interpreted issues/options; Python applies the assigned values.
- Keep the model interpretation, the participant offer, and the scored JSON separate.
- Do not draw a reviewer loop into the selected A1 architecture. Evaluation reviewers did not participate in its scoring calls.
- Do not draw a Nano-to-Luna chain into the latest fitted A2 job architecture.
- Do not describe customization as model fine-tuning.
- Do not describe a complete JSON schema or a supporting quote as proof of semantic accuracy.
- Do not call fitted development results untouched out-of-sample performance.
- Keep A/B accuracy separate from option-mapping accuracy, and do not promise zero future errors.

## Official API references

- [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
- [GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna)
- [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

These references document API features. The project's source files and saved evaluation records, not generic provider documentation, establish which configuration NOVA actually used.
