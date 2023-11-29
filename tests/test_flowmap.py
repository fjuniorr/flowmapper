from flowmapper.flowmap import Flowmap
from flowmapper.match import (
    match_emissions_with_suffix_ion,
    match_minor_land_name_differences,
    match_identical_names,
)


def test_flowmap(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows)
    flowmap.match()
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {
                "name": "1,4-Butanediol",
                "categories": ["Air", "(unspecified)"],
            },
            "target": {
                "uuid": "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
                "name": "1,4-Butanediol",
                "context": "air/unspecified",
                "unit": "kg",
            },
            "conversionFactor": 1,
            "comment": "Identical names",
        }
    ]
    assert actual == expected


def test_flowmap_with_custom_rules_no_match(source_flows, target_flows):
    flowmap = Flowmap(
        source_flows,
        target_flows,
        rules=[match_emissions_with_suffix_ion, match_minor_land_name_differences],
    )
    flowmap.match()
    actual = flowmap.mappings
    expected = []
    assert actual == expected


def test_flowmap_with_custom_rules_match(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows, rules=[match_identical_names])
    flowmap.match()
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {
                "name": "1,4-Butanediol",
                "categories": ["Air", "(unspecified)"],
            },
            "target": {
                "uuid": "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
                "name": "1,4-Butanediol",
                "context": "air/unspecified",
                "unit": "kg",
            },
            "conversionFactor": 1,
            "comment": "Identical names",
        }
    ]
    assert actual == expected
