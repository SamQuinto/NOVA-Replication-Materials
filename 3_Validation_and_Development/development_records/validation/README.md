# Validation prompts and request preparation

These prompts support interpretation-key drafting and checklist evaluation. They are not part of the live scorer's interpretation calls.

`Reference.txt` is used before viewing scorer outputs. Supply a list of records with `case_id`, `proposer_role`, `offer` and `previous_offer`. A case ID is a local evaluation label, not a participant identifier.

`Checklist_Review.txt` checks anonymized scorer outputs against the original input and exercise. Its request includes the original offer and role, relevant prior context, reference interpretation, and a `responses` object keyed by labels such as R1, R2 and R3. Use the same labels consistently. The evaluator returns separate A, B and mapping flags with reasons.

`Reference_Correction.txt` adds the source-review rules used to correct draft-reference errors. It should receive the original input, draft reference and review notes, not a desired pass rate. The original draft and changes should be saved separately.

```powershell
python prepare_review_request.py --task reference --exercise tutorial --input-json path/to/authorized_inputs.json
python prepare_review_request.py --task checklist --exercise tutorial --input-json path/to/authorized_review_input.json --advanced
```

These commands only print requests. Add `--live` deliberately to make a paid call with your own environment key. Low-cost review uses Luna at low reasoning; advanced review uses Sol at high reasoning. A returned model verdict remains a proposed classification for researcher review, not automatic ground truth.

The selected tutorial workflow escalated flags and sampled apparent passes. Earlier project work also explored multi-model committees; do not describe that historical approach as if every current tutorial result came from the same committee. See the protocol for the actual selected procedure.

For a fresh study, preserve original source inputs, reference versions, exact prompts, request settings, raw responses, usage receipts, semantic judgments and researcher overrides. Do not publish those human records by default, and never score only the easiest cases or resample an incorrect answer without labeling a new run.
