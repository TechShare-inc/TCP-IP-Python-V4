"""Forward decorator for DobotRobot method delegation."""

import functools
from typing import Any, Callable, TypeVar

from .responses import parse_response

_ResponseT = TypeVar("_ResponseT")


def forward_to(
    target_attr: str,
    response_type: type[_ResponseT],
) -> Callable[[Callable[..., Any]], Callable[..., _ResponseT]]:
    """Decorator that forwards a DobotRobot method to a sub-object.

    At runtime, replaces the method body with::

        raw = getattr(self, target_attr).<method_name>(*args, **kwargs)
        return parse_response(raw, response_type)

    Args:
        target_attr: Name of the sub-object attribute (e.g., ``"dashboard"``).
        response_type: Target response dataclass type.

    Returns:
        Decorator function.
    """

    def decorator(method: Callable[..., Any]) -> Callable[..., _ResponseT]:
        method_name = method.__name__

        @functools.wraps(method)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> _ResponseT:
            target = getattr(self, target_attr)
            raw = getattr(target, method_name)(*args, **kwargs)
            return parse_response(raw, response_type)  # type: ignore[return-value]

        return wrapper

    return decorator
