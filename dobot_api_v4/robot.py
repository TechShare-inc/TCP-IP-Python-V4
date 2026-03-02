"""Unified high-level façade for Dobot V4 robots.

Commonly-used dashboard commands (``enable_robot``, ``mov_j``, ``get_pose``,
etc.) are available directly on :class:`DobotRobot` via the ``@forward_to``
decorator, which provides full IDE autocompletion and static type checking.

Methods that compose multiple sub-objects (lifecycle, error convenience,
feedback convenience) are defined directly on this class.

For dashboard methods *not* forwarded here, access them through
``robot.dashboard`` (e.g. ``robot.dashboard.set_payload(...)``).
"""

from typing import Optional

import numpy as np

from ._forward import forward_to
from .commands.dashboard import DobotApiDashboard
from .dtypes import FeedbackData, Pose
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedback


class DobotRobot:
    """Unified high-level robot interface.

    Eagerly creates the dashboard (port 29999) and error monitor (HTTP 22000).
    Feedback connections (30004, 30005, 30006) are created lazily on first
    access.

    Commonly-used dashboard commands are forwarded with full type signatures
    via ``@forward_to``.  For the remaining ~120 dashboard commands, use
    ``robot.dashboard.<method>(...)`` directly.

    Example::

        with DobotRobot("192.168.1.6") as robot:
            robot.enable_robot()
            pose = robot.get_pose()       # returns Pose
            qid  = robot.mov_j(...)       # returns int
            data = robot.feedback_data()  # returns FeedbackData | None
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

    # ==================================================================
    # Forwarded dashboard commands — System
    # ==================================================================

    @forward_to(DobotApiDashboard.enable_robot, type(None))
    def enable_robot(
        self,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
        is_check: int = -1,
    ) -> None:
        """Enable the robot.

        Args:
            load: Load weight (kg).
            center_x: X eccentric distance (mm).
            center_y: Y eccentric distance (mm).
            center_z: Z eccentric distance (mm).
            is_check: Check load after enable. 1=check, 0=no check, -1=omit.
        """
        ...

    @forward_to(DobotApiDashboard.disable_robot, type(None))
    def disable_robot(self) -> None:
        """Disable the robot."""
        ...

    @forward_to(DobotApiDashboard.clear_error, type(None))
    def clear_error(self) -> None:
        """Clear controller alarm information."""
        ...

    @forward_to(DobotApiDashboard.power_on, type(None))
    def power_on(self) -> None:
        """Power on the robot."""
        ...

    @forward_to(DobotApiDashboard.emergency_stop, type(None))
    def emergency_stop(self, mode: int) -> None:
        """Emergency stop the robot.

        Args:
            mode: 1=press E-Stop, 0=release E-Stop.
        """
        ...

    @forward_to(DobotApiDashboard.reset_robot, type(None))
    def reset_robot(self) -> None:
        """Reset the robot."""
        ...

    @forward_to(DobotApiDashboard.sleep, type(None))
    def sleep(self, count: int) -> None:
        """Sleep (delay) command in the motion queue.

        Args:
            count: Sleep duration in milliseconds.
        """
        ...

    # ==================================================================
    # Forwarded dashboard commands — Config
    # ==================================================================

    @forward_to(DobotApiDashboard.speed_factor, type(None))
    def speed_factor(self, speed: int) -> None:
        """Set the global speed ratio.

        Args:
            speed: Global speed ratio. Range: [1, 100].
        """
        ...

    @forward_to(DobotApiDashboard.acc_j, type(None))
    def acc_j(self, speed: int) -> None:
        """Set acceleration ratio of joint motion.

        Args:
            speed: Acceleration ratio. Range: [1, 100].
        """
        ...

    @forward_to(DobotApiDashboard.acc_l, type(None))
    def acc_l(self, speed: int) -> None:
        """Set acceleration ratio of linear and arc motion.

        Args:
            speed: Acceleration ratio. Range: [1, 100].
        """
        ...

    @forward_to(DobotApiDashboard.vel_j, type(None))
    def vel_j(self, speed: int) -> None:
        """Set speed ratio of joint motion.

        Args:
            speed: Speed ratio. Range: [1, 100].
        """
        ...

    @forward_to(DobotApiDashboard.vel_l, type(None))
    def vel_l(self, speed: int) -> None:
        """Set speed ratio of linear and arc motion.

        Args:
            speed: Speed ratio. Range: [1, 100].
        """
        ...

    @forward_to(DobotApiDashboard.cp, type(None))
    def cp(self, ratio: int) -> None:
        """Set the continuous path (CP) ratio.

        Args:
            ratio: Continuous path ratio. Range: [0, 100].
        """
        ...

    @forward_to(DobotApiDashboard.user, type(None))
    def user(self, index: int) -> None:
        """Set the global user coordinate system.

        Args:
            index: User coordinate system index.
        """
        ...

    @forward_to(DobotApiDashboard.tool, type(None))
    def tool(self, index: int) -> None:
        """Set the global tool coordinate system.

        Args:
            index: Tool coordinate system index.
        """
        ...

    # ==================================================================
    # Forwarded dashboard commands — Query
    # ==================================================================

    @forward_to(DobotApiDashboard.robot_mode, int)
    def robot_mode(self) -> int:
        """Get the current robot mode.

        Returns:
            Robot mode value (e.g. 5=ENABLE, 7=RUNNING, 9=ERROR).
        """
        ...

    @forward_to(DobotApiDashboard.get_angle, Pose)
    def get_angle(self) -> Pose:
        """Get joint coordinates of the current posture.

        Returns:
            Joint coordinates as a Pose.
        """
        ...

    @forward_to(DobotApiDashboard.get_pose, Pose)
    def get_pose(self, user: int = -1, tool: int = -1) -> Pose:
        """Get Cartesian coordinates of the current posture.

        Args:
            user: User coordinate system index. -1 = not set.
            tool: Tool coordinate system index. -1 = not set.

        Returns:
            Current Cartesian pose.
        """
        ...

    @forward_to(DobotApiDashboard.get_error_id, tuple)
    def get_error_id(self) -> tuple[int, ...]:
        """Get current error IDs from the robot controller.

        Returns:
            Active error IDs (may be empty).
        """
        ...

    @forward_to(DobotApiDashboard.positive_kin, Pose)
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
    ) -> Pose:
        """Forward kinematics — joint angles to Cartesian pose.

        Args:
            j1..j6: Joint angles in degrees.
            user: User coordinate system index. -1 = global.
            tool: Tool coordinate system index. -1 = global.

        Returns:
            Calculated Cartesian pose.
        """
        ...

    @forward_to(DobotApiDashboard.inverse_kin, Pose)
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
    ) -> Pose:
        """Inverse kinematics — Cartesian pose to joint angles.

        Args:
            x..rz: Cartesian pose (mm / degrees).
            user: User coordinate system index. -1 = global.
            tool: Tool coordinate system index. -1 = global.
            use_joint_near: 0/-1=use current angles, 1=use *joint_near*.
            joint_near: Reference joint config ``"{j1,j2,j3,j4,j5,j6}"``.

        Returns:
            Calculated joint angles as a Pose.
        """
        ...

    @forward_to(DobotApiDashboard.get_current_command_id, int)
    def get_current_command_id(self) -> int:
        """Get the queue ID of the currently executed command.

        Returns:
            Algorithm queue ID.
        """
        ...

    @forward_to(DobotApiDashboard.start_drag, type(None))
    def start_drag(self) -> None:
        """Enter drag (freedrive) mode."""
        ...

    @forward_to(DobotApiDashboard.stop_drag, type(None))
    def stop_drag(self) -> None:
        """Exit drag (freedrive) mode."""
        ...

    # ==================================================================
    # Forwarded dashboard commands — Motion
    # ==================================================================

    @forward_to(DobotApiDashboard.mov_j, int)
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
    ) -> int:
        """Joint motion to target position.

        Args:
            a1..f1: Target point (6 values).
            coordinate_mode: 0=pose, 1=joint.
            user: User coordinate system. -1=not set.
            tool: Tool coordinate system. -1=not set.
            a: Acceleration ratio. -1=not set.
            v: Velocity ratio. -1=not set.
            cp: Continuous path ratio. -1=not set.

        Returns:
            Motion queue ID.
        """
        ...

    @forward_to(DobotApiDashboard.mov_l, int)
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
    ) -> int:
        """Linear motion to target position.

        Args:
            a1..f1: Target point (6 values).
            coordinate_mode: 0=pose, 1=joint.
            user: User coordinate system. -1=not set.
            tool: Tool coordinate system. -1=not set.
            a: Acceleration ratio. -1=not set.
            v: Velocity ratio. -1=not set.
            speed: Target speed (mm/s), takes precedence over *v*.
            cp: Continuous path ratio. -1=not set.
            r: Continuous path radius (mm), takes precedence over *cp*.

        Returns:
            Motion queue ID.
        """
        ...

    @forward_to(DobotApiDashboard.servo_j, int)
    def servo_j(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        t: float = -1.0,
        ahead_time: float = -1.0,
        gain: float = -1.0,
    ) -> int:
        """Dynamic servo joint motion.

        Args:
            j1..j6: Target joint variables.
            t: Running time (s).
            ahead_time: Advance time.
            gain: Proportional gain.

        Returns:
            Motion queue ID.
        """
        ...

    @forward_to(DobotApiDashboard.servo_p, int)
    def servo_p(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        t: float = -1.0,
        ahead_time: float = -1.0,
        gain: float = -1.0,
    ) -> int:
        """Dynamic servo Cartesian motion.

        Args:
            x..rz: Target Cartesian pose.
            t: Running time (s).
            ahead_time: Advance time.
            gain: Proportional gain.

        Returns:
            Motion queue ID.
        """
        ...

    @forward_to(DobotApiDashboard.arc, int)
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
    ) -> int:
        """Arc interpolated motion through two points.

        Args:
            a1..f1: Through point P1 (6 values).
            a2..f2: Target point P2 (6 values).
            coordinate_mode: 0=pose, 1=joint.
            user: User coordinate system. -1=not set.
            tool: Tool coordinate system. -1=not set.
            a: Acceleration ratio. -1=not set.
            v: Velocity ratio. -1=not set.
            speed: Target speed (mm/s).
            cp: Continuous path ratio. -1=not set.
            r: Continuous path radius (mm).

        Returns:
            Motion queue ID.
        """
        ...

    @forward_to(DobotApiDashboard.circle, int)
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
    ) -> int:
        """Full-circle interpolated motion.

        Args:
            a1..f1: Through point P1 (6 values).
            a2..f2: End point P2 (6 values).
            coordinate_mode: 0=pose, 1=joint.
            count: Number of full circles. Range: [1, 999].
            user: User coordinate system. -1=not set.
            tool: Tool coordinate system. -1=not set.
            a: Acceleration ratio. -1=not set.
            v: Velocity ratio. -1=not set.
            speed: Target speed (mm/s).
            cp: Continuous path ratio. -1=not set.
            r: Continuous path radius (mm).

        Returns:
            Motion queue ID.
        """
        ...

    @forward_to(DobotApiDashboard.move_jog, type(None))
    def move_jog(
        self,
        axis_id: str = "",
        coord_type: int = -1,
        user: int = -1,
        tool: int = -1,
    ) -> None:
        """Start or stop joint jog motion.

        Args:
            axis_id: Axis/direction string, e.g. ``"J1+"``, ``"X-"``, ``""``.
            coord_type: 1=user coordinate, 2=tool coordinate. -1=not set.
            user: User coordinate index. -1=not set.
            tool: Tool coordinate index. -1=not set.
        """
        ...

    @forward_to(DobotApiDashboard.move_l, int)
    def move_l(
        self,
        a1: float,
        b1: float,
        c1: float,
        d1: float,
        e1: float,
        f1: float,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        speed: int = -1,
        cp: int = -1,
        r: int = -1,
    ) -> int:
        """Linear motion to target pose (pose-only, no coordinate_mode).

        Args:
            a1..f1: Target Cartesian pose (X, Y, Z, Rx, Ry, Rz).
            user: User coordinate system. -1=not set.
            tool: Tool coordinate system. -1=not set.
            a: Acceleration ratio. -1=not set.
            v: Velocity ratio. -1=not set.
            speed: Target speed (mm/s).
            cp: Continuous path ratio. -1=not set.
            r: Continuous path radius (mm).

        Returns:
            Motion queue ID.
        """
        ...

    # ==================================================================
    # Forwarded dashboard commands — I/O
    # ==================================================================

    @forward_to(DobotApiDashboard.do_output, type(None))
    def do_output(self, index: int, status: int, time: int = -1) -> None:
        """Set digital output port status (queue command).

        Args:
            index: DO index.
            status: 1=ON, 0=OFF.
            time: Continuous output time in ms. -1=not set.
        """
        ...

    @forward_to(DobotApiDashboard.get_do, int)
    def get_do(self, index: int) -> int:
        """Get digital output port status.

        Args:
            index: DO index.

        Returns:
            DO status value.
        """
        ...

    @forward_to(DobotApiDashboard.di, int)
    def di(self, index: int) -> int:
        """Get digital input port status.

        Args:
            index: DI index.

        Returns:
            DI status value.
        """
        ...

    @forward_to(DobotApiDashboard.ao, type(None))
    def ao(self, index: int, value: float) -> None:
        """Set analog output port value (queue command).

        Args:
            index: AO index.
            value: Output value. Voltage: [0, 10] V; current: [4, 20] mA.
        """
        ...

    # ==================================================================
    # Forwarded dashboard commands — Force
    # ==================================================================

    @forward_to(DobotApiDashboard.get_force, Pose)
    def get_force(self, tool: int = -1) -> Pose:
        """Get current force/torque sensor readings.

        Args:
            tool: Tool coordinate system index. -1=default frame.

        Returns:
            Force/torque readings as a Pose.
        """
        ...

    @forward_to(DobotApiDashboard.fc_off, type(None))
    def fc_off(self) -> None:
        """Turn off force-compliance mode."""
        ...

    # ==================================================================
    # Lazy feedback properties
    # ==================================================================

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

    # ==================================================================
    # Lifecycle
    # ==================================================================

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

    # ==================================================================
    # Error convenience (composes dashboard + error monitor)
    # ==================================================================

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

    # ==================================================================
    # Feedback convenience (composes lazy feedback)
    # ==================================================================

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
