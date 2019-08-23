from typing import List

from typing import Tuple, Union

BOOLEAN_FORMAT_SYMBOL = '#'


def byte_to_booleans(bytes_: bytes) -> List[List[bool]]:
    """
    Convert byte to list of booleans.

    :param bytes_: bytes convert to lists
    :return: tuple with list of boolean
    """
    # unpacked byte to bits
    return [[bool(1 << i & byte) for i in range(7, -1, -1)] for byte in bytes_]


def boolean_to_byte(booleans: Union[Tuple[List[Union[int, bool]]], List[Union[int, bool]]]) -> bytes:
    """
    Convert list of bool or int (0 or 1) values to bytes. Length of list must be at least 8.

    :param booleans: list of bool or int value
    :return: one byte
    """
    result = bytes()
    for boolean_list in (booleans, ) if not isinstance(booleans, tuple) else booleans:

        if len(boolean_list) > 8:
            raise TypeError('function to_byte expected list with max len of 8')

        # convert to 8 bit
        boolean_list = boolean_list + [0]*(8-len(boolean_list))
        result += sum(b << i for i, b in enumerate(boolean_list[::-1])).to_bytes(1, 'little')

    return result
