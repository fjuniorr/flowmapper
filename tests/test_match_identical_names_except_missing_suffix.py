from flowmapper.flow import Flow
from flowmapper.match import match_identical_names_except_missing_suffix


def test_match_identical_names_except_missing_suffix(fields):
    source = {
        "Flowable": "Copper",
        "CAS No": "007440-50-8",
        "Unit": "kg",
        "Context": "Waterborne emissions",
        "Flow UUID": "F277F190-A8A4-4A2D-AAF6-F6CB3772A545",
    }

    target = {
        "Flowable": "Copper, ion",
        "CASNo": "017493-86-6",
        "Unit": "kg",
        "Context": "water/ground-",
        "FlowUUID": "c3b659e5-35f1-408c-8cb5-b5f9b295c76e",
    }

    s = Flow.from_dict(source, fields['source'])
    t = Flow.from_dict(target, fields['target'])
    
    actual = match_identical_names_except_missing_suffix(s, t, fields, suffix='ion')
    expected = {
        "source": {
            "Flow UUID": "F277F190-A8A4-4A2D-AAF6-F6CB3772A545",
            "Flowable": "Copper",
            "Context": "Waterborne emissions",
        },
        "target": {"FlowUUID": "c3b659e5-35f1-408c-8cb5-b5f9b295c76e"},
        "conversionFactor": 1,
        "MemoMapper": "Identical names except missing suffix",
    }

    assert actual == expected
