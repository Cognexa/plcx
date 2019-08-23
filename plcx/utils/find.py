from typing import List, Tuple


def find_all(text: str, symbol: str) -> List[int]:
    """
    Find all positions of symbol in text.

    :param text: text
    :param symbol: searched symbol in text
    :return: list of index
    """
    return [i for i, s in enumerate(text) if s == symbol]


def remove_number(text: str) -> str:
    """
    Remove number from sting.

    :param text: text
    :return: text without integers
    """
    return ''.join([c for c in text if not c.isdigit()])


def find_count(format_: str) -> int:
    """
    Find count of character.

    :param format_: bytes message format
    :return: count of character
    """
    result = ''
    for c in format_[::-1]:
        if not c.isdigit():
            break
        result += c

    return int(result[::-1] or '1')


def find_counts(format_: str) -> List[Tuple[str, int]]:
    """
    Find count of character in bytes message format.

    :param format_: bytes message format
    :return: list of tuples contain character and count
    """
    return [(c, find_count(format_[:i])) for i, c in enumerate(format_) if not c.isdigit()]
