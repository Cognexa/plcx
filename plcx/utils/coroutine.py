import inspect
from typing import Any


async def await_if_coroutine(obj: Any, *args, **kwargs) -> None:
    """if obj is coroutine await it"""
    if inspect.iscoroutine(obj):
        await obj(*args, **kwargs)
    else:
        obj(*args, **kwargs)
