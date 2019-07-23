import logging

from abc import abstractmethod, ABCMeta
from typing import Any, Dict, List, Tuple, Union


logger = logging.getLogger(__name__)


VALUE = Union[str, int, float, bool]
DEFINE = Tuple[int, int, Any, VALUE]  # (start, end, type and expected value)
BLOCKS = List[Tuple[int, int, str, Any]]  # list of tuple (start, end, name and type)


class BaseReader(metaclass=ABCMeta):
    def __init__(self, name: str, length: int, define: DEFINE, blocks: BLOCKS):
        self._name = name
        self._length = length
        self._define = define
        self._blocks = blocks

    @property
    def blocks(self) -> BLOCKS:
        """Get blocks of message."""
        return self._blocks

    @property
    def define(self) -> DEFINE:
        """Get definition of message."""
        return self._define

    @property
    def length(self) -> int:
        """Get length of message."""
        return self._length

    @property
    def name(self) -> str:
        """Get name of message."""
        return self._name

    @abstractmethod
    def is_readable(self, msg: Any) -> bool:
        """Test if message is readable with this reader."""
        pass

    @abstractmethod
    def read(self, msg: Any) -> Dict[str, VALUE]:
        """Read blocks of message and return it as dict/json."""
        pass
