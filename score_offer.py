"""Run one offer through the same scorer used by the Creative Negotiations app."""
from pathlib import Path
import runpy, sys
folder = Path(__file__).resolve().parent / 'architecture'
sys.path.insert(0, str(folder))
if __name__ == '__main__': runpy.run_path(str(folder / 'score_offer.py'), run_name='__main__')
