"""Generate one portable, comprehensive architecture handoff without API calls."""
from pathlib import Path
import ast, hashlib, json, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]

INTRO = '''NOVA ARCHITECTURE HANDOFF FOR APPENDIX B
Updated 29 October 2026

READ THIS FIRST
This is the single comprehensive handoff for an agent writing Appendix B. It explains the author's current architecture figure, the actual executable stages, the prompts and exercise files, the customization process, and the evaluation boundaries. The aim is a clear explanation that a reader can follow without this conversation.

All implementation paths in this handoff are RELATIVE TO THE ARCHITECTURE FOLDER. This means the folder containing A1-1.py, A1-2.py, A2-1.py, A2-2.py, score_offer.py, prompts/, frozen/, runtime/ and figures/. Its outer name and location do not matter. Do not turn these references into an absolute OneDrive path, a fixed parent repository layout or an assumed technical-supplement root. The package resolves its files from the scripts' own locations. The outer repository retains launch-command compatibility, but this folder does not depend on those launchers.

Use this framing: the architectures are templates that researchers can update as models and their own constraints change. A1 is the default, comparatively plug-and-play template driven by supplied exercise files. A2 adds substantial exercise-specific instructions and Python rules so that a cheaper model can be used. Configuration and validation are still necessary in both. Do not claim that any new exercise requires no work, or that the comparison has experimentally isolated every cost and transfer trade-off.

The figure headings are exactly:
A1 - Flexible, Higher API cost
A2 - Customized, Lower API cost

The main diagram is Figure B1. Appendix C points to replication files; Appendix D explains development and validation. Keep these roles separate when drafting. The detailed explanations below should be useful even if the appendix lettering changes later.

The author's other Word edits were preserved. Only the two approved headings and the final-output bullets were changed. The revised final box says that scores for interpreted terms can be returned, with totals when complete and valid, and that clarification questions and unscored ideas may also be present. A valid offer can retain a new unpriced idea; an incomplete offer can retain valid partial terms without a final total.

PUBLIC AND PRIVATE BOUNDARIES
The package contains code, prompts, exercise definitions, matching configuration, synthetic demonstrations and aggregate results. It does not publish participant-level offers, Prolific IDs, review workbooks, full human reference keys or API credentials. The examples used below are synthetic fixtures or explicitly marked teaching examples. Do not describe them as newly observed participant data. Independently auditing every reported human classification requires separately authorized private evidence.

HOW TO WRITE THE APPENDIX
Explain the flow in connected, plain-language paragraphs. Introduce each unfamiliar object before naming its code field. Keep the full prompts available as exact reference material, but explain what their themes do. Use scoring table, issue, option, offer and negotiator consistently. A Python script and a language-model call are different things; JSON is a data format, not automatically a file and not another model call. Keep the LLM's interpretation separate from Python's assigned arithmetic. Do not draw evaluation reviewers as live scorer components. Describe exercise-specific rules openly rather than implying they are general model reasoning or model-weight fine-tuning.

The first parts are the readable walkthrough. Later parts reproduce exact prompts, schemas, exercise examples and core code. A writer can read the walkthrough first and use the later parts to check every implementation claim.
'''

