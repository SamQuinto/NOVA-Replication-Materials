# Validation protocol

## The question being answered

Primary accuracy asks whether the scorer handled the ideas in an input without missing a meaningful idea or adding an unproposed issue. It does not ask whether the input reached an agreement, whether its total is positive, or whether a participant liked the result.

An incomplete proposal can be handled correctly. A low-value offer can be interpreted correctly. An out-of-range value can be correctly recognized and queried rather than forced into the nearest valid value.

## The checklist

1. **Coverage:** identify meaningful ideas despite ordinary wording, shorthand or spelling mistakes. Score clear table-supported choices. Ask a useful question when an essential detail is missing. Acknowledge a genuinely unrepresentable idea without points.
2. **Supported matching:** match a scored idea to the appropriate issue, option and assigned score. Keep quantities, people, conditions and units straight.
3. **No unproposed additions:** do not price, suggest, or acknowledge an optional issue the person did not actually introduce. Asking for an absent required issue is allowed.

The selected primary measure uses **Type A** and **Type B**. Type A is a missed idea or an unnecessarily unscored clear supported choice. Type B is an unproposed issue added. Wrong options, providers or amounts on a genuinely mentioned issue are monitored separately. This distinction prevents a wrong mapping from being automatically counted as an invented new idea, but it also means that primary accuracy is not full mapping accuracy.

## Reference interpretations

For the new tutorial evaluation, reference drafts were created from the original offer, role, prior context and exercise definitions before the reference model saw scorer outputs. A draft records the proposed idea, source quote, relevant issue, supported option when clear, and whether scoring, clarification or acknowledgement is appropriate.

The reference is not a requirement for an exact verbatim response. Different useful wording can satisfy the same checklist. It is an aid to deciding which ideas are present and which handling routes are defensible.

Drafting errors were retained in a change log and corrected after review. Examples include treating a conditional price ceiling as an exact replacement price, assigning every mention of volunteers to the organizer despite an explicit “your,” or mistaking a partial cancellation fee for complete non-refundability.

## Independent output review

A separate model reviewed the original offer, exercise information, reference and anonymized scorer outputs. It applied the same checklist to all three configurations. Flagged cases and a reproducibly selected sample of apparent passes received an advanced-model review. An assistant then examined important disagreements and recorded explicit corrections.

The final labels are **model-assisted and assistant-reviewed**. They are not independent human ground truth, and the advanced model's answer is not automatically ground truth. The researcher can change the workbook's Y/N flags. The Accuracy sheet recomputes from those editable flags.

All prompts used for reference drafting and checklist review are in `validation/`. Evaluation reviewers are not part of the live A1 scoring architecture. Do not draw them as an extra scorer call in Figure 2.

## Tutorial selection

The source contained 960 calculator inputs: 147 from October 20 and 813 from October 27. Removing 47 exact/formatting-only duplicates with the same role and prior context left 913. Of these, 165 were already in the saved tutorial development library and were separated. Seventeen non-offer fragments were separated. The final set contained 731 inputs from 134 participants, all from October 27.

Interpretable partial offers, errors, ambiguity, unsupported values and unusual ideas were retained. No case was removed because a scorer failed. Changing a number, date, condition or meaningful wording kept an input distinct. Related retries remain, so this is not 731 independent people or 731 wholly unrelated negotiation problems.

These inputs were absent from the saved development library under the stated matching rule. That alone does not prove a completely untouched holdout: the same exercise, predetermined practice offers and related wording had appeared during earlier work.

## Job evaluation

The selected main table contains 1,225 retained inputs. It prioritizes human pilot and role-feedback material, with one research-assistant offer included in the survey category. It is a fitted development set. Duplicate human records were retained; 1,089 role/text/context requests were distinct in the archived run.

The final A2 job rules were replayed on saved model interpretations. Their result must be called a fitted saved-interpretation evaluation, not fresh proof of 100% performance on future model responses. The public release does not include the private offers or answer key, and it does not silently replace them with synthetic examples.

## Computing the reported measures

- Primary passes: records with neither A nor B and no technical failure.
- Accuracy: primary passes divided by all retained evaluated inputs.
- Type A count: inputs flagged for A, whether or not B also occurs.
- Type B count: inputs flagged for B, whether or not A also occurs.
- Confidence interval: Wilson 95% interval using a retained input as the observation. It is not adjusted for participant clustering.
- Cost per 1,000 offers: sum of each input's scoring-call costs divided by the input count, multiplied by 1,000. Evaluation-model calls are excluded.
- Mean scoring time: average sum of API-response durations needed for each input. Queue, dispatch pacing and local processing are excluded.

Overlapping A/B errors must not be added as if they were different failed inputs. The existing A2 tutorial path had 146 A inputs and nine B inputs, with three overlapping, hence 152 failed inputs and 579 passes.

## What another researcher can reproduce

With the private saved checks, `tools/recompute_accuracy.py` reproduces the aggregation without model calls. With original interpretations, the scoring core reproduces numerical scoring without interpreting the offer again. With a key and `--live`, the runner makes a new model call, which may differ from the saved one.

Independent semantic validation requires access to the private offers and reviewed labels, with appropriate permission. The public repository is not a substitute for that access. It provides the architectures, prompts, exercise definitions, methods and synthetic executable examples.
