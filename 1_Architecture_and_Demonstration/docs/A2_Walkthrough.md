# How Architecture 2 works

This guide explains how Architecture 2 (A2) uses exercise-specific instructions and Python rules to help a lower-cost model interpret offers. File paths start from the architecture folder. The evaluated job scorer calls `gpt-5.6-luna` once at low reasoning. Some older code supports escalating to stronger models, but that is not how the current job scorer runs.

## Offer data and exercise files

The caller supplies the same ordinary offer text, assigned role and optional explicitly referenced previous offer. `code/frozen/Scoring_Table.json` supplies the job definitions and numerical values. `Role_Materials.json` supplies context. A2 also reads `code/prompts/A2_Interpretation.txt` and the separately editable `code/frozen/A2_Reading_Rules.json`. Those reading rules encode the exercise's conventions; they are not answer-key entries.

Examples of exercise facts include the annual vacation default, weekly remote-work unit, meaning of a bare company-car request, and how the candidate's package is described when the recruiter is proposing it. A new exercise needs its own justified conventions. Do not transfer those job assumptions silently to a different setting.

## Python script A2-1

`code/A2-1.py:prepare_request` initializes the job engine and calls `code/a2_extract.py:build_request`.

`retrieval_text` compares long words in the offer with vocabulary from issue names using `difflib.get_close_matches` at cutoff 0.86. It adds a vocabulary hint only when one match is clear. It does not rewrite the original proposal or its evidence quotes. `stream._catalog` then returns retrieved definitions, continuous domains/units or discrete option labels. This is Python selecting a shortlist, not the researcher choosing issues for each offer.

`build_request` constrains the interpretation schema's issue names to that shortlist. It places the role, current text, prior text, selected definitions, exercise reading rules and narratives into the user payload. The interpretation prompt is a system message. Together they form one request. Python does not yet calculate points.

This setup uses low reasoning and a smaller set of potentially relevant issue definitions, together with exercise-specific instructions and a required response format. Selecting fewer definitions shortens the request, but an issue can be missed at this step before the model sees it. When investigating a missed idea, check which definitions were sent as well as what the model returned.

## Economical LLM and interpretation JSON

The live caller sends the request. The model returns pairs with issue, option and literal source text, plus ambiguities and new/unsupported terms. `a2_extract.finish_extraction` retains the response bookkeeping and converts structured ambiguities into the representation expected by the finalizer. It does not perform a second interpretation call.

The prompt themes are Understanding, Matching, Questions, Earlier offers and changes, and Final check. They separate real requests from background, preserve amounts and actors, keep questions within the proposed idea, limit inheritance and require semantic source support. The separate reading-rules JSON makes job-specific assumptions visible and editable rather than burying all of them in the system prompt.

## Python script A2-2

`code/A2-2.py:score_interpretation` calls `code/a2_finalize.py:finalize`. The finalizer copies the model interpretation, restores structured ambiguity details, applies `a2_custom_rules.customize`, establishes explicit reference scope and calls the shared A1 finalizer. The result includes `custom_rule_trace`, which records named corrections and their source. Numerical scores still come from the scoring table, not the economical model.

The full implementation is in `code/a2_custom_rules.py`; these are the important operations and why they exist:

| Rule group | What the code changes | Why and example |
| --- | --- | --- |
| Scoped acceptance | Carries forward only accepted earlier issues; marks their source as previous text | “Keep the rest” and “keep the date” have different scopes. A new amount alone must not inherit every previous benefit. |
| Literal evidence | `tokens` and `restore_quote` recover a unique literal span when the model only altered punctuation/articles | A normalized option can be useful, but its quote should still be the person's actual words. Ambiguous quote matches are not invented. |
| Exact quantities | Parses labelled money, attached units, durations and clear preferred selections | A two-year six-month term can become 2.5 years. An explicit later total replaces an earlier total rather than counting both. |
| Periods and baselines | Applies the job's weekly or annual interpretation and five-workday convention | Percent remote work is converted only against the exercise's stated workweek. These are deliberately job-specific facts. |
| Participation and duties | Distinguishes receiving training/mentoring from performing a duty for other people | Training colleagues is not automatically receiving company-funded external training. A recruitment-fair participation request can be a commitment without elaborate wording. |
| Missing quantities | Removes unsupported numerical selections and asks a question about the proposed idea | Health insurance without an employer share does not establish a percentage. A leave heading does not establish a number of days. |
| Conflicts and alternatives | Replaces a guessed selection with a useful question when distinct choices remain unresolved | Two contradictory probation durations need one chosen duration unless a clear correction resolves them. |
| Related concepts | Removes a neighboring issue not established by the text | A general aim or topic does not request every related review, funding arrangement or guarantee. |
| Purpose of money | Keeps sums attached to their stated purpose | A development amount must not become the required client-expense budget just because both contain “budget.” |
| Safe questions | Retains unresolved wording without suggesting a menu of other benefits | Clarification itself can cause a Type B error if it introduces a distinct optional issue. |
| New ideas | Retains meaningful proposed topics missed by a short answer | A real unmatched request remains visible without arbitrary points. Background and abandoned headings need not become proposals. |

The helpers `put`, `query` and `omit` have distinct roles. `put` replaces a pair for an issue with a supported normalized choice and records the rule. `query` removes that issue's priced choice and adds a question. Omissions remove an unsupported mapping, but should preserve a meaningful unresolved request. The code operates on contents and definitions, never benchmark case IDs.

`code/runtime/app/backend/job_offer_refinements.py` supplies additional fitted safeguards, including clauses, alternatives, duty assignment and domain checks. `code/runtime/app/backend/offer_engine.py` implements date/money recognition, scoring functions and shared numerical rules. `code/runtime/app/a1/backend/interpretation.py` handles generic evidence and interpretation checks. These files are included, not remote dependencies.

## Scored offer JSON

The final JSON serves the same purpose as A1's: it gives the interface the interpreted terms, scores, any valid total, questions and acknowledged ideas without points. The `custom_rule_trace` field shows which Python corrections were applied. NOVA may understand part of an offer even when the offer is not yet complete or agreed.

## Separate tutorial path

`code/nova_cli.py` routes tutorial A2 through `stream.llm_extract` and `stream.score`. It uses the venue exercise and not job-specific `customize`. A dense input can trigger a second independent completeness extraction using the same Luna model. This is neither a stronger-model escalation nor a reviewer that edits a first answer after inspecting it. The separate tutorial evaluation documents its lower performance. The figure's job stages should not be mislabelled as identical tutorial custom rules.

## How to develop a rule responsibly

Save a real failing input and its context. Identify the broad cause before editing: retrieval omission, wrong actor, missing period, guessed amount, conflated concepts, failed quote support or unsupported clarification. Specify the exercise convention and an example where the correction must not apply. Place a semantic convention in the reading-rules file; use deterministic Python only when a sufficiently reliable pattern or calculation is available. Test the original failure, spelling/separator variants, negations, alternatives and near-neighbor ideas. Recheck a regression sample. Keep versions of the prompt, rules, source definitions, outputs and judgments. Evaluate fresh data separately from fitted development cases. This process is customization, not model-weight fine-tuning.
