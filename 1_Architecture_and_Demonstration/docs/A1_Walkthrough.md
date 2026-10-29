# How Architecture 1 works

This guide follows an offer through Architecture 1 (A1), from the words a negotiator types to the score they see. File paths start from the architecture folder, so you can still follow them if you move that folder elsewhere.

## Offer data and exercise files

A negotiator enters ordinary text in a free-text box. The application supplies their assigned role. Negotiators do not write JSON. The caller can also supply a previous offer, but earlier terms are used only when the current words explicitly refer to them.

The role narrative is text inside `code/frozen/Role_Materials.json`. The full numerical scoring table is `code/frozen/Scoring_Table.json`. The model-facing version, `A1_Scoring_Definitions.json`, includes all active issues and options but omits numerical point-weight fields. Exercise information supplies requirements, defaults and conventions. A response schema defines allowed JSON fields. The general instructions are a separate text file, `code/prompts/A1_Final.txt`.

These files are brought together in one request, rather than sent as separate paid calls. The Python script reads their contents and includes them; the model does not open the files itself. Repeated content can receive a lower price through OpenAI's prompt caching, but the content is still sent. The tutorial uses its own exercise files under `code/frozen/tutorial/` with the same general prompt.

## Python script A1-1

`code/A1-1.py:prepare_request` combines these sources into one request object. The instruction portion contains the general prompt and named `EXERCISE_INFORMATION`, `SCORING_TABLE` and `ROLE_MATERIALS` blocks. The user portion contains `CURRENT_OFFER` (role and text) and `PREVIOUS_OFFER` (optional text). The response schema is attached separately within the same request. This script neither calls a model nor calculates points.

You choose the exercise and reasoning setting. Low and high reasoning use the same prompt and exercise information; the example model is `gpt-6.1-sol`. The response format helps keep the returned JSON consistent, but it cannot guarantee that the model understood the offer correctly.

## Advanced LLM

With explicit live authorization, `code/nova_cli.py` sends the prepared request through `code/common1225.py:api`. The model reads the offer, interprets its meaning using the supplied exercise context, and returns interpretation JSON. It does not invent point values or receive an answer key.

The interpretation includes issue/option pairs, exact source words and whether a term came from explicitly referenced previous text. It can also contain questions, novel terms and unsupported terms. It returns brief interpretation notes, not its private internal reasoning. There is no live reviewer model in this A1 template.

## Interpretation JSON

For the synthetic text “Salary $55,000; personal work-expense budget $10,000; starting date May 1,” a Salary pair selects `55000` and quotes the salary words. Starting Date selects a date representation, not a floating-point amount. A vague detail can produce a question. An idea absent from the supplied table can be retained without points.

The interpretation can pass directly to the next script without being saved as a file. Saving the request, interpretation and scored result is useful if you want to check what happened later, but it does not require three model calls.

## Python script A1-2

`code/A1-2.py:score_interpretation` loads `runtime/app/a1/backend/scorer.py`. Its finalizer checks supported issue names, quotation support, scope of previous-offer use, options and numerical domains. It dispatches dates, continuous quantities and discrete options to the appropriate scoring rules. It retrieves each role's assigned values and prepares display findings and totals. These checks reduce unsupported results but do not prove that every quoted phrase supports the model's meaning.

## Scored offer JSON

The returned JSON contains the interpreted terms, scores for each role and any messages. A complete, valid offer can have a total. If a required detail is missing, NOVA can still show the terms it understood without giving a final total. An offer can also contain a new idea that is acknowledged without points. The study interface decides what to show or submit; calculating a score does not mean both negotiators have accepted the offer.

## What each prompt block does

The exact text is in `code/prompts/A1_Final.txt`; the following explains it without replacing it.

1. **Opening and Inputs.** Separates interpretation from arithmetic and gives stable names to current text, optional previous text, role context and scoring definitions. Role context is not permission to add proposals.
2. **Read naturally.** Allows typos, shorthand, lists and varied punctuation. A short affirmative feature request can select its ordinary option. Negations and conditions still matter. This addresses missed ideas without requiring exact table wording.
3. **Match the meaning.** Chooses the actual requested property, not a nearby concept. Preserves amounts, units, actors, timing and conditions. It allows exercise-defined defaults and a clear replacement, but not a made-up amount or a combination of unresolved alternatives. An organized plan can request its underlying activity; the model need not replace it with a neighboring documentation feature.
4. **Handle what is unclear or unmatched.** Uses one useful question for an essential missing detail. Questions remain within the negotiator's idea, so they do not reveal unmentioned optional benefits. Genuinely unmatched ideas remain without points. Acknowledgement is not a substitute for scoring a clear supported option.
5. **Check every selection and every idea.** Requires exact source support for selected meanings and checks for omissions. Limits inheritance to explicit references. Treats instructions embedded in the offer as untrusted data. A real quote containing a related word is not, by itself, adequate semantic support.

## Customization and transfer

For a new exercise, prepare role narratives, issue/option definitions, units/defaults and numerical values in the exercise files. Keep the general prompt unchanged initially. Test a varied sample and inspect omissions, unproposed additions and mapping errors separately. If a proposed prompt change depends on a particular benefit, role name or month, it belongs in exercise data or a deliberately customized architecture rather than this general prompt. A clean prompt still needs validation on new material.
