import pytest
import struct

from plcx.bag.writer import Writer


@pytest.mark.parametrize('kwargs, tag, arguments, byte_order, exp_value, exp_size', [
    (
        {'a': 5, 'b': 3, 'c': 4},
        ('c', b'a'),
        [('a', 'i'), ('b', 'i'), ('c', 'i')],
        '@',
        b'a\x00\x00\x00\x05\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00',
        16
    ),
    (
        {'a': 5, 'b': 3, 'c': 4},
        ('c', b'a'),
        [('a', 'i'), ('b', 'i'), ('c', 'i')],
        '=',
        b'a\x05\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00',
        13
    ),
    ({'a': 5, 'b': b'a'}, ('i', 101), [('a', 'i'), ('b', 's')], '=', b'e\x00\x00\x00\x05\x00\x00\x00a', 9),
    ({'a': 5, 'b': b'a'}, ('i', 101), [('a', 'i'), ('b', 's')], '@', b'e\x00\x00\x00\x05\x00\x00\x00a', 9),
    ({'a': 5}, ('c', b'S'), [(None, 'x'), ('a', 'i')], '@', b'S\x00\x00\x00\x05\x00\x00\x00', 8),
    ({'a': [1, 2]}, ('c', b'S'), [(None, 'x'), ('a', '2i')], '@', b'S\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00', 12),
    (
        {'a': 6*[[True] + 7*[False]], 'b': 1},
        ('c', b'S'),
        [(None, 'x'), ('a', '6#xx'), ('b', 'B')],
        '=',
        b'S\x00\x80\x80\x80\x80\x80\x80\x00\x00\x01',
        11
    ),
])
def test_write(kwargs, tag, arguments, byte_order, exp_value, exp_size):
    """
    Test base behavior of plcx.bag.writer.Writer.

    :param kwargs: dict of arguments
    :param tag: writer tag (<format>, <value>)
    :param arguments: list of parameters, define as (<name>, <format>)
    :param byte_order: indicate the byte order
    :param exp_value: expected value
    :param exp_size: expected message size
    """
    writer = Writer(tag, arguments, byte_order)

    message = writer.write(**kwargs)

    assert message == exp_value
    assert len(message) == exp_size


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
