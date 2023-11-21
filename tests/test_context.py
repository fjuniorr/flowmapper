from flowmapper.context import Context

def test_context():
    data = {
        "name": "Carbon dioxide, in air",
        "categories": ["Raw", "(unspecified)"],
        "unit": "kg",
        "CAS": "000124-38-9",
    }
    fields = ["categories.0", "categories.1"]
    actual = Context.from_dict(data, fields).to_dict()
    expected = {'full': 'Raw/(unspecified)', 'primary': 'Raw', 'secondary': '(unspecified)'}
    assert actual == expected


def test_context_multiple_levels_list():
    data = {
        "name": "Carbon dioxide, in air",
        "categories": ["emission/air", ["troposphere", "high"]],
        "unit": "kg",
        "CAS": "000124-38-9",
    }
    fields = ["categories.0", "categories.1"]
    actual = Context.from_dict(data, fields).to_dict()
    expected = {'full': 'emission/air/troposphere/high', 'primary': 'emission/air', 'secondary': 'troposphere/high'}
    assert actual == expected

def test_context_multiple_levels_list():
    data = {
        "name": "Carbon dioxide, in air",
        "categories": "emission/air",
        "subcategories": ["troposphere", "high"],
        "unit": "kg",
        "CAS": "000124-38-9",
    }
    fields = ["categories", "subcategories"]
    actual = Context.from_dict(data, fields).to_dict()
    expected = {'full': 'emission/air/troposphere/high', 'primary': 'emission/air', 'secondary': 'troposphere/high'}
    assert actual == expected