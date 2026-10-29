# NOVA replication materials

The self-contained scorer implementation is in [architecture/](architecture/). That folder can be renamed or moved into another replication package without relying on this repository's outer layout.

Start with:

- [One comprehensive LLM handoff](architecture/LLM_Architecture_Dump.txt)
- [Runnable examples and instructions](architecture/README.md)
- [The four named Python stages](architecture/docs/File_Map.md)
- [Edited Word figure and image files](architecture/figures/README.md)
- [Exact prompts](architecture/docs/Exact_Prompts.md)
- [Validation procedure](architecture/docs/Validation_Protocol.md)
- [Aggregate results](architecture/results/aggregate_results.json)

The main figure uses these exact headings: **A1 - Flexible, Higher API cost** and **A2 - Customized, Lower API cost**. Its numbered boxes map to `architecture/A1-1.py`, `architecture/A1-2.py`, `architecture/A2-1.py` and `architecture/A2-2.py`.

The top-level `score_offer.py`, `score_tutorial_offer.py` and `nova_cli.py` remain compatibility launchers. The architecture folder does not depend on them. For example:

```powershell
python architecture/score_offer.py --architecture A1 --case-json examples/job_offer.json
python architecture/score_offer.py --architecture A2 --case-json examples/job_offer.json
python -m unittest discover -s architecture/tests -v
```

These commands do not call an API. A paid model call requires `--live` and a key supplied through the environment. No credentials or participant-level offers, validation keys or review workbooks are published.

This repository is separate from [Joshua's Empirica deployment package](https://github.com/SamQuinto/Creative-Negotiations-Materials/tree/main/empirica). The reorganization does not change that package, the study server or the manuscript.

The public code can prepare requests and score saved or synthetic interpretations. Independently recoding the human validation data requires authorized private access. A new model response is not guaranteed to match a saved response. The reported A/B measure is also not complete option-and-score accuracy.

Public visibility does not itself grant a reuse license. The authors should choose software licensing and human-data access terms before formal archival release.
