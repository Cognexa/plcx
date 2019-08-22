import pytest
import struct

from plcx.bag.reader import Reader
from plcx.utils.boolean import list_to_byte


@pytest.mark.parametrize('msg, tag, arguments, byte_order, exp_value', [
    (
        struct.pack('=B3s?', 1, b'abc', False),  # message
        ('B4x', 1),  # message tag
        [(None, 'x'), ('t1', '3s'), ('t2', '?')],  # message format
        '@',
        {'t1': b'abc', 't2': False}  # expected value
    ), (
        struct.pack('=''s''2s''i''i''?''c', b'p', b'ab', 5, 4, True, list_to_byte([True, False, True])),
        ('x2s10x', b'ab'),
        [(None, 'x'), (None, '2x'), ('i1', 'i'), ('i2', 'i'), ('b', '?'), ('lb', '#')],
        '=',
        {'i1': 5, 'i2': 4, 'b': True, 'lb': [True, False, True, False, False, False, False, False]}
    )
])
def test_reader(msg, tag, arguments, byte_order, exp_value):
    """
    Test base behavior of plcx.bag.reader.Reader.

    :param msg: bytes message
    :param tag: message tag
    :param arguments: list of parameters, define as (<name>, <format>)
    :param byte_order: indicate the byte order
    :param exp_value: expected value
    """
    reader = Reader(tag, arguments, byte_order)

    assert reader.is_readable(msg)
    assert reader.read(msg) == exp_value


@pytest.mark.parametrize('msg, tag, byte_order, is_readable', [
    (struct.pack('=''s''c', b'a', list_to_byte([True, False, True])), ('sx', b'a'), '=', True),
    (struct.pack('=''s''c', b'a', list_to_byte([True, False, True])), ('sx', b'b'), '=', False),
    (struct.pack('=''2s''c', b'ab', list_to_byte([True, False, True])), ('sx', b'a'), '=', False),
    (struct.pack('=''2s''c', b'ab', list_to_byte([True, False, True])), ('s2x', b'a'), '=', True)
])
def test_reader_not_readable(msg, tag, byte_order, is_readable):
    """
    Test Reader tes message readability.

    :param msg: bytes message
    :param tag: message tag
    :param byte_order: indicate the byte order
    :param is_readable: bool if message could be readable
    """
    reader = Reader(tag, [], '=')

    assert reader.is_readable(msg) == is_readable
