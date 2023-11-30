from flowmapper.flow import Flow
from flowmapper.match import match_biogenic_to_non_fossil

def test_match_biogenic_to_non_fossil():
    fields = {"name": "name", "context": "context"}
    s = Flow.from_dict({"name": "Oils, biogenic", "context": "air"}, fields)
    t = Flow.from_dict({"name": "Oils, non-fossil", "context": "air"}, fields)

    actual = match_biogenic_to_non_fossil(s, t)
    expected = {
        "comment": "Biogenic to non-fossil if no better match"
    }
    assert actual == expected
