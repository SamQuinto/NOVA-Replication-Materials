# Source data

Use the Validation Tables in the parent folder to review offers and error classifications. These records provide the context and measurements needed to reproduce the calculations. Match scoring records using the exercise, offer ID and scorer together.

| Filename | Description |
| --- | --- |
| [main_review.csv](main_review.csv) | Type A and Type B classifications and explanations from the main job-negotiation Validation Table. Used to recalculate Table D1. |
| [tutorial_review.csv](tutorial_review.csv) | Corresponding classifications from the tutorial Validation Table. Used to recalculate Table D2. |
| [api_usage.json](api_usage.json) | Recorded models, token usage, cached tokens, API durations and estimated costs for each offer and scorer. |
| [main_offers.json](main_offers.json) | The 1,225 main offers, including assigned roles, sources and previous-offer context where applicable. |
| [tutorial_offers.json](tutorial_offers.json) | The 731 tutorial offers and their corresponding roles and context. |
| [main_scorer_outputs.json](main_scorer_outputs.json) | Complete saved interpretations and scored responses for the main Validation Table. |
| [tutorial_scorer_outputs.json](tutorial_scorer_outputs.json) | Complete saved responses for the tutorial Validation Table. |
| [trials.json](trials.json) | All 56 assigned NOVA pairs, including completion and exclusion indicators. |
| [negotiations.json](negotiations.json) | The 39 eligible NOVA negotiation records, including the pair that quit early. |
| [sent_offers.json](sent_offers.json) | Chronological proposals sent to counterparts, with interpreted issues, options and scores. Used for Table D3 and Figure 2. |
| [post_negotiation_responses.json](post_negotiation_responses.json) | De-identified post-negotiation answers from 76 participants in valid pairs with both surveys. |
| [feedback_survey_responses.json](feedback_survey_responses.json) | Answers from the 98 completed role-materials feedback surveys, including the offer-generation questions. |
| [questionnaire_configurations.json](questionnaire_configurations.json) | Question wording, response choices and settings for the pilot and feedback surveys, with the analysis schema. Read the [Survey Questionnaire](../../../2_Exercise_Materials/questionnaires/Survey_Questionnaire.pdf) for the questions and survey dates. |
| [development_refinements.json](development_refinements.json) | Full earlier and later scorer responses for the two refinement examples summarized in the development archive. |

The main Validation Table combines 930 live-negotiation scoring attempts, 294 offer-generation answers from 98 survey participants and one research-assistant example. Seven answers from unfinished surveys were excluded. Retries remain separate. The tutorial collection started with 960 submissions; removing 47 formatting duplicates, 165 previously used development submissions and 17 fragments left 731 offers.

The main and tutorial confidence intervals treat offers as separate observations, including repeated submissions from a participant. The workbooks contain the final model-assisted classifications developed using researcher feedback. A relevant clarification can pass even when direct scoring would have been possible. The tutorial A2 results apply that same criterion throughout.

## Participant data

Names, Prolific IDs, contact details, exact event timestamps, private linking records and API keys are excluded. An email address was removed from one survey response. Shared records use new participant and negotiation labels. Free-text responses were checked for private identifiers and contact information. The original study records remain private.

Distinctive wording can still be recognizable. Please use the records for research and replication and avoid attempts to identify participants. The raw pilot records in this package cover NOVA negotiations.
