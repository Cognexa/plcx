from bitarray import bitarray as original_bitarray


def bitarray(string: str) -> original_bitarray:
    """
    Get bits array from string.

    Wrapper of default bitarray excepting string with space (separate bytes).

    :param string: string object
    :return: bitarray
    """
    return original_bitarray(string.replace(' ', ''))
