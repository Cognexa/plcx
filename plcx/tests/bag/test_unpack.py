import pytest
import struct


from plcx.bag.unpack import bytes_to_list, bytes_to_dict


@pytest.mark.parametrize('msg, format_, exp_value', [
    (struct.pack('=i', 100), 'i', [100]),
    (struct.pack('=B', 100) + int('00100100', 2).to_bytes(1, 'little'), 'B''#', [100, [0, 0, 1, 0, 0, 1, 0, 0]]),
    (struct.pack('=ibBc', 28888, -16, 32, b'$'), 'i''b''B''#', [28888, -16, 32, [0, 0, 1, 0, 0, 1, 0, 0]]),
    (struct.pack('=ibBc', 28888, -16, 32, b'$'), 'ixxx', [28888]),
    (struct.pack('=s', b'abcdefgh'), 'c', [b'a']),
    (struct.pack('=x3s', b'abc'), 'x3s', [b'abc']),
    (struct.pack('=cx3i', b'a', 2, 3, 4), 'cx3i', [b'a', [2, 3, 4]]),
    (struct.pack('=ss', b'$', b'$'), '#''#', [[0, 0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0, 0]]),
    (struct.pack('=2s', b'$$'), '2#', [[[0, 0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0, 0]]])

])
def test_bytes_to_list(msg, format_, exp_value):
    """
    Test unpacking bytes to list of values.

    :param msg: bytes message
    :param format_: message format
    :param exp_value: expected value
    """
    assert bytes_to_list(msg, format_) == exp_value


@pytest.mark.parametrize('msg, format_, error', [
    (struct.pack('i', 1000), 'b', struct.error),
    (struct.pack('s', b'abcdefgh'), 'lbs', struct.error),
    (struct.pack('3s', b'abc'), '4s', struct.error),
    (struct.pack('x3s', b'abc'), '3s', struct.error)
])
def test_bytes_to_list_error(msg, format_, error):
    """
    Test raise error while unpacking bytes.

    :param msg: bytes message
    :param format_: message format
    :param error: expected error
    """
    with pytest.raises(error):
        bytes_to_list(msg, format_)


@pytest.mark.parametrize('msg, config, exp_value, byte_order', [
    (
        struct.pack('il', 100, 100),
        [('t1', 'i'), ('t2', 'l')],
        {'t1': 100, 't2': 100},
        '@'
    ), (
        struct.pack('xil', 100, 100),
        [(None, 'x'), ('t1', 'i'), ('t2', 'l')],
        {'t1': 100, 't2': 100},
        '@'
    ), (
        struct.pack('=''s''2s''i''i''c', b'p', b'ab', 5, 4, b'$'),
        [(None, '3x'), ('i1', 'i'), ('i2', 'i'), ('bl', '#')],
        {'i1': 5, 'i2': 4, 'bl': [0, 0, 1, 0, 0, 1, 0, 0]},
        '='
    ), (
        struct.pack('x3i3s', 1, 2, 3, b'abc'),
        [(None, 'x'), ('int', '3i'), ('text', '3s')],
        {'int': [1, 2, 3], 'text': b'abc'},
        '@'
    ),
])
def test_bytes_to_dict(msg, config, exp_value, byte_order):
    """
    Test unpacking bytes to dictionary.

    :param msg: bytes message
    :param config: list of tuples, (<name>, <format>)
    :param exp_value: expected value
    :param byte_order: indicate the byte order
    """
    assert bytes_to_dict(msg, config, byte_order) == exp_value
