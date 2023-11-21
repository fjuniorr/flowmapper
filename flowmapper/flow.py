from dataclasses import dataclass, asdict
from .cas import CAS
import flowmapper.jsonpath as jp

@dataclass
class Flow():
    uuid: str = None
    name: str = None
    context: str = None
    unit: str = None
    cas: CAS = None
    raw: dict = None

    @classmethod
    def from_dict(cls, d, fields):
        result = Flow(
            uuid = jp.extract(fields['uuid'], d) if fields.get('uuid') else None,
            name = jp.extract(fields['name'], d) if fields.get('name') else None,
            context = Context.from_dict(d, fields['context']) if fields.get('context') else None,
            unit = jp.extract(fields['unit'], d) if fields.get('unit') else None,
            cas = CAS(jp.extract(fields['cas'], d)) if fields.get('cas') else CAS(''),
            raw = d
        )
        return result

    def to_dict(self):
        return asdict(self)

@dataclass
class Context():
    full: str = None
    primary: str = None
    secondary: str = None

    @classmethod
    def from_dict(cls, d, fields):
        fields = [fields] if isinstance(fields, str) else fields
        context_mapping_length = len(fields)
        if context_mapping_length == 1:
            result = Context(
                full = jp.extract(fields[0], d),
                primary = jp.extract(fields[0], d))
        elif context_mapping_length == 2:
            result = Context(
                full = f"{jp.extract(fields[0], d)}/{jp.extract(fields[1], d)}",
                primary = jp.extract(fields[0], d),
                secondary = jp.extract(fields[1], d)
            )
        return result
