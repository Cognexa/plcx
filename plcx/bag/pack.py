import struct

from typing import Any, Dict, List, Union, Tuple

from plcx.utils.boolean import find_boolean_format, list_to_byte


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


def list_to_bytes(format_: str, args: Union[Tuple[Any], List[Any]], byte_order: str = '@') -> bytes:
    """
    Pack list of arguments to bytes message.

    :param format_: message format
    :param args: list of arguments
    :param byte_order: indicate the byte order
    :return: bytes message
    """
    return to_bytes(format_, *args, byte_order=byte_order)


def dict_to_bytes(format_: str, kwargs: Dict[str, Any], byte_order: str = '@') -> bytes:
    """
    Pack dictionary  to bytes message.

    :param format_: message format
    :param kwargs: dictionary
    :param byte_order: indicate the byte order
    :return: bytes message
    """
    return to_bytes(format_, *kwargs.values(), byte_order=byte_order)
