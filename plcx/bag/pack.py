import struct
from typing import Any, Dict, List, Tuple, Union

from plcx.constants import BYTE_ORDER
from plcx.utils.boolean import BOOLEAN_FORMAT_SYMBOL, boolean_to_byte
from plcx.utils.find import args_counts


def to_bytes(format_: str, *args, byte_order: str = BYTE_ORDER) -> bytes:
    """
    Pack arguments to bytes message.

    :param format_: message format
    :param args: arguments
    :param byte_order: indicate the byte order
    :return: bytes message
    """
    # count character in format
    arguments_count = args_counts(format_)

    # convert args to bytes
    arguments = []
    for arg, char_count in zip(args, arguments_count):
        character, count = char_count
        if character == BOOLEAN_FORMAT_SYMBOL:
            arguments.append(boolean_to_byte(arg))
        elif count == 1 or character in ["c", "s"]:
            arguments.append(arg)
        else:
            arguments += arg

    # convert args to bytes
    plcx_format = format_.replace(BOOLEAN_FORMAT_SYMBOL, "s")
    return struct.pack(f"{byte_order}{plcx_format}", *arguments)


def list_to_bytes(
    format_: str, args: Union[Tuple[Any], List[Any]], byte_order: str = BYTE_ORDER
) -> bytes:
    """
    Pack list of arguments to bytes message.

    :param format_: message format
    :param args: list of arguments
    :param byte_order: indicate the byte order
    :return: bytes message
    """
    return to_bytes(format_, *args, byte_order=byte_order)


def dict_to_bytes(
    format_: str, kwargs: Dict[str, Any], byte_order: str = BYTE_ORDER
) -> bytes:
    """
    Pack dictionary  to bytes message.

    :param format_: message format
    :param kwargs: dictionary
    :param byte_order: indicate the byte order
    :return: bytes message
    """
    return to_bytes(format_, *kwargs.values(), byte_order=byte_order)
