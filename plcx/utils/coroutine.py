import inspect
from typing import Any


async def await_if_coroutine(obj: Any, *args, **kwargs) -> Any:
    """if obj is coroutine await it"""
    if inspect.iscoroutinefunction(obj):
        return await obj(*args, **kwargs)
    else:
        return obj(*args, **kwargs)
