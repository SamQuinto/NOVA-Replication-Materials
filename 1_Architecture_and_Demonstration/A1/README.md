# Architecture 1 (A1)

A1 is the more flexible template. It gives a stronger model every active issue and option in the scoring table, together with general instructions for reading an offer. The example model is `gpt-6.1-sol`, which we evaluated at low and high reasoning.

Here is how an offer moves through A1:

1. [Python script A1-1](../code/A1-1.py) brings together the offer, the negotiator's role, the exercise files and the prompt. If the offer refers to an earlier offer, that earlier text can also be included. The script prepares one request but does not call the model itself.
2. [The caller](../code/nova_cli.py) sends that request when live scoring is requested. The model returns its interpretation as JSON: the issues and options it identified, the words supporting them, and any questions or ideas it could not match.
3. [Python script A1-2](../code/A1-2.py) checks the interpretation, looks up the researcher's scores and returns the scored offer as JSON.

The model interprets the offer; the Python script calculates the points. The model receives issue and option definitions without the numerical scoring weights, although role materials can mention example scores.

You can inspect each part here:

- [General-purpose prompt](../code/prompts/A1_Final.txt)
- [Role materials](../code/frozen/Role_Materials.json)
- [Issue and option definitions sent to the model](../code/frozen/A1_Scoring_Definitions.json)
- [Full scoring table used to calculate points](../code/frozen/Scoring_Table.json)
- [Explanation of each step and prompt section](../docs/A1_Walkthrough.md)

The main exercise and tutorial use the same general prompt with different exercise files. To use A1 for a new exercise, prepare those files and test a varied set of offers before collecting data.
