"""Compatibility import; the self-contained implementation lives in architecture/."""
from pathlib import Path
import importlib.util, sys
folder = Path(__file__).resolve().parent / 'architecture'
sys.path.insert(0, str(folder))
spec = importlib.util.spec_from_file_location('nova_architecture_cli', folder / 'nova_cli.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
run = module.run
main = module.main
a1_request = module.a1_request
a1_setup = module.a1_setup
a2_setup = module.a2_setup
if __name__ == '__main__': main()
