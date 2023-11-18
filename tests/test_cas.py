from flowmapper.cas import CAS
import pytest

def test_cas_format():
    assert CAS('96-49-1') == CAS('0000096-49-1')

def test_invalid_cas():
    assert not CAS('96-49-2').valid
    assert CAS('96-49-2').check_digit_expected == 1

def test_integer_cas():
    with pytest.raises(TypeError):
        CAS(96491)

def test_cas_repr():
    repr('0000096-49-1') == '96-49-1'
