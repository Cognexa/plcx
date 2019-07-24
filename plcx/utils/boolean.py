from typing import List

from typing import Tuple

from plcx.utils.find import find_all


def find_boolean_format(format_: str) -> Tuple[str, List[int]]:
    """
    Replace symbol `@` represent byte to list of bool value.

    :param format_: bytes format
    :return: tuple with edit format and list of positions
    """
    return format_.replace('@', 'c'), find_all(format_, '@')


def to_boolean_list(byte: bytes) -> List[bool]:
    """
    Convert byte to list of boolean.

    :param byte: one byte
    :return: list of boolean
    """
    if len(byte) != 1 or not isinstance(byte, bytes):
        raise TypeError(f'function to_boolean_list expected one byte')

    # unpacked byte to bits
    bits = f'{int(byte.hex(), 16):08b}'

    return [bool(int(bit)) for bit in bits]
