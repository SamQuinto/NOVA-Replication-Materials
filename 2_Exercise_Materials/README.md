# Negotiation exercise materials

Start with the [negotiation exercise role materials](Negotiation_Exercise_Role_Materials.pdf). This document brings together the main exercise and tutorial, with a short introduction to each.

The **main exercise** is a two-party job negotiation: one person plays the Candidate and the other plays the Recruiter. The document includes the NOVA version, where negotiators write offers in their own words, and the fixed version, where they choose among nine issues.

The **tutorial** is a short venue-hire negotiation. Participants in our pilot studies completed it before the main task to become familiar with NOVA and its scoring calculator.

Both roles are included for researchers to read. When running a study, give each negotiator only their own role information.

| Where to look | What it contains |
| --- | --- |
| [Negotiation exercise role materials](Negotiation_Exercise_Role_Materials.pdf) | Main exercise and tutorial in one document |
| [Job exercise scoring table](scoring_tables/Job_Exercise_Scoring_Table_Main.xlsx) | All 215 issues, with continuous scoring rules, reference points and discrete options. A separate sheet contains the Fixed 9 menu. |
| [Venue rental scoring table](scoring_tables/Venue_Rental_Scoring_Table.xlsx) | The tutorial's nine issues and the scores for the Organizer and Venue Manager |
| [Scoring definitions](scoring_tables/) | JSON files used by the scorer and study interface |
| [Questionnaires](questionnaires/) | Questions used after the main task and in the earlier feedback survey |

Each scoring workbook separates **continuous rules and reference points** from **discrete options**. Continuous issues show their allowed values and how scores change between reference points. Those points are not a fixed menu. Discrete issues list each scored option and its value to both roles. Scores are displayed to two decimal places without rounding the underlying values.

The job workbook's **Fixed 9** sheet is a separate, restricted menu for the fixed-issue condition. It does not limit the flexible 215-issue exercise. In `fixed-9.json`, only the nine active issues belong to the fixed negotiation; other definitions are retained in the file for compatibility.

The questionnaire files include question wording, response choices and settings used by the study interface. The participant responses and analysis are in [Validation and development](../3_Validation_and_Development/).
