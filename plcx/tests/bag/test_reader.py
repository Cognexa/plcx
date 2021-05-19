import struct

import pytest

from plcx.bag.reader import Reader
from plcx.utils.boolean import boolean_to_byte


@pytest.mark.parametrize(
    "msg, tag, arguments, byte_order, bit_order, exp_value",
    [
        (
            struct.pack("=B3s?", 1, b"abc", False),  # message
            ("B", 1),  # message tag
            [("t1", "3s"), ("t2", "?")],  # message format
            "=",
            "MSB",
            {"t1": b"abc", "t2": False},  # expected value
        ),
        (
            struct.pack(
                "=" "2s" "i" "i" "?" "c",
                b"ab",
                5,
                4,
                True,
                boolean_to_byte([True, False, True]),
            ),
            ("2s", b"ab"),
            [("i1", "i"), ("i2", "i"), ("b", "?"), ("lb", "#")],
            "=",
            "MSB",
            {
                "i1": 5,
                "i2": 4,
                "b": True,
                "lb": [True, False, True, False, False, False, False, False],
            },
        ),
        (
            struct.pack("=c2sx2s2i", b"x", b"tt", b"ab", 5, 4),
            ("x2s", b"tt"),
            [(None, "x"), ("text", "2s"), ("integers", "2i")],
            "=",
            "MSB",
            {"text": b"ab", "integers": [5, 4]},
        ),
        (
            struct.pack("=c2s" "2B" "2s" "2B", b"x", b"tt", 1, 2, b"$$", 1, 2),
            ("x2s", b"tt"),
            [("integers_1", "2B"), ("booleans", "2#"), ("integers_2", "2B")],
            "=",
            "MSB",
            {
                "integers_1": [1, 2],
                "booleans": [[0, 0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0, 0]],
                "integers_2": [1, 2],
            },
        ),
        (
            struct.pack("=c" "B" "2sxx" "2B", b"x", 2, b"$$", 1, 2),
            ("c", b"x"),
            [("integers_1", "1B"), ("booleans", "2#xx"), ("integers_2", "2B")],
            "=",
            "MSB",
            {
                "integers_1": 2,
                "booleans": [[0, 0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0, 0]],
                "integers_2": [1, 2],
            },
        ),
        (
            struct.pack("=c" "2s", b"x", b"\x05\x01"),
            ("c", b"x"),
            [("booleans", "2#")],
            "=",
            "LSB",
            {"booleans": [[1, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]]},
        ),
        (
            struct.pack("=c", b"S"),
            ("c", b"S"),
            [],
            "=",
            "LSB",
            {},
        ),
        (
            struct.pack("=c" "x", b"S"),
            ("c", b"S"),
            [(None, "x")],
            "=",
            "LSB",
            {},
        ),
    ],
)
def test_reader(msg, tag, arguments, byte_order, bit_order, exp_value):
    """
    Test base behavior of plcx.bag.reader.Reader.

    :param msg: bytes message
    :param tag: message tag
    :param arguments: list of parameters, define as (<name>, <format>)
    :param byte_order: indicate the byte order
    :param bit_order: bit order
    :param exp_value: expected value
    """
    reader = Reader(tag, arguments, byte_order=byte_order, bit_order=bit_order)

    assert reader.is_readable(msg)
    assert reader.read(msg) == exp_value


@pytest.mark.parametrize(
    "msg, tag, arguments, byte_order, is_readable",
    [
        (struct.pack("=" "s" "c", b"a", b"t"), ("s", b"a"), [(None, "x")], "=", True),
        (struct.pack("=" "s" "c", b"a", b"t"), ("s", b"b"), [(None, "x")], "=", False),
        (
            struct.pack("=" "2s" "c", b"ab", b"t"),
            ("s", b"a"),
            [(None, "2x")],
            "=",
            True,
        ),
        (
            struct.pack("=" "2s" "c", b"ab", b"t"),
            ("2s", b"ab"),
            [(None, "x")],
            "=",
            True,
        ),
    ],
)
def test_reader_message_not_readable(msg, tag, arguments, byte_order, is_readable):
    """
    Test Reader tes message readability.

    :param msg: bytes message
    :param tag: message tag
    :param arguments: list of parameters, define as (<name>, <format>)
    :param byte_order: indicate the byte order
    :param is_readable: bool if message could be readable
    """
    reader = Reader(tag, arguments, byte_order="=")

    assert reader.is_readable(msg) == is_readable
