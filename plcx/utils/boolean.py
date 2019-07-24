from typing import List

from typing import Tuple, Union

from plcx.utils.find import find_all


def find_boolean_format(format_: str) -> Tuple[str, List[int]]:
    """
    Replace symbol `@` represent byte to list of bool value.

    :param format_: bytes format
    :return: tuple with edit format and list of positions
    """
    return format_.replace('@', 'c'), find_all(format_, '@')


def to_list(byte: bytes) -> List[bool]:
    """
    Convert byte to list of boolean.

    :param byte: one byte
    :return: list of boolean
    """
    if len(byte) != 1 or not isinstance(byte, bytes):
        raise TypeError('function to_list expected one byte')

    # unpacked byte to bits
    bits = f'{int(byte.hex(), 16):08b}'

    return [bool(int(bit)) for bit in bits]


def to_byte(boolean_list: List[Union[int, bool]]) -> bytes:
    """
    Convert list of bool or int value to bytes. Len of list must be at least 8.

    :param boolean_list: list of bool or int value
    :return: one byte
    """
    if len(boolean_list) > 8:
        raise TypeError('function to_byte expected list with max len of 8')

    # convert to 8 bit
    bits = ''.join(map(lambda x: str(x), boolean_list + [0]*(8-len(boolean_list))))

    return int(bits, 2).to_bytes(1, 'little')
