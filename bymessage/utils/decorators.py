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


def msg_length(func):
    """
    Test bitarray length.
    """

    @wraps(func)
    def wrapper(self, msg: bitarray):
        if msg.length() != getattr(self, 'length', 0):
            raise TypeError('wrong message length')

        return func(self, msg=msg)

    return wrapper
