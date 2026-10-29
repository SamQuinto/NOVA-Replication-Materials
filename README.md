# NOVA replication materials

NOVA interprets offers written in ordinary language and assigns researcher-defined scores. This package provides the two scorer templates, the exercises, and de-identified records used to evaluate them.

| Folder | Contents |
| --- | --- |
| [1 Architecture and demonstration](1_Architecture_and_Demonstration/) | A1 and A2, exact prompts, Python scripts, editable architecture figure, local demonstration |
| [2 Exercise materials](2_Exercise_Materials/) | Job and tutorial role materials in Word and PDF, scoring tables, study questionnaires |
| [3 Validation and development](3_Validation_and_Development/) | Reviewed offer workbooks, anonymous human data, executed analysis notebook and HTML, results and figures |

## Try NOVA

Download the repository, or the complete `1_Architecture_and_Demonstration` folder. With Python 3.11 or later:

```sh
cd 1_Architecture_and_Demonstration
python demo/Start_Demo.py
```

The saved example is free and needs no API key. To score your own offers, copy `.env.example` to `.env` in that folder and replace the placeholder with your own key. Never upload `.env`. The demonstration needs no additional Python packages.

## Reproduce the results

Open [the executed analysis](3_Validation_and_Development/Analysis.html) or [the notebook](3_Validation_and_Development/Analysis.ipynb). Recomputing the results makes **no API calls**. Workbook accuracy sheets also calculate directly from the reviewed Y/N flags.

The main evaluation contains 1,225 inputs; the separate tutorial evaluation contains 731. These include calculator retries and incomplete inputs, not exclusively proposals sent to a counterpart. [Methods](3_Validation_and_Development/Methods.md) explains the populations and definitions.

## Privacy and versions

Human rows are published with researcher authorization after a privacy review. Direct identifiers, contact details, exact timestamps and private paths are excluded or redacted. Originals and the identity crosswalk remain private. See the [privacy review](3_Validation_and_Development/Privacy_Review.md).

This release preserves the evaluated prompts, scoring code and historical exercise snapshots. It does not retune the scorers or change the separate Empirica deployment repository. New model responses can differ from saved responses. Primary accuracy concerns Types A and B, not an exhaustive independent audit of every numerical mapping.

For appendix writers: [Appendix C replication guide](Appendix_C_Replication_Guide.txt) explains navigation and reproduction; [the architecture handoff](1_Architecture_and_Demonstration/LLM_Architecture_Dump.txt) gives the detailed Appendix B walkthrough, prompt commentary and code references.
