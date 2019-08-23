import pytest

from plcx.bag.pack import to_bytes, dict_to_bytes, list_to_bytes


@pytest.mark.parametrize('format_, values, exp_value, exp_len', [
    ('i', (100, ), b'd\x00\x00\x00', 4),
    ('i3s?', (100, b'abc', False, ), b'd\x00\x00\x00abc\x00', 8),
    ('i3s?xx', (100, b'abc', False, ), b'd\x00\x00\x00abc\x00\x00\x00', 10),
    ('b#', (100, [1, 0, 1], ), b'd\xa0', 2),
    ('#', ([True] + 7*[False], ), b'\x80', 1),
    ('3f', ([2.2, 2.3, 2.4], ), b'\xcd\xcc\x0c@33\x13@\x9a\x99\x19@', 12),
    ('2f#2i', ([.1, .2], [True], [1, 2]), b'\xcd\xcc\xcc=\xcd\xccL>\x80\x01\x00\x00\x00\x02\x00\x00\x00', 17),
    ('##', ([True] + 7*[False], [True] + 7*[False], ), b'\x80\x80', 2),
    ('2#', (([True] + 7*[False], [True] + 7*[False]), ), b'\x80\x80', 2),
    ('2B2#', ([1, 2], ([True] + 7*[False], [True] + 7*[False]), ), b'\x01\x02\x80\x80', 4)
])
def test_to_bytes(format_, values, exp_value, exp_len):
    """
    Test convert tuple of arguments to bytes message.

    :param format_: message format
    :param values: tuple with values
    :param exp_value: expected value
    :param exp_len: expected len of bytes
    """
    message = to_bytes(format_, *values)

    assert len(message) == exp_len
    assert message == exp_value

    message_from_list = list_to_bytes(format_, list(values))
    message_from_dict = dict_to_bytes(format_, {i: value for i, value in enumerate(values)})

    assert message == message_from_list == message_from_dict
