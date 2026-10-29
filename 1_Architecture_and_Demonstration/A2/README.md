# Architecture 2 (A2)

A2 reduces the cost of scoring by combining a less expensive model with instructions and Python rules developed for a particular exercise. The job-negotiation example uses `gpt-5.6-luna` at low reasoning.

Here is how an offer moves through A2:

1. [Python script A2-1](../code/A2-1.py) selects potentially relevant issues from the scoring table. It combines their definitions with the offer, role materials, prompt and exercise-specific instructions in one request.
2. The model reads the request and returns its interpretation as JSON. The current job scorer makes one model call; it does not move through a sequence of stronger models.
3. [Python script A2-2](../code/A2-2.py) applies the custom rules, checks the interpretation, looks up scores and returns the scored offer as JSON.

You can inspect each part here:

- [Interpretation prompt](../code/prompts/A2_Interpretation.txt)
- [Instructions specific to the job exercise](../code/frozen/A2_Reading_Rules.json)
- [Code that selects issues and prepares the request](../code/a2_extract.py)
- [Custom Python rules](../code/a2_custom_rules.py)
- [Code that checks and scores the interpretation](../code/a2_finalize.py)

The rules read the offer and exercise definitions, not benchmark IDs or expected answers. When adapting a rule, test the problem it is meant to solve and other offers that might be affected.

The tutorial uses a separate A2 scorer, without the job-specific rules. It performed less well in the tutorial evaluation. We include that result so you can see where further adaptation is needed.
