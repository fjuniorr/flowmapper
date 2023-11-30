from flowmapper.flow import Flow
from flowmapper.flowmap import Flowmap

def test_match_non_ionic_state():
    fields = {"name": "name", "context": "context"}
    s = [
        Flow.from_dict({"name": "Mercury (II)", "context": "air"}, fields),
        Flow.from_dict({"name": "Manganese (II)", "context": "air"}, fields),
    ]
    t = [
        Flow.from_dict({"name": "Mercury", "context": "air"}, fields),
        Flow.from_dict({"name": "Manganese II", "context": "air"}, fields),
    ]

    flowmap = Flowmap(s, t)
    flowmap.match()
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {"name": "Mercury (II)", "context": "air"},
            "target": {"uuid": None, "name": "Mercury", "context": "air", "unit": None},
            "conversion_factor": 1,
            "comment": "Non-ionic state if no better match",
        },
        {
            "source": {"name": "Manganese (II)", "context": "air"},
            "target": {
                "uuid": None,
                "name": "Manganese II",
                "context": "air",
                "unit": None,
            },
            "conversion_factor": 1,
            "comment": "With/without roman numerals in parentheses",
        },
    ]
    assert actual == expected
