import struct

import pytest

from plcx.bag.writer import Writer


@pytest.mark.parametrize(
    "kwargs, tag, arguments, byte_order, bit_order, exp_value, exp_size",
    [
        (
            {"a": 5, "b": 3, "c": 4},
            ("c", b"a"),
            [("a", "i"), ("b", "i"), ("c", "i")],
            "@",
            "MSB",
            b"a\x00\x00\x00\x05\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00",
            16,
        ),
        (
            {"a": 5, "b": 3, "c": 4},
            ("c", b"a"),
            [("a", "i"), ("b", "i"), ("c", "i")],
            "=",
            "MSB",
            b"a\x05\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00",
            13,
        ),
        (
            {"a": 5, "b": b"a"},
            ("i", 101),
            [("a", "i"), ("b", "s")],
            "=",
            "MSB",
            b"e\x00\x00\x00\x05\x00\x00\x00a",
            9,
        ),
        (
            {"a": 5, "b": b"a"},
            ("i", 101),
            [("a", "i"), ("b", "s")],
            "@",
            "MSB",
            b"e\x00\x00\x00\x05\x00\x00\x00a",
            9,
        ),
        (
            {"a": 5},
            ("c", b"S"),
            [(None, "x"), ("a", "i")],
            "@",
            "MSB",
            b"S\x00\x00\x00\x05\x00\x00\x00",
            8,
        ),
        (
            {"a": [1, 2]},
            ("c", b"S"),
            [(None, "x"), ("a", "2i")],
            "@",
            "MSB",
            b"S\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00",
            12,
        ),
        (
            {"a": 6 * [[True] + 7 * [False]], "b": 1},
            ("c", b"S"),
            [(None, "x"), ("a", "6#xx"), ("b", "B")],
            "=",
            "MSB",
            b"S\x00\x80\x80\x80\x80\x80\x80\x00\x00\x01",
            11,
        ),
        (
            {"a": 1, "b": 2},
            ("c", b"S"),
            [("a", "B")],
            "=",
            "MSB",
            b"S\01",
            2,
        ),  # skip b
        (
            {"b": 2, "a": 1},
            ("c", b"S"),
            [("a", "B"), ("b", "B")],
            "=",
            "MSB",
            b"S\01\02",
            3,
        ),  # change order of kwargs
        (
            {"a": [True, False, True]},
            ("c", b"S"),
            [("a", "#")],
            "=",
            "LSB",
            b"S\x05",
            2,
        ),
        (
            {},
            ("c", b"S"),
            [],
            "=",
            "LSB",
            b"S",
            1,
        ),
        (
            {},
            ("c", b"S"),
            [(None, "x")],
            "=",
            "LSB",
            b"S\x00",
            2,
        ),
    ],
)
def test_writer(kwargs, tag, arguments, byte_order, bit_order, exp_value, exp_size):
    """
    Test base behavior of plcx.bag.writer.Writer.

    :param kwargs: dict of arguments
    :param tag: writer tag (<format>, <value>)
    :param arguments: list of parameters, define as (<name>, <format>)
    :param byte_order: indicate the byte order
    :param bit_order: bit order
    :param exp_value: expected value
    :param exp_size: expected message size
    """
    writer = Writer(tag, arguments, byte_order=byte_order, bit_order=bit_order)

    message = writer.write(**kwargs)

    assert message == exp_value
    assert len(message) == exp_size


@pytest.mark.parametrize(
    "kwargs, tag, arguments, byte_order, error",
    [
        ({"b": b"a"}, ("s", 101), [("b", "s")], "@", struct.error),
    ],
)
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
