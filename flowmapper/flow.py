from dataclasses import asdict, dataclass, field

import flowmapper.jsonpath as jp

from .unit import Unit
from .cas import CAS
from .context import Context
from .utils import generate_flow_id

@dataclass
class Flow:
    id: str = None
    uuid: str = None
    name: str = None
    synonyms: list[str] = None
    context: str = None
    unit: Unit = None
    cas: CAS = None
    fields: dict = field(default_factory=lambda: {"uuid": "uuid", 
                                                  "name": "name", 
                                                  "synonyms": "synonyms",
                                                  "context": "context", 
                                                  "unit": "unit", 
                                                  "cas":"cas"})
    raw: dict = None

    @classmethod
    def from_dict(cls, d, fields):
        result = Flow(
            id = generate_flow_id(d),
            uuid = jp.extract(fields['uuid'], d) if fields.get('uuid') else None,
            name = jp.extract(fields['name'], d) if fields.get('name') else None,
            synonyms = jp.extract(fields['synonyms'], d) if fields.get('synonyms') else None,
            context = Context.from_dict(d, fields['context']) if fields.get('context') else None,
            unit = Unit.from_dict(d, fields['unit']),
            cas = CAS(jp.extract(fields['cas'], d)) if fields.get('cas') else CAS(''),
            fields = fields.copy(),
            raw = d
        )
        return result

    def to_dict(self):
        return asdict(self)

    def __repr__(self) -> str:
        return f'{self.name} <{self.context.full.lower()}>'