WALKTHROUGH = '''THE SHARED FLOW AND THE OBJECTS BETWEEN BOXES

A negotiator types an ordinary-language proposal into a free-text box. They do not write JSON. The application already knows their assigned role. When they ask to calculate an offer, the caller supplies that text and role to the scorer; calculation is not necessarily submission to the counterpart. A previous offer may be supplied if available. This is caller-provided context, not a complete automatic memory of the conversation.

Role materials are narrative text stored inside a JSON file. The scoring table is also JSON: it describes issues, options or numerical domains, and the researcher-defined values for each role. A text prompt is a separate file. A schema describes the fields expected in an interpretation. Python reads these files and places their contents into a model request. The LLM does not browse the researcher's folders or follow a GitHub URL to fetch them.

Three JSON objects occur at different stages: the request prepared for the LLM, the interpretation returned by the LLM, and the scored offer returned by Python. There are not three mandatory disk files or three automatic API calls. They can exist in memory. Saving them is useful for audit and replication, but is a separate logging choice. Several message blocks and a response schema can all be part of one request.

The model interprets what was proposed. Python retrieves the assigned values. This separation makes scores traceable to researcher choices, but it does not make every interpretation correct. A model can select the wrong meaning while returning perfectly valid JSON and a quote that really appears in the offer. Semantic validation is still needed.

A1 BOX 1: INITIAL INPUTS
The first box describes sources, not a model response. Offer text comes from the free-text box; the role comes from assignment by the experiment. frozen/Role_Materials.json contains contextual narrative, frozen/Scoring_Table.json contains the numerical scoring configuration, and prompts/A1_Final.txt contains the general interpretation instructions. The job profile also uses frozen/A1_Exercise.json, frozen/A1_Scoring_Definitions.json and frozen/SOURCE_FIRST_FORMAT.json. Their tutorial counterparts are in frozen/tutorial/.

For example, examples/job_offer.json packages the synthetic text “Salary $55,000; personal work-expense budget $10,000; starting date May 1.” with role Candidate and an empty previous_offer. This JSON is a convenient calling example, not a format imposed on the negotiator. A caller can supply equivalent text arguments instead.

If the current offer says “Keep everything from the previous offer, but change the salary to $60,000,” previous_offer must actually contain the relevant earlier text. Without it, the scorer cannot reconstruct the retained terms from memory. If the current input simply says a new salary without a reference, previous choices should not automatically be inherited. The assigned role identifies the scoring perspective; ordinary job terms describe the candidate's package unless an explicit duty assigns an action differently.

A1 BOX 2: PYTHON SCRIPT A1-1
A1-1.py is the real file corresponding to this box. Its prepare_request function reads the selected exercise files and prompt and constructs one JSON request. It makes no API call and assigns no points. The next stage receives that request object.

The stable instruction portion comes first. It contains the literal general prompt and separately named EXERCISE_INFORMATION, SCORING_TABLE and ROLE_MATERIALS blocks. The changing user portion contains CURRENT_OFFER, with proposer_role and text, and PREVIOUS_OFFER, with text. The response schema is supplied as the request's structured-output format. The schema constrains the shape of the answer; it does not perform an independent semantic check.

“Full scoring table” in the figure means that A1's model receives every active issue definition and available option, rather than a retrieved shortlist. The model-facing definitions are in frozen/A1_Scoring_Definitions.json. Numerical point-weight fields are omitted from that view; Python uses frozen/Scoring_Table.json for scoring. Role narratives can themselves mention illustrative points. Therefore write that Python determines the assigned score, not that the model receives every numerical weight or never sees any information about values.

Repeated stable prompt and exercise content can benefit from provider-side caching. The model still receives the request content; the code is not merely sending a filename and relying on a remembered attachment. Caching is not local answer reuse. The low and high A1 configurations use the same prompt and data layout and differ in the reasoning setting.

A1 BOX 3: ADVANCED LLM
nova_cli.py sends the prepared request through common1225.api when live use is explicitly requested. The selected model example is gpt-6.1-sol. It reads the original words, uses role and exercise context to resolve their meaning, and selects supported issues and options from the supplied definitions. It normalizes values where the exercise conventions allow it, asks about genuinely missing essential details, and retains an idea without points when no table entry can represent it.

The model must not add a benefit merely because a related topic appears in the role narrative or a scoring-table entry. For example, proposing a learning goal is not automatic permission to add every related training, funding, mentoring and review arrangement. Conversely, a meaningful proposed feature should not be missed solely because it is loosely phrased or misspelled. The source-support instructions apply to questions as well as priced terms: a leading question about an unmentioned optional issue can reveal that issue.

The response is structured interpretation JSON. The model is not asked to invent point values. Increasing reasoning effort is an API setting for this interpretation call, not a separate reviewer or a guarantee that the answer improves. The response contains the requested interpretation and supporting words, not private internal reasoning.

A1 BOX 4: INTERPRETATION JSON
The model returns pairs containing issue, option, source_text and from_previous_offer. It can also return ambiguities, novel_terms, unsupported_terms, offer_intent, explicit_reference and brief interpretation_notes according to the supplied schema. A source_text quote should copy the offer's actual words; normalization belongs in option, not in an invented cleaned-up quote.

In the synthetic base example, the Salary pair selects 55000 and quotes “Salary $55,000.” The Starting Date pair selects the normalized date 2026-05-01 and quotes “starting date May 1.” A date is not a floating-point salary amount: the scoring core dispatches the value to its issue-specific scoring definition. A vague essential detail should appear as a useful short question rather than a made-up amount.

The interpretation can be correct even when an offer is incomplete. If an optional known issue lacks an essential amount, a targeted clarification can be the correct handling. If the idea cannot be represented by any issue or option, it can be retained without points. The numerical scoring stage must distinguish these cases from simply leaving a clear supported choice unscored.

A1 BOX 5: PYTHON SCRIPT A1-2
A1-2.py receives the interpretation plus the original offer, assigned role, previous-offer text if supplied, and the selected scoring configuration. It delegates to the preserved Scorer and interpretation.finalize functions. The original text is needed to check quoted support; this stage is not processing the model response in isolation.

Python checks known issue names, duplicate selections, supported quotations, referenced earlier text, valid options and numerical domains. It asks for confirmation when returned source support cannot be found. It rejects non-finite values rather than assigning arbitrary points. It identifies missing required issues and applies the configured policy on outside-table terms. These checks constrain the interpretation but do not prove that a quote semantically entails a selected option.

For accepted terms, score_pair looks up an option's assigned values or applies the configured numerical scoring function, separately for both roles. A final total is calculated when no blocking finding remains. The adapter converts this result to the fields expected by the interface. No second LLM is called here. The numerical rules and researcher-defined values, not an LLM's guessed utility, determine the result.

A1 BOX 6: SCORED OFFER JSON
The result retains interpreted terms and their individual scores. When complete and valid, it includes role-specific totals. If a required term is absent or an essential detail needs confirmation, valid partial terms can remain while the complete-offer total is withheld. A genuinely new unpriced idea can coexist with an otherwise complete scored offer. The two final-box bullets are therefore independent, not an either/or split.

This is a server-side response. Having both role totals in the response does not mean that both totals should be shown to each negotiator. The caller should show only the information intended for that role. “Scorable” also does not mean “both parties have accepted.” Agreement acceptance and the final experimental interface are separate from the flow ending at scored JSON.

A2 BOX 1: OFFER DATA AND EXERCISE FILES
A2 receives the same kinds of original offer text, assigned role and optional prior context. Its role materials and numerical table are separate exercise files. In addition, it uses matching vocabulary and exercise-specific reading guidance. The current matching dictionary is runtime/app/config/issue-phrase-registry.json. prompts/A2_Interpretation.txt supplies main instructions, while frozen/A2_Reading_Rules.json supplies themed exercise conventions.

The researcher prepares these resources using exercise design and development evidence. They do not manually choose the final issues for each incoming offer. Matching vocabulary can include wording learned from human and researcher tests; that makes it fitted configuration, not a general-purpose language model. It should be described honestly as such. The dictionary is not a published table of participant records, and its origin annotations were removed from this public package.

A2 BOX 2: PYTHON SCRIPT A2-1
A2-1.py prepares the request without calling a model. It configures the packaged runtime and calls a2_extract.build_request. That helper supplements retrieval text with a close spelling match when the exercise vocabulary supplies a clear candidate. stream._catalog then retrieves likely relevant issue definitions and options, including required anchors. The selected issue names become allowed issue names in the output schema.

This is where A2 differs from A1's full-definition request. Python chooses the candidates the model can see; it does not yet assign the offer's final interpretation. A failure to retrieve a relevant optional issue can limit the model downstream. The model still receives the original offer for source support, not a fabricated corrected quotation.

The one request combines proposer_role, current_offer, previous_offer, scoring_table, exercise_reading_rules and role_materials with the A2 prompt and structured response schema. The extra reading instructions are data in this request, not a second model call. A2's request uses a different API message envelope from A1; that transport detail is not a separate conceptual architecture step.

A2 BOX 3: ECONOMICAL LLM
The selected main job configuration uses one gpt-5.6-luna call at low reasoning. It identifies supported issues and options among the retrieved definitions and returns quoted support, questions and unpriced ideas. It does not escalate from Nano to Luna. The older runtime still contains escalation-related code for traceability, but the current runner explicitly selects the single-model path.

The general A2 prompt controls interpretation style and source support. The reading-rules JSON supplies job-exercise conventions such as annual vacation, weekly remote working, month/day date interpretation, and distinctions between neighboring benefits. Those details are customization. They must not be copied into A1's general prompt while claiming that A1 remains exercise independent.

A2 BOX 4: INTERPRETATION JSON
The raw interpretation contains supported pairs and other findings. a2_extract.finish_extraction preserves the evaluated bookkeeping: it records usage/model information and represents detailed ambiguity objects consistently for downstream rules. This reshaping is not another interpretation call. It does not determine points.

The main fields correspond to A1's conceptual interpretation, although helper metadata and the internal representation of ambiguities differ. Saving the original raw response and its normalized object separately is useful for audit. An issue omitted by the model can sometimes be recovered by a supported exercise-specific rule, but the existence of that repair should be recorded rather than attributed to the original model response.

A2 BOX 5: PYTHON SCRIPT A2-2
A2-2.py receives the current case and interpretation and calls a2_finalize.finalize. That function applies a2_custom_rules.customize, then the shared quotation, option and scoring checks. The custom Python rules can recover exact literal support, apply a defined exercise convention, repair an option selection or replace an unresolved choice with a useful question. The result records custom_rule_trace so the repair is inspectable.

For example, the actual rules recover harmless quotation changes without inventing words, recognize explicitly stated durations and attached-unit wording, distinguish receiving training from training colleagues, preserve who performs a recruitment-fair duty, and ask for a missing health-insurance contribution. They also distinguish a professional-development budget from training-program participation. Exact examples and the full custom-rule source appear later in this handoff. These repairs are not universal rules and are not guaranteed to transfer to a different exercise.

The final job implementation does not simply reapply every older lexical rejection rule after the model. It uses its selected custom interpretation rules followed by the shared finalizer. The finalizer retrieves the assigned values and calculates totals. Model weights are unchanged. A researcher or coding agent is changing prompt text, exercise guidance, vocabulary or Python code, not fine-tuning an LLM.

A2 BOX 6: SCORED OFFER JSON
The same complete-versus-partial output logic applies. The result includes scored interpreted terms, totals when complete, findings and unpriced material where present. The custom-rule trace is additional audit information, not an extra benefit or negotiator message. Primary A/B accuracy should be assessed on what the negotiator is actually told, not only on the raw model response before the fitted repairs.

THE SEPARATE TUTORIAL PATH
The tutorial is a venue negotiation, not the job exercise. Its nine issues are configured in frozen/tutorial/Scoring_Table.json. Internal Candidate and Recruiter identifiers correspond to Organizer and Venue Manager. A1 uses the same general prompt but different exercise files. The existing A2 tutorial path uses stream.llm_extract and stream.score and does not apply the job-specific A2 custom patch.

For a dense tutorial offer, the existing code can make a second independent Luna read. That model sees the original offer and context, not the first answer. Python merges readings and flags conflicts. This is not escalation to a stronger model and not a reviewer loop in the default A1. Figure_B2_Tutorial_Path.svg documents it separately. Its labels refer to existing tutorial functions; the four main numbered .py files correspond to the main Figure B1 flow.

CUSTOMIZATION AS A REPRODUCIBLE PROCESS
Keep the original input and output first. Identify the error's broader cause rather than inserting a special case keyed to a participant or case ID. Decide the intended interpretation using exercise definitions and researcher conventions. For A1, improve a generally applicable interpretation instruction without inserting this exercise's issue names or numerical defaults. For A2, choose among the matching dictionary, reading guidance and a supported Python repair.

Then add contrasting tests. If a rule handles a positive request, also test its negation; if it handles attached units, change punctuation and order; if it maps one benefit, test a neighboring benefit that should not be added. Replay saved interpretations to test deterministic scoring changes. Make fresh model calls only for affected interpretation changes or a planned fresh comparison. Keep versions and do not silently overwrite the original key, prompt, response or researcher override.

No finite development set establishes that all future natural-language proposals will be handled correctly. Near-perfect fitted A/B accuracy is useful development evidence but not a universal guarantee. A new exercise, model, prompt, reading-rule file or numerical definition can require renewed validation. A2's lower per-call cost must be weighed against human/agent development effort; these records do not provide a controlled monetary estimate of all researcher setup time.

THE THREE VALIDATION PRINCIPLES AND THE PRIMARY A/B MEASURE
The intended principles are coverage of meaningful ideas, correct matching to supported options and assigned scores, and no unproposed additions. A useful clarification can correctly handle an essential missing detail; an acknowledged genuinely unrepresentable idea can be correct without points. Different wording can satisfy the same principle, so an expected interpretation is not a requirement to reproduce an exact sentence.

The selected primary measure counts Type A (a missed idea or an unnecessarily unscored clear supported choice) and Type B (an unproposed issue added). Type B can include a leading question or acknowledgement that introduces an optional feature the negotiator never proposed. Asking for an absent required issue is allowed. A wrong option, amount or actor within an actually mentioned issue is a separate mapping concern, not automatically an invented new issue.

Primary pass = no Type A and no Type B and no technical failure. An input with both A and B is one failed input, not two failed observations. Accuracy = primary passes / retained inputs. Report separate A and B counts, the overlap when relevant, and a Wilson 95% interval if treating inputs as observations. Related retries and multiple inputs per person mean that this is not a participant-cluster-adjusted interval.

The historical reference workflow is model-assisted and assistant-reviewed. Reference drafts, low-cost checks, advanced checks and researcher corrections support a reproducible review process, but an advanced model is not automatically ground truth. A researcher should be able to inspect the original offer, scorer response, proposed error flags and reasons and override them. Public code-and-prompts alone cannot independently establish the correctness of every private human classification.

THE EVALUATION RESULTS AND WHAT THEY DO NOT ESTABLISH
The main 1,225-input results are fitted development evidence. The final A2 Python rules were applied to saved model interpretations. The main set retained duplicate human records; 1,089 role/text/context requests were distinct in the archived evaluation. Do not describe those final rules as achieving independently verified accuracy on an untouched holdout.

The tutorial comparison retained 731 new-to-the-saved-library inputs after the documented filtering. They came from 134 participants, with related wording and retries still present. These records differ from the fitted main exercise and its reference history. Their performance does not isolate the causal effect of customization and should not be pooled with main results as one independently sampled population. Mapping flags are monitored separately and are not verified full numerical-accuracy rates.

Cost per 1,000 offers uses scoring-call costs only: sum scoring API costs / number of offers * 1,000. Validation-model calls are a separate research expense. For a multi-call tutorial input, sum both scoring calls before averaging. Mean API scoring time similarly sums required call durations per input and averages across inputs; it excludes queue pacing, user time and local processing. Cost estimates use saved token usage and stated rate/cache assumptions; they are not reconciled invoices or a claim about permanent provider pricing.

An uncached input token, cached input token and output token can have different prices. The usual calculation is ((input - cached input) * input rate + cached input * cached rate + output * output rate) / 1,000,000. Cache-write or cache-rate uncertainty should be shown separately. Do not infer the cost per person without specifying how many calculator inputs a person makes; a participant is not an API call.

KNOWN CONFIGURATION BOUNDARY
The frozen job agreement metadata retains historical inconsistent fields: a nonnegative-each-party flag appears alongside strict-positive comparison fields. The researcher's stated study rule was nonnegative scores. This release preserves historical files rather than silently changing experiment settings. The architecture diagram ends at score output and does not establish final agreement acceptance. A deployment needs an explicit consistent agreement configuration. Do not turn a score-validity statement into a claim that the platform will permit agreement under a particular threshold without checking that deployment.

RUNNING THE PACKAGE
Run Python 3.11 or later from the architecture folder. No pip install is required for scoring and request preparation. Optional figure authoring uses python-docx and image rendering tools. Preview and replay do not need a key. Live scoring needs OPENAI_API_KEY and an explicit --live flag. No old shared cost-guard ledger or unknown-billing lock is required by the replication runner. Do not embed a real key in a file, prompt, issue, screenshot or commit.

Each named stage can be run alone: A1-1.py or A2-1.py with --case-json prepares a request; A1-2.py or A2-2.py with --case-json and --interpretation-json scores a supplied interpretation. The main score_offer.py command connects the stages and makes the model call only with --live. A1's named stages support job and tutorial profiles; A2's four-box main route is job specific, while score_tutorial_offer.py invokes the existing tutorial A2 route.

Use a fresh command-line process for an exercise run; the retained engines have module-level exercise state. The portable folder does not need the outer repository, a OneDrive path or an assumed working directory. User-supplied output paths remain the caller's choice. The package's internal files are resolved from the script folder. The root compatibility launchers are conveniences, not hidden dependencies.

WHAT THIS REORGANIZATION CHANGED
The four main numbered stages became actual Python files and the package moved into one portable folder. A1 request construction was moved without changing its payload. A2 request construction was separated from the API call, keeping the selected Luna request and response bookkeeping. The custom-rule bodies, numerical scoring logic and selected A1 prompt were not retuned. Saved synthetic requests, named-stage tests, relocated-folder checks and sampled saved-response scoring are the appropriate checks for this structural change. They are not a new paid fresh-response accuracy experiment.
'''

