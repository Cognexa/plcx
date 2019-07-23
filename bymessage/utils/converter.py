from bitarray import bitarray
from typing import Any, Dict, List, Tuple, Union

from bymessage.utils.decorators import not_empty_bits


@not_empty_bits
def bits_to_bool(bits: bitarray) -> bool:
    """
    Convert bites to bool value.

    :param bits: bits array with length 1
    :return: bool value
    """
    if bits.length() != 1:
        raise TypeError(f'`{bits}` could not be converted to bool')

    return bool(bits[0])


@not_empty_bits
def bits_to_float(bits: bitarray) -> float:
    """
    Convert bites to float value.

    :param bits: bits array with length 1
    :return: float value
    """
    return float(bits.tostring())


@not_empty_bits
def bits_to_int(bits: bitarray) -> int:
    """
    Convert bites to int value.

    :param bits: bits array with length 1
    :return: int value
    """
    return int(bits.tostring())


@not_empty_bits
def bits_to_type(bits: bitarray, type_: Any) -> Union[str, int, float, bool]:
    """
    Convert bits to define type.

    :param bits: bits array
    :param type_: value type
    :return: converted value
    """
    if type_ == bool:
        return bits_to_bool(bits)
    elif type_ == float:
        return bits_to_float(bits)
    elif type_ == int:
        return bits_to_int(bits)
    else:
        return bits.tostring()


def bits_to_dict(bits: bitarray, config: List[Tuple[int, int, str, Any]]) -> Dict[str, Union[str, int, float, bool]]:
    """
    Convert bits to dictionary.

    :param bits: bits array
    :param config: list of message components define as tuple, (<start>, <end>, <name>, <type>)
    :return: dictionary with parameters name as keys and values as values
    """
    return {name: bits_to_type(bits[start:end], type_) for start, end, name, type_ in config}
