from deepdiff import DeepDiff
from flowmapper.flow import Flow
from flowmapper.flowmap import Flowmap

def test_match_non_ionic_state():
    fields = {"name": "name", "context": "context", "unit": "unit"}
    s = [
        Flow.from_dict({"name": "Ammonia, as N", "context": "air", "unit": "kg"}, fields),
        Flow.from_dict({"name": "AOX (Adsorbable Organic Halogens)", "context": "air", "unit": "kg"}, fields),
    ]
    t = [
        Flow.from_dict({"name": "Ammonia", "context": "air", "unit": "kg"}, fields),
        Flow.from_dict({"name": "AOX, Adsorbable Organic Halogen as Cl", "context": "air", "unit": "kg"}, fields),
    ]

    flowmap = Flowmap(s, t)
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {"name": "Ammonia, as N", "context": "air", "unit": "kg"},
            "target": {"uuid": None, "name": "Ammonia", "context": "air", "unit": "kg"},
            "conversion_factor": 1,
            "comment": "Mapped name differences with unit conversions",
        },
        {
            "source": {"name": "AOX (Adsorbable Organic Halogens)", "context": "air", "unit": "kg"},
            "target": {
                "uuid": None,
                "name": "AOX, Adsorbable Organic Halogen as Cl",
                "context": "air",
                "unit": "kg",
            },
            "conversion_factor": 1,
            "comment": "Mapped name differences with unit conversions",
        },
    ]
    diff = DeepDiff(actual, expected)
    assert not diff
