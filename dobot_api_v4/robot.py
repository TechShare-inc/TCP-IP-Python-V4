"""Unified high-level façade for Dobot V4 robots.

All dashboard commands (``enable_robot``, ``mov_j``, ``get_pose``, etc.)
are available directly on :class:`DobotRobot` via ``__getattr__`` delegation
to ``self.dashboard``.  Only methods that compose multiple sub-objects
(lifecycle, error convenience, feedback convenience) are defined here.
"""

from typing import Any, Optional

import numpy as np

from .commands.dashboard import DobotApiDashboard
from .dtypes import FeedbackData
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedback


class DobotRobot:
    """Unified high-level robot interface.

    Eagerly creates the dashboard (port 29999) and error monitor (HTTP 22000).
    Feedback connections (30004, 30005, 30006) are created lazily on first access.

    All dashboard commands are accessible directly on this object via
    attribute delegation (e.g. ``robot.enable_robot()`` calls
    ``robot.dashboard.enable_robot()``).

    Example::

        with DobotRobot("192.168.1.6") as robot:
            robot.enable_robot()
            pose = robot.get_pose()
            data = robot.feedback_data()
    """

    def __init__(self, ip: str, *, language: str = "en") -> None:
        """Initialize robot connections.

        Args:
            ip: Robot IP address.
            language: Default language for error messages.
        """
        self.ip = ip
        self.dashboard = DobotApiDashboard(ip, 29999)
        self.errors = RobotErrorMonitor(ip)
        self._language = language
        self._feedback: Optional[DobotApiFeedback] = None
        self._feedback_30005: Optional[DobotApiFeedback] = None
        self._feedback_30006: Optional[DobotApiFeedback] = None

    # ------------------------------------------------------------------
    # Attribute delegation
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the dashboard.

        This allows ``robot.enable_robot()`` to transparently call
        ``robot.dashboard.enable_robot()`` without redeclaring every
        method signature.

        Only public names (no leading underscore) are delegated to
        avoid interfering with Python internals.
        """
        if name.startswith("_"):
            raise AttributeError(name)
        return getattr(self.dashboard, name)

    # ------------------------------------------------------------------
    # Lazy feedback properties
    # ------------------------------------------------------------------

    @property
    def feedback(self) -> DobotApiFeedback:
        """Feedback connection on port 30004 (8 ms cycle)."""
        if self._feedback is None:
            self._feedback = DobotApiFeedback(self.ip, 30004)
        return self._feedback

    @property
    def feedback_30005(self) -> DobotApiFeedback:
        """Feedback connection on port 30005 (200 ms cycle)."""
        if self._feedback_30005 is None:
            self._feedback_30005 = DobotApiFeedback(self.ip, 30005)
        return self._feedback_30005

    @property
    def feedback_30006(self) -> DobotApiFeedback:
        """Feedback connection on port 30006 (configurable cycle)."""
        if self._feedback_30006 is None:
            self._feedback_30006 = DobotApiFeedback(self.ip, 30006)
        return self._feedback_30006

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close all open connections."""
        self.dashboard.close()
        if self._feedback is not None:
            self._feedback.close()
        if self._feedback_30005 is not None:
            self._feedback_30005.close()
        if self._feedback_30006 is not None:
            self._feedback_30006.close()

    def reconnect(self) -> None:
        """Reconnect the dashboard and any active feedback connections."""
        self.dashboard.reconnect()
        if self._feedback is not None:
            self._feedback.reconnect()
        if self._feedback_30005 is not None:
            self._feedback_30005.reconnect()
        if self._feedback_30006 is not None:
            self._feedback_30006.reconnect()

    def __enter__(self) -> "DobotRobot":
        return self

    def __exit__(self, *exc_info) -> None:  # type: ignore[override]
        self.close()

    # ------------------------------------------------------------------
    # Error convenience (composes dashboard + error monitor)
    # ------------------------------------------------------------------

    def check_errors(self, language: Optional[str] = None) -> bool:
        """Check and display current robot errors.

        Args:
            language: Override default language for error messages.

        Returns:
            ``True`` if errors are present, ``False`` otherwise.
        """
        lang = language or self._language
        return self.errors.check_errors(lang)

    def clear_robot_error(self, language: Optional[str] = None) -> bool:
        """Clear robot errors and verify they are gone.

        Args:
            language: Override default language for error messages.

        Returns:
            ``True`` if errors remain after clearing, ``False`` if clear.
        """
        self.dashboard.clear_error()
        lang = language or self._language
        return self.errors.check_errors(lang)

    # ------------------------------------------------------------------
    # Feedback convenience (composes lazy feedback)
    # ------------------------------------------------------------------

    def feedback_data(self) -> Optional[FeedbackData]:
        """Get feedback data as a typed dataclass (port 30004).

        Returns:
            ``FeedbackData`` instance, or ``None`` if no valid data.
        """
        return self.feedback.feedback_data()

    def raw_feedback_data(self) -> Optional[np.ndarray]:
        """Get raw feedback data as numpy array (port 30004).

        Returns:
            Numpy structured array, or ``None`` if no valid data.
        """
        return self.feedback.raw_feedback_data()
