# Data dictionary

Paths below are inside `data/`. Main and tutorial IDs are separate namespaces; always include the dataset when joining usage. IDs repeat across scorer blocks.

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

Nested lists/dictionaries are native JSON and encoded as JSON text in CSV. Human text starting with a spreadsheet formula character is escaped in CSV for safety; JSON retains the de-identified text. The notebook reads JSON for nested data and CSV for reviewed flags.

Trial and respondent IDs are fresh aliases, not Prolific hashes. Feedback respondents are not automatically linked to live participants. Input text, prior context, model interpretation and final scored result are distinct objects. An evaluated calculator input need not have been sent; use `sent_offers` for behavior.
