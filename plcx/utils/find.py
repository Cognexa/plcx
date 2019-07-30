from typing import List


def find_all(text: str, symbol: str) -> List[int]:
    """
    Find all positions of symbol in text.

    :param text: text
    :param symbol: searched symbol in text
    :return: list of index
    """
    return [i for i, s in enumerate(text) if s == symbol]
