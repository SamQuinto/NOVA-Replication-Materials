# Offline tests

Run `python -m unittest discover -s code/tests -v` from the architecture folder. These tests make no API calls.

| Filename | Description |
| --- | --- |
| [test_replication.py](test_replication.py) | Checks A1/A2 model requests, scoring calculations, named scripts and the saved Appendix A example. |
| [test_portability.py](test_portability.py) | Checks that the downloaded folder works after being moved and renamed. |
| [test_demo_materials.py](test_demo_materials.py) | Checks the role materials and saved examples used by the web app. |
