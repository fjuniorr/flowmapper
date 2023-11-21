from flowmapper.flow import Flow
from flowmapper.cas import CAS

def test_flow_with_jsonpath_expr():
    data =   {
        "@id": "87883a4e-1e3e-4c9d-90c0-f1bea36f8014",
        "@unitId": "487df68b-4994-4027-8fdc-a4dc298257b7",
        "@casNumber": "007664-41-7",
        "name": {
        "@xml:lang": "en",
        "#text": "Ammonia"
        },
        "unitName": {
        "@xml:lang": "en",
        "#text": "kg"
        },
        "compartment": {
        "@subcompartmentId": "7011f0aa-f5f9-4901-8c10-884ad8296812",
        "compartment": {
            "@xml:lang": "en",
            "#text": "air"
        },
        "subcompartment": {
            "@xml:lang": "en",
            "#text": "unspecified"
        }
        }
    }

    fields = {
        'cas': '@casNumber',
        'context': ["compartment.compartment.'#text'", "compartment.subcompartment.'#text'"],
        'name': "name.'#text'",
        'unit': "unitName.'#text'",
        'uuid': "'@id'"
    }

    flow = Flow.from_dict(data, fields)
    assert flow.context.full == "air/unspecified"
    assert flow.context.primary == "air"
    assert flow.context.secondary == "unspecified"

def test_flow_from_sp_categories():
    data = {
        "name": "Carbon dioxide, in air",
        "categories": ["Raw", "(unspecified)"],
        "unit": "kg",
        "CAS": "000124-38-9",
    }

    fields = {
            "name": "name",
            "context": ["categories[0]", "categories[1]"],
            "unit": "unit",
            "cas": "CAS",
        }

    flow = Flow.from_dict(data, fields)
    assert flow.uuid == None
    assert flow.name == 'Carbon dioxide, in air'
    assert flow.context.full == 'Raw/(unspecified)'
    assert flow.context.primary == 'Raw'
    assert flow.context.secondary == '(unspecified)'
    assert id(flow.raw) == id(data)

def test_flow_from_sp_missing():
    data = {
        "name": "Chrysotile",
        "context": ["Resources", "in ground"],
        "unit": "kg"
    }

    fields = {
        "name": "name",
        "context": ["context[0]", "context[1]"],
        "unit": "unit",
    }

    flow = Flow.from_dict(data, fields)
    assert flow.name == "Chrysotile"
    assert repr(flow.cas) == ''
    assert flow.context.full == "Resources/in ground"
    assert flow.context.primary == "Resources"
    assert flow.context.secondary == "in ground"


def test_flow_from_sp():
    data = {
        "Flowable": "Actinium",
        "CAS No": "007440-34-8",
        "Formula": "Ac\u007f",
        "Synonyms": "Actinium",
        "Unit": "kg",
        "Class": "Raw materials",
        "Context": "Raw materials",
        "Flow UUID": "90004354-71D3-47E8-B322-300BA5A98F7B",
        "Description": "",
    }

    fields = {
        "uuid": "'Flow UUID'",
        "name": "Flowable",
        "context": "Context",
        "unit": "Unit",
        "cas": "'CAS No'",
    }

    flow = Flow.from_dict(data, fields)
    assert flow.uuid == "90004354-71D3-47E8-B322-300BA5A98F7B"
    assert flow.cas == CAS("007440-34-8")
    assert flow.cas.cas == "7440-34-8"

def test_flow_from_ei():
    data = {
        "Flowable": "1,3-Dioxolan-2-one",
        "CASNo": "000096-49-1",
        "Formula": "",
        "Synonyms": "",
        "Unit": "kg",
        "Class": "chemical",
        "ExternalReference": "",
        "Preferred": "",
        "Context": "water/unspecified",
        "FlowUUID": "5b7d620e-2238-5ec9-888a-6999218b6974",
        "AltUnit": "",
        "Var": "",
        "Second CAS": "96-49-1"
    }
      
    fields = {
        "uuid": "FlowUUID",
        "name": "Flowable",
        "context": "Context",
        "unit": "Unit",
        "cas": "CASNo",
    }

    flow = Flow.from_dict(data, fields)
    assert flow.uuid == "5b7d620e-2238-5ec9-888a-6999218b6974"

