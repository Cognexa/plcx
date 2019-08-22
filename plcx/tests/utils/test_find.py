import pytest

from plcx.utils.find import find_all, start_with_integer


@pytest.mark.parametrize('text, symbol, exp_indexes', [
    ('2a2b2c2', '2', [0, 2, 4, 6]),
    ('#asdad#', '#', [0, 6])
])
def test_find_all(text, symbol, exp_indexes):
    """
    Test find all symbols in text.

    :param text: find in text
    :param symbol: find symbol
    :param exp_indexes: expected list of indexes
    """
    assert find_all(text, symbol) == exp_indexes


@pytest.mark.parametrize("text, exp_integer", [
    ("2a2b", 2),
    ("32a5", 32),
    ("abc", 1)
])
def test_start_with_integer(text, exp_integer):
    """
    Test start with integer function, which find out if text start with integer.

    :param text: text
    :param exp_integer: expected integer
    """
    assert start_with_integer(text) == exp_integer
