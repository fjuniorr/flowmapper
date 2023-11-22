from dataclasses import asdict, dataclass

import flowmapper.jsonpath as jp

from .cas import CAS
from .context import Context


@dataclass
class Flow:
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
