from flowmapper.flow import Flow
from flowmapper.match import match_mapped_name_differences


def test_match_mapped_name_differences(fields):
    source = {
        "Flowable": "Flurochloridone",
        "CAS No": "061213-25-0",
        "Synonyms": "Flurochloridone",
        "Unit": "kg",
        "Context": "Soil/agricultural",
        "Flow UUID": "B0E6801E-D75E-4DDB-AE28-29530A8A57C2",
    }

    target = {
        "Flowable": "Fluorochloridone",
        "CASNo": "061213-25-0",
        "Synonyms": "2-Pyrrolidon-3-chloro-4-chloromethyl-1-(3-trifluoromethylphenyl)",
        "Unit": "kg",
        "Context": "soil/agricultural",
        "FlowUUID": "831f48fc-ca00-4534-9ede-730190b3bee0",
    }

    s = Flow(source, fields['source'])
    t = Flow(target, fields['target'])

    match = match_mapped_name_differences(s, t, mapping={'flurochloridone': 'fluorochloridone'}, comment = "Minor random name differences")
    assert match
