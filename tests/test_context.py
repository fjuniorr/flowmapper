from flowmapper.context import Context


def test_context():
    data = {
        "name": "Carbon dioxide, in air",
        "categories": ["Raw", "(unspecified)"],
        "unit": "kg",
        "CAS": "000124-38-9",
    }
    fields = "categories"
    actual = Context.from_dict(data, fields).to_dict()
    expected = {
        "value": "natural resource/in ground",
        "raw_value": "Raw/(unspecified)",
        "raw_object": {"categories": ["Raw", "(unspecified)"]},
    }
    assert actual == expected


def test_trailing_slash():
    c1 = Context.from_dict({"categories": ["Raw", "(unspecified)"]}, "categories")
    c2 = Context.from_dict({"categories": ["Raw"]}, "categories")
    c3 = Context.from_dict({"categories": ["Raw/"]}, "categories")
    assert c1.value == c2.value
    assert c2.value == c3.value
    "/".join(c1.value)


def test_unspecified():
    c1 = Context.from_dict(
        {
            "compartment": {
                "@subcompartmentId": "e47f0a6c-3be8-4027-9eee-de251784f708",
                "compartment": {"@xml:lang": "en", "#text": "water"},
                "subcompartment": {"@xml:lang": "en", "#text": "unspecified"},
            },
        },
        "compartment.*.#text",
    )

    c2 = Context.from_dict({"categories": ["Emissions to water", ""]}, "categories")
    c3 = Context.from_dict({"categories": ["Water", "(unspecified)"]}, "categories")
    c4 = Context.from_dict({"categories": ["Water", ""]}, "categories")
    c5 = Context.from_dict({"categories": ["Water/", ""]}, "categories")
    c6 = Context.from_dict({"categories": ["Water/"]}, "categories")
    c7 = Context.from_dict({"categories": "Water/(unspecified)"}, "categories")
    c8 = Context.from_dict({"categories": "Water/unspecified"}, "categories")
    c9 = Context.from_dict({"categories": "Water/"}, "categories")
    c10 = Context.from_dict({"categories": "Water"}, "categories")
    c11 = Context.from_dict(
        {"context": [{"name": "Water"}, {"name": "unspecified"}]}, ("context", ["name"])
    )
    c12 = Context.from_dict({"categories": ["Water"]}, "categories")

    actual = set(
        [
            c1.value,
            c2.value,
            c3.value,
            c4.value,
            c5.value,
            c6.value,
            c7.value,
            c8.value,
            c9.value,
            c10.value,
            c11.value,
            c12.value,
        ]
    )
    expected = {"water"}
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
