import logging
from .cas import CAS
from .constants import CONTEXT_MAPPING, RANDOM_NAME_DIFFERENCES_MAPPING, MINOR_LAND_NAME_DIFFERENCES_MAPPING, MISSING_FOSSIL_AND_BIOGENIC_CARBON_MAPPING

logger = logging.getLogger(__name__)

def is_same_context(source, target, fields):
    return source[fields['source']['context']] == CONTEXT_MAPPING[target[fields['target']['context']]]

def conversion_factor(source, target, fields):
    result = 1 if source[fields['source']['unit']] == target[fields['target']['unit']] else '?'
    return result

def match_identical_cas_numbers(source, target, fields, memo = 'Identical CAS numbers'):
    is_match = CAS(source[fields['source']['cas']]) == CAS(target[fields['target']['cas']]) and is_same_context(source, target, fields)
    if is_match:
        result = {
            'source': {
                fields['source']['uuid']: source[fields['source']['uuid']],
                fields['source']['name']: source[fields['source']['name']],
                fields['source']['context']: source[fields['source']['context']]
            },
            'target': {
                fields['target']['uuid']: target[fields['target']['uuid']],
            },
            'conversionFactor': conversion_factor(source, target, fields),
            'MemoMapper': memo
        }
    else:
        result = None
    return result

def match_identical_names(source, target, fields, memo = 'Identical names'):
    is_match = source[fields['source']['name']] == target[fields['target']['name']] and is_same_context(source, target, fields)
    if is_match:
        result = {
            'source': {
                fields['source']['uuid']: source[fields['source']['uuid']],
                fields['source']['name']: source[fields['source']['name']],
                fields['source']['context']: source[fields['source']['context']]
            },
            'target': {
                fields['target']['uuid']: target[fields['target']['uuid']],
            },
            'conversionFactor': conversion_factor(source, target, fields),
            'MemoMapper': memo
        }
    else:
        result = None    
    return result

def match_identical_names_except_missing_suffix(source, target, fields, suffix, memo = 'Identical names except missing suffix'):
    is_match = f"{source[fields['source']['name']]}, {suffix}" == target[fields['target']['name']] and is_same_context(source, target, fields)
    if is_match:
        result = {
            'source': {
                fields['source']['uuid']: source[fields['source']['uuid']],
                fields['source']['name']: source[fields['source']['name']],
                fields['source']['context']: source[fields['source']['context']]
            },
            'target': {
                fields['target']['uuid']: target[fields['target']['uuid']],
            },
            'conversionFactor': conversion_factor(source, target, fields),
            'MemoMapper': memo
        }
    else:
        result = None
    return result

def match_mapped_name_differences(source, target, fields, mapping, memo = 'Mapped name differences'):
    is_match = mapping.get(source[fields['source']['name']], None) == target[fields['target']['name']] and is_same_context(source, target, fields)
    if is_match:
        result = {
            'source': {
                fields['source']['uuid']: source[fields['source']['uuid']],
                fields['source']['name']: source[fields['source']['name']],
                fields['source']['context']: source[fields['source']['context']]
            },
            'target': {
                fields['target']['uuid']: target[fields['target']['uuid']],
            },
            'conversionFactor': conversion_factor(source, target, fields),
            'MemoMapper': memo
        }
    else:
        result = None
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
