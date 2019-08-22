import struct

from typing import Dict, List, Tuple, Union

from plcx.constants import BYTE_ORDER
from plcx.utils.boolean import find_boolean_format, byte_to_booleans
from plcx.utils.find import start_with_integer


VALUE = Union[str, int, float, bool, List[bool]]


def bytes_to_list(msg: bytes, format_: str, byte_order: str = BYTE_ORDER) -> List[VALUE]:
    """
    Unpack bytes with define format to list.

    :param msg: bytes message
    :param format_: message format
    :param byte_order: indicate the byte order
    :return: tuple with unpacked values
    """
    if not isinstance(msg, bytes):
        raise TypeError('Got unexpected type of message.')

    # find all defined boolean list in format
    format_, indexes = find_boolean_format(format_)
    # unpack bytes to tuple
    result = struct.unpack(f'{byte_order}{format_}', msg)
    # convert one byte character to boolean list
    return [byte_to_booleans(r) if i in indexes else r for i, r in enumerate(result)]


def bytes_to_dict(msg: bytes, config: List[Tuple[str, str]], byte_order: str = BYTE_ORDER) -> Dict[str, VALUE]:
    """
    Unpack bytes with define format to dictionary.

    :param msg: bytes message
    :param config: list of message components define as tuple, (<name>, <format>)
    :param byte_order: indicate the byte order
    :return: dictionary with parameters name as keys and values as values
    """
    keys = [name for name, format_ in config if 'x' not in format_]
    counts = [start_with_integer(format_) for _, format_ in config if 'x' not in format_]
    values = bytes_to_list(msg=msg, format_=''.join([f for _, f in config]), byte_order=byte_order)
    # convert args to one arg
    values = [
        values.pop(0) if count == 1 or isinstance(values[0], bytes) else [values.pop(0) for _ in range(count)]
        for count in counts
    ]
    return dict(zip(keys, values))
