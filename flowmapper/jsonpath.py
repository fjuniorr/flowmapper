from jsonpath_ng import parse

def extract(expr, data):
    matches = parse(expr).find(data)
    result = [match.value for match in matches]
    if len(result) != 1:
        raise Exception(f'JSONPath expression returned {len(result)} matches.')
    return result[0]
