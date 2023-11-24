from flowmapper.context import Context


def test_context():
    data = {
        "name": "Carbon dioxide, in air",
        "categories": ["Raw", "(unspecified)"],
        "unit": "kg",
        "CAS": "000124-38-9",
    }
    fields = ["categories.0", "categories.1"]
    actual = Context.from_dict(data, fields).to_dict()
    expected = {
        "full": "Raw/(unspecified)",
        "primary": "Raw",
        "secondary": "(unspecified)",
    }
    assert actual == expected


def test_context_multiple_levels_list():
    data = {
        "name": "Carbon dioxide, in air",
        "categories": ["emission/air", ["troposphere", "high"]],
        "unit": "kg",
        "CAS": "000124-38-9",
    }
    fields = ["categories.0", "categories.1"]
    actual = Context.from_dict(data, fields).to_dict()
    expected = {
        "full": "emission/air/troposphere/high",
        "primary": "emission/air",
        "secondary": "troposphere/high",
    }
    assert actual == expected


def test_context_multiple_levels():
    data = {
        "name": "Carbon dioxide, in air",
        "categories": "emission/air",
        "subcategories": ["troposphere", "high"],
        "unit": "kg",
        "CAS": "000124-38-9",
    }
    fields = ["categories", "subcategories"]
    actual = Context.from_dict(data, fields).to_dict()
    expected = {
        "full": "emission/air/troposphere/high",
        "primary": "emission/air",
        "secondary": "troposphere/high",
    }
    assert actual == expected


def test_context_equality_true():
    s = {"name": "2-Propanol", "categories": ["Air", "low. pop."]}
    sc = Context.from_dict(s, ["categories.0", "categories.1"])

    t = {
        "@id": "ed1aff41-0bfc-48b8-8250-840c0a2f6961",
        "name": {"@xml:lang": "en", "#text": "2-Propanol"},
        "compartment": {
            "@subcompartmentId": "be7e06e9-0bf5-462e-99dc-fe4aee383c48",
            "compartment": {"@xml:lang": "en", "#text": "air"},
            "subcompartment": {
                "@xml:lang": "en",
                "#text": "non-urban air or from high stacks",
            },
        },
    }
    tc = Context.from_dict(
        t, ["compartment.compartment.#text", "compartment.subcompartment.#text"]
    )

    assert sc == tc


def test_context_equality_false():
    s = {
        "CAS": "007440-61-1",
        "categories": ["Raw", "(unspecified)"],
        "name": "Uranium",
        "unit": "kg",
    }
    sc = Context.from_dict(s, ["categories.0", "categories.1"])

    t = {
        "@casNumber": "007440-61-1",
        "@id": "2ba5e39b-adb6-4767-a51d-90c1cf32fe98",
        "compartment": {
            "@subcompartmentId": "6a098164-9f04-4f65-8104-ffab7f2677f3",
            "compartment": {"#text": "natural resource", "@xml:lang": "en"},
            "subcompartment": {"#text": "in ground", "@xml:lang": "en"},
        },
        "name": {"#text": "Uranium, in ground", "@xml:lang": "en"},
    }
    tc = Context.from_dict(
        t, ["compartment.compartment.#text", "compartment.subcompartment.#text"]
    )

    assert sc == tc
