import asyncio

import pytest

from plcx.utils.coroutine import await_if_coroutine


def not_coroutine(x, *args):
    return x


async def is_coroutine(x, *args):
    await asyncio.sleep(0.001)
    return x


@pytest.mark.parametrize(
    "coroutine, exp_return, args",
    [
        (not_coroutine, 2, (2,)),
        (not_coroutine, "a", ("a", 1, 2, 3,)),
        (is_coroutine, 2, (2,)),
        (is_coroutine, "a", ("a", 1, 2, 3,)),
    ],
)
def test_await_if_coroutine(coroutine, exp_return, args):
    """test awaiting function if it's coroutine"""
    result = asyncio.run(await_if_coroutine(coroutine, *args))

    assert result == exp_return
