import logging

from bitarray import bitarray
from typing import Dict, NoReturn

from plcx.reader.base import BaseReader, VALUE
from plcx.utils.converter import bits_to_type, bits_to_dict
from plcx.utils.decorators import msg_length


logger = logging.getLogger(__name__)


class BitesReader(BaseReader):
    """
    Convert bites message to json format.

    """
    def is_define(self, msg: bitarray) -> NoReturn:
        """
        Test if message contain define value.

        :param msg: bits array
        """
        start, end, type_, expect_value = self.define

        if bits_to_type(msg[start:end], type_) != expect_value:
            raise TypeError(f'Reader `{self.name}` cloud not read message.')

    @msg_length
    def is_readable(self, msg: bitarray) -> bool:
        """
        Test if reader could read this type of message.

        :param msg: bits array
        :return: bool if is readable
        """
        try:
            self.is_define(msg)
        except (TypeError, ValueError):
            return False
        else:
            return True

    @msg_length
    def read(self, msg: bitarray) -> Dict[str, VALUE]:
        """
        Read and convert message.

        :param msg: message as bites
        :return: command type and dictionary with message as json
        """
        self.is_define(msg)  # test message
        return bits_to_dict(msg, self.blocks)
