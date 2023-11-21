import logging
from .cas import CAS
from .flow import Flow
from .constants import CONTEXT_MAPPING, RANDOM_NAME_DIFFERENCES_MAPPING, MINOR_LAND_NAME_DIFFERENCES_MAPPING, MISSING_FOSSIL_AND_BIOGENIC_CARBON_MAPPING

logger = logging.getLogger(__name__)

def format_match_result(s: Flow, t: Flow, fields: dict, memo: str, is_match: bool):
    if is_match:
        result = {
                'source': {
                    fields['source']['uuid'].replace("'", ""): s.uuid,
                    fields['source']['name'].replace("'", ""): s.name,
                    fields['source']['context'].replace("'", ""): s.context.full
                },
                'target': {
                    fields['target']['uuid'].replace("'", ""): t.uuid,
                },
                'conversionFactor': 1 if s.unit == t.unit else '?',
                'MemoMapper': memo
            }
    else:
        result = None
    return result

def match_identical_cas_numbers(source: dict, target: dict, fields: dict, memo: str = 'Identical CAS numbers'):
    s = Flow.from_dict(source, fields['source'])
    t = Flow.from_dict(target, fields['target'])
    
    is_match = s.cas == t.cas and s.context.full == CONTEXT_MAPPING[t.context.full]

    result = format_match_result(s, t, fields = fields, memo = memo, is_match = is_match)
    return result

def match_identical_names(source, target, fields, memo = 'Identical names'):
    s = Flow.from_dict(source, fields['source'])
    t = Flow.from_dict(target, fields['target'])

    is_match = s.name == t.name and s.context.full == CONTEXT_MAPPING[t.context.full]
    
    result = format_match_result(s, t, fields = fields, memo = memo, is_match = is_match)
    return result

def match_identical_names_except_missing_suffix(source, target, fields, suffix, memo = 'Identical names except missing suffix'):
    s = Flow.from_dict(source, fields['source'])
    t = Flow.from_dict(target, fields['target'])

    is_match = f"{s.name}, {suffix}" == t.name and s.context.full == CONTEXT_MAPPING[t.context.full]
    
    result = format_match_result(s, t, fields = fields, memo = memo, is_match = is_match)
    return result

def match_mapped_name_differences(source, target, fields, mapping, memo = 'Mapped name differences'):
    s = Flow.from_dict(source, fields['source'])
    t = Flow.from_dict(target, fields['target'])
    
    is_match = mapping.get(s.name) == t.name and s.context.full == CONTEXT_MAPPING[t.context.full]
    
    result = format_match_result(s, t, fields = fields, memo = memo, is_match = is_match)
    return result

def match_resources_with_suffix_in_ground(source, target, fields):
    return match_identical_names_except_missing_suffix(source, target, fields, suffix = 'in ground', memo = 'Resources with suffix in ground')

def match_emissions_with_suffix_ion(source, target, fields):
    return match_identical_names_except_missing_suffix(source, target, fields, suffix = 'ion', memo = 'Match emissions with suffix ion')

def match_minor_random_name_differences(source, target, fields):
    return match_mapped_name_differences(source, target, fields, mapping = RANDOM_NAME_DIFFERENCES_MAPPING, memo = 'Minor random name differences')

def match_minor_land_name_differences(source, target, fields):
    return match_mapped_name_differences(source, target, fields, mapping = MINOR_LAND_NAME_DIFFERENCES_MAPPING, memo = 'Minor land name differences')

def match_missing_fossil_and_biogenic_carbon(source, target, fields):
    return match_mapped_name_differences(source, target, fields, mapping = MISSING_FOSSIL_AND_BIOGENIC_CARBON_MAPPING, memo = 'Missing biogenic and fossil carbon')

def match_rules(): 
    return [
            match_identical_names,
            match_resources_with_suffix_in_ground,
            match_minor_random_name_differences,
            match_emissions_with_suffix_ion,
            match_minor_land_name_differences,
            match_missing_fossil_and_biogenic_carbon,
            match_identical_cas_numbers,
    ]
