import pytest

from bymessage.utils.converter import bits_to_type, bits_to_dict
from bymessage.utils.bitarray import bitarray


@pytest.mark.parametrize('bits, type_, expect_value', [
    (bitarray('0'), bool, False),
    (bitarray('1'), bool, True),
    (bitarray('00110001 00101110 00110010'), float, 1.2),
    (bitarray('00110001 00101110 00110'), float, 1.),
    (bitarray('00110001'), int, 1),
    (bitarray('01100001 01100010 01100011'), str, 'abc')
])
def test_convert_bits(bits, type_, expect_value):
    """
    Test converting bitarray to format.

    :param bits: bitarray
    :param type_: convert to type
    :param expect_value: expected value
    """
    assert bits_to_type(bits, type_) == expect_value


@pytest.mark.parametrize('bits, type_, expect_error', [
    (bitarray(''), bool, TypeError),
    (bitarray(''), int, TypeError),
    (bitarray(''), float, TypeError),
    (bitarray(''), str, TypeError),
    (bitarray('10'), bool, TypeError),
    (bitarray('00110001 00101110 00110010'), int, ValueError),
    (bitarray('000'), bool, TypeError),
    (bitarray('000'), int, ValueError),
    (bitarray('000'), float, ValueError)
])
def test_convert_bits_error(bits, type_, expect_error):
    """
    Test raise error while converting to format.

    :param bits: bitarray
    :param type_: convert to type
    :param expect_error: expect_error
    """
    with pytest.raises(expect_error):
        bits_to_type(bits, type_)


@pytest.mark.parametrize('bits, config, expect_value', [
    (
        bitarray('01100001 00110010 00110010 00101110 00110011 0 1'),
        [(0, 8, 'letter', str), (8, 40, 'number', float), (40, 41, 'bool1', bool), (41, 42, 'bool2', bool)],
        {'letter': 'a', 'number': 22.3, 'bool1': False, 'bool2': True}
    ),
    (
        bitarray('0 00110001 00101110 00110010 00110101 1'),
        [(0, 1, 'bool1', bool), (1, 25, 'float', float), (25, 33, 'int', int), (33, 34, 'bool2', bool)],
        {'bool1': False, 'float': 1.2, 'int': 5, 'bool2': True}
    )
])
def test_convert_bits_to_dict(bits, config, expect_value):
    """
    Test of convert bits array to dict/json from configuration.

    :param bits: bits array
    :param config: configuration of converting
    :param expect_value: expected values in dictionary
    """
    assert bits_to_dict(bits, config) == expect_value
