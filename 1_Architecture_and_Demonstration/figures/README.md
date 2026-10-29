# Architecture figures

`Figure_B1_NOVA_Architectures.svg` compares the latest evaluated job A1 and A2 configurations. `Figure_B2_Tutorial_Path.svg` shows the existing tutorial A2 path separately. SVG text and boxes can be edited in a vector editor. PNG copies are ready to inspect or insert into a manuscript.

Suggested caption: **Figure B1. NOVA scorer architecture templates.**

Suggested note: The language model identifies the proposed issues and options; Python scripts apply researcher-defined scores. A1 receives every active issue definition. A2 retrieves possible issues and uses fitted reading rules. The four main numbered script boxes correspond to `A1-1.py`, `A1-2.py`, `A2-1.py` and `A2-2.py`. The optional second tutorial reading is shown separately, not as part of the fitted one-call A2 job scorer.

`Architecture_Figure_Editable.docx` is the editable text-and-box master. From the architecture folder, run `python code/tools/sync_figure_from_word.py` after editing it, then `python code/tools/build_figures_source.py` to update the SVG from `Figure_Content.json`. Rasterizing the SVG is a separate optional image step. `code/tools/build_word_figure_source.py` can build a fresh editable Word layout from JSON, but should not overwrite unsynchronized Word edits. Figure-generation tools may need their own document/graphics packages; these are not dependencies of the scorer demonstration. The images contain no embedded figure number or caption.
