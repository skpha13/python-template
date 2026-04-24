from collections.abc import Callable

from ._hello_cpp import hello_world as _hello_world

hello_world: Callable[[], str] = _hello_world

__all__ = ["hello_world"]
