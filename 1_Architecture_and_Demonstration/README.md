# Architecture and demonstration

This folder contains everything needed to run the supplied job and tutorial scorers. It works independently of the outer repository. Keep its contents together when downloading or moving it.

| Item | Purpose |
| --- | --- |
| [A1](A1/) | Flexible template using a stronger model and all active issue definitions |
| [A2](A2/) | Customized template using a lower-cost model and exercise-specific rules |
| [demo](demo/) | Browser interface served locally by Python |
| [code](code/) | Numbered scripts, exact prompts, scoring definitions and runtime dependencies |
| [figures](figures/) | Architecture image and editable Word version |
| [Architecture handoff](LLM_Architecture_Dump.txt) | Detailed walkthrough, prompt commentary and code references for Appendix B |

## Demonstration

Run `python demo/Start_Demo.py` from this folder. **Try a saved example** needs no key or charge. To score your text live, copy `.env.example` to `.env`, enter your own key, then click **Score with API**. The key stays in the local Python process, not the browser. Only live scoring sends offers to the model provider. Do not enter private information in a demonstration offer.

The tutorial displays Organizer and Venue manager. Its historical internal role labels are `Candidate` and `Recruiter` respectively.

## Command line

Preview a model request without a paid call:

```sh
python code/score_offer.py --case-json code/examples/job_offer.json
```

Score the synthetic example using its saved interpretation:

```sh
python code/score_offer.py --case-json code/examples/job_offer.json --interpretation-json code/examples/job_interpretation.json
```

For live command-line use, set `OPENAI_API_KEY` in your environment, then add `--live`. The `.env` reader belongs to the browser demonstration; command-line scripts read the environment directly. Use `--architecture A2` for A2, `--reasoning high` for A1-high, or `code/score_tutorial_offer.py` for the tutorial.

## Offline checks

```sh
python -m unittest discover -s code/tests -v
```

These checks make no API calls. They test saved requests, finalization, and operation after copying and renaming the code folder. Analysis dependencies are needed only for the notebook in section 3.

The figure describes the job flow. A2's separate tutorial parser can make a second same-model completeness call for a dense input. It does not escalate to a stronger model.

Requests explicitly use `store:false`. See OpenAI's [response-storage documentation](https://developers.openai.com/api/docs/guides/migrate-to-responses) and [structured-output documentation](https://developers.openai.com/api/docs/guides/structured-outputs). A valid JSON response still needs semantic checks; schema conformance alone does not establish interpretation accuracy.
