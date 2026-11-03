# Scoring scripts

The named scripts correspond to Figure B1 and Appendix B. Keep this folder intact when downloading the web app; the supporting files are needed to run the scorer.

| Filename | Description |
| --- | --- |
| [A1-1.py](A1-1.py) | Python script A1-1: prepares A1's model request from the offer, role, exercise information and general-purpose prompt. |
| [A1-2.py](A1-2.py) | Python script A1-2: checks A1's interpretation and calculates the scored offer. |
| [A2-1.py](A2-1.py) | Python script A2-1: selects potentially relevant issues and prepares A2's model request. |
| [A2-2.py](A2-2.py) | Python script A2-2: applies custom rules, checks the interpretation and calculates the scored offer. |
| [a2_extract.py](a2_extract.py) | Matching vocabulary and issue selection used by A2-1. |
| [a2_custom_rules.py](a2_custom_rules.py) | Exercise-specific corrections applied by A2-2. |
| [a2_finalize.py](a2_finalize.py) | Applies those corrections and the shared scoring checks. |
| [common1225.py](common1225.py) | Shared file loading and API-call handling. The filename does not limit the number of offers. |
| [nova_cli.py](nova_cli.py) | Runs the selected architecture and connects request preparation, the model call and score calculation. |
| [runtime_setup.py](runtime_setup.py) | Loads the appropriate exercise and underlying scoring functions. |
| [stage_support.py](stage_support.py) | Command-line options shared by the named Python scripts. |
| [score_offer.py](score_offer.py) | Command-line entry point for scoring main job-negotiation offers. |
| [score_tutorial_offer.py](score_tutorial_offer.py) | Command-line entry point for scoring tutorial offers. |
| [prompts/](prompts/) | Exact prompts described in Appendix B. |
| [frozen/](frozen/) | Exercise definitions used for the reported validation. |
| [examples/](examples/) | Saved offers, interpretations and model requests for the demo and offline tests. |
| [runtime/](runtime/) | Underlying interpretation, checking and scoring functions imported by the scripts. |
| [tests/](tests/) | Offline checks of scoring, saved examples and folder portability. |
