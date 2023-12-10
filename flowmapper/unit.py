from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Any
import flowmapper.jsonpath as jp
from pint import UnitRegistry, errors
import importlib.resources as resource
from .utils import normalize_str

ureg = UnitRegistry()

with resource.as_file(resource.files('flowmapper').joinpath('data/units.txt')) as filepath:
    ureg.load_definitions(filepath)

UNITS_NORMALIZATION = {
    "a": "year",  # Common in LCA circles; could be confused with are
    "bq": "becquerel",
    "g": "gram",
    "gj": "gigajoule",
    "h": "hour",
    "ha": "hectare",
    "hr": "hour",
    "kbq": "kilobecquerel",
    "kg": "kilogram",
    "kgkm": "kilogram_kilometer",
    "km": "kilometer",
    "kj": "kilojoule",
    "kwh": "kilowatt hour",
    "l": "litre",
    "lu": "livestock unit",
    "m": "meter",
    "m*year": "meter_year",
    "m2": "square_meter",
    "m2*year": "square_meter_year",
    "m2a": "square_meter_year",
    "m2y": "square_meter_year",
    "m3": "cubic_meter",
    "m3*year": "cubic_meter_year",
    "m3a": "cubic_meter_year",
    "m3y": "cubic_meter_year",
    "ma": "meter_year",
    "metric ton*km": "ton_kilometer",
    "mj": "megajoule",
    "my": "meter_year",
    "nm3": "cubic_meter",
    "p": "unit",
    "personkm": "person_kilometer",
    "person*km": "person_kilometer",
    "pkm": "person_kilometer",
    "tkm": "ton_kilometer",
    "vkm": "vehicle_kilometer",
    'kg sw': "kilogram_separative_work_unit",
    'km*year': "kilometer_year",
    'metric ton*km': "ton_kilometer",
    'person*km': "person_kilometer",
    'wh': 'watt_hour',
}

normalize_unit = lambda x: UNITS_NORMALIZATION.get(x, x)

@dataclass
class Unit:
    value: str
    raw_value: str = ""
    raw_object: dict = field(default_factory=lambda: {})

    def __post_init__(self):
        if not self.raw_value:
            self.raw_value = self.value
        self.value = self.normalize(self.raw_value)

    @classmethod
    def from_dict(cls, d, spec):
        key = jp.root(spec)
        value = jp.extract(spec, d)
        result = Unit(
            value = None,
            raw_value = value,
            raw_object = {key: d.get(key)},
        )
        return result

    def to_dict(self):
        return asdict(self)

    def __eq__(self, other):
        return self.value == other.value

    def conversion_factor(self, to: Unit):
        if self.value == to.value:
            result = 1.0
        else:
            try:
                result = ureg(self.value).to(ureg(to.value)).magnitude
            except errors.DimensionalityError:
                result = float('nan')
        return result

    @staticmethod
    def normalize(x):
        return normalize_unit(normalize_str(x))
