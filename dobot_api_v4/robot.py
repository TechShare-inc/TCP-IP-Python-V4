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

    @forward_to("dashboard", AckResponse)
    def run_script(self, project_name: str) -> AckResponse:
        """Run a script file."""
        ...

    @forward_to("dashboard", AckResponse)
    def brake_control(self, axis_id: int, value: int) -> AckResponse:
        """Control the brake of a specified joint."""
        ...

    @forward_to("dashboard", AckResponse)
    def request_control(self) -> AckResponse:
        """Request control of the robot."""
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

    @forward_to("dashboard", AckResponse)
    def user(self, index: int) -> AckResponse:
        """Set the global user coordinate system."""
        ...

    @forward_to("dashboard", AckResponse)
    def tool(self, index: int) -> AckResponse:
        """Set the global tool coordinate system."""
        ...

    @forward_to("dashboard", AckResponse)
    def set_payload(
        self,
        load: float = 0.0,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        name: str = "F",
    ) -> AckResponse:
        """Set the load of the robot arm."""
        ...

    @forward_to("dashboard", AckResponse)
    def set_collision_level(self, level: int) -> AckResponse:
        """Set the collision detection level."""
        ...

    @forward_to("dashboard", AckResponse)
    def set_back_distance(self, distance: int) -> AckResponse:
        """Set the backoff distance after collision detection."""
        ...

    @forward_to("dashboard", AckResponse)
    def set_post_collision_mode(self, mode: int) -> AckResponse:
        """Set the post-collision processing mode."""
        ...

    @forward_to("dashboard", AckResponse)
    def drag_sensitivity(self, index: int, value: int) -> AckResponse:
        """Set the drag sensitivity."""
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

    @forward_to("dashboard", PoseResponse)
    def get_angle(self) -> PoseResponse:
        """Get the joint coordinates of the current posture."""
        ...

    @forward_to("dashboard", PoseResponse)
    def positive_kin(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        user: int = -1,
        tool: int = -1,
    ) -> PoseResponse:
        """Forward kinematics — calculate Cartesian pose from joint angles."""
        ...

    @forward_to("dashboard", PoseResponse)
    def inverse_kin(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        user: int = -1,
        tool: int = -1,
        use_joint_near: int = -1,
        joint_near: str = "",
    ) -> PoseResponse:
        """Inverse kinematics — calculate joint angles from Cartesian pose."""
        ...

    @forward_to("dashboard", IntResponse)
    def get_current_command_id(self) -> IntResponse:
        """Get the algorithm queue ID of the currently executed command."""
        ...

    @forward_to("dashboard", AckResponse)
    def start_drag(self) -> AckResponse:
        """Enter drag (freedrive) mode."""
        ...

    @forward_to("dashboard", AckResponse)
    def stop_drag(self) -> AckResponse:
        """Exit drag (freedrive) mode."""
        ...

    @forward_to("dashboard", AckResponse)
    def path_recovery(self) -> AckResponse:
        """Start path recovery."""
        ...

    @forward_to("dashboard", IntResponse)
    def path_recovery_status(self) -> IntResponse:
        """Get path recovery status."""
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

    @forward_to("dashboard", IntResponse)
    def arc(
        self,
        a1: float,
        b1: float,
        c1: float,
        d1: float,
        e1: float,
        f1: float,
        a2: float,
        b2: float,
        c2: float,
        d2: float,
        e2: float,
        f2: float,
        coordinate_mode: int,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        speed: int = -1,
        cp: int = -1,
        r: int = -1,
    ) -> IntResponse:
        """Arc interpolated motion through two points.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def circle(
        self,
        a1: float,
        b1: float,
        c1: float,
        d1: float,
        e1: float,
        f1: float,
        a2: float,
        b2: float,
        c2: float,
        d2: float,
        e2: float,
        f2: float,
        coordinate_mode: int,
        count: int,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        speed: int = -1,
        cp: int = -1,
        r: int = -1,
    ) -> IntResponse:
        """Full-circle interpolated motion.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def mov_l_io(
        self,
        a1: float,
        b1: float,
        c1: float,
        d1: float,
        e1: float,
        f1: float,
        coordinate_mode: int,
        mode: int,
        distance: int,
        index: int,
        status: int,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        speed: int = -1,
        cp: int = -1,
        r: int = -1,
    ) -> IntResponse:
        """Linear motion with digital-output triggering.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def mov_j_io(
        self,
        a1: float,
        b1: float,
        c1: float,
        d1: float,
        e1: float,
        f1: float,
        coordinate_mode: int,
        mode: int,
        distance: int,
        index: int,
        status: int,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        cp: int = -1,
    ) -> IntResponse:
        """Joint motion with digital-output triggering.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def rel_mov_j_tool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        cp: int = -1,
    ) -> IntResponse:
        """Relative joint motion along the tool coordinate system.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def rel_mov_l_tool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        speed: int = -1,
        cp: int = -1,
        r: int = -1,
    ) -> IntResponse:
        """Relative linear motion along the tool coordinate system.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def rel_mov_j_user(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        cp: int = -1,
    ) -> IntResponse:
        """Relative joint motion along the user coordinate system.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def rel_mov_l_user(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        speed: int = -1,
        cp: int = -1,
        r: int = -1,
    ) -> IntResponse:
        """Relative linear motion along the user coordinate system.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def rel_joint_mov_j(
        self,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
        a: int = -1,
        v: int = -1,
        cp: int = -1,
    ) -> IntResponse:
        """Relative joint motion along the joint coordinate system.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
        ...

    @forward_to("dashboard", IntResponse)
    def start_path(
        self,
        trace_name: str,
        is_const: int = -1,
        multi: float = -1.0,
        user: int = -1,
        tool: int = -1,
    ) -> IntResponse:
        """Play back a recorded trajectory.

        Returns:
            IntResponse whose ``value`` is the motion queue ID.
        """
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

    @forward_to("dashboard", AckResponse)
    def six_force_home(self) -> AckResponse:
        """Zero (home) the six-axis force sensor."""
        ...

    @forward_to("dashboard", PoseResponse)
    def get_force(self, tool: int = -1) -> PoseResponse:
        """Get current force/torque sensor readings."""
        ...

    @forward_to("dashboard", AckResponse)
    def fc_force_mode(
        self,
        x: int,
        y: int,
        z: int,
        rx: int,
        ry: int,
        rz: int,
        fx: int,
        fy: int,
        fz: int,
        frx: int,
        fry: int,
        frz: int,
        reference: int = -1,
        user: int = -1,
        tool: int = -1,
    ) -> AckResponse:
        """Set force-compliance mode parameters."""
        ...

    @forward_to("dashboard", AckResponse)
    def fc_set_deviation(
        self,
        x: int,
        y: int,
        z: int,
        rx: int,
        ry: int,
        rz: int,
        control_type: int = -1,
    ) -> AckResponse:
        """Set maximum deviation for force-compliance mode."""
        ...

    @forward_to("dashboard", AckResponse)
    def fc_collision_switch(self, enable: int) -> AckResponse:
        """Enable or disable force-compliance collision detection."""
        ...

    # ------------------------------------------------------------------
    # Forwarded IO commands
    # ------------------------------------------------------------------

    @forward_to("dashboard", AckResponse)
    def do_output(self, index: int, status: int, time: int = -1) -> AckResponse:
        """Set digital output port status (queue command)."""
        ...

    @forward_to("dashboard", AckResponse)
    def do_instant(self, index: int, status: int) -> AckResponse:
        """Set digital output port status (immediate command)."""
        ...

    @forward_to("dashboard", IntResponse)
    def get_do(self, index: int) -> IntResponse:
        """Get the status of digital output port."""
        ...

    @forward_to("dashboard", AckResponse)
    def tool_do(self, index: int, status: int) -> AckResponse:
        """Set tool digital output port status (queue command)."""
        ...

    @forward_to("dashboard", IntResponse)
    def get_tool_do(self, index: int) -> IntResponse:
        """Get the status of tool digital output port."""
        ...

    @forward_to("dashboard", IntResponse)
    def di(self, index: int) -> IntResponse:
        """Get the status of digital input port."""
        ...

    @forward_to("dashboard", IntResponse)
    def tool_di(self, index: int) -> IntResponse:
        """Get the status of tool digital input port."""
        ...

    @forward_to("dashboard", AckResponse)
    def ao(self, index: int, value: float) -> AckResponse:
        """Set analog output port value (queue command)."""
        ...

    @forward_to("dashboard", IntResponse)
    def ai(self, index: int) -> IntResponse:
        """Get the value of analog input port."""
        ...

    @forward_to("dashboard", IntResponse)
    def tool_ai(self, index: int) -> IntResponse:
        """Get the value of tool analog input port."""
        ...
