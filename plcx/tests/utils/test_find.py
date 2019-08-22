import pytest

from plcx.utils.find import find_all, find_first_integer


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
    ("abc", 1),
    ("x22abc", 22)
])
def test_find_first_integer(text, exp_integer):
    """
    Test finding first integer in text.

    :param text: text
    :param exp_integer: expected integer
    """
    assert find_first_integer(text) == exp_integer
