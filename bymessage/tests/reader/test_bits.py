import pytest

from bymessage.utils.bitarray import bitarray


@pytest.mark.parametrize('message, readable, expect_value', [
    (
            bitarray('00110001 01100001 01100010 00110001 00101110 00110010 00110000 00000000'),
            True,
            {'2letter': 'ab', 'float': 1.2, 'bool1': False, 'bool2': False}
    ),
    (
            bitarray('00110001 01100001 01100010 00110001 00101110 00110010 00110001 01000000'),
            True,
            {'2letter': 'ab', 'float': 1.21, 'bool1': False, 'bool2': True}
    ),
    (
            bitarray('00110010 01100001 01100010 00110001 00101110 00110010 00110000 00000000'),
            False,
            None
    )
])
def test_bits_reader(bits_reader, message, readable, expect_value):
    """
    Test read function of BitsReader.

    :param bits_reader: basic BitsReader
    :param message: message as bitarray
    :param readable: if message is readable
    :param expect_value: expected dictionary if message is readable
    """
    assert bits_reader.is_readable(message) == readable
    if readable:
        assert bits_reader.read(message) == expect_value


@pytest.mark.parametrize('message, error', [
    (
        bitarray('00110001'), TypeError
    ),
    (
        # could not convert second bytes to string
        bitarray('00110001 11101001 01100010 00110001 00101110 00110010 00110001 00000000'), ValueError
    ),
    (
        # wrong code of message, expected 1 in first byte and got 2
        bitarray('00110010 01100001 01100010 00110001 00101110 00110010 00110000 00000000'), TypeError
    )
])
def test_bits_reader_error(bits_reader, message, error):
    """
    Test BitsReader error while reading message.

    :param bits_reader: basic BitsReader
    :param message: message as bitarray
    :param error: expected error
    """
    with pytest.raises(error):
        bits_reader.read(message)
