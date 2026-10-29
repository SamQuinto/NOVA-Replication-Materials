# NOVA replication materials

NOVA turns a negotiator's own words into an interpretation that can be checked against a researcher-defined scoring table. The language model interprets the proposal. Python scripts check that interpretation, retrieve the assigned scores, and prepare the result for the interface.

This repository documents the two architectures evaluated on 29 October 2026. It contains code, exact prompts, exercise definitions, fitted matching vocabulary, synthetic examples, and aggregate results. It does **not** contain participant-level offers, Prolific identifiers, private review workbooks, API keys, or the researcher's billing records.

## Start here

- [Appendix B writer handbook](docs/Appendix_B_Writer_Handbook.md): a complete, plain-language explanation of the implementation and what the evidence does and does not show.
- [Architecture figures](figures/README.md): editable vector diagrams and image previews.
- [Exact prompts](prompts/): the evaluated instructions, kept separate from exercise data.
- [Validation protocol](docs/Validation_Protocol.md): the A/B checklist, reference interpretations, review process, and limitations.
- [Results](results/aggregate_results.json): published aggregate counts, cost estimates, and scoring times.

The public data are insufficient to independently recode every human response. Those records remain private. The tools can recompute results from the researcher's saved checks when access is authorized, or run the same architecture on new offers.

## Run an example without paying for an API call

Use Python 3.11 or later. Scoring and request preparation use the Python standard library; no `pip install` is needed.

```powershell
python score_offer.py --architecture A1 --case-json examples/job_offer.json
python score_tutorial_offer.py --architecture A1 --case-json examples/tutorial_offer.json
python score_offer.py --architecture A2 --case-json examples/job_offer.json
```

These commands show the model request only. Local file paths are resolved from the package, not the terminal's current directory. To replay a synthetic saved interpretation and perform the numerical scoring:

```powershell
python score_offer.py --architecture A1 --case-json examples/job_offer.json --interpretation-json examples/job_interpretation.json
python score_offer.py --architecture A2 --case-json examples/job_offer.json --interpretation-json examples/job_interpretation.json
python score_tutorial_offer.py --architecture A1 --case-json examples/tutorial_offer.json --interpretation-json examples/tutorial_interpretation.json
python -m unittest discover -s tests -v
```

The examples are newly written synthetic fixtures. They are not participant records and are not part of the reported human benchmarks.

## Make a live call deliberately

Set your own key in the environment. Never put a real key into this repository.

```powershell
$env:OPENAI_API_KEY = "your-own-key"
python score_offer.py --architecture A1 --reasoning low --case-json examples/job_offer.json --live --output local-output/result.json
```

For A1-high, change `low` to `high`. The evaluated A2 setting is low reasoning. Live tutorial A2 can make a second Luna call for a dense offer. The `--live` flag is required for all paid calls. No shared experimental-budget ledger or earlier unknown-billing lock is imposed by this runner.

A fresh model response can differ from a saved response. Repeating a run is not the same as reproducing the arithmetic on a fixed interpretation.

## Important implementation distinctions

- **A1:** one GPT-6.1 Sol interpretation call using the same general prompt for the job exercise and tutorial. Exercise information, role materials, table definitions, and response format are separate inputs.
- **A2 job exercise:** one GPT-5.6 Luna call followed by fitted job-exercise Python rules.
- **A2 tutorial:** the existing tutorial extraction and scoring path, with an optional second Luna completeness call. It is not the job-specific fitted Python patch applied to a different scenario.
- The older Nano-to-Luna escalation design is historical. It is not the latest evaluated A2 job configuration.

This is a replication runner, **not a replacement for Joshua's Empirica deployment folder**. The deployment package remains at [Creative Negotiations Materials](https://github.com/SamQuinto/Creative-Negotiations-Materials/tree/main/empirica). This release does not change it.

## Reproduce recorded accuracy

```powershell
python tools/recompute_accuracy.py --checks path/to/Checks_and_Responses.json
```

This recomputes counts from saved judgments without an API call. It does not independently establish that those judgments are correct. The spreadsheet's editable Y/N flags are the simplest route for researcher review.

The primary measure checks for missed ideas and unproposed issues added. It is not full verification of every option, quantity, provider, or score. See the validation protocol before using the figures in a manuscript.

## Files and permissions

`frozen/Scoring_Table.json` is the evaluated 215-issue job configuration. `frozen/tutorial/Scoring_Table.json` is the nine-issue tutorial configuration. The model-facing definitions omit the table's numerical point weights, but the role-material narratives can themselves describe illustrative values. Python remains responsible for the assigned arithmetic.

The fitted phrase dictionary is matching configuration, not a participant-level dataset. Origin annotations have been removed; runtime matching strings are retained. No human input tables or validation keys are included publicly.

Repository visibility does not itself grant a reuse license. The authors should specify licensing and any data-access terms before a formal archival release. Never add private data or credentials to a public issue or commit.
