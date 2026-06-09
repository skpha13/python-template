import asyncio
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


DEFAULT_EXECUTOR = ThreadPoolExecutor(max_workers=4)


async def run_in_background(
    executor: ThreadPoolExecutor | None,
    func: Callable[P, R],
    /,
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    executor = executor if executor is not None else DEFAULT_EXECUTOR

    loop = asyncio.get_running_loop()
    if kwargs:
        return await loop.run_in_executor(
            executor,
            partial(func, *args, **kwargs),
        )

    return await loop.run_in_executor(executor, func, *args)
