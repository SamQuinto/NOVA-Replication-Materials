# A1

**Flexible, higher API cost.** The supplied model is `gpt-6.1-sol`, evaluated at low and high reasoning.

1. [A1-1.py](../code/A1-1.py) combines offer text, role, optional referenced previous offer, role materials, all active issue definitions and the prompt into one request. It makes no API call.
2. [nova_cli.py](../code/nova_cli.py) sends that request when `--live` is supplied. The model returns interpretation JSON containing issues, options, quotes, questions and unmatched ideas.
3. [A1-2.py](../code/A1-2.py) checks that interpretation, retrieves researcher-defined values and returns scored JSON.

The LLM interprets; Python calculates points. Model-facing definitions omit numerical point-weight fields. Role narratives can contain illustrative scores, so this is not a claim that the model sees no valuation information.

- [Exact general prompt](../code/prompts/A1_Final.txt)
- [Role materials](../code/frozen/Role_Materials.json)
- [Model-facing definitions](../code/frozen/A1_Scoring_Definitions.json)
- [Full scoring table](../code/frozen/Scoring_Table.json)
- [Component and prompt commentary](../docs/A1_Walkthrough.md)

The tutorial uses the same general prompt. Exercise content is supplied separately as data. This is an evaluated template, not a guarantee of perfect transfer to every new exercise without validation.
