import pytest

from plcx.utils.find import find_all, remove_number, args_counts


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


@pytest.mark.parametrize("text, exp_text", [
    ("1x2s", "xs"),
    ("111ssx", "ssx")
])
def test_remove_number(text, exp_text):
    """
    Test removing numbers from text.

    :param text: text
    :param exp_text: expected text
    """
    assert remove_number(text) == exp_text


@pytest.mark.parametrize("format_, exp_counts", [
    ("2s3sf", [("s", 2), ("s", 3), ("f", 1)]),
    ("ssf", [("s", 1), ("s", 1), ("f", 1)]),
    ("22ssf", [("s", 22), ("s", 1), ("f", 1)]),
])
def test_args_counts(format_, exp_counts):
    """
    Test found counts of character in format.

    :param format_: bytes message format
    :param exp_counts: expected list of character and their count
    """
    assert args_counts(format_) == exp_counts
