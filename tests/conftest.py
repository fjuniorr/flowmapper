"""Fixtures for flowmapper"""

import pytest


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
