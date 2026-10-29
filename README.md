# NOVA replication materials

Here you can try NOVA, read the negotiation exercises, and explore the data and tests behind the paper. NOVA reads offers written in ordinary language and scores them using a scoring table prepared by the researcher.

| Folder | What you will find |
| --- | --- |
| [1 Architecture and web app](1_Architecture_and_Demonstration/) | Architecture 1 and 2 (A1 and A2) prompts, scoring code, and a downloadable web app where you can try NOVA in your local browser using your own OpenAI key |
| [2 Exercise materials](2_Exercise_Materials/) | Negotiation exercise role materials for the main task and tutorial, scoring tables, and study questionnaires |
| [3 Validation and development](3_Validation_and_Development/) | Offers and survey responses from the pilot tests, scoring reviews, and the code and results for the analyses reported in the paper |

## Try NOVA

Download this repository, or just the complete `1_Architecture_and_Demonstration` folder. To score your own offers, you will need Python 3.11 or later and your own OpenAI API key.

1. In that folder, copy `.env.example` to a file called `.env` and replace the placeholder with your key. Keep this file private.
2. From the same folder, run:

```sh
python demo/Start_Demo.py
```

The web app will open in your browser. Write an offer, choose a scorer, and click **Score with API**. Calls are charged to your OpenAI account. You can also look at a saved example without a key or charge. The app does not need any additional Python packages.

## Explore the materials and results

The [negotiation exercise role materials](2_Exercise_Materials/Negotiation_Exercise_Role_Materials.pdf) bring the main exercise and tutorial together in one document. The tutorial is the short negotiation participants completed before the main task in our pilot studies to become familiar with NOVA.

Open [the analysis](3_Validation_and_Development/Analysis.html) to read the results, or use [the notebook](3_Validation_and_Development/Analysis.ipynb) to reproduce them. Rerunning these calculations does not make API calls. The validation spreadsheets also let you inspect individual offers and see how accuracy was calculated.

The main evaluation includes 1,225 offer inputs, and the separate tutorial evaluation includes 731. These include retries and incomplete calculator inputs, not just offers sent to another negotiator. [Methods](3_Validation_and_Development/Methods.md) explains how we selected the data and calculated each measure.

## Participant privacy

Participant data from the pilot tests have been de-identified before sharing. Names, Prolific IDs and contact details are not included, and the original records remain private. The [privacy note](3_Validation_and_Development/Privacy_Review.md) explains what we removed and the limits of sharing free-text responses.

For more detail, the [repository guide](NOVA_Repository_Guide.md) maps the files, explains how to use them, and identifies the sources for each appendix. You can also read its [formatted HTML version](NOVA_Repository_Guide.html). The [architecture guide](1_Architecture_and_Demonstration/Architecture_Guide.md) explains the prompts and scoring code step by step, with expandable sections containing the exact source text. The prompts and scoring behavior used in the evaluation have not been changed by this documentation update.
