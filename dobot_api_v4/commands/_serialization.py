"""Shared serialization mixin for protocol command formatting."""

from __future__ import annotations

from typing import TYPE_CHECKING


class _SerializationMixin:
    """Mixin providing argument serialization for Dobot protocol commands.

    The real ``send_recv_msg`` is inherited from ``DobotApi`` via MRO.
    This class must appear before ``DobotApi`` in the MRO of the composed
    class (e.g. ``DobotApiDashboard``) so that ``DobotApi.send_recv_msg``
    is not shadowed at runtime.
    """

    if TYPE_CHECKING:  # pragma: no cover

        def send_recv_msg(self, string: str) -> str:
            """Declared for type-checker and IDE support only.

            At runtime this method is never reached; ``DobotApi.send_recv_msg``
            is resolved via MRO instead.
            """
            ...

    def _fmt(self, value: object) -> str:
        """Format one argument into protocol text.

        Args:
            value: Argument to format. Supports int, float, str, list, tuple.

        Returns:
            Formatted string representation.
        """
        if isinstance(value, (list, tuple)):
            return "{" + ",".join(self._fmt(x) for x in value) + "}"
        if isinstance(value, float):
            return f"{value:f}"
        if isinstance(value, int):
            return f"{value:d}"
        return str(value)

    def _build_cmd(self, name: str, *args: object, **kwargs: object) -> str:
        """Build a complete ``CommandName(arg1,arg2,key=val)`` string.

        Args:
            name: Protocol command name.
            *args: Positional arguments.
            **kwargs: Keyword arguments (rendered as ``key=value``).

        Returns:
            Fully formatted command string.
        """
        parts: list[str] = []
        for a in args:
            parts.append(self._fmt(a))
        for k, v in kwargs.items():
            parts.append(f"{k}={self._fmt(v)}")
        return f"{name}(" + ",".join(parts) + ")"
