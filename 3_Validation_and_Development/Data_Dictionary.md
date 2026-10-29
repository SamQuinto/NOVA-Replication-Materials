# Data dictionary

The files below are in `data/`. Main-exercise and tutorial offer IDs are numbered separately, and each ID repeats for the different scorers. When linking a response to its API usage, use the exercise, offer ID and scorer together.

| File | One record | Main fields |
| --- | --- | --- |
| `main_offers.json` / `.csv` | One main input | offer ID, source, role, offer, previous offer, input kind |
| `main_review.csv` | One input/scorer pair | Offer ID, Source, Role, Offer, Scorer Architecture, Scorer Output, Type A Error, Type B Error, Error reason |
| `main_scorer_outputs.json` | Saved interpretation and scored JSON | offer ID, scorer, interpretation, scored offer, reviewed flags/reason |
| `main_references.json` | Reviewed reference interpretation | offer ID and reference handling; historical explanatory labels may remain inside it |
| `tutorial_*` | Corresponding tutorial records | Same structure, with tutorial roles and previous-offer context |
| `api_usage.json` / `.csv` | Calls attributed to one input/scorer | dataset, offer ID, scorer, model, tokens, summed API seconds, cost range, call count |
| `trials.json` / `.csv` | One assigned pair | trial ID, pilot, condition, anonymous role IDs, inclusion/completion/failure indicators |
| `negotiations.json` / `.csv` | One valid reciprocal dyad | trial ID, counts, timing proxies, agreement, scores, issues, early-quit flag |
| `sent_offers.json` / `.csv` | One proposal sent to a counterpart | trial ID, chronological offer number, role, offer text, choices, scores, event labels |
| `post_negotiation_responses.json` / `.csv` | One respondent in a valid both-survey dyad | trial ID, pilot, condition, role, raw answers |
| `feedback_survey_responses.json` / `.csv` | One completed feedback questionnaire | anonymous respondent ID, assigned role, raw answers including three offer questions |

JSON keeps lists and related fields together in their original structure. CSV stores those fields as JSON text within a cell. We also protect CSV cells that start with a spreadsheet formula character so that a participant's text is not accidentally run as a formula. The JSON version retains the de-identified wording. The notebook uses JSON for these structured records and CSV for the scoring judgments.

Trial and respondent labels were created for sharing these data; they are not Prolific IDs or hashes of those IDs. The earlier feedback-survey respondents are not automatically linked to the live-study participants. Keep the offer text, previous-offer context, model interpretation and final score distinct when following a record. For negotiation behavior, use `sent_offers`: a calculator attempt was not necessarily sent to the other negotiator.
