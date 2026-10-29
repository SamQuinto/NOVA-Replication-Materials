# Validation and development

Start with [Analysis.html](Analysis.html) or rerun [Analysis.ipynb](Analysis.ipynb). Neither makes paid API calls.

| File or folder | Purpose |
| --- | --- |
| [NOVA Offer Validation](NOVA_Offer_Validation.xlsx) | 1,225 main inputs, three scorers, reviewed Types A/B flags, formulas and prompts |
| [NOVA Tutorial Validation](NOVA_Tutorial_Validation.xlsx) | Separate 731-input tutorial evaluation |
| [data](data/) | Anonymous offers/context, saved interpretations, references, API usage, trials and survey responses |
| [results](results/) | Recomputed metrics and checks as CSV |
| [figures](figures/) | Issue frequency and NOVA-only diversity histogram, PNG and SVG |
| [Methods](Methods.md) | Definitions, populations and statistical methods |
| [Data dictionary](Data_Dictionary.md) | Fields and links between files |

## Run

Use Python 3.11 or newer. From this folder, run `python -m venv .venv`, then activate it (`.venv\Scripts\activate` on Windows; `source .venv/bin/activate` on macOS/Linux).

```sh
python -m pip install -r requirements.txt
python analysis.py
jupyter nbconvert --to notebook --execute Analysis.ipynb --output Analysis_executed.ipynb
```

The supplied notebook already contains executed outputs. Open `Analysis.html` to read or print it. Analysis packages are not required by the scorer demonstration.

The spreadsheets preserve reviewed reasons and flags. The same IDs repeat across scorer blocks. Accuracy formulas read the Y/N flags. Long cells retain complete text even where Excel's maximum row height requires selecting a cell to read everything.

Feedback influenced later scorer instructions and reference judgments. Do not describe the full collection as an untouched, blinded holdout. Recomputing saved classifications is deterministic; repeating paid model calls need not return identical responses.
