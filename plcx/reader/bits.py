from bitarray import bitarray
from typing import Dict

from plcx.reader.base import BaseReader, VALUE
from plcx.utils.converter import bits_to_type, bits_to_dict


class BitesReader(BaseReader):
    """
    Convert bites message to json format.

    """
    def is_readable(self, msg: bitarray) -> bool:
        """
        Test if reader could read this type of message.

        :param msg: bits array
        :return: bool if is readable
        """
        start, end, type_, expect_value = self.define

        try:
            return bits_to_type(msg[start:end], type_) == expect_value
        except (TypeError, ValueError):
            return False

    def read(self, msg: bitarray) -> Dict[str, VALUE]:
        """
        Read and convert message.

        :param msg: message as bites
        :return: command type and dictionary with message as json
        """
        return bits_to_dict(msg, self.blocks)
