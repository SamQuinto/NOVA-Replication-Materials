# Validation and development

This folder lets you inspect the offers from our pilot tests, see how we reviewed NOVA's responses, and reproduce the reported results. Participant information has been de-identified before sharing.

Start with [the analysis](Analysis.html) to read the results. If you would like to run the calculations yourself, use [the Python notebook](Analysis.ipynb). Neither needs an API key or makes model calls.

| Where to look | What it contains |
| --- | --- |
| [Main offer validation](NOVA_Offer_Validation.xlsx) | 1,225 inputs, responses from three scorer settings, error reviews, accuracy calculations and prompt text |
| [Tutorial offer validation](NOVA_Tutorial_Validation.xlsx) | The separate evaluation of 731 tutorial inputs |
| [Earlier development inputs](data/early_development_offers.csv) | 568 earlier tests and wording variations, kept separate from the main and tutorial evaluations |
| [Data](data/) | Participant offers and survey responses, recorded scorer responses, review decisions and API usage |
| [Results](results/) | Tables calculated from the supplied data |
| [Figures](figures/) | The issue-frequency chart and issue-diversity histogram |
| [Methods](Methods.md) | How we selected the data and defined each measure |
| [Data dictionary](Data_Dictionary.md) | What each file and field means, and how to link them |

## Inspect the scoring reviews

Each spreadsheet includes the offer, NOVA's response and our Type A and Type B error judgments. The same offer ID appears once for each scorer, so you can compare their responses. The Accuracy sheet calculates directly from the Y/N judgments. If you edit one, the accuracy updates too.

Your spreadsheet program may limit how much text fits in a row. Selecting a long cell lets you read the complete offer or response.

## Run the analysis

Use Python 3.11 or later. From this folder, run `python -m venv .venv` and activate it: `.venv\Scripts\activate` on Windows, or `source .venv/bin/activate` on macOS/Linux. Then run:

```sh
python -m pip install -r requirements.txt
python analysis.py
jupyter nbconvert --to notebook --execute Analysis.ipynb --output Analysis_executed.ipynb
```

The notebook already includes the results from a completed run. You can read or print `Analysis.html` without installing anything. These analysis packages are not needed to try the downloadable web app.

Feedback from earlier tests helped us improve both the scorer and the review decisions. The full collection should therefore not be treated as an untouched test set. The supplied files reproduce the recorded results; asking a model to score the offers again may produce somewhat different responses.
