from glom import glom, Coalesce

def extract(expr, data):
    return glom(data, Coalesce(expr, default = ''))
