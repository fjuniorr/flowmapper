import pandas as pd
from flowmapper.flowmap import Flowmap
from flowmapper.match import (
    match_emissions_with_suffix_ion,
    match_identical_names,
)


def test_flowmap_mappings(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows)
    actual = flowmap.mappings[0]
    assert list(actual.keys()) == [
        "from",
        "to",
        "conversion_factor",
        "match_rule",
        "match_rule_priority",
        "info",
    ]
    assert actual["match_rule"] == "match_identical_names"


def test_flowmap_to_randonneur(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows)
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {
                "name": "1,4-Butanediol",
                "categories": ["Air", "(unspecified)"],
                "unit": "kg",
            },
            "target": {
                "uuid": "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
                "name": "1,4-Butanediol",
                "context": "air/unspecified",
                "unit": "kg",
            },
            "conversion_factor": 1.0,
            "comment": "Identical names",
        },
        {
            "source": {
                "name": "Ammonia, FR",
                "categories": ["Emissions to air", "low. pop."],
                "unit": "kg",
            },
            "target": {
                "uuid": "0f440cc0-0f74-446d-99d6-8ff0e97a2444",
                "name": "Ammonia",
                "context": "air/non-urban air or from high stacks",
                "unit": "kg",
                "location": "FR",
            },
            "conversion_factor": 1.0,
            "comment": "Names with country code",
        },
    ]
    assert actual == expected


def test_flowmap_with_custom_rules_no_match(source_flows, target_flows):
    flowmap = Flowmap(
        source_flows,
        target_flows,
        rules=[match_emissions_with_suffix_ion],
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
                "unit": "kg",
            },
            "target": {
                "uuid": "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
                "name": "1,4-Butanediol",
                "context": "air/unspecified",
                "unit": "kg",
            },
            "conversion_factor": 1.0,
            "comment": "Identical names",
        }
    ]
    assert actual == expected


def test_flowmap_to_glad(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows)
    actual = flowmap.to_glad()
    expected = {
        "SourceFlowName": ["1,4-Butanediol", "Ammonia, FR"],
        "SourceFlowUUID": [None, None],
        "SourceFlowContext": ["Air/(unspecified)", "Emissions to air/low. pop."],
        "SourceUnit": ["kg", "kg"],
        "MatchCondition": ["", ""],
        "ConversionFactor": [1.0, 1.0],
        "TargetFlowName": ["1,4-Butanediol", "Ammonia"],
        "TargetFlowUUID": [
            "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
            "0f440cc0-0f74-446d-99d6-8ff0e97a2444",
        ],
        "TargetFlowContext": [
            "air/unspecified",
            "air/non-urban air or from high stacks",
        ],
        "TargetUnit": ["kg", "kg"],
        "MemoMapper": ["Identical names", "Names with country code"],
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
        },
        {
            "name": "Ammonia, FR",
            "unit": "kg",
            "categories": ["Emissions to air", "low. pop."],
        },
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
        },
        {
            "name": "Cesium-134",
            "unit": "kBq",
            "categories": ["Emissions to air", "low. pop."],
        },
        {"name": "Cesium-134", "unit": "kBq", "categories": ["Emissions to soil", ""]},
        {
            "name": "Zinc, Zn 0.63%, Au 9.7E-4%, Ag 9.7E-4%, Cu 0.38%, Pb 0.014%, in ore",
            "unit": "kg",
            "categories": ["Resources", "in ground"],
        },
    ]
    assert actual == expected


def test_flowmap_nomatch_rule(source_flows, target_flows):
    nomatch = lambda flow: flow.context.value == "air/urban air close to ground"
    flowmap = Flowmap(source_flows, target_flows, nomatch_rules=[nomatch])

    actual_source_flows_nomatch = [flow.raw for flow in flowmap.source_flows_nomatch]
    expected_source_flows_nomatch = [
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "high. pop."],
            "unit": "kg",
            "CAS": "000110-63-4",
        }
    ]
    assert actual_source_flows_nomatch == expected_source_flows_nomatch

    actual_source_flows = [flow.raw for flow in flowmap.source_flows]
    expected_source_flows = [
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "(unspecified)"],
            "unit": "kg",
            "CAS": "000110-63-4",
        },
        {
            "name": "Cesium-134",
            "unit": "kBq",
            "categories": ["Emissions to air", "low. pop."],
        },
        {"name": "Cesium-134", "unit": "kBq", "categories": ["Emissions to soil", ""]},
        {
            "name": "Zinc, Zn 0.63%, Au 9.7E-4%, Ag 9.7E-4%, Cu 0.38%, Pb 0.014%, in ore",
            "unit": "kg",
            "categories": ["Resources", "in ground"],
        },
        {
            "name": "Ammonia, FR",
            "unit": "kg",
            "categories": ["Emissions to air", "low. pop."],
        },
    ]
    assert actual_source_flows == expected_source_flows


