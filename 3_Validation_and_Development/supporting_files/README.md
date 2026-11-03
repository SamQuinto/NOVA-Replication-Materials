# Files used by the analysis

These files let `Analysis.ipynb` reproduce the Validation Tables and the pilot measures described in Appendix D. The notebook and HTML remain in the parent folder.

| Filename | Description |
| --- | --- |
| [analysis.py](analysis.py) | Calculates accuracy, confidence intervals, API costs, scoring times, negotiation activity, issue development and survey summaries. |
| [requirements.txt](requirements.txt) | Python packages needed to run the analysis. |
| [data/](data/) | Source records used by the calculations. Its README describes every file. |
| [results/](results/) | Calculated tables supporting Tables D1–D3, Figure 2 and the survey summaries. |
| [figures/](figures/) | The issue-frequency chart used for Figure 2. |

## API costs and scoring time

For each recorded call, the calculation is:

`((input tokens − cached tokens) × input rate + cached tokens × cached rate + output tokens × output rate) / 1,000,000`.

The historical rates in US dollars per million tokens are: `gpt-6.1-sol`, input 2.00–2.50, cached input 0.10, output 10.00; `gpt-5.6-luna`, input 0.20–0.25, cached input 0.02, output 1.20. The analysis averages recorded costs per offer and multiplies by 1,000. It includes observed prompt caching and counts saved calls when estimating normal scoring costs. These are the assumptions used in the reported evaluation.

Scoring time is the sum of API-call durations for an offer, averaged across offers. It excludes preparation, browser interaction and development effort. The A2 tutorial scorer can make two calls for an offer.

## Negotiation and survey measures

Behavior uses proposals sent to the counterpart. Issue diversity counts distinct issues across a negotiation. Additional issue diversity excludes salary, personal work-expense budget and starting date. Introduction adds a previously unmentioned issue after opening. Exploration changes the issue set relative to the union of the parties' latest offers. Exploitation revises an option on an issue already introduced. Rates are calculated within each negotiation, then averaged across negotiations.

Agreement requires mutual finalization and nonnegative scores for both parties. Behavioral summaries cover 38 completed negotiations; 36 had post-opening offers. Survey summaries average partners' responses, with usable answers required from both partners. Means use Student-t 95% confidence intervals, while accuracy and agreement use Wilson intervals.
