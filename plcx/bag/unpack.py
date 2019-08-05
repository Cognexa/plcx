import struct

from typing import Dict, List, Tuple, Union

from plcx.utils.boolean import find_boolean_format, byte_to_list


VALUE = Union[str, int, float, bool, List[bool]]


def bytes_to_list(msg: bytes, format_: str, byte_order: str = '@') -> List[VALUE]:
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
    return [byte_to_list(r) if i in indexes else r for i, r in enumerate(result)]


def bytes_to_dict(msg: bytes, config: List[Tuple[str, str]], byte_order: str = '@') -> Dict[str, VALUE]:
    """
    Unpack bytes with define format to dictionary.

    :param msg: bytes message
    :param config: list of message components define as tuple, (<name>, <format>)
    :param byte_order: indicate the byte order
    :return: dictionary with parameters name as keys and values as values
    """
    keys = [name for name, format_ in config if 'x' not in format_]
    values = bytes_to_list(msg=msg, format_=''.join([f for _, f in config]), byte_order=byte_order)
    return dict(zip(keys, values))
