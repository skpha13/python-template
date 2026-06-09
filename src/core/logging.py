import datetime
import inspect
import logging
import logging.config
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, ParamSpec, TypeVar, cast

import yaml

from src.config import get_settings

settings = get_settings()


def _get_log_dir(log_dir: str | Path) -> Path:
    """
    Resolve the configured log directory under the base log directory and
    ensure it cannot escape `_BASE_LOG_DIR` via absolute paths or `..` segments.
    """
    candidate = (_BASE_LOG_DIR / log_dir).resolve()
    try:
        # raises ValueError if `candidate` is not within `_BASE_LOG_DIR`
        candidate.relative_to(_BASE_LOG_DIR)
    except ValueError as exc:
        raise ValueError(
            f"Invalid log_dir '{log_dir}': must resolve inside '{_BASE_LOG_DIR}'."
        ) from exc
    return candidate


_LOGGER_NAME = "src"
_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "configs" / "logger.yaml"
_BASE_LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
_LOG_DIR = _get_log_dir(settings.log_dir)


def _load_dict_config(log_dir: str | Path | None = None) -> dict[str, Any]:
    log_dir = Path(log_dir) if log_dir is not None else _LOG_DIR
    log_dir = _get_log_dir(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".log"
    raw = _CONFIG_PATH.read_text(encoding="utf-8")
    config: dict[str, Any] = yaml.safe_load(raw)
    config["handlers"]["file"]["filename"] = log_dir / log_filename

    return config


logging.config.dictConfig(_load_dict_config())
logger = logging.getLogger(_LOGGER_NAME)


def set_level(level: int) -> None:
    logger.setLevel(level)


def set_log_dir(log_dir: str | Path) -> None:
    logging.config.dictConfig(_load_dict_config(log_dir=log_dir))


P = ParamSpec("P")
T = TypeVar("T")


def log_performance(
    *, log_args: list[str] | None = None
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(fn: Callable[P, T]) -> Callable[P, T]:
        def _build_arg_string(*args: P.args, **kwargs: P.kwargs) -> str:
            selected = {}
            if log_args:
                signature = inspect.signature(fn)
                bound = signature.bind(*args, **kwargs)
                bound.apply_defaults()
                selected = {
                    name: bound.arguments[name]
                    for name in log_args
                    if name in bound.arguments
                }
            return (
                "["
                + ", ".join(f"{key}={repr(value)}" for key, value in selected.items())
                + "]"
            )

        fully_qualified_name = fn.__module__ + "." + fn.__qualname__  # ty: ignore[unresolved-attribute]

        if inspect.iscoroutinefunction(fn):

            @wraps(fn)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                logger.info(
                    f"[{fully_qualified_name}] started with args: "
                    f"{_build_arg_string(*args, **kwargs)}"
                )
                start = time.monotonic()
                result = await fn(*args, **kwargs)
                elapsed = time.monotonic() - start
                logger.info(f"[{fully_qualified_name}] finished in {elapsed:.4f}s")
                return result
        else:

            @wraps(fn)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                logger.info(
                    f"[{fully_qualified_name}] started with args: "
                    f"{_build_arg_string(*args, **kwargs)}"
                )
                start = time.monotonic()
                result = fn(*args, **kwargs)
                elapsed = time.monotonic() - start
                logger.info(f"[{fully_qualified_name}] finished in {elapsed:.4f}s")
                return result

        return cast(Callable[P, T], wrapper)

    return decorator
