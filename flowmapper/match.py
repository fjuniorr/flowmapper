import logging
from tqdm import tqdm

from .constants import (
    MINOR_LAND_NAME_DIFFERENCES_MAPPING,
    MISSING_FOSSIL_AND_BIOGENIC_CARBON_MAPPING,
    RANDOM_NAME_DIFFERENCES_MAPPING,
    NAME_DIFFERENCES_WITH_UNIT_CONVERSION_MAPPING,
)
from .flow import Flow
from .utils import rm_parentheses_roman_numerals, extract_country_code, rm_roman_numerals_ionic_state

logger = logging.getLogger(__name__)

def format_match_result(s: Flow, t: Flow, conversion_factor: float, match_info: dict):
    source_context_key = s.fields['context'] if isinstance(s.fields['context'], str) else s.fields['context'][0].split('.')[0]
    source_result = {
                s.fields['name']: s.name,
                source_context_key: s.raw[source_context_key],
                s.fields['unit']: s.unit
            }
    if s.uuid:
        source_result.update({s.fields['uuid']: s.uuid})
    
    target_result = {
                'uuid': t.uuid,
                'name': t.name,
                'context': t.context.full,
                'unit': t.unit
            }
    if match_info.get('location'):
        target_result.update({'location': match_info['location']})

    result = {
            'source': source_result,
            'target': target_result,
            'conversion_factor': conversion_factor,
            'comment': match_info['comment']
        }
    return result

def get_conversion_factor(s:Flow, t: Flow):
    if s.name == 'Ammonia, as N' and t.name == 'Ammonia':
        result = 17 / 14
    elif s.unit == t.unit:
        result = 1.0
    elif s.unit == 'm2a' and t.unit == 'm2*year':
        result = 1.0
    elif s.unit == 'm3y' and t.unit == 'm3*year':
        result = 1.0
    elif s.name.startswith('Water') and t.name.startswith('Water') and s.unit == 'ton' and t.unit == 'm3':
        result = 1.0
    elif s.name.startswith('Water') and t.name.startswith('Water') and s.unit == 'g' and t.unit == 'm3':
        result = 1e-6
    elif s.name.startswith('Water') and t.name.startswith('Water') and s.unit == 'kg' and t.unit == 'm3':
        result = 1e-3
    elif s.name.startswith('Water') and t.name.startswith('Water') and s.unit == 'l' and t.unit == 'm3':
        result = 1e-3
    elif s.unit == 'Bq' and t.unit == 'kBq':
        result = 1e-3
    elif s.unit == 'ton' and t.unit == 'kg':
        result = 1e-3
    elif s.unit == 'g' and t.unit == 'kg':
        result = 1e3
    elif s.unit == 'mg' and t.unit == 'kg':
        result = 1e-6
    else:
        result = float('nan')

    return result

def match_identical_cas_numbers(s: Flow, t: Flow, comment: str = 'Identical CAS numbers'):    
    is_match = s.cas == t.cas and s.context == t.context
    if is_match:
        return {'comment': comment}

def match_identical_names(s: Flow, t: Flow, comment = 'Identical names'):
    is_match = s.name == t.name and s.context == t.context
    
    if is_match:
        return {'comment': comment}

def match_identical_names_except_missing_suffix(s: Flow, t: Flow, suffix, comment = 'Identical names except missing suffix'):
    is_match = f"{s.name}, {suffix}" == t.name and s.context == t.context
    
    if is_match:
        return {'comment': comment}

def match_mapped_name_differences(s: Flow, t: Flow, mapping, comment = 'Mapped name differences'):    
    is_match = mapping.get(s.name) == t.name and s.context == t.context
    
    if is_match:
        return {'comment': comment}

def match_names_with_roman_numerals_in_parentheses(s: Flow, t: Flow, comment = 'With/without roman numerals in parentheses'):
    is_match = rm_parentheses_roman_numerals(s.name) == rm_parentheses_roman_numerals(t.name) and s.context == t.context
    
    if is_match:
        return {'comment': comment}

def match_names_with_country_codes(s: Flow, t: Flow, comment = 'Names with country code'):
    s_name, s_location = extract_country_code(s.name)
    is_match = s_location and s_name == t.name and s.context == t.context
    
    if is_match:
        return {'comment': comment, 'location': s_location}

def match_non_ionic_state(s: Flow, t: Flow, comment = 'Non-ionic state if no better match'):
    is_match = rm_roman_numerals_ionic_state(s.name) == t.name and s.context == t.context

    if is_match:
        return {'comment': comment}

def match_biogenic_to_non_fossil(s: Flow, t: Flow, comment = 'Biogenic to non-fossil if no better match'):
    is_match = s.name.removesuffix(', biogenic') == t.name.removesuffix(', non-fossil') and s.context == t.context

    if is_match:
        return {'comment': comment}

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

def match_mapped_name_differences_with_unit_conversion(s: Flow, t: Flow):
    return match_mapped_name_differences(s, t, mapping = NAME_DIFFERENCES_WITH_UNIT_CONVERSION_MAPPING, comment = 'Mapped name differences with unit conversions')

def match_rules(): 
    return [
            match_identical_names,
            match_resources_with_suffix_in_ground,
            match_minor_random_name_differences,
            match_emissions_with_suffix_ion,
            match_minor_land_name_differences,
            match_missing_fossil_and_biogenic_carbon,
            match_names_with_roman_numerals_in_parentheses,
            match_names_with_country_codes,
            match_mapped_name_differences_with_unit_conversion,
            match_identical_cas_numbers,
            match_non_ionic_state,
            match_biogenic_to_non_fossil,
    ]
