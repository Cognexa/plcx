import pytest

from plcx.utils.boolean import byte_to_list, list_to_byte


@pytest.mark.parametrize('one_byte, exp', [
    (int('00100100', 2).to_bytes(1, 'little'), [False, False, True, False, False, True, False, False]),
    (int('10100001', 2).to_bytes(1, 'little'), [True, False, True, False, False, False, False, True])
])
def test_byte_to_list(one_byte, exp):
    """
    Test converting one byte to list of boolean.

    :param one_byte: one byte
    :param exp: expected value as list
    """
    assert byte_to_list(one_byte) == exp


def test_byte_to_list_error():
    """
    Test raise error.
    """
    with pytest.raises(TypeError):
        byte_to_list(int("10100001""10100001", 2).to_bytes(2, 'little'))


@pytest.mark.parametrize('boolean_list, exp', [
    ([True, False, True, False, False, True, False, False], int('10100100', 2).to_bytes(1, 'little')),
    ([True, False, True], int('10100000', 2).to_bytes(1, 'little'))
])
def test_list_to_byte(boolean_list, exp):
    """
    Test converting list of boolean to one byte,

    :param boolean_list: list of boolean
    :param exp: expected byte
    """
    assert list_to_byte(boolean_list) == exp
