from functools import cached_property

class CAS():
    """
    Class for CAS Registry Numbers® (CAS RN®) that accepts padded or non-padded strings
    """
    def __init__(self, cas: str):
        if not isinstance(cas, str):
            raise TypeError(f'cas should be a str, not {type(cas).__name__}')
        else:
            self.cas = cas.lstrip('0')
            self.digits = tuple(int(d) for d in self.cas[0:-1].replace('-', ''))
            self.check_digit_actual = int(self.cas[-1])
    def __repr__(self):
        return self.cas
    def __eq__(self, other):
        return self.cas == other.cas
    @cached_property
    def check_digit_expected(self):
        """
        Expected digit acording to https://www.cas.org/support/documentation/chemical-substances/checkdig algorithm
        """
        result = sum([
            index * value 
            for index, value in enumerate(self.digits[::-1], start=1)
        ]) % 10
        return result
    @property
    def valid(self):
        """
        True if check if CAS number is valid acording to https://www.cas.org/support/documentation/chemical-substances/checkdig algorithm
        """
        return self.check_digit_actual == self.check_digit_expected
