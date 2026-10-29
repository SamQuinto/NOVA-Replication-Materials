# A2

**Customized, lower API cost.** The supplied job model is `gpt-5.6-luna` at low reasoning.

1. [A2-1.py](../code/A2-1.py) selects relevant issue definitions and prepares a request with the offer, role, prompt, role materials and exercise reading rules.
2. The LLM returns interpretation JSON. The current job path makes one model call, not a Nano-to-Luna escalation.
3. [A2-2.py](../code/A2-2.py) applies exercise-specific corrections and shared checks, looks up scores and returns scored JSON.

- [Interpretation prompt](../code/prompts/A2_Interpretation.txt)
- [Exercise reading rules](../code/frozen/A2_Reading_Rules.json)
- [Issue selection and request construction](../code/a2_extract.py)
- [Custom Python rules](../code/a2_custom_rules.py)
- [Finalization](../code/a2_finalize.py)
- [Detailed rule and code commentary](../docs/A2_Walkthrough.md)

Rules read proposal content and exercise definitions, never benchmark IDs or expected answers. Changing rules requires retesting affected cases and a regression sample.

A2's tutorial path is retained as evaluated. It does not use fitted job rules and performs less well in the tutorial evaluation. This release does not apply an untested tutorial repair.
