from dataclasses import asdict, dataclass

import flowmapper.jsonpath as jp


@dataclass
class Context:
    full: str = None
    primary: str = None
    secondary: str = None

    @classmethod
    def from_dict(cls, d, fields):
        fields = [fields] if isinstance(fields, str) else fields
        context_mapping_length = len(fields)
        primary_context = jp.extract(fields[0], d)
        if context_mapping_length == 1:
            result = Context(primary_context, primary_context)
        elif context_mapping_length == 2:
            secondary_context = jp.extract(fields[1], d)
            secondary_context = secondary_context if isinstance(secondary_context, str) else '/'.join(secondary_context)
            result = Context(
                full = f"{primary_context}/{secondary_context}",
                primary = primary_context,
                secondary = secondary_context
            )
        return result

    def to_dict(self):
        return asdict(self)
