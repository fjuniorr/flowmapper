import logging

from .constants import (
    CONTEXT_MAPPING,
    MINOR_LAND_NAME_DIFFERENCES_MAPPING,
    MISSING_FOSSIL_AND_BIOGENIC_CARBON_MAPPING,
    RANDOM_NAME_DIFFERENCES_MAPPING,
)
from .flow import Flow

logger = logging.getLogger(__name__)

def format_match_result(s: Flow, t: Flow, fields: dict, comment: str, is_match: bool):
    if is_match:
        result = {
                'source': {
                    fields['source']['uuid']: s.uuid,
                    fields['source']['name']: s.name,
                    fields['source']['context']: s.context.full
                },
                'target': {
                    fields['target']['uuid']: t.uuid,
                },
                'conversionFactor': 1 if s.unit == t.unit else '?',
                'comment': comment
            }
    else:
        result = None
    return result

def match_identical_cas_numbers(s: Flow, t: Flow, fields: dict, comment: str = 'Identical CAS numbers'):    
    is_match = s.cas == t.cas and s.context.full == CONTEXT_MAPPING[t.context.full]

    result = format_match_result(s, t, fields = fields, comment = comment, is_match = is_match)
    return result

def match_identical_names(s: Flow, t: Flow, fields, comment = 'Identical names'):
    is_match = s.name == t.name and s.context.full == CONTEXT_MAPPING[t.context.full]
    
    result = format_match_result(s, t, fields = fields, comment = comment, is_match = is_match)
    return result

def match_identical_names_except_missing_suffix(s: Flow, t: Flow, fields, suffix, comment = 'Identical names except missing suffix'):
    is_match = f"{s.name}, {suffix}" == t.name and s.context.full == CONTEXT_MAPPING[t.context.full]
    
    result = format_match_result(s, t, fields = fields, comment = comment, is_match = is_match)
    return result

def match_mapped_name_differences(s: Flow, t: Flow, fields, mapping, comment = 'Mapped name differences'):    
    is_match = mapping.get(s.name) == t.name and s.context.full == CONTEXT_MAPPING[t.context.full]
    
    result = format_match_result(s, t, fields = fields, comment = comment, is_match = is_match)
    return result

def match_resources_with_suffix_in_ground(s: Flow, t: Flow, fields):
    return match_identical_names_except_missing_suffix(s, t, fields, suffix = 'in ground', comment = 'Resources with suffix in ground')

def match_emissions_with_suffix_ion(s: Flow, t: Flow, fields):
    return match_identical_names_except_missing_suffix(s, t, fields, suffix = 'ion', comment = 'Match emissions with suffix ion')

def match_minor_random_name_differences(s: Flow, t: Flow, fields):
    return match_mapped_name_differences(s, t, fields, mapping = RANDOM_NAME_DIFFERENCES_MAPPING, comment = 'Minor random name differences')

def match_minor_land_name_differences(s: Flow, t: Flow, fields):
    return match_mapped_name_differences(s, t, fields, mapping = MINOR_LAND_NAME_DIFFERENCES_MAPPING, comment = 'Minor land name differences')

def match_missing_fossil_and_biogenic_carbon(s: Flow, t: Flow, fields):
    return match_mapped_name_differences(s, t, fields, mapping = MISSING_FOSSIL_AND_BIOGENIC_CARBON_MAPPING, comment = 'Missing biogenic and fossil carbon')

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
