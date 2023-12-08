from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Any
import flowmapper.jsonpath as jp
from bw2io.units import normalize_units, DEFAULT_UNITS_CONVERSION

@dataclass
class Unit:
    value: str
    raw_value: str = ""
    raw_object: dict = field(default_factory=lambda: {})

    def __post_init__(self):
        raw_value = self.value
        self.value = normalize_units(self.value)
        if raw_value != self.value:
            self.raw_value = raw_value

    @classmethod
    def from_dict(cls, d, spec):
        key = jp.root(spec)
        value = jp.extract(spec, d)
        result = Unit(
            value = normalize_units(value),
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
            result = [1.0]
        else:
            result = [
                multiplier
                for from_unit, to_unit, multiplier in DEFAULT_UNITS_CONVERSION 
                if from_unit == self.value and to.value == to_unit
            ]

        result = float('nan') if not result else result[0]
        
        return result
