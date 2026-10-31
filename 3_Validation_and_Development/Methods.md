# Measures and validation

## Accuracy

- **Type A: missed or unscored idea.** A meaningful proposal is omitted, or a clear supported option is left unscored without a relevant clarification. A question addressing the proposed issue is accepted even when direct scoring would have been preferable. Mere fragments that lose the idea's meaning do not count as acknowledgement. Acknowledgement without points can handle an idea that the table genuinely cannot represent. Unfinished fragments need not become complete proposals.
- **Type B: unproposed issue added.** A distinct unproposed issue is priced or introduced. A leading question about an unmentioned optional issue can also reveal it. Reasonable shorthand, such as recruitment-fair participation meaning commitment, is not automatically an addition.
- **Primary accuracy:** neither A nor B is present. Divide accurate rows by all evaluated inputs for that scorer. An input with both errors is one inaccurate input.

The manuscript's **Type C** means a meaningful idea absent from the table. It is not the historical “type3” option-mapping warning. A/B accuracy is not an exhaustive independent audit of every mapping or score. The frozen 215-issue snapshot has no coffee entry; a later coffee addition mentioned in the manuscript is not reproduced here.

We drafted reference interpretations with model assistance and reviewed them using researcher feedback about what counted as a reasonable interpretation. The Y/N decisions in the workbooks are the final decisions from that process, rather than a new independent human audit. The notebook counts those decisions; it does not ask another model to judge them again.

On October 31, we accepted two tutorial clarification responses: A1-low on o288 asked about cancellation, and A1-high on o295 asked about the event date. Both acknowledged the proposed issue, so asking an unnecessary clarification was treated as a usability limitation rather than a Type A omission. These corrections raise both A1 tutorial counts from 730/731 to 731/731.

We then inspected all 152 previously flagged A2 tutorial responses using the same criterion. We removed 63 Type A flags for responses that addressed the issue with a clarification. Two of these offers still had a Type B error, so the accurate count increased by 61, from 579 to 640 of 731. We also marked o60 as Type B because it added early access from a promise to perform setup work, using the same distinction already applied to o205. A2 now has 83 Type A flags, 10 Type B flags and two offers with both errors. The [offer-by-offer review log](data/tutorial_A2_review_corrections.json) retains the previous judgments and the reasons for the decisions. No scorer responses, prompts, main-exercise results, API costs or timings changed, and no new API calls were made.

### Inputs

The main collection contains 1,225 inputs: 139 calculator attempts from October 20, 791 from October 27, 294 answers to offer questions from 98 completed feedback surveys, and one research-assistant example. We excluded seven answers from unfinished feedback surveys. Retries remain separate rather than being deduplicated. The confidence intervals treat offers as observations and do not adjust for several offers coming from the same person. Identical wording can still have a different meaning when the role or previous-offer context differs.

For the tutorial, we started with 960 inputs: 147 from October 20 and 813 from October 27. We removed 47 formatting duplicates with the same role and context, then set aside 165 inputs used earlier and 17 fragments that were not offers. This left 731 October 27 inputs. We did not remove difficult, partial or unusual offers simply because scoring failed. A2 uses its separate tutorial scorer, without the job-specific rules.

### API costs and scoring time

For each input, sum all recorded calls:

`((input tokens − cached tokens) × input rate + cached tokens × cached rate + output tokens × output rate) / 1,000,000`.

The calculations use historical rates in US dollars per million tokens: `gpt-6.1-sol` input 2.00–2.50, cached input 0.10, output 10.00; `gpt-5.6-luna` input 0.20–0.25, cached input 0.02, output 1.20. These are the assumptions used for this evaluation, not current price quotes. We average the cost across inputs and multiply by 1,000. The estimates include the observed caching discount. If a saved response was reused during evaluation, we still count the cost of scoring that offer when estimating normal use. The result estimates operating costs, not the total of past invoices.

For scoring time, we add the API-call times for each input and then average across inputs. This excludes time spent in the browser, preparing offers or developing the scorer. A2 can make more than one call for a tutorial offer. Prices, caching and service load can change both costs and timing in future use.

## Behavior

Across the pilots, we assigned 109 pairs: 56 to NOVA and 53 to Fixed 9. The NOVA trials involved 112 distinct participants. Of the recorded negotiations, 81 passed the attendance and scoring checks and showed participation by both parties; some ended with an explicit quit. The completed NOVA sample used in the manuscript excludes early quits and contains 38 pairs. A completed survey is not required to study negotiation behavior. Survey comparisons, however, use valid pairs where both participants completed the questionnaire and answered the measure being compared.

- **Issue diversity:** union of distinct issues across submitted offers in a negotiation. Includes the three required issues. Additional diversity excludes Salary, Personal Budget and Starting Date.
- **Introduction:** a post-opening offer adds an issue never mentioned earlier in that dyad.
- **Exploration:** a post-opening offer changes the issue set relative to the union of the two parties' latest offers immediately beforehand. Additions or omissions can change the set.
- **Exploitation:** a post-opening offer revises the latest observed option for an issue previously introduced.
- **Rates:** event count divided by post-opening offers. The opening offer is excluded. A dyad-mean rate and an offer-weighted pooled rate are different summaries and are labelled separately.
- **Issue frequency:** number of completed NOVA dyads mentioning each nonrequired issue. Opening and introduced-later segments are mutually exclusive per dyad/issue.
- **Agreement:** recorded mutual finalization with both scores nonnegative, including zero. Legacy JSON includes contradictory strictly-positive metadata; analysis uses the researcher's nonnegative rule.

For behavior, we use offers sent to the counterpart, not calculator attempts that were never sent. The notebook works through the recorded `choices` to recalculate which issues appeared and when they changed. We could not reliably determine exact tutorial duration, so preparation time is labelled as an approximation rather than treated as a direct measure.

## Surveys and uncertainty

Subjective value averages Q1–Q16, reversing Q3 and Q5. Creative engagement averages Q20–Q24 on a five-point frequency scale. Creative confidence averages Q25–Q27 on a seven-point agreement scale. Q18 is perceived realism. Q29 is feeling stuck, not a validated temporary-impasse measure. Section 2 provides full questions and response choices.

We average the two partners' answers before comparing conditions, so a pair is not treated as two independent observations. Both partners need a usable answer for that measure. Continuous comparisons use Welch's t test with unadjusted p values. We report sample SDs and Student-t 95% confidence intervals for means, and Wilson 95% intervals for accuracy and agreement. These comparisons are exploratory; a nonsignificant difference does not establish equivalence or noninferiority.
