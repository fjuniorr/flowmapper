import pandas as pd
from flowmapper.flowmap import Flowmap
from flowmapper.match import (
    match_emissions_with_suffix_ion,
    match_minor_land_name_differences,
    match_identical_names,
)

def test_flowmap_to_randonneur(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows)
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {
                "name": "1,4-Butanediol",
                "categories": ["Air", "(unspecified)"],
                "unit": "kg"
            },
            "target": {
                "uuid": "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
                "name": "1,4-Butanediol",
                "context": "air/unspecified",
                "unit": "kg",
            },
            "conversion_factor": 1,
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
    actual = flowmap.mappings
    expected = []
    assert actual == expected


def test_flowmap_with_custom_rules_match(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows, rules=[match_identical_names])
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {
                "name": "1,4-Butanediol",
                "categories": ["Air", "(unspecified)"],
                "unit": "kg"
            },
            "target": {
                "uuid": "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
                "name": "1,4-Butanediol",
                "context": "air/unspecified",
                "unit": "kg",
            },
            "conversion_factor": 1,
            "comment": "Identical names",
        }
    ]
    assert actual == expected


def test_flowmap_to_glad(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows)
    actual = flowmap.to_glad()
    expected = {
        "SourceFlowName": ["1,4-Butanediol"],
        "SourceFlowUUID": [None],
        "SourceFlowContext": ["Air/(unspecified)"],
        "SourceUnit": ["kg"],
        "MatchCondition": [""],
        "ConversionFactor": [None], # FIXME
        "TargetFlowName": ["1,4-Butanediol"],
        "TargetFlowUUID": ["09db39be-d9a6-4fc3-8d25-1f80b23e9131"],
        "TargetFlowContext": ["air/unspecified"],
        "TargetUnit": ["kg"],
        "MemoMapper": ["Identical names"],
    }
    assert actual.equals(pd.DataFrame(expected))


def test_flowmap_export_matched(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows)
    actual = [flow.raw for flow in flowmap.matched_source]
    expected = [
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "(unspecified)"],
            "unit": "kg",
            "CAS": "000110-63-4",
        }
    ]
    assert actual == expected


def test_flowmap_export_unmatched(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows)
    actual = [flow.raw for flow in flowmap.unmatched_source]
    expected = [
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "high. pop."],
            "unit": "kg",
            "CAS": "000110-63-4",
        }
    ]
    assert actual == expected
