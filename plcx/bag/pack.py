import struct

from typing import Any, Dict, List, Union, Tuple

from plcx.constants import BYTE_ORDER
from plcx.utils.boolean import find_boolean_format, boolean_to_byte


def arg_to_args(argument: Any) -> Tuple[Any]:
    """
    Convert one argument to tuple.

    :param argument: any argument
    :return: tuple with arguments
    """
    if isinstance(argument, (Tuple, List)):
        return tuple(argument)
    else:
        return (argument, )


def to_bytes(format_: str, *args, byte_order: str = BYTE_ORDER) -> bytes:
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
    arguments = []
    for i, arg in enumerate(args):
        if i in indexes:
            arguments.append(boolean_to_byte(arg))
        else:
            arguments += arg_to_args(arg)
    # convert args to bytes
    return struct.pack(f'{byte_order}{format_}', *arguments)


def list_to_bytes(format_: str, args: Union[Tuple[Any], List[Any]], byte_order: str = BYTE_ORDER) -> bytes:
    """
    Pack list of arguments to bytes message.

    :param format_: message format
    :param args: list of arguments
    :param byte_order: indicate the byte order
    :return: bytes message
    """
    return to_bytes(format_, *args, byte_order=byte_order)


def dict_to_bytes(format_: str, kwargs: Dict[str, Any], byte_order: str = BYTE_ORDER) -> bytes:
    """
    Pack dictionary  to bytes message.

    :param format_: message format
    :param kwargs: dictionary
    :param byte_order: indicate the byte order
    :return: bytes message
    """
    return to_bytes(format_, *kwargs.values(), byte_order=byte_order)
