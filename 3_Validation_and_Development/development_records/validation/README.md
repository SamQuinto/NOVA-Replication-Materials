# Prompts for reviewing scoring accuracy

These prompts helped us draft expected interpretations and review NOVA's responses. They are separate from the prompts used to score offers during a negotiation.

`Reference.txt` asks for an interpretation before the reviewer sees scorer responses. Supply the offer text, assigned role, any relevant previous offer, and a case label so you can match the result back to the input. That label is not a participant ID.

`Checklist_Review.txt` asks the reviewer to compare scorer responses with the original offer and exercise. Include the offer, role, prior context, reference interpretation and the scorer responses. Give the responses neutral labels such as R1, R2 and R3. The reviewer returns separate judgments and reasons for omissions, unproposed additions and option-mapping problems.

`Reference_Correction.txt` helps review a draft interpretation when a mistake is suspected. Give it the original input, the draft and the review notes. Keep both versions so you can see what changed. The goal is to correct the interpretation, not to obtain a particular accuracy percentage.

From this folder, you can prepare a request without calling a model:

```sh
python prepare_review_request.py --task reference --exercise tutorial --input-json path/to/your_inputs.json
python prepare_review_request.py --task checklist --exercise tutorial --input-json path/to/your_review_input.json --advanced
```

Only add `--live` if you want to make a paid call using your own environment key. The lower-cost review uses Luna at low reasoning; the advanced review uses Sol at high reasoning. Treat its decision as something to review, not automatically the correct answer.

For the tutorial evaluation, flagged cases and a sample of apparent passes received additional review. Earlier work also tried multi-model committees, but not every result came from the same review setup. Keep that distinction when describing the methods.

For a new study, save the original input and context, each reference version, the prompts and model settings, the responses and usage, and any researcher corrections. Share participant data only with permission and after checking privacy. Keep difficult inputs in the evaluation rather than removing them because a scorer struggled with them.
