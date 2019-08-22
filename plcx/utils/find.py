from typing import List


def find_all(text: str, symbol: str) -> List[int]:
    """
    Find all positions of symbol in text.

    :param text: text
    :param symbol: searched symbol in text
    :return: list of index
    """
    return [i for i, s in enumerate(text) if s == symbol]


def find_first_integer(text: str, default: int = 1) -> int:
    """
    Find first integer in text or return default.

    :param text: text
    :param default: default integer if none is found [1]
    :return: first integer in text or default value
    """
    result = ''
    for c in text:
        if c.isdigit():
            result += c
        elif result:
            break
    return int(result or default)


def remove_number(text: str) -> str:
    """
    Remove number from sting.

    :param text: text
    :return: text without integers
    """
    return ''.join([c for c in text if not c.isdigit()])
