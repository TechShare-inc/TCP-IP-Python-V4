"""Decorator for forwarding DobotRobot methods to the dashboard layer.

The ``@forward_to`` decorator replaces a method stub on
:class:`~dobot_api_v4.robot.DobotRobot` with a thin wrapper that delegates
the call to the corresponding method on ``self.dashboard``
(:class:`~dobot_api_v4.commands.dashboard.DobotApiDashboard`).

Because the dashboard mixin methods already parse TCP responses into typed
Python values (``None``, ``int``, ``Pose``, ``tuple[int, ...]``, ``str``),
the decorator performs **pure delegation** — no additional parsing is needed.

Usage::

    from dobot_api_v4.commands.dashboard import DobotApiDashboard

    class DobotRobot:
        @forward_to(DobotApiDashboard.enable_robot, type(None))
        def enable_robot(self, load: float = 0.0, ...) -> None:
            \"\"\"Enable the robot.\"\"\"
            ...
"""

from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def forward_to(
    dashboard_method: Callable[..., Any], return_type: type | None = None
) -> Callable[[F], F]:
    """Decorator that forwards a DobotRobot method call to dashboard.

    At decoration time the decorator captures *dashboard_method.__name__*
    so the wrapper knows which dashboard method to call at runtime.

    The decorated method's body (conventionally ``...``) is **never
    executed**.  The wrapper calls
    ``self.dashboard.<method_name>(*args, **kwargs)`` and returns the
    result unchanged.

    Args:
        dashboard_method: The unbound method on
            :class:`DobotApiDashboard` (e.g.
            ``DobotApiDashboard.enable_robot``).  Used only to derive
            the method name — it is not called directly.
        return_type: Optional type metadata stored on the wrapper as
            ``__forward_return_type__`` for introspection and
            documentation tooling.  Not used at runtime.

    Returns:
        A decorator that replaces *method* with a forwarding wrapper
        while preserving its docstring, annotations, and signature.
    """
    method_name: str = dashboard_method.__name__

    def decorator(method: F) -> F:
        @functools.wraps(method)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            target = self.dashboard
            return getattr(target, method_name)(*args, **kwargs)

        # Attach metadata for introspection / documentation tooling.
        wrapper.__forward_target__ = "dashboard"  # type: ignore[attr-defined]
        wrapper.__forward_method__ = method_name  # type: ignore[attr-defined]
        if return_type is not None:
            wrapper.__forward_return_type__ = return_type  # type: ignore[attr-defined]

        return wrapper  # type: ignore[return-value]

    return decorator
