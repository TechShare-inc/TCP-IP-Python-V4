"""Status query and utility commands for Dobot V4 API."""

from ..dtypes import Pose
from ._parse import parse_ack, parse_error_ids, parse_int, parse_pose
from ._serialization import _SerializationMixin


class _QueryMixin(_SerializationMixin):
    """Mixin for robot status queries and utility commands.

    Includes robot mode, pose/angle queries, error queries, kinematics
    (forward/inverse), path recovery, drag mode, tray operations, and
    log export.
    """

    # ------------------------------------------------------------------
    # Robot Status
    # ------------------------------------------------------------------

    def robot_mode(self) -> int:
        """Get the current status of the robot.

        Robot mode values:
            1: INIT — Initialized status
            2: BRAKE_OPEN — Brake switched on
            3: POWEROFF — Power-off status
            4: DISABLED — Disabled (no brake switched on)
            5: ENABLE — Enabled and idle
            6: BACKDRIVE — Drag mode
            7: RUNNING — Running status (project, TCP queue)
            8: SINGLE_MOVE — Single motion status (jog, RunTo)
            9: ERROR — Uncleared alarms (highest priority)
            10: PAUSE — Pause status
            11: COLLISION — Collision status

        Returns:
            int: Current robot mode value.
        """
        string = "RobotMode()"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Pose / Angle Queries
    # ------------------------------------------------------------------

    def get_angle(self) -> Pose:
        """Get the joint coordinates of the current posture.

        Returns:
            Pose: Joint coordinates as a Pose.
        """
        string = "GetAngle()"
        return parse_pose(self.send_recv_msg(string))

    def get_pose(self, user: int = -1, tool: int = -1) -> Pose:
        """Get Cartesian coordinates of the current posture.

        Both ``user`` and ``tool`` must be set together, or neither.
        If neither is set, the global user/tool coordinate systems are used.

        Args:
            user: Index of the calibrated user coordinate system. -1 = not set.
            tool: Index of the calibrated tool coordinate system. -1 = not set.

        Returns:
            Pose: Current Cartesian pose (x, y, z, rx, ry, rz).
        """
        string = "GetPose("
        params = []
        state = True
        if user != -1:
            params.append(f"user={user:d}")
            state = not state
        if tool != -1:
            params.append(f"tool={tool:d}")
            state = not state
        if not state:
            raise ValueError(
                "user and tool must be set or not set at the same time. "
                "They are global user coordinate system and global "
                "tool coordinate system if not set."
            )

        for i, param in enumerate(params):
            string = string + param if i == len(params) - 1 else string + param + ","

        string = string + ")"
        return parse_pose(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Error Query
    # ------------------------------------------------------------------

    def get_error_id(self) -> tuple[int, ...]:
        """Get current error IDs from the robot controller.

        Returns:
            tuple[int, ...]: Active error IDs (may be empty).
        """
        string = "GetErrorID()"
        return parse_error_ids(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Kinematics
    # ------------------------------------------------------------------

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
        """Forward kinematics — calculate Cartesian pose from joint angles.

        Args:
            j1: J1-axis position in degrees.
            j2: J2-axis position in degrees.
            j3: J3-axis position in degrees.
            j4: J4-axis position in degrees.
            j5: J5-axis position in degrees.
            j6: J6-axis position in degrees.
            user: Index of user coordinate system. -1 = global.
            tool: Index of tool coordinate system. -1 = global.

        Returns:
            Pose: Calculated Cartesian pose.
        """
        string = f"PositiveKin({j1:f},{j2:f},{j3:f},{j4:f},{j5:f},{j6:f}"
        params = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_pose(self.send_recv_msg(string))

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
        """Inverse kinematics — calculate joint angles from Cartesian pose.

        As one Cartesian pose can correspond to multiple joint solutions,
        ``use_joint_near`` and ``joint_near`` can be used to select the
        closest solution to a reference configuration.

        Args:
            x: X-axis position in mm.
            y: Y-axis position in mm.
            z: Z-axis position in mm.
            rx: Rx-axis position in degrees.
            ry: Ry-axis position in degrees.
            rz: Rz-axis position in degrees.
            user: Index of user coordinate system. -1 = global.
            tool: Index of tool coordinate system. -1 = global.
            use_joint_near: Whether ``joint_near`` is effective.
                0 or -1: use current angles, 1: use ``joint_near`` data.
            joint_near: Reference joint coordinates for solution selection.
                Format: ``"{j1,j2,j3,j4,j5,j6}"``.

        Returns:
            Pose: Calculated joint angles as a Pose.
        """
        string = f"InverseKin({x:f},{y:f},{z:f},{rx:f},{ry:f},{rz:f}"
        params = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if use_joint_near != -1:
            params.append(f"useJointNear={use_joint_near:d}")
        if joint_near != "":
            params.append(f"JointNear={joint_near:s}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_pose(self.send_recv_msg(string))

    def inverse_solution(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        user: int = -1,
        tool: int = -1,
        is_joint: int = 0,
    ) -> Pose:
        """Compute inverse solution for the given Cartesian pose.

        Args:
            x: X-axis position in mm.
            y: Y-axis position in mm.
            z: Z-axis position in mm.
            rx: Rx-axis position in degrees.
            ry: Ry-axis position in degrees.
            rz: Rz-axis position in degrees.
            user: Index of user coordinate system. -1 = global.
            tool: Index of tool coordinate system. -1 = global.
            is_joint: Whether to return joint angles. 0 = Cartesian, 1 = joint.

        Returns:
            Pose: Computed inverse solution.
        """
        string = f"InverseSolution(pose={{{x:f},{y:f},{z:f},{rx:f},{ry:f},{rz:f}}}"
        params = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if is_joint != 0:
            params.append(f"isJoint={is_joint:d}")
        for ii in params:
            string += "," + ii
        string += ")"
        return parse_pose(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Command Queue / Path Recovery
    # ------------------------------------------------------------------

    def get_current_command_id(self) -> int:
        """Get the algorithm queue ID of the currently executed command.

        Can be used to determine which command the robot is currently executing.

        Returns:
            int: Algorithm queue ID.
        """
        string = "GetCurrentCommandID()"
        return parse_int(self.send_recv_msg(string))

    def path_recovery(self) -> None:
        """Start path recovery.

        Returns:
            None
        """
        string = "PathRecovery()"
        return parse_ack(self.send_recv_msg(string))

    def path_recovery_stop(self) -> None:
        """Stop path recovery.

        Returns:
            None
        """
        string = "PathRecoveryStop()"
        return parse_ack(self.send_recv_msg(string))

    def path_recovery_status(self) -> int:
        """Get path recovery status.

        Returns:
            int: Path recovery status code.
        """
        string = "PathRecoveryStatus()"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Log Export
    # ------------------------------------------------------------------

    def log_export_usb(self, range: int) -> None:  # noqa: A002
        """Export logs to USB storage.

        Args:
            range: Log export range specifier.

        Returns:
            None
        """
        string = f"LogExportUSB({range:d})"
        return parse_ack(self.send_recv_msg(string))

    def get_export_status(self) -> int:
        """Get the status of a log export operation.

        Returns:
            int: Export status code.
        """
        string = "GetExportStatus()"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Drag Mode
    # ------------------------------------------------------------------

    def start_drag(self) -> None:
        """Enter drag (freedrive) mode.

        The robot cannot enter drag mode if it is in error status.

        Returns:
            None
        """
        string = "StartDrag()"
        return parse_ack(self.send_recv_msg(string))

    def stop_drag(self) -> None:
        """Exit drag (freedrive) mode.

        Returns:
            None
        """
        string = "StopDrag()"
        return parse_ack(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Tray Operations
    # ------------------------------------------------------------------

    def create_tray(self, *args: object, **kwargs: object) -> None:
        """Create a tray (pallet) pattern.

        Due to flexible parameter sets, this method accepts dynamic arguments.

        Args:
            *args: Positional arguments forwarded to the protocol command.
            **kwargs: Keyword arguments forwarded to the protocol command.

        Returns:
            None
        """
        return parse_ack(
            self.send_recv_msg(self._build_cmd("CreateTray", *args, **kwargs))
        )

    def get_tray_point(self, *args: object, **kwargs: object) -> Pose:
        """Get a point from a tray (pallet) pattern.

        Due to flexible parameter sets, this method accepts dynamic arguments.

        Args:
            *args: Positional arguments forwarded to the protocol command.
            **kwargs: Keyword arguments forwarded to the protocol command.

        Returns:
            Pose: Tray point as a Pose.
        """
        return parse_pose(
            self.send_recv_msg(self._build_cmd("GetTrayPoint", *args, **kwargs))
        )