def test_flowmap_nomatch_rule_false(source_flows, target_flows):
    nomatch = lambda flow: flow.context.value == "water"
    flowmap = Flowmap(source_flows, target_flows, nomatch_rules=[nomatch])

    actual_source_flows_nomatch = [flow.raw for flow in flowmap.source_flows_nomatch]
    expected_source_flows_nomatch = []
    assert actual_source_flows_nomatch == expected_source_flows_nomatch

    actual_source_flows = [flow.raw for flow in flowmap.source_flows]
    expected_source_flows = [
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "(unspecified)"],
            "unit": "kg",
            "CAS": "000110-63-4",
        },
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "high. pop."],
            "unit": "kg",
            "CAS": "000110-63-4",
        },
        {
            "name": "Cesium-134",
            "unit": "kBq",
            "categories": ["Emissions to air", "low. pop."],
        },
        {"name": "Cesium-134", "unit": "kBq", "categories": ["Emissions to soil", ""]},
        {
            "name": "Zinc, Zn 0.63%, Au 9.7E-4%, Ag 9.7E-4%, Cu 0.38%, Pb 0.014%, in ore",
            "unit": "kg",
            "categories": ["Resources", "in ground"],
        },
        {
            "name": "Ammonia, FR",
            "unit": "kg",
            "categories": ["Emissions to air", "low. pop."],
        },
    ]
    assert actual_source_flows == expected_source_flows


def test_flowmap_nomatch_multiple_rules(source_flows, target_flows):
    nomatch1 = lambda flow: flow.context.value == "air/urban air close to ground"
    nomatch2 = lambda flow: flow.context.value == "air"
    flowmap = Flowmap(source_flows, target_flows, nomatch_rules=[nomatch1, nomatch2])

    actual_source_flows_nomatch = [flow.raw for flow in flowmap.source_flows_nomatch]
    expected_source_flows_nomatch = [
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "(unspecified)"],
            "unit": "kg",
            "CAS": "000110-63-4",
        },
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "high. pop."],
            "unit": "kg",
            "CAS": "000110-63-4",
        },
    ]
    assert actual_source_flows_nomatch == expected_source_flows_nomatch

    actual_source_flows = [flow.raw for flow in flowmap.source_flows]
    expected_source_flows = [
        {
            "name": "Cesium-134",
            "unit": "kBq",
            "categories": ["Emissions to air", "low. pop."],
        },
        {"name": "Cesium-134", "unit": "kBq", "categories": ["Emissions to soil", ""]},
        {
            "name": "Zinc, Zn 0.63%, Au 9.7E-4%, Ag 9.7E-4%, Cu 0.38%, Pb 0.014%, in ore",
            "unit": "kg",
            "categories": ["Resources", "in ground"],
        },
        {
            "name": "Ammonia, FR",
            "unit": "kg",
            "categories": ["Emissions to air", "low. pop."],
        },
    ]
    assert actual_source_flows == expected_source_flows


def test_flowmap_mappings_ei_ei(target_flows):
    flowmap = Flowmap(target_flows, target_flows)
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {
                "name": {"@xml:lang": "en", "#text": "1,4-Butanediol"},
                "compartment": {
                    "@subcompartmentId": "7011f0aa-f5f9-4901-8c10-884ad8296812",
                    "compartment": {"@xml:lang": "en", "#text": "air"},
                    "subcompartment": {"@xml:lang": "en", "#text": "unspecified"},
                },
                "unitName": {"@xml:lang": "en", "#text": "kg"},
                "@id": "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
            },
            "target": {
                "uuid": "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
                "name": "1,4-Butanediol",
                "context": "air/unspecified",
                "unit": "kg",
            },
            "conversion_factor": 1.0,
            "comment": "Identical uuid",
        },
        {
            "source": {
                "name": {"@xml:lang": "en", "#text": "Ammonia"},
                "compartment": {
                    "@subcompartmentId": "be7e06e9-0bf5-462e-99dc-fe4aee383c48",
                    "compartment": {"@xml:lang": "en", "#text": "air"},
                    "subcompartment": {
                        "@xml:lang": "en",
                        "#text": "non-urban air or from high stacks",
                    },
                },
                "unitName": {"@xml:lang": "en", "#text": "kg"},
                "@id": "0f440cc0-0f74-446d-99d6-8ff0e97a2444",
            },
            "target": {
                "uuid": "0f440cc0-0f74-446d-99d6-8ff0e97a2444",
                "name": "Ammonia",
                "context": "air/non-urban air or from high stacks",
                "unit": "kg",
            },
            "conversion_factor": 1.0,
            "comment": "Identical uuid",
        },
    ]
    assert actual == expected


def test_flowmap_mappings_ei39_ei310(flows_ei39, flows_ei310):
    flowmap = Flowmap(flows_ei39, flows_ei310)
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {
                "name": {"@xml:lang": "en", "#text": "2,4-D amines"},
                "compartment": {
                    "@subcompartmentId": "be7e06e9-0bf5-462e-99dc-fe4aee383c48",
                    "compartment": {"@xml:lang": "en", "#text": "air"},
                    "subcompartment": {
                        "@xml:lang": "en",
                        "#text": "non-urban air or from high stacks",
                    },
                },
                "unitName": {"@xml:lang": "en", "#text": "kg"},
                "@id": "4f777e05-70f9-4a18-a406-d8232325073f",
            },
            "target": {
                "uuid": "b6b4201e-0561-5992-912f-e729fbf04e41",
                "name": "2,4-D dimethylamine salt",
                "context": "air/non-urban air or from high stacks",
                "unit": "kg",
            },
            "conversion_factor": 1.0,
            "comment": "Identical uuid",
        }
    ]
    assert actual == expected
