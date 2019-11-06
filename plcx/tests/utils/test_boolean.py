import pytest

from plcx.utils.boolean import boolean_to_byte, byte_to_booleans


@pytest.mark.parametrize(
    "one_byte, bit_order, exp",
    [
        (int("00100100", 2).to_bytes(1, "little"), "MSB", [False, False, True, False, False, True, False, False],),
        (int("10100001", 2).to_bytes(1, "little"), "MSB", [True, False, True, False, False, False, False, True],),
        (int("10100001", 2).to_bytes(1, "little"), "LSB", [True, False, False, False, False, True, False, True],),
        (int("10000011", 2).to_bytes(1, "little"), "LSB", [True, True, False, False, False, False, False, True],),
    ],
)
def test_byte_to_booleans(one_byte, bit_order, exp):
    """Test converting one byte to list of boolean."""
    assert byte_to_booleans(one_byte, bit_order=bit_order) == [exp]


@pytest.mark.parametrize(
    "boolean_list, bit_order, exp",
    [
        ([True, False, True, False, False, True, False, False], "MSB", int("10100100", 2).to_bytes(1, "little"),),
        ([True, False, True], "MSB", int("10100000", 2).to_bytes(1, "little")),
        (([True], [True],), "MSB", int("1000000010000000", 2).to_bytes(2, "little")),
        (([True], [True],), "LSB", int("0000000100000001", 2).to_bytes(2, "little")),
        ([True, False, True], "LSB", int("00000101", 2).to_bytes(1, "little")),
    ],
)
def test_list_to_byte(boolean_list, bit_order, exp):
    """Test converting list of boolean to one byte,"""
    assert boolean_to_byte(boolean_list, bit_order=bit_order) == exp
