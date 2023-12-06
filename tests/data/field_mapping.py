config = {
    "uuid": ["", "@id"],
    "name": ["name", "name.#text"],
    "synonyms": ["", ("synonym", ["#text"])],
    "context": [["categories.0", "categories.1"], ["compartment.compartment.#text", "compartment.subcompartment.#text"]],
    "unit": ["unit", "unitName.#text"],
    "cas": ["CAS", "@casNumber"],
}
