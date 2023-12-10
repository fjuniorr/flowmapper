from flowmapper.unit import Unit
import math

def test_conversion():
    x = 0.8 * Unit('square_meter_year / t').value
    assert x.to('(meter ** 2 * month) / kg').magnitude == 0.009600000000000001

def test_init():
    unit = Unit.from_dict(
        {"unitName": {"@xml:lang": "en", "#text": "M2A"}}, "unitName.#text"
    )
    assert str(unit.value.units) == "square_meter_year"
    assert unit.raw_value == "M2A"
    assert unit.raw_object == {"unitName": {"@xml:lang": "en", "#text": "M2A"}}

def test_equals():
    u1 = Unit("M2A")
    u2 = Unit("m2y")

    assert u1 == u2

def test_equals_mass():
    u1 = Unit("kg")
    u2 = Unit("kilogram")

    assert u1 == u2

def test_conversion_factor():
    u1 = Unit("mg")
    u2 = Unit("kg")
    actual = u1.conversion_factor(u2)
    expected = 1e-06

    assert actual == expected

def test_nan_conversion_factor():
    u1 = Unit("bq")
    u2 = Unit("kg")
    actual = u1.conversion_factor(u2)
    assert math.isnan(actual)
