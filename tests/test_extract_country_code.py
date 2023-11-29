from flowmapper.utils import extract_country_code

def test_with_valid_country_code():
    assert extract_country_code('Ammonia, NL') == ('Ammonia', 'NL')

def test_with_invalid_country_code_lowercase():
    assert extract_country_code('Ammonia, nl') == ('Ammonia, nl', None)

def test_with_no_country_code():
    assert extract_country_code('Ammonia') == ('Ammonia', None)

def test_with_additional_text():
    assert extract_country_code('Ammonia, NL something') == ('Ammonia, NL something', None)

def test_with_space_before_country_code():
    assert extract_country_code('Ammonia,   NL') == ('Ammonia', 'NL')
