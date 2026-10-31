# Architecture and downloadable web app

This folder contains the Architecture 1 and 2 (A1 and A2) prompts, the scoring code, and a downloadable web app where you can try NOVA in your local browser. To score your own offers, you will need your own OpenAI API key.

| Where to look | What it contains |
| --- | --- |
| [Architecture 1 (A1)](A1/) | General-purpose instructions and a stronger model that reads the full scoring table |
| [Architecture 2 (A2)](A2/) | A lower-cost model supported by instructions and Python rules developed for the exercise |
| [Web app](demo/) | The app you can download and run in your browser |
| [Scoring code](code/) | Python scripts, exact prompt text, exercise definitions and the files they need |

## Try it in your browser

Download this whole folder and keep its contents together. You will need Python 3.11 or later, but no additional Python packages.

You can use the **SAVED EXAMPLES** dropdown without a key or charge. To score your own text, please add your key first:

### Add or update your OpenAI key

1. Extract the download and open this folder, `1_Architecture_and_Demonstration`. You should see `.env.example`, `code` and `demo` together.
2. Create an API key in your [OpenAI API settings](https://platform.openai.com/api-keys) if you do not already have one. The [official quickstart](https://developers.openai.com/api/docs/quickstart) walks you through getting started. Your account needs available API credit and access to NOVA’s models.
3. Copy `.env.example` and rename the **copy** to **`.env`**, in this same folder. On Windows, enable **View → Show → File name extensions** in File Explorer, then check that the name is `.env`, not `.env.txt`.
4. Open `.env` in Notepad or another plain-text editor. Replace `replace_with_your_own_api_key` with your key. Leave `OPENAI_API_KEY=` at the beginning, without spaces around the key, and save.
5. Updating a key later is just as simple: open this same `.env`, replace the old key and save. Please do not share this file or upload it to GitHub. The browser never needs to see your key.
6. Open a terminal in this folder and run:

```sh
python demo/Start_Demo.py
```

Your browser should open automatically. If not, visit `http://127.0.0.1:8765/`. Choose the exercise, role and scorer, write an offer, and click **Score**. On Windows, try `py demo/Start_Demo.py` if `python` is not recognized.

After a key change, refresh the page. If needed, stop the app with **Ctrl+C** in its terminal and run it again. An existing `OPENAI_API_KEY` environment variable takes priority over `.env`; if you set one before, update or remove it in the terminal used to start the app. If OpenAI reports a billing or model-access problem, check those settings in your OpenAI account. You can still load the saved examples meanwhile.

Read your role materials in the scrollable panel on the left, then write an offer alongside them. The panel uses the bundled exercise text and changes when you choose a different exercise or role. The app shows how NOVA interpreted the offer and what it is worth to the selected role. You can edit the offer and score it again without clearing the text. Calls are charged to your OpenAI account. The app reads your key from your computer without showing it in the browser or publishing it with the repository.

The **SAVED EXAMPLES** dropdown contains six examples: an informal offer with typos, a Candidate proposal, its Recruiter counteroffer, an unresolved choice, an idea outside the scoring table, and a tutorial offer. These reuse saved A1-low interpretations and calculate values locally without asking a model to read new text. The app identifies that setting when an example loads. Changing its text and clicking Score makes a new call. You can also change whose value is displayed without making another call. The app lets you test scoring, but does not pair you with another negotiator or run a complete study.

The tutorial roles are Organizer and Venue manager. The code uses the internal labels `Candidate` and `Recruiter` for them, respectively.

## Use the Python scripts directly

To see the request NOVA would send, without calling a model:

```sh
python code/score_offer.py --case-json code/examples/job_offer.json
```

To calculate scores from a saved example interpretation, also without calling a model:

```sh
python code/score_offer.py --case-json code/examples/job_offer.json --interpretation-json code/examples/job_interpretation.json
```

For a live call from the command line, set `OPENAI_API_KEY` in your environment and add `--live`. The command-line scripts read that environment variable; the web app also supports the `.env` file. Choose `--architecture A2` for A2 or `--reasoning high` for A1-high. Use `code/score_tutorial_offer.py` for the tutorial.

## Check that it works

```sh
python -m unittest discover -s code/tests -v
```

These tests do not call a model. They check request preparation, score calculation, and whether the app still works after its folder is copied and renamed.

A2 uses a separate tutorial scorer. A long tutorial offer can receive a second reading by the same model; it is not sent to a stronger model.

Requests use `store:false`. OpenAI explains this setting in its [response-storage documentation](https://developers.openai.com/api/docs/guides/migrate-to-responses). Its [structured-output documentation](https://developers.openai.com/api/docs/guides/structured-outputs) explains the JSON format we request. Getting valid JSON does not by itself mean the model understood the offer correctly; NOVA also checks the interpretation before calculating points.
