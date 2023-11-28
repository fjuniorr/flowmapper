import logging
from tqdm import tqdm

from .constants import (
    MINOR_LAND_NAME_DIFFERENCES_MAPPING,
    MISSING_FOSSIL_AND_BIOGENIC_CARBON_MAPPING,
    RANDOM_NAME_DIFFERENCES_MAPPING,
)
from .flow import Flow

logger = logging.getLogger(__name__)

def format_match_result(s: Flow, t: Flow, comment: str, is_match: bool):
    if is_match:
        source_context_key = s.fields['context'] if isinstance(s.fields['context'], str) else s.fields['context'][0].split('.')[0]
        source_result = {
                    s.fields['name']: s.name,
                    source_context_key: s.raw[source_context_key]
                }
        if s.uuid:
            source_result.update({s.fields['uuid']: s.uuid})
        
        result = {
                'source': source_result,
                'target': {
                    'uuid': t.uuid,
                    'name': t.name,
                    'context': t.context.full,
                    'unit': t.unit
                },
                'conversionFactor': 1 if s.unit == t.unit else '?',
                'comment': comment
            }
    else:
        result = None
    return result

def match_identical_cas_numbers(s: Flow, t: Flow, comment: str = 'Identical CAS numbers'):    
    is_match = s.cas == t.cas and s.context == t.context

    result = format_match_result(s, t, comment = comment, is_match = is_match)
    return result

def match_identical_names(s: Flow, t: Flow, comment = 'Identical names'):
    is_match = s.name == t.name and s.context == t.context
    
    result = format_match_result(s, t, comment = comment, is_match = is_match)
    return result

def match_identical_names_except_missing_suffix(s: Flow, t: Flow, suffix, comment = 'Identical names except missing suffix'):
    is_match = f"{s.name}, {suffix}" == t.name and s.context == t.context
    
    result = format_match_result(s, t, comment = comment, is_match = is_match)
    return result

def match_mapped_name_differences(s: Flow, t: Flow, mapping, comment = 'Mapped name differences'):    
    is_match = mapping.get(s.name) == t.name and s.context == t.context
    
    result = format_match_result(s, t, comment = comment, is_match = is_match)
    return result

def match_resources_with_suffix_in_ground(s: Flow, t: Flow):
    return match_identical_names_except_missing_suffix(s, t, suffix = 'in ground', comment = 'Resources with suffix in ground')

def match_emissions_with_suffix_ion(s: Flow, t: Flow):
    return match_identical_names_except_missing_suffix(s, t, suffix = 'ion', comment = 'Match emissions with suffix ion')

def match_minor_random_name_differences(s: Flow, t: Flow):
    return match_mapped_name_differences(s, t, mapping = RANDOM_NAME_DIFFERENCES_MAPPING, comment = 'Minor random name differences')

def match_minor_land_name_differences(s: Flow, t: Flow):
    return match_mapped_name_differences(s, t, mapping = MINOR_LAND_NAME_DIFFERENCES_MAPPING, comment = 'Minor land name differences')

def match_missing_fossil_and_biogenic_carbon(s: Flow, t: Flow):
    return match_mapped_name_differences(s, t, mapping = MISSING_FOSSIL_AND_BIOGENIC_CARBON_MAPPING, comment = 'Missing biogenic and fossil carbon')

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
