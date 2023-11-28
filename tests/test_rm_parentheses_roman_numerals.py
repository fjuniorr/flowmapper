from flowmapper.utils import rm_parentheses_roman_numerals

def test_rm_parentheses_roman_numerals():
    assert rm_parentheses_roman_numerals('Chromium (III)') == 'Chromium III'
    assert rm_parentheses_roman_numerals('Chromium ( III )') == 'Chromium III'
    assert rm_parentheses_roman_numerals('Water (evapotranspiration)') == 'Water (evapotranspiration)'
    assert rm_parentheses_roman_numerals('Metolachlor, (S)') == 'Metolachlor, (S)'
    assert rm_parentheses_roman_numerals('Chromium (VI)') == 'Chromium VI'
    assert rm_parentheses_roman_numerals('Beryllium (II)') == 'Beryllium II'
    assert rm_parentheses_roman_numerals('Thallium (I)') == 'Thallium I'
    assert rm_parentheses_roman_numerals('Tin (IV) oxide') == 'Tin IV oxide'
