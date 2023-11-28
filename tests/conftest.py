"""Fixtures for flowmapper"""

import pytest
from flowmapper.utils import read_field_mapping, read_flowlist
from flowmapper.flow import Flow


@pytest.fixture
def fields():
    result = {
        "source": {
            "uuid": "Flow UUID",
            "name": "Flowable",
            "context": "Context",
            "unit": "Unit",
            "cas": "CAS No",
        },
        "target": {
            "uuid": "FlowUUID",
            "name": "Flowable",
            "context": "Context",
            "unit": "Unit",
            "cas": "CASNo",
        },
    }

    return result

@pytest.fixture
def source_flows():
    fields = read_field_mapping("tests/data/field_mapping.toml")
    result = [
        Flow.from_dict(flow, fields["source"])
        for flow in read_flowlist("tests/data/sp.json")
    ]
    return result


@pytest.fixture
def target_flows():
    fields = read_field_mapping("tests/data/field_mapping.toml")
    result = [
        Flow.from_dict(flow, fields["target"])
        for flow in read_flowlist("tests/data/ei.json")
    ]
    return result
