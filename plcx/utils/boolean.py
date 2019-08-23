from typing import List

from typing import Tuple, Union

from plcx.utils.find import find_all

BOOLEAN_FORMAT_SYMBOL = '#'


def find_boolean_format(format_: str) -> Tuple[str, List[int]]:
    """
    Find symbol `#` representing byte to list of boolean values conversion.
    Convert format to format string for struct.pack.

    :param format_: message format
    :return: tuple with edited format string and list of positions of character '#'
    """
    arguments = ''.join([f for f in format_ if not f.isdigit() and 'x' not in f])

    return format_.replace(BOOLEAN_FORMAT_SYMBOL, 's'), find_all(arguments, BOOLEAN_FORMAT_SYMBOL)


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


def boolean_to_byte(boolean_list: Union[Tuple[List[Union[int, bool]]], List[Union[int, bool]]]) -> bytes:
    """
    Convert list of bool or int (0 or 1) values to bytes. Length of list must be at least 8.

    :param boolean_list: list of bool or int value
    :return: one byte
    """
    result = bytes()
    for boolean in (boolean_list, ) if not isinstance(boolean_list, tuple) else boolean_list:

        if len(boolean) > 8:
            raise TypeError('function to_byte expected list with max len of 8')

        # convert to 8 bit
        boolean = boolean + [0]*(8-len(boolean))
        result += sum(b << i for i, b in enumerate(boolean[::-1])).to_bytes(1, 'little')

    return result
