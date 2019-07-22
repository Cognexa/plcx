import pytest

from bitarray import bitarray

from plcx.utils.converter import read_bits


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
