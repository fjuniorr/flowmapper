from typer.testing import CliRunner
from flowmapper.cli import app
import json
import pandas as pd

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.output.startswith("flowmapper, version")


def test_format_glad(tmp_path):
    result = runner.invoke(
        app,
        [
            "map",
            "tests/data/sp.json",
            "tests/data/ei.json",
            "--format",
            "glad",
            "--fields",
            "tests/data/field_mapping.py",
            "--output-dir",
            str(tmp_path),
        ],
    )
    expected_files = sorted(
        [
            tmp_path / "sp-ei.xlsx",
            tmp_path / "sp-ei-unmatched-source.json",
            tmp_path / "sp-ei-unmatched-target.json",
        ]
    )

    files = sorted(tmp_path.glob("**/*"))

    assert result.exit_code == 0
    assert expected_files == files


def test_format_randonneur(tmp_path):
    result = runner.invoke(
        app,
        [
            "map",
            "tests/data/sp.json",
            "tests/data/ei.json",
            "--format",
            "randonneur",
            "--fields",
            "tests/data/field_mapping.py",
            "--output-dir",
            str(tmp_path),
        ],
    )
    expected_files = sorted(
        [
            tmp_path / "sp-ei.json",
            tmp_path / "sp-ei-unmatched-source.json",
            tmp_path / "sp-ei-unmatched-target.json",
        ]
    )

    files = sorted(tmp_path.glob("**/*"))

    assert result.exit_code == 0
    assert expected_files == files


def test_matched_flows(tmp_path):
    result = runner.invoke(
        app,
        [
            "map",
            "tests/data/sp.json",
            "tests/data/ei.json",
            "--matched-source",
            "--matched-target",
            "--fields",
            "tests/data/field_mapping.py",
            "--output-dir",
            str(tmp_path),
        ],
    )
    expected_files = sorted(
        [
            tmp_path / "sp-ei.json",
            tmp_path / "sp-ei.xlsx",
            tmp_path / "sp-ei-unmatched-source.json",
            tmp_path / "sp-ei-matched-source.json",
            tmp_path / "sp-ei-unmatched-target.json",
            tmp_path / "sp-ei-matched-target.json",
        ]
    )

    files = sorted(tmp_path.glob("**/*"))

    with open(tmp_path / "sp-ei-unmatched-source.json") as fs:
        unmatched_source = json.load(fs)

    with open(tmp_path / "sp-ei-matched-source.json") as fs:
        matched_source = json.load(fs)

    with open(tmp_path / "sp-ei-unmatched-target.json") as fs:
        unmatched_target = json.load(fs)

    with open(tmp_path / "sp-ei-matched-target.json") as fs:
        matched_target = json.load(fs)

    assert unmatched_source == [
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "high. pop."],
            "unit": "kg",
            "CAS": "000110-63-4",
        },
        {
            "name": "Cesium-134",
            "unit": "kBq",
            "categories": ["Emissions to air", "low. pop."],
        },
        {"name": "Cesium-134", "unit": "kBq", "categories": ["Emissions to soil", ""]},
        {
            "name": "Zinc, Zn 0.63%, Au 9.7E-4%, Ag 9.7E-4%, Cu 0.38%, Pb 0.014%, in ore",
            "unit": "kg",
            "categories": ["Resources", "in ground"],
        },
    ]
    assert matched_source == [
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "(unspecified)"],
            "unit": "kg",
            "CAS": "000110-63-4",
        }
    ]
    assert unmatched_target == []
    assert matched_target == [
        {
            "@id": "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
            "@unitId": "487df68b-4994-4027-8fdc-a4dc298257b7",
            "@casNumber": "000110-63-4",
            "name": {"@xml:lang": "en", "#text": "1,4-Butanediol"},
            "unitName": {"@xml:lang": "en", "#text": "kg"},
            "compartment": {
                "@subcompartmentId": "7011f0aa-f5f9-4901-8c10-884ad8296812",
                "compartment": {"@xml:lang": "en", "#text": "air"},
                "subcompartment": {"@xml:lang": "en", "#text": "unspecified"},
            },
            "synonym": {"@xml:lang": "en", "#text": "Butylene glycol"},
        }
    ]

    assert result.exit_code == 0
    assert expected_files == files


def test_matched_flows_with_randonneur_transformations(tmp_path):
    result = runner.invoke(
        app,
        [
            "map",
            "tests/data/sp.json",
            "tests/data/ei.json",
            "--transformations",
            "tests/data/transformations.json",
            "--matched-source",
            "--matched-target",
            "--fields",
            "tests/data/field_mapping.py",
            "--output-dir",
            str(tmp_path),
        ],
    )
    expected_files = sorted(
        [
            tmp_path / "sp-ei.json",
            tmp_path / "sp-ei.xlsx",
            tmp_path / "sp-ei-unmatched-source.json",
            tmp_path / "sp-ei-matched-source.json",
            tmp_path / "sp-ei-unmatched-target.json",
            tmp_path / "sp-ei-matched-target.json",
        ]
    )

    files = sorted(tmp_path.glob("**/*"))

    with open(tmp_path / "sp-ei-unmatched-source.json") as fs:
        unmatched_source = json.load(fs)

    with open(tmp_path / "sp-ei-matched-source.json") as fs:
        matched_source = json.load(fs)

    with open(tmp_path / "sp-ei-unmatched-target.json") as fs:
        unmatched_target = json.load(fs)

    with open(tmp_path / "sp-ei-matched-target.json") as fs:
        matched_target = json.load(fs)

    assert unmatched_source == [
        {
            "name": "Cesium-134",
            "unit": "kBq",
            "categories": ["Emissions to air", "low. pop."],
        },
        {"name": "Cesium-134", "unit": "kBq", "categories": ["Emissions to soil", ""]},
        {
            "name": "Zinc, Zn 0.63%, Au 9.7E-4%, Ag 9.7E-4%, Cu 0.38%, Pb 0.014%, in ore",
            "unit": "kg",
            "categories": ["Resources", "in ground"],
        },
    ]
    assert matched_source == [
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "(unspecified)"],
            "unit": "kg",
            "CAS": "000110-63-4",
        },
        {
            "name": "1,4-Butanediol",
            "categories": ["Air", "(unspecified)"],
            "unit": "kg",
            "CAS": "000110-63-4",
        },
    ]
    assert unmatched_target == []
    assert matched_target == [
        {
            "@id": "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
            "@unitId": "487df68b-4994-4027-8fdc-a4dc298257b7",
            "@casNumber": "000110-63-4",
            "name": {"@xml:lang": "en", "#text": "1,4-Butanediol"},
            "unitName": {"@xml:lang": "en", "#text": "kg"},
            "compartment": {
                "@subcompartmentId": "7011f0aa-f5f9-4901-8c10-884ad8296812",
                "compartment": {"@xml:lang": "en", "#text": "air"},
                "subcompartment": {"@xml:lang": "en", "#text": "unspecified"},
            },
            "synonym": {"@xml:lang": "en", "#text": "Butylene glycol"},
        }
    ]

    assert result.exit_code == 0
    assert expected_files == files
