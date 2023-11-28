import json
from pathlib import Path
import hashlib
import re
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

def read_field_mapping(filepath: Path):
    with open(filepath, 'rb') as file:
        data = tomllib.load(file)
    fields = data['fields']

    result = {
        'source': {},
        'target': {}
    }

    for key, values in fields.items():
        if len(values) == 1:
            result['source'][key] = values[0]
            result['target'][key] = values[0]
        else:
            result['source'][key] = values[0]
            result['target'][key] = values[1]
    
    return result


def generate_flow_id(flow: dict):
    flow_str = json.dumps(flow, sort_keys=True)
    result = hashlib.md5(flow_str.encode('utf-8')).hexdigest()
    return result


def read_flowlist(filepath: Path):
    with open(filepath, 'r') as fs:
        result = json.load(fs)
    return result

def rm_parentheses_roman_numerals(x):
    pattern = r'\(\s*([IVXLCDM]+)\s*\)'
    return re.sub(pattern, r'\1', x)
