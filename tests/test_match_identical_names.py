from flowmapper.match import match_identical_names

def test_match_identical_names(fields):
    source = {
        "Flowable": "Carbon dioxide, in air",
        "CAS No": "000124-38-9",
        "Unit": "kg",
        "Context": "Raw materials",
        "Flow UUID": "32722990-B7D8-44A8-BC7D-EC3A89F533FF",
    }

    target = {
        "Flowable": "Carbon dioxide, in air",
        "CASNo": "000124-38-9",
        "Unit": "kg",
        "Context": "natural resource/in air",
        "FlowUUID": "cc6a1abb-b123-4ca6-8f16-38209df609be",
    }

    actual = match_identical_names(source, target, fields)
    expected = {
        "source": {
            "Flow UUID": "32722990-B7D8-44A8-BC7D-EC3A89F533FF",
            "Flowable": "Carbon dioxide, in air",
            "Context": "Raw materials",
        },
        "target": {"FlowUUID": "cc6a1abb-b123-4ca6-8f16-38209df609be"},
        "conversionFactor": 1,
        "MemoMapper": "Identical names",
    }

    assert actual == expected
