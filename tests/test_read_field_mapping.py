from flowmapper.utils import read_field_mapping

def test_read_field_mapping():
    expected = {
        "source": {
            "uuid": "",
            "name": "name",
            "context": ["categories.0", "categories.1"],
            "unit": "unit",
            "cas": "CAS",
        },
        "target": {
            "uuid": "@id",
            "name": "name.#text",
            "context": ["compartment.compartment.#text", "compartment.subcompartment.#text"],
            "unit": "unitName.#text",
            "cas": "@casNumber",
        },
    }
    actual = read_field_mapping("tests/data/field_mapping.toml")
    assert expected == actual

