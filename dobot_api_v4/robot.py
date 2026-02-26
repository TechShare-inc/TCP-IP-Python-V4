"""Unified high-level façade for Dobot V4 robots."""

from typing import Optional

import numpy as np

from ._forward import forward_to
from .commands.dashboard import DobotApiDashboard
from .dtypes import FeedbackData
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedback
from .responses import AckResponse, ErrorIdResponse, IntResponse, PoseResponse


class DobotRobot:
    """Unified high-level robot interface.

    Eagerly creates the dashboard (port 29999) and error monitor (HTTP 22000).
    Feedback connections (30004, 30005, 30006) are created lazily on first access.

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
    # Error convenience
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
    # Feedback convenience
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

    # ------------------------------------------------------------------
    # Forwarded system commands
    # ------------------------------------------------------------------

    @forward_to("dashboard", AckResponse)
    def enable_robot(
        self,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
        is_check: int = 0,
    ) -> AckResponse:
        """Enable the robot."""
        ...

    @forward_to("dashboard", AckResponse)
    def disable_robot(self) -> AckResponse:
        """Disable the robot."""
        ...

    @forward_to("dashboard", AckResponse)
    def clear_error(self) -> AckResponse:
        """Clear robot errors."""
        ...

    @forward_to("dashboard", AckResponse)
    def power_on(self) -> AckResponse:
        """Power on the robot."""
        ...

    @forward_to("dashboard", AckResponse)
    def emergency_stop(self, mode: int = 0) -> AckResponse:
        """Trigger emergency stop."""
        ...

    @forward_to("dashboard", AckResponse)
    def reset_robot(self) -> AckResponse:
        """Reset the robot."""
        ...

    @forward_to("dashboard", AckResponse)
    def stop_script(self) -> AckResponse:
        """Stop running script."""
        ...

    @forward_to("dashboard", AckResponse)
    def pause_script(self) -> AckResponse:
        """Pause running script."""
        ...

    @forward_to("dashboard", AckResponse)
    def resume(self) -> AckResponse:
        """Resume paused script."""
        ...

    # ------------------------------------------------------------------
    # Forwarded config commands
    # ------------------------------------------------------------------

    @forward_to("dashboard", AckResponse)
    def speed_factor(self, ratio: int) -> AckResponse:
        """Set global speed factor."""
        ...

    @forward_to("dashboard", AckResponse)
    def acc_j(self, r: int) -> AckResponse:
        """Set joint acceleration."""
        ...

    @forward_to("dashboard", AckResponse)
    def acc_l(self, r: int) -> AckResponse:
        """Set linear acceleration."""
        ...

    @forward_to("dashboard", AckResponse)
    def vel_j(self, r: int) -> AckResponse:
        """Set joint velocity."""
        ...

    @forward_to("dashboard", AckResponse)
    def vel_l(self, r: int) -> AckResponse:
        """Set linear velocity."""
        ...

    @forward_to("dashboard", AckResponse)
    def cp(self, r: int) -> AckResponse:
        """Set continuous path rate."""
        ...

    # ------------------------------------------------------------------
    # Forwarded query commands
    # ------------------------------------------------------------------

    @forward_to("dashboard", IntResponse)
    def robot_mode(self) -> IntResponse:
        """Query current robot mode."""
        ...

    @forward_to("dashboard", PoseResponse)
    def get_pose(self, user: int = -1, tool: int = -1) -> PoseResponse:
        """Get current TCP pose."""
        ...

    @forward_to("dashboard", ErrorIdResponse)
    def get_error_id(self) -> ErrorIdResponse:
        """Get current error IDs."""
        ...

    # ------------------------------------------------------------------
    # Forwarded motion commands
    # ------------------------------------------------------------------

    @forward_to("dashboard", IntResponse)
    def mov_j(
        self,
        a1: float,
        b1: float,
        c1: float,
        d1: float,
        e1: float,
        f1: float,
        coordinate_mode: int,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        cp: int = -1,
    ) -> IntResponse:
        """Joint motion to target position.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def mov_l(
        self,
        a1: float,
        b1: float,
        c1: float,
        d1: float,
        e1: float,
        f1: float,
        coordinate_mode: int,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        speed: int = -1,
        cp: int = -1,
        r: int = -1,
    ) -> IntResponse:
        """Linear motion to target position.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def servo_j(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        t: float = 0.008,
        ahead_time: float = 30,
        gain: float = 0,
    ) -> IntResponse:
        """Servo joint motion.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def servo_p(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        t: float = 0.008,
        ahead_time: float = 30,
        gain: float = 0,
    ) -> IntResponse:
        """Servo Cartesian motion.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", AckResponse)
    def move_jog(self, axis_id: str = "", coordinate_mode: int = -1) -> AckResponse:
        """Jog motion along specified axis."""
        ...

    # ------------------------------------------------------------------
    # Forwarded force commands
    # ------------------------------------------------------------------

    @forward_to("dashboard", AckResponse)
    def enable_ft_sensor(self, status: int) -> AckResponse:
        """Enable or disable the force/torque sensor."""
        ...

    @forward_to("dashboard", AckResponse)
    def fc_off(self) -> AckResponse:
        """Turn off force compliance mode."""
        ...
