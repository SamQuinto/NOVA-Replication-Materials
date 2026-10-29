# Architecture figures

`Figure_2_Current_Architectures.svg` compares the latest evaluated job A1 and A2 configurations. `Figure_B2_Tutorial_Path.svg` shows the existing tutorial A2 path separately. SVG text and boxes can be edited in a vector editor. PNG copies are ready to inspect or insert into a manuscript.

Suggested caption: **Figure 2. Alternative scorer architectures in NOVA.**

Suggested note: The language model identifies the proposed issues and options; Python scripts apply researcher-defined scores. A1 receives every active issue definition. A2 retrieves possible issues and uses fitted reading rules. Script numbers identify processing stages rather than separate source files. The optional second tutorial reading is shown separately, not as part of the fitted one-call A2 job scorer.

`Figure_Content.json` records the figure text and feeds the Word builder. `Architecture_Figure_Editable.docx` provides a native Word text-and-box version of the main comparison. For vector changes, edit the SVG directly or edit and rerun `tools/build_figures_source.py`; that builder keeps its own layout and text definitions. The images contain no embedded figure number or caption.
