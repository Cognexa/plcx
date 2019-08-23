from typing import List

from typing import Tuple, Union

from plcx.utils.find import find_all


def find_boolean_format(format_: str) -> Tuple[str, List[int]]:
    """
    Find symbol `#` representing byte to list of boolean values conversion.
    Convert format to format string for struct.pack.

    :param format_: message format
    :return: tuple with edited format string and list of positions of character '#'
    """
    indexes = ''.join([f for f in format_ if not f.isdigit() and 'x' not in f])
    return format_.replace('#', 's'), find_all(indexes, '#')


def byte_to_booleans(byte: bytes) -> List[bool]:
    """
    Convert byte to list of booleans.

    :param byte: one byte
    :return: list of boolean
    """
    if len(byte) != 1 or not isinstance(byte, bytes):
        raise TypeError('function to_list expected one byte')

    # unpacked byte to bits
    return [bool(1 << i & ord(byte)) for i in range(7, -1, -1)]


def list_to_byte(boolean_list: List[Union[int, bool]]) -> bytes:
    """
    Convert list of bool or int (0 or 1) values to bytes. Length of list must be at least 8.

    :param boolean_list: list of bool or int value
    :return: one byte
    """
    if len(boolean_list) > 8:
        raise TypeError('function to_byte expected list with max len of 8')

    # convert to 8 bit
    boolean_list = boolean_list + [0]*(8-len(boolean_list))
    return sum(b<<i for i, b in enumerate(boolean_list[::-1])).to_bytes(1, 'little')
