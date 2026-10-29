# How we developed and reviewed the scorer

The [validation folder](validation/) contains the prompts and response formats we used to draft reference interpretations, review scorer responses and correct review mistakes. These are evaluation tools, separate from the prompts NOVA uses when scoring an offer.

The [earlier results](results/) retain aggregate figures and package checks from previous versions. Use the main [results folder](../results/) for the current calculations. Some older records use different labels and folder paths; they are kept to help trace the work, not as a second set of headline results.

To see how a review request is prepared, run `python validation/prepare_review_request.py --help`. It does not call a model unless you add `--live` and supply your own API key. A model's review is a judgment for the researcher to check, not automatically the correct answer.
