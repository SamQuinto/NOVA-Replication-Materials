# Replication notes

## Tested packaging changes

The portable runner adds paths, request preview, explicit live-call control, and environment-only key handling. The self-contained architecture folder uses four real numbered stage files. A1's request builder was moved into `A1-1.py`; A2's request construction was separated from its API call in `a2_extract.py`. Its selected default is Luna. The evaluated final prompt, custom-rule bodies and numerical scoring logic were not changed. The public wording dictionary removes origin annotations but keeps matching strings and runtime flags.

Sixteen offline tests cover previews, saved-interpretation scoring, the four named stage scripts, equality to the saved synthetic requests, compatibility with the top-level launch command, execution after renaming and moving the folder, and single-call A2 orchestration using a fake API. The outer-launcher test is skipped when only the architecture folder is copied. A private seeded sample of 100 saved interpretations per architecture/exercise combination was replayed again after the move: 400 cases in total. Decisions, valid pairs, role totals, novel terms and unsupported terms matched the evaluated records in all checks. No API call was needed. These checks support packaging parity on the sampled saved interpretations, not a new full-corpus accuracy claim or a guarantee of identical future model responses.

## Interpreting the two result sets

The job and tutorial evaluations use the same high-level A/B distinction but different datasets and reference-review implementations. The fitted job set and the new tutorial inputs are not a randomized comparison of customization, and they are not independent observations of one common population. Their estimates should not be added together as if the human cases were independent or their grading histories identical.

## Historical costs

The main table preserves the recorded development-run cost estimates. The tutorial uses its documented standard/cache-write sensitivity calculation. These are token-based estimates, not reconciled invoices. Before a formal cost comparison, use one explicit rate card for all saved token receipts and state the cache assumptions. Do not call the historic development ceiling or an unknown-billing receipt lock part of NOVA's scoring architecture. The portable runner has neither an inherited global spending ledger nor an implicit billing lock.

## License and data access

This public release does not publish participant records or imply permission to redistribute them. The authors should specify a software license and a separate human-data access process before the final archival release.
