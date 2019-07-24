import struct

from typing import Dict, List, Tuple, Union

from plcx.utils.boolean import find_boolean_format, to_list


VALUE = Union[str, int, float, bool, List[bool]]


def bytes_to_list(msg: bytes, format_: str) -> List[VALUE]:
    """
    Unpack bytes with define format to list.

    :param msg: bytes message
    :param format_: bytes format
    :return: tuple with unpacked values
    """
    if not isinstance(msg, bytes):
        raise TypeError('Got unexpected type of message.')

    # find all defined boolean list in format
    format_, indexes = find_boolean_format(format_)
    # unpack bytes to tuple
    result = struct.unpack(format_, msg)
    # convert one byte character to boolean list
    return [to_list(r) if i in indexes else r for i, r in enumerate(result)]


def bytes_to_dict(msg: bytes, config: List[Tuple[str, str]]) -> Dict[str, VALUE]:
    """
    Unpack bytes with define format to dictionary.

    :param msg: bytes message
    :param config: list of message components define as tuple, (<name>, <format>)
    :return: dictionary with parameters name as keys and values as values
    """
    keys = [name for name, _ in config]
    values = bytes_to_list(msg=msg, format_=''.join([f for _, f in config]))
    return dict(zip(keys, values))
