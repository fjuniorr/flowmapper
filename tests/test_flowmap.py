from flowmapper.flowmap import Flowmap
from flowmapper.match import match_emissions_with_suffix_ion, match_minor_land_name_differences, match_identical_names

def test_flowmap(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows)
    flowmap.match()
    actual = flowmap.mappings
    expected = [
        {
            "from": "9b680160081438f81d551c724c30b09b",
            "to": "70e4b1b6b6604811cb46114962a4d003",
            "info": {
                "comment": "Identical names",
            },
        }
    ]
    assert actual == expected

def test_flowmap_with_custom_rules_no_match(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows, rules=[match_emissions_with_suffix_ion, match_minor_land_name_differences])
    flowmap.match()
    actual = flowmap.mappings
    expected = []
    assert actual == expected

def test_flowmap_with_custom_rules_match(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows, rules=[match_identical_names])
    flowmap.match()
    actual = flowmap.mappings
    expected = [
        {
            "from": "9b680160081438f81d551c724c30b09b",
            "to": "70e4b1b6b6604811cb46114962a4d003",
            "info": {
                "comment": "Identical names",
            },
        }
    ]
    assert actual == expected
