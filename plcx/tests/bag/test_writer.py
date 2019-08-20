import pytest
import struct

from plcx.bag.writer import Writer


@pytest.mark.parametrize('kwargs, tag, arguments, byte_order, exp_value', [
    (
        {'a': 5, 'b': 3, 'c': 4},
        ('c', b'a'),
        [('a', 'i'), ('b', 'i'), ('c', 'i')],
        '@',
        b'a\x00\x00\x00\x05\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00'
    ),
    (
        {'a': 5, 'b': 3, 'c': 4},
        ('c', b'a'),
        [('a', 'i'), ('b', 'i'), ('c', 'i')],
        '=',
        b'a\x05\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00'
    ),
    ({'a': 5, 'b': b'a'}, ('i', 101), [('a', 'i'), ('b', 's')], '=', b'e\x00\x00\x00\x05\x00\x00\x00a'),
    ({'a': 5, 'b': b'a'}, ('i', 101), [('a', 'i'), ('b', 's')], '@', b'e\x00\x00\x00\x05\x00\x00\x00a'),
])
def test_write(kwargs, tag, arguments, byte_order, exp_value):
    """
    Test base behavior of plcx.bag.writer.Writer.

    :param kwargs: dict of arguments
    :param tag: writer tag (<format>, <value>)
    :param arguments: list of parameters, define as (<name>, <format>)
    :param byte_order: indicate the byte order
    :param exp_value: expected value
    """
    writer = Writer(tag, arguments, byte_order)

    assert writer.write(**kwargs) == exp_value


@pytest.mark.parametrize('kwargs, tag, arguments, byte_order, error', [
    ({'a': 5, 'b': b'a'}, ('i', 101), [('b', 's')], '@', struct.error),
    ({'b': b'a'}, ('s', 101), [('b', 's')], '@', struct.error)
])
def test_write_error(kwargs, tag, arguments, byte_order, error):
    """
    Test writer raise error.

    :param kwargs: dict of arguments
    :param tag: writer tag (<format>, <value>)
    :param arguments: list of parameters, define as (<name>, <format>)
    :param byte_order: indicate the byte order
    :param error: expected error
    """
    with pytest.raises(error):
        writer = Writer(tag, arguments, byte_order)
        writer.write(**kwargs)
