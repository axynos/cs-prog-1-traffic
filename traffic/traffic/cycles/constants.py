import os
import json

_script_dir = os.path.dirname(__file__)
_json_path = os.path.join(_script_dir, 'cycles.json')

# Load traffic cycle definitions from file.
with open(_json_path, 'r') as file:
    _cycles = json.load(file)

CYCLES = {
    'tl1': _cycles['cycle_tl1'],
    'tl2': _cycles['cycle_tl2']
}

DEFAULT_CYCLE_NAME = 'tl1'
DEFAULT_CYCLE = CYCLES[DEFAULT_CYCLE_NAME]