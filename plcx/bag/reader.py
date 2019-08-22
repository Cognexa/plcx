import logging
import struct

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from plcx.constants import BYTE_ORDER
from plcx.bag.unpack import bytes_to_list, bytes_to_dict

logger = logging.getLogger(__name__)


@dataclass
class Reader:
    tag: Tuple[str, Any]  # (<format>, <value>)
    arguments: List[Tuple[Optional[str], str]]  # (<name>, <format>)
    byte_order: str = BYTE_ORDER

    def is_readable(self, message: bytes) -> bool:
        """
        Test if reader could read message.

        :param message: bytes message
        :return: bool value
        """
        format_, exp_value = self.tag
        try:
            value = bytes_to_list(message, format_, self.byte_order)[0]
        except struct.error:
            logger.debug(f'Error while reading message `{message}`.')
            return False
        else:
            logger.debug(f'Reader read tag value `{value}` and expected `{exp_value}`.')
            return value == exp_value

    def read(self, message: bytes) -> Dict[str, Any]:
        """
        Unpack message to dictionary.

        :param message: bytes message
        :return: dictionary with parameters
        """
        return bytes_to_dict(message, self.arguments, self.byte_order)
