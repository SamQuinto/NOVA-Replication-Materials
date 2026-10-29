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

1. Copy `.env.example` to `.env` in this folder and replace the placeholder with your own OpenAI API key. Do not share or upload that file.
2. Run `python demo/Start_Demo.py` from this folder.
3. In the browser, choose the exercise, your role and the scorer. Write an offer and click **Score with API**.

The app shows how NOVA interpreted the offer and what it is worth to the selected role. You can edit the offer and score it again without clearing the text. Calls are charged to your OpenAI account. The app reads your key from your computer without showing it in the browser or publishing it with the repository.

If you just want to see how the app looks, **Try a saved example** works without a key or charge. This loads an existing interpretation; it does not ask a model to read new text. The app lets you test scoring, but does not pair you with another negotiator or run a complete study.

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
