from glom import glom

def extract(expr, data):
    return glom(data, expr)
