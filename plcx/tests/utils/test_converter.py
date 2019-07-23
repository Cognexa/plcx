import pytest

from bitarray import bitarray

from plcx.utils.converter import read_bits, bits_to_dict


@pytest.mark.parametrize('bits, type_, expect_value', [
    (bitarray('0'), bool, False),
    (bitarray('1'), bool, True),
    (bitarray('001100010010111000110010'), float, 1.2),
    (bitarray('001100010010111000110'), float, 1.),
    (bitarray('00110001'), int, 1),
    (bitarray('011000010110001001100011'), str, 'abc')
])
def test_convert_bits(bits, type_, expect_value):
    """
    Test converting bitarray to format.

    :param bits: bitarray
    :param type_: convert to type
    :param expect_value: expected value
    """
    assert read_bits(bits, type_) == expect_value


@pytest.mark.parametrize('bits, type_, expect_error', [
    (bitarray(''), bool, TypeError),
    (bitarray(''), int, TypeError),
    (bitarray(''), float, TypeError),
    (bitarray(''), str, TypeError),
    (bitarray('10'), bool, TypeError),
    (bitarray('001100010010111000110010'), int, ValueError),
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
        read_bits(bits, type_)


@pytest.mark.parametrize('bits, config, expect_value', [
    (
        bitarray('011000010011001000110010001011100011001101'),
        [(0, 8, 'letter', str), (8, 40, 'number', float), (40, 41, 'bool1', bool), (41, 42, 'bool2', bool)],
        {'letter': 'a', 'number': 22.3, 'bool1': False, 'bool2': True}
    ),
    (
        bitarray('0001100010010111000110010001101011'),
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
