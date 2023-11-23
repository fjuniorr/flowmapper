from deepdiff import DeepDiff
from flowmapper.match import format_match_result
from flowmapper.flow import Flow

def test_format_match_result_missing_id():
    source = {
        "name": "Carbon dioxide, in air",
        "context": "Raw materials",
        "unit": "kg",
    }

    source_fields = {
            "uuid": "",
            "name": "name",
            "context": "context",
            "unit": "unit",
        }

    s = Flow.from_dict(source, source_fields)

    target = {
        "id": "cc6a1abb-b123-4ca6-8f16-38209df609be",
        "name": "Carbon dioxide, in air",
        "context": "natural resource/in air",
        "unit": "kg",
    }

    target_fields = {
            "uuid": "id",
            "name": "name",
            "context": "context",
            "unit": "unit",
        }

    t = Flow.from_dict(target, target_fields)

    actual = format_match_result(s, t, is_match=True, comment="foo")
    expected = {'source': {'name': 'Carbon dioxide, in air', 'context': 'Raw materials'}, 
                'target': {'id': 'cc6a1abb-b123-4ca6-8f16-38209df609be'}, 
                'conversionFactor': 1, 
                'comment': 'foo'}

    diff = DeepDiff(actual, expected)
    assert not diff