PROMPT_NOTES = '''A1 PROMPT COMMENTARY BY THEME

Opening instruction and named inputs. The opening gives the model one job: interpret CURRENT_OFFER and return the prescribed structure. It says a separate script calculates points. The named inputs distinguish present words, prior context, narrative context and available issue definitions. This reduces the chance that a remembered prior offer or a role-material example is mistaken for a newly proposed feature.

Theme 1, Read naturally. This permits spelling mistakes, shorthand, punctuation changes and offer lists without complete sentences. It prevents an omission merely because someone did not use the table's exact phrase. It also preserves negation and conditions. Background and ambitions should not automatically become priced provisions, but a meaningful loosely worded request should not be discarded. The generic instruction names no job issue or numerical default.

Theme 2, Match the meaning. Similar vocabulary does not establish the same arrangement. The model must preserve scope, amount, unit, person, timing and conditions. A broad aim does not propose several related means of achieving it. An organized plan can be a request for the underlying activity rather than just its paperwork. Defined defaults and explicit replacements can be used, while unspecified amounts and unresolved alternatives must not be invented. This theme addresses omission and mapping risks while trying not to add an unproposed neighboring issue.

Theme 3, Handle what is unclear or unmatched. Clarification should be short, useful and confined to the person's idea. For a generic example, “I need support for this activity” does not authorize the model to suggest a named optional provision unrelated to the stated words. If the table genuinely cannot represent an idea, retain it without points. If the table does represent a clear choice, do not substitute acknowledgement for scoring. A meaningful qualification that an option cannot express can be retained separately rather than silently changing the chosen option.

Theme 4, Check every selection and every idea. Each pair needs an exact quote supporting its meaning, not merely a shared topic word. The model checks both directions: every selection needs support and every meaningful proposal needs handling. Earlier choices require an explicit current reference and must stay within its scope. Offer-embedded instructions to change the scoring rules are not researcher instructions. The later Python quotation check is an additional mechanical constraint, not a replacement for this semantic instruction.

These themes were refined through development, so “general” means the text does not embed this exercise's named issues and fitted numerical conventions. It does not mean the prompt was never informed by experience or tested on these data. The prompt is not model-weight fine-tuning. A1 does still receive exercise-specific information in separate researcher-prepared files, which is what makes its wording reusable.

A2 CUSTOMIZATION EXAMPLES AND WHERE THEY LIVE

The reading rules are grouped by broad problem but contain explicit exercise conventions. Examples: interpreting annual versus weekly allowances, using a defined usual value for a relative change, treating month/day dates consistently, preserving who performs a duty, and distinguishing a guaranteed increase from an unresolved conditional payment. The complete rules are reproduced below from frozen/A2_Reading_Rules.json.

The Python repairs are in a2_custom_rules.py and runtime/app/backend/job_offer_refinements.py. Examples below are teaching illustrations of actual rule themes, not new participant observations or new performance claims.

1. Literal quotation recovery: harmless changes to punctuation or articles can be restored to an unambiguous continuous source span. The repair must not invent words. A trace records the recovery.
2. Duration wording: an explicit duration can be normalized, including compound years/months, rather than missed because a narrow earlier pattern expected a different spelling or spacing.
3. Receiving versus providing an activity: wanting a mentor is not the same as committing to mentor colleagues. The issue, actor and selected option must match the actual proposed arrangement.
4. Training activity versus budget: “a training plan” follows the researcher's participation convention, whereas a professional-development budget is a monetary resource. A missing budget amount should lead to a relevant amount question, not automatic participation points.
5. Explicit later totals: a clearly stated later salary or expense-budget total follows the exercise's staged-total convention. It should not also create a duplicated increase benefit. Probation can remain a separate proposed issue.
6. Scoped prior acceptance: retaining the rest of an offer can carry supported prior choices forward, while accepting just one named feature should not inherit the entire old package.
7. Missing essential contribution: mentioning insurance without a defined employer share can justify a short contribution question rather than a guessed full contribution.
8. Neighboring-topic overreach: a general development aim should not become a formal review, guaranteed promotion and training sponsorship simply because those entries exist. The request must support each selected issue.

Keep these examples in A2's explanation. They are not text to insert into A1's general prompt. For a new exercise, researchers need to identify its own ambiguity and default conventions, record why a repair is justified, and test both the intended positive case and cases that should not trigger it.
'''

