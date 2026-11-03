# Validation and Development

The Validation Tables contain the original offers, scorer responses, Type A and Type B classifications, and explanations. They cover A1-low, A1-high and A2. These materials accompany Appendices C and D.

| Filename | Description |
| --- | --- |
| [NOVA_Offer_Validation.xlsx](NOVA_Offer_Validation.xlsx) | Main job-negotiation Validation Table: 1,225 offers, with scorer responses, error classifications, accuracy calculations and prompts. Results are reported in Table D1. |
| [NOVA_Tutorial_Validation.xlsx](NOVA_Tutorial_Validation.xlsx) | Venue-hire tutorial Validation Table: 731 offers, with the same review columns and accuracy calculations. Results are reported in Table D2. |
| [NOVA_Development_Archive.xlsx](NOVA_Development_Archive.xlsx) | Development archive containing 568 offers and examples of how scoring errors were addressed. Described at the start of Appendix D. |
| [Analysis.html](Analysis.html) | Read the completed analysis of scoring accuracy, API costs, processing time, negotiation activity and creative issue development. Opens without installing anything. |
| [Analysis.ipynb](Analysis.ipynb) | Python notebook that reproduces the calculations, including Tables D1–D3 and the issue frequencies shown in Figure 2. |
| [supporting_files/](supporting_files/) | Data and Python files required by the notebook, with calculated results and the Figure 2 chart. Each subfolder explains its files. |

## How accuracy is calculated

An offer passes when neither error occurs. **Type A** means the scorer misses a meaningful idea or leaves a supported option unscored without a relevant clarification. A useful clarification can pass even when direct scoring would have been possible. An idea outside the scoring table can be acknowledged without points. **Type B** means the scorer introduces an issue the negotiator did not propose, including through a leading question.

The Accuracy sheet in each Validation Table calculates directly from its Y/N classifications. The notebook repeats the calculation using matching CSV records. The classifications were developed with LLM assistance and researcher feedback. This measure does not independently verify every numerical score. Offers used during refinement remain in the collection, so it is a development benchmark.

## Reproduce the results

Open `Analysis.ipynb` from this folder. With Python 3.11 or later, install its packages using:

```sh
python -m pip install -r supporting_files/requirements.txt
```

Run the notebook cells in order. To run the calculations without opening the notebook:

```sh
python supporting_files/analysis.py
```

These calculations use saved records and make no API calls. The pilot studies and analyses were exploratory and were not preregistered. The shared pilot records cover NOVA negotiations.

Participant names, Prolific IDs, contact details and private linking records are excluded. [The data README](supporting_files/data/README.md#participant-data) explains the de-identification and the records provided.
