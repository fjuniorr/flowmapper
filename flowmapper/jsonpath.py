from glom import Coalesce, glom


def extract(expr, data):
    return glom(data, Coalesce(expr, default = ''))

def root(spec):
    result = None
    if isinstance(spec, str):
        result = spec.split('.')[0]
    else:
        try:
            result = next(iter(spec))
        except TypeError:
            pass
    return result
