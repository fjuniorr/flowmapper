from deepdiff import DeepDiff
from flowmapper.flow import Flow
from flowmapper.flowmap import Flowmap

def test_match_non_ionic_state():
    fields = {"name": "name", "context": "context"}
    s = [
        Flow.from_dict({"name": "Ammonia, as N", "context": "air"}, fields),
        Flow.from_dict({"name": "AOX (Adsorbable Organic Halogens)", "context": "air"}, fields),
    ]
    t = [
        Flow.from_dict({"name": "Ammonia", "context": "air"}, fields),
        Flow.from_dict({"name": "AOX, Adsorbable Organic Halogen as Cl", "context": "air"}, fields),
    ]

    flowmap = Flowmap(s, t)
    flowmap.match()
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {"name": "Ammonia, as N", "context": "air"},
            "target": {"uuid": None, "name": "Ammonia", "context": "air", "unit": None},
            "conversionFactor": 1.2142857142857142,
            "comment": "Mapped name differences with unit conversions",
        },
        {
            "source": {"name": "AOX (Adsorbable Organic Halogens)", "context": "air"},
            "target": {
                "uuid": None,
                "name": "AOX, Adsorbable Organic Halogen as Cl",
                "context": "air",
                "unit": None,
            },
            "conversionFactor": 1,
            "comment": "Mapped name differences with unit conversions",
        },
    ]
    diff = DeepDiff(actual, expected)
    assert not diff
