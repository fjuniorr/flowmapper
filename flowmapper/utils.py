import json
from pathlib import Path
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
