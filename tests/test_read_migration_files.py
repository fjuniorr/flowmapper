from flowmapper.utils import read_migration_files


def test_read_single_migration_file():
    actual = read_migration_files("tests/data/migrations.json")
    expected = {
        "update": [
            {
                "target": {"categories": ["Emissions to air", "low. pop., long-term"]},
                "source": {
                    "name": "Cesium-134",
                    "categories": ["Emissions to air", "low. pop."],
                    "unit": "kBq",
                },
            },
            {
                "target": {"name": "Zinc, Zn 0.63%, in mixed ore"},
                "source": {
                    "name": "Zinc, Zn 0.63%, Au 9.7E-4%, Ag 9.7E-4%, Cu 0.38%, Pb 0.014%, in ore"
                },
            },
            {
                "source": {"@id": "4f777e05-70f9-4a18-a406-d8232325073f"},
                "target": {"@id": "b6b4201e-0561-5992-912f-e729fbf04e41"},
            },
        ]
    }
    assert actual == expected


def test_read_multiple_migration_files():
    actual = read_migration_files(
        "tests/data/migrations.json", "tests/data/transformations.json"
    )
    expected = {
        "update": [
            {
                "target": {"categories": ["Emissions to air", "low. pop., long-term"]},
                "source": {
                    "name": "Cesium-134",
                    "categories": ["Emissions to air", "low. pop."],
                    "unit": "kBq",
                },
            },
            {
                "target": {"name": "Zinc, Zn 0.63%, in mixed ore"},
                "source": {
                    "name": "Zinc, Zn 0.63%, Au 9.7E-4%, Ag 9.7E-4%, Cu 0.38%, Pb 0.014%, in ore"
                },
            },
            {
                "source": {"@id": "4f777e05-70f9-4a18-a406-d8232325073f"},
                "target": {"@id": "b6b4201e-0561-5992-912f-e729fbf04e41"},
            },
            {
                "target": {"categories": ["Air", "(unspecified)"]},
                "source": {
                    "name": "1,4-Butanediol",
                    "categories": ["Air", "high. pop."],
                },
            },
        ]
    }
    assert actual == expected
