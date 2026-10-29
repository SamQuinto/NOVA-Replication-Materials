# Development records

`validation/` contains the exact reference-drafting, correction and checklist-review prompts and schemas. They support the documented human/LLM review process; they are not live scorer prompts. Use the reviewed workbooks for final supplied classifications.

`results/` preserves earlier aggregate and packaging records for provenance. Their paths describe the earlier package layout and their historical mapping flags are not the manuscript's Type C measure. Current recomputed results are in the parent section's `results/` folder.

To preview a review request without a paid call, use `validation/prepare_review_request.py --help`. Live review needs your own environment key and explicit `--live`. A returned model judgment remains subject to researcher review; it is not automatically ground truth.
