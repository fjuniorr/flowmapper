import logging
from .flow import Flow
from .utils import rm_parentheses_roman_numerals, extract_country_code, rm_roman_numerals_ionic_state

logger = logging.getLogger(__name__)

def format_match_result(s: Flow, t: Flow, conversion_factor: float, match_info: dict):
    source_result = {
                     **s.name_raw_object, 
                     **s.context_raw_object,
                     **s.unit_raw_object
    }
    if s.uuid:
        source_result.update(**s.uuid_raw_object)
    
    target_result = {
                'uuid': t.uuid,
                'name': t.name_raw_value,
                'context': t.context.raw_value,
                'unit': t.unit.raw_value
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

def match_identical_uuid(s: Flow, t: Flow, comment: str = 'Identical uuid'):
    is_match = True if s.uuid and t.uuid and s.uuid == t.uuid else False
    if is_match:
        return {'comment': comment}

def match_identical_names_in_synonyms(s: Flow, t: Flow, comment: str = 'Identical synonyms'):
    is_match = True if t.synonyms and s.name.value in t.synonyms.value and s.context == t.context else False
    if is_match:
        return {'comment': comment}

def match_identical_cas_numbers(s: Flow, t: Flow, comment: str = 'Identical CAS numbers'):    
    is_match = s.cas == t.cas and s.context == t.context
    if is_match:
        return {'comment': comment}

def match_identical_names(s: Flow, t: Flow, comment = 'Identical names'):
    is_match = s.name == t.name and s.context == t.context
    
    if is_match:
        return {'comment': comment}

def match_identical_names_except_missing_suffix(s: Flow, t: Flow, suffix, comment = 'Identical names except missing suffix'):
    is_match = (
                (f"{s.name}, {suffix}" == t.name) or
                (f"{t.name}, {suffix}" == s.name) or
                (f"{s.name} {suffix}" == t.name) or
                (f"{t.name} {suffix}" == s.name)
    ) and s.context == t.context
    
    if is_match:
        return {'comment': comment}

def match_names_with_roman_numerals_in_parentheses(s: Flow, t: Flow, comment = 'With/without roman numerals in parentheses'):
    is_match = rm_parentheses_roman_numerals(s.name.value) == rm_parentheses_roman_numerals(t.name.value) and s.context == t.context
    
    if is_match:
        return {'comment': comment}

def match_names_with_country_codes(s: Flow, t: Flow, comment = 'Names with country code'):
    s_name, s_location = extract_country_code(s.name.value)
    is_match = s_location and s_name == t.name and s.context == t.context
    
    if is_match:
        return {'comment': comment, 'location': s_location.upper()}

def match_non_ionic_state(s: Flow, t: Flow, comment = 'Non-ionic state if no better match'):
    is_match = rm_roman_numerals_ionic_state(s.name.value) == t.name and s.context == t.context

    if is_match:
        return {'comment': comment}

def match_biogenic_to_non_fossil(s: Flow, t: Flow, comment = 'Biogenic to non-fossil if no better match'):
    is_match = s.name.value.removesuffix(', biogenic') == t.name.value.removesuffix(', non-fossil') and s.context == t.context

    if is_match:
        return {'comment': comment}

def match_resources_with_suffix_in_ground(s: Flow, t: Flow):
    return match_identical_names_except_missing_suffix(s, t, suffix = 'in ground', comment = 'Resources with suffix in ground')

def match_emissions_with_suffix_ion(s: Flow, t: Flow):
    return match_identical_names_except_missing_suffix(s, t, suffix = 'ion', comment = 'Match emissions with suffix ion')

def match_rules(): 
    return [
            match_identical_uuid,
            match_identical_names,
            match_resources_with_suffix_in_ground,
            match_emissions_with_suffix_ion,
            match_names_with_roman_numerals_in_parentheses,
            match_names_with_country_codes,
            match_identical_cas_numbers,
            match_non_ionic_state,
            match_biogenic_to_non_fossil,
            match_identical_names_in_synonyms,
    ]
