import pytest

from bymessage.reader.bits import BitesReader


@pytest.fixture
def bits_reader():
    """Define base bits reader."""
    yield BitesReader(
            name='message_1',
            length=64,
            define=(0, 8, int, 1),
            blocks=[
                (8, 24, '2letter', str),  # (start, end, name, type)
                (24, 56, 'float', float),
                (56, 57, 'bool1', bool),
                (57, 58, 'bool2', bool)
            ]
        )
