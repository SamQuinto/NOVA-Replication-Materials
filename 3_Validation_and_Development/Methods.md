# Measures and validation

## Accuracy

- **Type A: missed or unscored idea.** A meaningful proposal is omitted, or a clear supported option is left unscored without a necessary clarification. A useful question can handle missing essential details. Acknowledgement without points can handle an idea that the table genuinely cannot represent. Unfinished fragments need not become complete proposals.
- **Type B: unproposed issue added.** A distinct unproposed issue is priced or introduced. A leading question about an unmentioned optional issue can also reveal it. Reasonable shorthand, such as recruitment-fair participation meaning commitment, is not automatically an addition.
- **Primary accuracy:** neither A nor B is present. Divide accurate rows by all evaluated inputs for that scorer. An input with both errors is one inaccurate input.

The manuscript's **Type C** means a meaningful idea absent from the table. It is not the historical “type3” option-mapping warning. A/B accuracy is not an exhaustive independent audit of every mapping or score. The frozen 215-issue snapshot has no coffee entry; a later coffee addition mentioned in the manuscript is not reproduced here.

References and labels were produced through model-assisted interpretation and assistant/researcher review, including researcher decisions about reasonable meanings. The reviewed workbook flags are the supplied final labels, not a new independent human-coded gold standard. The notebook recomputes their counts without asking another model to certify them.

### Inputs

The main 1,225 records include 139 October 20 calculator inputs, 791 October 27 calculator inputs, 294 offer-question answers from 98 completed feedback surveys, and one research-assistant example. Seven answers from unfinished feedback surveys are excluded. The main set is not deduplicated; retries remain separate. Wilson intervals are descriptive offer-level intervals and do not account for within-person dependence. Role and previous-offer context can distinguish otherwise identical text.

Tutorial selection starts with 960 inputs (147 October 20; 813 October 27). Removing 47 same-role/context formatting duplicates leaves 913. Separating 165 previously used inputs and 17 non-offer fragments leaves 731 October 27 inputs. Difficult, partial and unusual offers were not excluded just because scoring failed. A2 uses its separate tutorial implementation, not fitted job rules.

### API costs and scoring time

For each input, sum all recorded calls:

`((input tokens − cached tokens) × input rate + cached tokens × cached rate + output tokens × output rate) / 1,000,000`.

Historical rates in US dollars per million tokens: `gpt-6.1-sol` input 2.00–2.50, cached input 0.10, output 10.00; `gpt-5.6-luna` input 0.20–0.25, cached input 0.02, output 1.20. These retain historical pricing assumptions, not current provider quotations. Average across retained inputs and multiply by 1,000. Estimates use observed prompt caching and attribute the full scored-request cost even if an identical saved response was reused during evaluation. They estimate operating cost, not total historical invoices.

Time is the sum of API durations per input, averaged across inputs. It excludes browser overhead, human preparation and development. A2 tutorial can use multiple calls. Future rates, caching, availability and service load can change costs and times.

## Behavior

All assigned trials: 109 dyads, 56 NOVA and 53 Fixed 9. NOVA involved 112 distinct participants. The behavioral file retains 81 valid reciprocal concluded dyads, including explicit quits. The manuscript's completed NOVA cohort excludes early quits: 38 dyads. Behavioral inclusion does not require a survey. Survey comparisons require valid dyads with both questionnaires and both partners' answers to a measure.

- **Issue diversity:** union of distinct issues across submitted offers in a negotiation. Includes the three required issues. Additional diversity excludes Salary, Personal Budget and Starting Date.
- **Introduction:** a post-opening offer adds an issue never mentioned earlier in that dyad.
- **Exploration:** a post-opening offer changes the issue set relative to the union of the two parties' latest offers immediately beforehand. Additions or omissions can change the set.
- **Exploitation:** a post-opening offer revises the latest observed option for an issue previously introduced.
- **Rates:** event count divided by post-opening offers. The opening offer is excluded. A dyad-mean rate and an offer-weighted pooled rate are different summaries and are labelled separately.
- **Issue frequency:** number of completed NOVA dyads mentioning each nonrequired issue. Opening and introduced-later segments are mutually exclusive per dyad/issue.
- **Agreement:** recorded mutual finalization with both scores nonnegative, including zero. Legacy JSON includes contradictory strictly-positive metadata; analysis uses the researcher's nonnegative rule.

Behavior uses submitted offers, not unsent calculator attempts. The notebook recomputes issue sets and events from `choices`. Exact tutorial duration is unavailable; preparation time is a labelled proxy.

## Surveys and uncertainty

Subjective value averages Q1–Q16, reversing Q3 and Q5. Creative engagement averages Q20–Q24 on a five-point frequency scale. Creative confidence averages Q25–Q27 on a seven-point agreement scale. Q18 is perceived realism. Q29 is feeling stuck, not a validated temporary-impasse measure. Section 2 provides full questions and response choices.

Compare dyad means, not two independent observations per pair. Both partners need a usable answer for a measure. Continuous comparisons use Welch's t test and unadjusted p values; means have Student-t 95% intervals and sample SDs. Accuracy and agreement have Wilson 95% intervals. Tests are exploratory. A nonsignificant difference is not equivalence or noninferiority.
