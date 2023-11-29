from flowmapper.flow import Flow
from flowmapper.context import Context
from flowmapper.match import match_names_with_country_codes


def test_match_names_with_country_codes():
    fields = {"name": "name", "context": "context"}
    s = Flow.from_dict({"name": "Ammonia, NL", "context": "air"}, fields)
    t = Flow.from_dict({"name": "Ammonia", "context": "air"}, fields)

    actual = match_names_with_country_codes(s, t)
    expected = {
        "source": {"name": "Ammonia, NL", "context": "air"},
        "target": {"uuid": None, "name": "Ammonia", "context": "air", "unit": None},
        "conversionFactor": 1,
        "comment": "Names with country code NL",
    }
    assert actual == expected
