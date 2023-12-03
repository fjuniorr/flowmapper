from flowmapper.flow import Flow
from flowmapper.flowmap import Flowmap

def test_match_non_ionic_state():
    fields = {"name": "name", "context": "context", "unit": "unit"}
    s = [
        Flow.from_dict({"name": "Mercury (II)", "context": "air", "unit": "kg"}, fields),
        Flow.from_dict({"name": "Manganese (II)", "context": "air", "unit": "kg"}, fields),
    ]
    t = [
        Flow.from_dict({"name": "Mercury", "context": "air", "unit": "kg"}, fields),
        Flow.from_dict({"name": "Manganese II", "context": "air", "unit": "kg"}, fields),
    ]

    flowmap = Flowmap(s, t)
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {"name": "Mercury (II)", "context": "air", "unit": "kg"},
            "target": {"uuid": None, "name": "Mercury", "context": "air", "unit": "kg"},
            "conversion_factor": 1,
            "comment": "Non-ionic state if no better match",
        },
        {
            "source": {"name": "Manganese (II)", "context": "air", "unit": "kg"},
            "target": {
                "uuid": None,
                "name": "Manganese II",
                "context": "air",
                "unit": "kg",
            },
            "conversion_factor": 1,
            "comment": "With/without roman numerals in parentheses",
        },
    ]
    assert actual == expected
