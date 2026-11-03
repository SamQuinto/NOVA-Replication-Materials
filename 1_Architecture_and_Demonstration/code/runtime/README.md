# Underlying scoring functions

The named A1 and A2 scripts import these functions. Keep them together when downloading the architecture folder. The published A1 runner supplies `A1_Final.txt` and disables the optional exercise-reading helper in the underlying library.

| Filename | Description |
| --- | --- |
| [app/a1/backend/scorer.py](app/a1/backend/scorer.py) | Loads the scoring table, checks interpreted offers and returns role-specific scores. |
| [app/a1/backend/interpretation.py](app/a1/backend/interpretation.py) | Checks supporting quotations, options, values, references and clarification handling. |
| [app/a1/backend/offer_engine.py](app/a1/backend/offer_engine.py) | Applies the numerical scoring rules used by the shared final scoring step. |
| [app/a1/backend/scenario.py](app/a1/backend/scenario.py) | Reads the active issues from an exercise definition. |
| [app/a1/backend/scenario_rules.py](app/a1/backend/scenario_rules.py) | Shared rules for numerical domains, dates and exercise conventions. |
| [app/a1/backend/api_budget.py](app/a1/backend/api_budget.py) | Optional API spending records supported by the underlying scorer library. |
| [app/a1/formats/interpretation.json](app/a1/formats/interpretation.json) | Default structured-interpretation format loaded by that library. |
| [app/a1/model_settings.json](app/a1/model_settings.json) | Model and pricing settings loaded during initialization. |
| [app/a1/scoring_table.json](app/a1/scoring_table.json) | Default scoring table bundled with the underlying library; the validation runners supply their frozen exercise files. |
| [app/a1/prompts/general_interpretation.txt](app/a1/prompts/general_interpretation.txt) | Default prompt loaded by the library; the evaluated A1 request uses `prompts/A1_Final.txt`. |
| [app/a1/prompts/job_reading_notes.txt](app/a1/prompts/job_reading_notes.txt) | Optional job-reading helper notes; disabled by the evaluated A1 runner. |
| [app/backend/stream.py](app/backend/stream.py) | Issue matching and interpretation handling used by A2, including its separate tutorial path. |
| [app/backend/job_offer_refinements.py](app/backend/job_offer_refinements.py) | Job-specific interpretation corrections imported by `a2_custom_rules.py`. |
| [app/backend/offer_engine.py](app/backend/offer_engine.py) | Scoring functions imported by the A2 implementation. |
| [app/backend/scenario_rules.py](app/backend/scenario_rules.py) | Numerical and date conventions used by those functions. |
| [app/backend/structured_offer.py](app/backend/structured_offer.py) | Reads structured issue-to-option choices and validates their form. |
| [app/backend/scorer_routing.py](app/backend/scorer_routing.py) | Underlying model-routing functions. The evaluated main A2 runner selects one economical call. |
| [app/backend/api_budget.py](app/backend/api_budget.py) | Optional spending records used by the underlying runtime. |
| [app/config/issue-phrase-registry.json](app/config/issue-phrase-registry.json) | Matching vocabulary and aliases used to recognize exercise issues. |
| [app/config/large-215.json](app/config/large-215.json) | Job-exercise configuration supported by the underlying runtime. |
| [app/config/small-15.json](app/config/small-15.json) | Default configuration required by the underlying runtime, preserving the initial 15-issue exercise. |
| [app/config/tutorial.json](app/config/tutorial.json) | Venue-hire tutorial configuration used by the A2 tutorial path. |
