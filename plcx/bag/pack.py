import struct

from typing import Dict, List, Union

from plcx.utils.boolean import find_boolean_format, list_to_byte


VALUE = Union[str, int, float, bool, List[bool]]


def to_bytes(format_: str, *args, byte_order: str = '@') -> bytes:
    """
    Pack arguments to bytes message.

    :param format_: message format
    :param args: arguments
    :param byte_order: indicate the byte order
    :return: bytes message
    """
    # find all defined boolean list in format
    format_, indexes = find_boolean_format(format_)
    # convert args to bytes
    arguments = (list_to_byte(arg) if i in indexes else arg for i, arg in enumerate(args))
    # convert args to bytes
    return struct.pack(f'{byte_order}{format_}', *arguments)


def list_to_bytes(format_: str, args: List[VALUE], byte_order: str = '@') -> bytes:
    """
    Pack list of arguments to bytes message.

    :param format_: message format
    :param args: list of arguments
    :param byte_order: indicate the byte order
    :return: bytes message
    """
    return to_bytes(format_, *args, byte_order=byte_order)


def dict_to_bytes(format_: str, kwargs: Dict[str, VALUE], byte_order: str = '@') -> bytes:
    """
    Pack dictionary  to bytes message.

    :param format_: message format
    :param kwargs: dictionary
    :param byte_order: indicate the byte order
    :return: bytes message
    """
    return to_bytes(format_, *kwargs.values(), byte_order=byte_order)
