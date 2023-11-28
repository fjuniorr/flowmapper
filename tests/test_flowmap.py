from flowmapper.utils import read_field_mapping, read_flowlist
from flowmapper.flow import Flow
from flowmapper.flowmap import Flowmap

def test_flowmap():
    fields = read_field_mapping("tests/data/field_mapping.toml")
    source_flows = [
        Flow.from_dict(flow, fields["source"])
        for flow in read_flowlist("tests/data/sp.json")
    ]
    target_flows = [
        Flow.from_dict(flow, fields["target"])
        for flow in read_flowlist("tests/data/ei.json")
    ]

    flowmap = Flowmap(source_flows, target_flows)
    flowmap.match()
    actual = flowmap.mappings
    expected = [
        {
            "from": "9b680160081438f81d551c724c30b09b",
            "to": "70e4b1b6b6604811cb46114962a4d003",
            "info": {
                "source": {
                    "name": "1,4-Butanediol",
                    "categories": ["Air", "(unspecified)"],
                },
                "target": {"uuid": "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
                           'name': '1,4-Butanediol',
                           'context': 'air/unspecified', 
                           'unit': 'kg'},
                "conversionFactor": 1,
                "comment": "Identical names",
            },
        }
    ]
    assert actual == expected
