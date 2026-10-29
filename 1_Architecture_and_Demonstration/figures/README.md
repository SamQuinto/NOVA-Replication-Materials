# Architecture figures

`Figure_B1_NOVA_Architectures` shows how the job-negotiation versions of A1 and A2 process an offer. `Figure_B2_Tutorial_Path` shows A2's separate tutorial steps. Each figure has an image copy for the manuscript and an SVG you can edit in a vector editor.

Suggested caption: **Figure B1. NOVA scorer architecture templates.**

`Figure_B1_NOVA_Architectures_Compact` is a wider, shorter alternative: 1,770 × 1,873 pixels rather than 1,510 × 2,517. It retains every word, the original font sizes and the same arrows. The paired boxes stay aligned. Use the PNG as an image or the SVG for vector editing. The original diagram and Word file are unchanged.

The model identifies the proposed issues and options. The Python scripts then calculate the researcher-defined scores. A1 reads every active issue definition; A2 first selects potentially relevant issues and also uses exercise-specific instructions and rules. The numbered boxes refer to the scripts in `code/`. A2's optional second tutorial reading is shown separately because it is not part of the job scorer.

If you want to change the diagram text in Word, use `Architecture_Figure_Editable.docx`. From the architecture folder, run `python code/tools/sync_figure_from_word.py` to copy those edits into `Figure_Content.json`, then `python code/tools/build_figures_source.py` to update the SVG. Creating a PNG from the SVG is a separate step.

`code/tools/build_word_figure_source.py` can create a new Word layout from the JSON. Save any Word edits back to JSON before using it, so those edits are not overwritten. These figure tools may need extra document or graphics packages; you do not need them to run the NOVA web app. The images have no figure number or caption embedded in them.
