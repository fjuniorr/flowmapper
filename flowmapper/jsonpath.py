from glom import Coalesce, glom


def extract(expr, data):
    return glom(data, Coalesce(expr, default = ''))
