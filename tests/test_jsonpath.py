import flowmapper.jsonpath as jp


def test_basic_access():
    data = {
    "name": "Chrysotile",
    "context": [
      "Resources",
      "in ground"
    ],
    "unit": {"kg": 1}
  }

    assert jp.extract("name", data,) == "Chrysotile"
    assert jp.extract("context.0", data) == "Resources"

def test_special_characters():
    data = {
        "@id": "be73218b-18af-492e-96e6-addd309d1e32",
        "name": {"#text": "Zinc, in ground", "@xml:lang": "en"}
    }

    assert jp.extract("@id", data) == "be73218b-18af-492e-96e6-addd309d1e32"
    assert jp.extract("name.#text", data) == "Zinc, in ground"
