import logging

from dataclasses import dataclass
from typing import Any, List, Tuple

from plcx.constants import BYTE_ORDER
from plcx.bag.pack import list_to_bytes

logger = logging.getLogger(__name__)


@dataclass
class Writer:
    tag: Tuple[str, Any]  # (<format>, <value>)
    arguments: List[Tuple[str, str]]  # (<name>, <format>)
    byte_order: str = BYTE_ORDER

    def write(self, **kwargs) -> bytes:
        """
        Write args or kwargs to bytes message.

        :param kwargs: arguments define as kwargs
        :return: bytes message
        """
        tag_format_, tag_value = self.tag

        format_ = tag_format_ + ''.join([f for _, f in self.arguments])

        return list_to_bytes(format_=format_, args=(tag_value,) + tuple(kwargs.values()), byte_order=self.byte_order)
