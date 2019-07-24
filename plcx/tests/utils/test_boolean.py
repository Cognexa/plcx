import pytest

from plcx.utils.boolean import to_list


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
    assert to_list(one_byte) == exp


def test_byte_to_list_error():
    """
    Test raise error.
    """
    with pytest.raises(TypeError):
        to_list(int("10100001""10100001", 2).to_bytes(2, 'little'))