def read(relative): return (ROOT/relative).read_text(encoding='utf-8-sig')
def section(parts,title,body): parts.append('\n\n'+'='*78+'\n'+title+'\n'+'='*78+'\n\n'+body.strip()+'\n')

def main():
    parts=[INTRO]
    section(parts,'1. THE AUTHOR\'S TEMPLATE FRAMING',read('docs/Template_Overview.md'))
    section(parts,'2. COMPLETE BOX-BY-BOX WALKTHROUGH',WALKTHROUGH)
    figure=json.loads(read('figures/Figure_Content.json'))
    exact=[]
    for name, spec in figure['main'].items():
        exact.extend(spec['header'])
        for number,(title,body) in enumerate(spec['boxes'],1):
            exact.append('\nBox '+str(number)+': '+title+'\n'+'\n'.join('• '+x for x in body))
    section(parts,'3. EXACT WORDING IN THE AUTHOR\'S CURRENT FIGURE B1','\n'.join(exact))
    section(parts,'4. A1 INSTRUCTION THEMES AND A2 CUSTOMIZATION',PROMPT_NOTES)
    section(parts,'5. FILE-TO-STAGE MAP',read('docs/File_Map.md'))
    section(parts,'6. EXTENDED IMPLEMENTATION HANDBOOK',read('docs/Appendix_B_Writer_Handbook.md'))
    section(parts,'7. VALIDATION AND REVIEW PROCEDURE',read('docs/Validation_Protocol.md'))
    section(parts,'8. FLOWCHART LOGIC CHECK',read('docs/Flowchart_Logic_Check.md'))
    section(parts,'9. PACKAGING AND REPLICATION LIMITATIONS',read('docs/Replication_Notes.md'))
    section(parts,'10. EXACT SELECTED SCORER PROMPTS','These are the actual file contents, not paraphrases. Low/high A1 use the same main prompt. Tutorial A2 instructions belong to its separate existing path.')
    for file in ['prompts/A1_Final.txt','prompts/A2_Interpretation.txt','frozen/A2_Reading_Rules.json','prompts/A2_Tutorial_Standard.txt','prompts/A2_Tutorial_Completeness.txt']:
        section(parts,file,read(file))
    section(parts,'11. EXACT VALIDATION INSTRUCTIONS','These prompts evaluate responses and draft or correct references. They are not extra live A1 scorer calls and do not automatically establish human ground truth.')
    for file in ['validation/Reference.txt','validation/Checklist_Review.txt','validation/Reference_Correction.txt','validation/Reference_Format.json','validation/Checklist_Format.json']:
        section(parts,file,read(file))
    section(parts,'12. EXERCISE OBJECTS AND RESPONSE SCHEMAS','The complete job scoring table remains in frozen/Scoring_Table.json. The model-facing complete definitions are in frozen/A1_Scoring_Definitions.json. The counterpart tutorial files are in frozen/tutorial/. Do not replace those definitions with this illustrative subset.')
    for file in ['frozen/A1_Exercise.json','frozen/Role_Materials.json','frozen/SOURCE_FIRST_FORMAT.json','frozen/tutorial/A1_Exercise.json','frozen/tutorial/Role_Materials.json','frozen/tutorial/OUTPUT_FORMAT.json']:
        section(parts,file,read(file))
    table=json.loads(read('frozen/Scoring_Table.json'))
    defs=json.loads(read('frozen/A1_Scoring_Definitions.json'))
    names=['Salary','Personal Budget','Starting Date','Professional Training Program','Professional Development Budget','Role in Recruitment Fair','Mentorship Program']
    section(parts,'Selected actual job scoring-table entries',json.dumps([i for i in table['issues'] if i['name'] in names],ensure_ascii=False,indent=2))
    section(parts,'Matching model-facing definitions for the same examples',json.dumps([i for i in defs if i['name'] in names],ensure_ascii=False,indent=2))
    section(parts,'All active job issue names','\n'.join(str(i)+'. '+item['name'] for i,item in enumerate(table['issues'],1)))
    section(parts,'13. SYNTHETIC END-TO-END DEMONSTRATIONS','The input and interpretation fixtures below were written for reproducible offline demonstrations. They are not a fresh model result or a sampled human case. Prepared full requests are available in examples/A1_Job_Request.json, examples/A2_Job_Request.json, examples/A1_Tutorial_Request.json and examples/A2_Tutorial_Request.json.')
    for exercise in ['job','tutorial']:
        for suffix in ['offer','interpretation']:section(parts,f'examples/{exercise}_{suffix}.json',read(f'examples/{exercise}_{suffix}.json'))
        for architecture in ['A1','A2']:
            command=[sys.executable,str(ROOT/('score_offer.py' if exercise=='job' else 'score_tutorial_offer.py')),'--architecture',architecture,'--case-json',str(ROOT/f'examples/{exercise}_offer.json'),'--interpretation-json',str(ROOT/f'examples/{exercise}_interpretation.json')]
            run=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',timeout=40,check=True)
            response=json.loads(run.stdout)['response']
            keys=['decision','valid_pairs','issue_breakdown','total_for_proposer','total_for_receiver','message','findings','novel_terms','custom_rule_trace']
            section(parts,architecture+' '+exercise+' offline output excerpt',json.dumps({k:response[k] for k in keys if k in response},ensure_ascii=False,indent=2))
    section(parts,'14. RECORDED AGGREGATE RESULTS',read('results/aggregate_results.json'))
    section(parts,'15. SELECTED EVALUATION PROVENANCE',read('results/evaluation_provenance.json'))
    section(parts,'Current offline packaging checks',read('results/packaging_checks.json'))
    section(parts,'16. REPLICATION COMMANDS AND SAFETY',read('README.md'))
    section(parts,'17. CORE EXECUTABLE SOURCE','The following source is included so a writing agent can inspect the actual transformations. The large shared numerical engines are referenced by path in the inventory rather than duplicated twice. Full source is in the architecture folder.')
    sources=['A1-1.py','A1-2.py','A2-1.py','A2-2.py','nova_cli.py','stage_support.py','runtime_setup.py','common1225.py','a2_extract.py','a2_finalize.py','a2_custom_rules.py','runtime/app/backend/job_offer_refinements.py','runtime/app/a1/backend/interpretation.py','runtime/app/a1/backend/scorer.py','tools/recompute_accuracy.py','tools/build_validation_request.py']
    for file in sources:section(parts,file,read(file))
    section(parts,'18. HISTORICAL PROMPTS RETAINED FOR TRACEABILITY','These legacy runtime files are not the selected current general A1 prompt. Their existence must not be used to relabel the architecture or insert exercise-specific helper instructions into the selected A1 run.')
    for file in ['runtime/app/a1/prompts/general_interpretation.txt','runtime/app/a1/prompts/job_reading_notes.txt','runtime/app/a1/model_settings.json']:
        section(parts,file,read(file))
    inventory=[]
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or any(x in p.parts for x in ['__pycache__','local-output']):continue
        relative=p.relative_to(ROOT).as_posix()
        if relative in ['LLM_Architecture_Dump.txt','ARCHITECTURE_MANIFEST.json']:continue
        inventory.append(relative+'  ['+str(p.stat().st_size)+' bytes; SHA256 '+hashlib.sha256(p.read_bytes()).hexdigest()+']')
    section(parts,'19. ARCHITECTURE FOLDER INVENTORY','Every path below starts inside the architecture folder. No item depends on the outer package name. ARCHITECTURE_MANIFEST.json contains the release hashes, including this handoff after generation.\n\n'+'\n'.join(inventory))
    section(parts,'20. FINAL WRITER CHECKLIST','Explain every box and the object passed onward. Use the four actual script filenames. Keep the researcher-defined numerical scoring separate from model interpretation. Keep A1 general instructions separate from A2 exercise conventions. Do not resurrect the historical Nano-to-Luna chain in the selected main A2. Keep optional tutorial rereading and evaluation review separate from the main diagram. Do not call model-assisted labels independent human ground truth or A/B accuracy full option-and-score accuracy. Do not promise perfect transfer, zero future errors, measured setup-time savings or an unqualified causal explanation of the performance difference. Link Appendix C to the files and leave detailed development and validation for Appendix D. Preserve the author’s plain, conversational explanations while adding enough detail for someone new to reproduce each stage.')
    output=ROOT/'LLM_Architecture_Dump.txt'
    output.write_text('\n'.join(parts),encoding='utf-8')
    print(json.dumps(dict(file=output.name,characters=output.stat().st_size,words=len(output.read_text(encoding='utf-8').split()),api_calls=0)))

if __name__=='__main__':main()
