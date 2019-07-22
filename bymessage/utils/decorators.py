from functools import wraps
from bitarray import bitarray


def not_empty_bits(func):
    """
    Test if bits (define as first arguments) is not empty.
    """

    @wraps(func)
    def wrapper(bits: bitarray, *args, **kwargs):
        if bits.length() == 0:
            raise TypeError('empty bitarray')

        return func(bits, *args, **kwargs)

    return wrapper
