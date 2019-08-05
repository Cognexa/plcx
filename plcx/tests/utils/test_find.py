import pytest

from plcx.utils.find import find_all


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
