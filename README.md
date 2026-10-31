# NOVA replication materials

Here you can try NOVA, read the negotiation exercises, and explore the data and tests behind the paper. NOVA reads offers written in ordinary language and scores them using a scoring table prepared by the researcher.

| Folder | What you will find |
| --- | --- |
| [1 Architecture and web app](1_Architecture_and_Demonstration/) | Architecture 1 and 2 (A1 and A2) prompts, scoring code, and a downloadable web app where you can try NOVA in your local browser using your own OpenAI key |
| [2 Exercise materials](2_Exercise_Materials/) | Negotiation exercise role materials for the main task and tutorial, scoring tables, and study questionnaires |
| [3 Validation and development](3_Validation_and_Development/) | Offers and survey responses from the pilot tests, scoring reviews, and the code and results for the analyses reported in the paper |

## Try NOVA

Download this repository, or just the complete `1_Architecture_and_Demonstration` folder. To score your own offers, you will need Python 3.11 or later and your own OpenAI API key.

You can try six saved examples without a key or charge. To score new text, take a moment to add your own key using the steps below.

### Add or update your OpenAI key

1. Download and extract the files first; do not run the app from inside the ZIP. Open `1_Architecture_and_Demonstration`—the folder containing `.env.example`, `code` and `demo`.
2. If you do not have an API key yet, create one in your [OpenAI API settings](https://platform.openai.com/api-keys). OpenAI’s [quickstart](https://developers.openai.com/api/docs/quickstart) explains how to get started. You will need access to the models used by NOVA and available API credit.
3. Make a **copy** of `.env.example` in that same folder and name the copy **`.env`**. On Windows, turn on **View → Show → File name extensions** in File Explorer so you can check that it is not named `.env.txt`.
4. Open `.env` in a plain-text editor such as Notepad. Replace `replace_with_your_own_api_key` with your key, keeping `OPENAI_API_KEY=` at the start of the line. Save the file. There should be just one key on that line, with no spaces around it.
5. To change the key later, edit this same `.env` file and replace the old key. Please keep it private: do not email it, commit it to GitHub, or include it in screenshots. The app reads it on your computer, not in the browser.
6. Open a terminal **in `1_Architecture_and_Demonstration`** and run:

```sh
python demo/Start_Demo.py
```

The web app will open in your browser. If it does not, open `http://127.0.0.1:8765/`. Choose an exercise and scorer, write an offer, and click **Score**. New calls are charged to your OpenAI account. The **SAVED EXAMPLES** dropdown is free to use. The app does not need any additional Python packages.

If `python` is not recognized on Windows, try `py demo/Start_Demo.py`. After editing the key, refresh the page; if it still does not work, stop the app with **Ctrl+C** in its terminal and run the command again. If you previously set `OPENAI_API_KEY` as an environment variable, that setting takes priority over `.env`—update it too, or remove it from the terminal you use to start the app. A billing or model-access error needs to be resolved in your OpenAI account; loading a saved example will still work.

## Explore the materials and results

The [negotiation exercise role materials](2_Exercise_Materials/Negotiation_Exercise_Role_Materials.pdf) bring the main exercise and tutorial together in one document. The tutorial is the short negotiation participants completed before the main task in our pilot studies to become familiar with NOVA.

Open [the analysis](3_Validation_and_Development/Analysis.html) to read the results, or use [the notebook](3_Validation_and_Development/Analysis.ipynb) to reproduce them. Rerunning these calculations does not make API calls. The validation spreadsheets also let you inspect individual offers and see how accuracy was calculated.

The main evaluation includes 1,225 offer inputs, and the separate tutorial evaluation includes 731. These include retries and incomplete calculator inputs, not just offers sent to another negotiator. [Methods](3_Validation_and_Development/Methods.md) explains how we selected the data and calculated each measure.

The [NOVA development archive](3_Validation_and_Development/NOVA_Development_Archive.xlsx) contains 568 development offers and two examples showing how we identified and addressed scoring errors. It is separate from the reported validation results.

## Participant privacy

Participant data from the pilot tests have been de-identified before sharing. Names, Prolific IDs and contact details are not included, and the original records remain private. The [privacy note](3_Validation_and_Development/Privacy_Review.md) explains what we removed and the limits of sharing free-text responses.
