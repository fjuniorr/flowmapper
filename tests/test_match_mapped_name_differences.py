from flowmapper.match import match_mapped_name_differences


def test_match_mapped_name_differences(fields):
    source = {
        "Flowable": "Flurochloridone",
        "CAS No": "061213-25-0",
        "Synonyms": "Flurochloridone",
        "Unit": "kg",
        "Context": "Emissions to soil",
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

    actual = match_mapped_name_differences(source, target, fields, mapping={'Flurochloridone': 'Fluorochloridone'}, memo = "Minor random name differences")
    expected = {
        "source": {
            "Flow UUID": "B0E6801E-D75E-4DDB-AE28-29530A8A57C2",
            "Flowable": "Flurochloridone",
            "Context": "Emissions to soil",
        },
        "target": {"FlowUUID": "831f48fc-ca00-4534-9ede-730190b3bee0"},
        "conversionFactor": 1,
        "MemoMapper": "Minor random name differences",
    }

    assert actual == expected
