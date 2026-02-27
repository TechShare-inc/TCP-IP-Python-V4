"""Motion commands for Dobot V4 API."""

from collections.abc import Sequence
from typing import Optional, Union

from loguru import logger

from ..dtypes import Pose
from ._parse import parse_ack, parse_int, parse_pose
from ._serialization import _SerializationMixin


class _MotionMixin(_SerializationMixin):
    """Mixin for robot motion commands.

    Includes joint/linear/arc/circle motions, servo control, relative motions,
    jog, trajectory playback, spline, and motion-with-IO commands.
    """

    # ------------------------------------------------------------------
    # helpers (private)
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_coordinate_mode(coordinate_mode: int, cmd: str) -> None:
        """Raise ValueError if coordinate_mode is not 0 or 1."""
        if coordinate_mode not in (0, 1):
            logger.error(
                f"Invalid coordinateMode parameter: {coordinate_mode}. "
                "Expected 0 (pose) or 1 (joint)"
            )
            raise ValueError(
                f"Invalid coordinateMode parameter: {coordinate_mode}. "
                "Expected 0 (pose) or 1 (joint)"
            )

    @staticmethod
    def _pose_or_joint(coordinate_mode: int) -> str:
        """Return ``'pose'`` or ``'joint'`` based on *coordinate_mode*."""
        return "pose" if coordinate_mode == 0 else "joint"

    @staticmethod
    def _append_speed_params(
        params: list,
        v: int,
        speed: int,
        cp: int,
        r: int,
    ) -> None:
        """Append v/speed and cp/r params with precedence rules."""
        if v != -1 and speed != -1 or speed != -1:
            params.append(f"speed={speed:d}")
        elif v != -1:
            params.append(f"v={v:d}")
        if cp != -1 and r != -1 or r != -1:
            params.append(f"r={r:d}")
        elif cp != -1:
            params.append(f"cp={cp:d}")

    # ------------------------------------------------------------------
    # Basic Motion
    # ------------------------------------------------------------------

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
        """Move to target position through joint motion.

        Args:
            a1..f1: Target point (6 values — joint angles or Cartesian pose).
            coordinate_mode: 0 = pose, 1 = joint.
            user: User coordinate system index. -1 = not set.
            tool: Tool coordinate system index. -1 = not set.
            a: Acceleration ratio. Range: (0, 100]. -1 = not set.
            v: Velocity ratio. Range: (0, 100]. -1 = not set.
            cp: Continuous path ratio. Range: [0, 100]. -1 = not set.

        Returns:
            int: Motion queue ID.
        """
        self._validate_coordinate_mode(coordinate_mode, "MovJ")
        kind = self._pose_or_joint(coordinate_mode)
        string = f"MovJ({kind:s}={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}}"
        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        if v != -1:
            params.append(f"v={v:d}")
        if cp != -1:
            params.append(f"cp={cp:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

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
        """Move to target position in linear mode.

        Args:
            a1..f1: Target point (6 values — joint angles or Cartesian pose).
            coordinate_mode: 0 = pose, 1 = joint.
            user: User coordinate system index. -1 = not set.
            tool: Tool coordinate system index. -1 = not set.
            a: Acceleration ratio. Range: (0, 100]. -1 = not set.
            v: Velocity ratio, incompatible with *speed*. Range: (0, 100].
            speed: Target speed (mm/s), takes precedence over *v*.
            cp: Continuous path ratio, incompatible with *r*. Range: [0, 100].
            r: Continuous path radius (mm), takes precedence over *cp*.

        Returns:
            int: Motion queue ID.
        """
        self._validate_coordinate_mode(coordinate_mode, "MovL")
        kind = self._pose_or_joint(coordinate_mode)
        string = f"MovL({kind:s}={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}}"
        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        self._append_speed_params(params, v, speed, cp, r)
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Servo
    # ------------------------------------------------------------------

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
            t: Running time (s). Range: [0.02, 3600.0]. Default: 0.1.
            ahead_time: Advance time (D-like PID). Range: [20.0, 100.0]. Default: 50.
            gain: Proportional gain (P-like PID). Range: [200.0, 1000.0]. Default: 500.

        Returns:
            int: Motion queue ID.
        """
        string = f"ServoJ({j1:f},{j2:f},{j3:f},{j4:f},{j5:f},{j6:f}"
        params: list[str] = []
        if t != -1:
            params.append(f"t={t:f}")
        if ahead_time != -1:
            params.append(f"aheadtime={ahead_time:f}")
        if gain != -1:
            params.append(f"gain={gain:f}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

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
            x..rz: Target posture variables (global user/tool coordinate).
            t: Running time (s). Range: [0.02, 3600.0]. Default: 0.1.
            ahead_time: Advance time (D-like PID). Range: [20.0, 100.0]. Default: 50.
            gain: Proportional gain (P-like PID). Range: [200.0, 1000.0]. Default: 500.

        Returns:
            int: Motion queue ID.
        """
        string = f"ServoP({x:f},{y:f},{z:f},{rx:f},{ry:f},{rz:f}"
        params: list[str] = []
        if t != -1:
            params.append(f"t={t:f}")
        if ahead_time != -1:
            params.append(f"aheadtime={ahead_time:f}")
        if gain != -1:
            params.append(f"gain={gain:f}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Motion with IO
    # ------------------------------------------------------------------

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
    ) -> int:
        """Linear motion with digital-output triggering.

        Args:
            a1..f1: Target point (6 values).
            coordinate_mode: 0 = pose, 1 = joint.
            mode: Trigger mode. 0 = distance percentage, 1 = distance value.
            distance: Trigger distance. Positive = from start, negative = from end.
                If mode 0: percentage (0, 100]. If mode 1: mm.
            index: DO index.
            status: DO status. 0 = no signal, 1 = signal.
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio, incompatible with *speed*. -1 = not set.
            speed: Target speed (mm/s), takes precedence over *v*.
            cp: Continuous path ratio, incompatible with *r*.
            r: Continuous path radius (mm), takes precedence over *cp*.

        Returns:
            int: Motion queue ID.
        """
        self._validate_coordinate_mode(coordinate_mode, "MovLIO")
        kind = self._pose_or_joint(coordinate_mode)
        string = (
            f"MovLIO({kind:s}={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}},"
            f"{{{mode:d},{distance:d},{index:d},{status:d}}}"
        )
        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        self._append_speed_params(params, v, speed, cp, r)
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

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
    ) -> int:
        """Joint motion with digital-output triggering.

        Args:
            a1..f1: Target point (6 values).
            coordinate_mode: 0 = pose, 1 = joint.
            mode: Trigger mode. 0 = distance percentage, 1 = distance value.
            distance: Trigger distance (percentage or degrees).
            index: DO index.
            status: DO status. 0 = no signal, 1 = signal.
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio. -1 = not set.
            cp: Continuous path ratio. -1 = not set.

        Returns:
            int: Motion queue ID.
        """
        self._validate_coordinate_mode(coordinate_mode, "MovJIO")
        kind = self._pose_or_joint(coordinate_mode)
        string = (
            f"MovJIO({kind:s}={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}},"
            f"{{{mode:d},{distance:d},{index:d},{status:d}}}"
        )
        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        if v != -1:
            params.append(f"v={v:d}")
        if cp != -1:
            params.append(f"cp={cp:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Arc / Circle
    # ------------------------------------------------------------------

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

        The current position, through-point P1, and target-point P2 define the
        arc. They must not be collinear.

        Args:
            a1..f1: Through point P1 (6 values).
            a2..f2: Target point P2 (6 values).
            coordinate_mode: 0 = pose, 1 = joint.
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio, incompatible with *speed*.
            speed: Target speed (mm/s), takes precedence over *v*.
            cp: Continuous path ratio, incompatible with *r*.
            r: Continuous path radius (mm), takes precedence over *cp*.

        Returns:
            int: Motion queue ID.
        """
        self._validate_coordinate_mode(coordinate_mode, "Arc")
        kind = self._pose_or_joint(coordinate_mode)
        string = (
            f"Arc({kind}={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}},"
            f"{kind}={{{a2:f},{b2:f},{c2:f},{d2:f},{e2:f},{f2:f}}}"
        )
        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        self._append_speed_params(params, v, speed, cp, r)
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

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

        The current position, P1, and P2 define the circle. They must not
        be collinear.

        Args:
            a1..f1: Through point P1 (6 values).
            a2..f2: End point P2 (6 values).
            coordinate_mode: 0 = pose, 1 = joint.
            count: Number of full circles. Range: [1, 999].
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio, incompatible with *speed*.
            speed: Target speed (mm/s), takes precedence over *v*.
            cp: Continuous path ratio, incompatible with *r*.
            r: Continuous path radius (mm), takes precedence over *cp*.

        Returns:
            int: Motion queue ID.
        """
        self._validate_coordinate_mode(coordinate_mode, "Circle")
        kind = self._pose_or_joint(coordinate_mode)
        string = (
            f"Circle({kind}={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}},"
            f"{kind}={{{a2:f},{b2:f},{c2:f},{d2:f},{e2:f},{f2:f}}},{count:d}"
        )
        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        self._append_speed_params(params, v, speed, cp, r)
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

    def arc_io(
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
        *io_params: Union[list, tuple],
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        speed: int = -1,
        cp: int = -1,
        r: int = -1,
        mode: int = -1,
    ) -> int:
        """Arc motion with digital-output triggering.

        Args:
            a1..f1: Through point P1 (6 values).
            a2..f2: Target point P2 (6 values).
            coordinate_mode: 0 = pose, 1 = joint.
            *io_params: IO trigger groups, each a 4-element list/tuple
                ``(Mode, Distance, Index, Status)``.
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio, incompatible with *speed*.
            speed: Target speed (mm/s), takes precedence over *v*.
            cp: Continuous path ratio, incompatible with *r*.
            r: Continuous path radius (mm), takes precedence over *cp*.
            mode: Arc mode. -1 = not set.

        Returns:
            int: Motion queue ID.
        """
        self._validate_coordinate_mode(coordinate_mode, "ArcIO")
        kind = self._pose_or_joint(coordinate_mode)
        string = (
            f"ArcIO({kind}={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}},"
            f"{kind}={{{a2:f},{b2:f},{c2:f},{d2:f},{e2:f},{f2:f}}}"
        )

        for io_param in io_params:
            if isinstance(io_param, (list, tuple)) and len(io_param) == 4:
                string += ",{{{:d},{:d},{:d},{:d}}}".format(*io_param)
            else:
                logger.error(
                    f"Invalid io_param format: {io_param}. "
                    "Expected list or tuple with 4 elements"
                )
                raise ValueError(
                    f"Invalid io_param format: {io_param}. "
                    "Expected list or tuple with 4 elements"
                )

        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        self._append_speed_params(params, v, speed, cp, r)
        if mode != -1:
            params.append(f"mode={mode:d}")
        for ii in params:
            string += "," + ii
        string += ")"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Jog
    # ------------------------------------------------------------------

    def move_jog(
        self,
        axis_id: str = "",
        coord_type: int = -1,
        user: int = -1,
        tool: int = -1,
    ) -> None:
        """Start or stop joint jog motion.

        Call with an ``axis_id`` to start jogging, or with an empty string
        to stop.

        Args:
            axis_id: Axis/direction string, e.g. ``"J1+"``, ``"X-"``, ``""``.
            coord_type: 1 = user coordinate, 2 = tool coordinate. -1 = not set.
            user: User coordinate index. -1 = not set.
            tool: Tool coordinate index. -1 = not set.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"MoveJog({axis_id:s}"
        params: list[str] = []
        if coord_type != -1:
            params.append(f"coordtype={coord_type:d}")
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Trajectory Playback
    # ------------------------------------------------------------------

    def get_start_pose(self, trace_name: str) -> Pose:
        """Get the start point of a trajectory file.

        Args:
            trace_name: Trajectory file name (with suffix). Stored in
                ``/dobot/userdata/project/process/trajectory/``.

        Returns:
            Pose: Start pose of the trajectory.
        """
        string = f"GetStartPose({trace_name:s})"
        return parse_pose(self.send_recv_msg(string))

    def start_path(
        self,
        trace_name: str,
        is_const: int = -1,
        multi: float = -1.0,
        user: int = -1,
        tool: int = -1,
    ) -> int:
        """Play back a recorded trajectory.

        Args:
            trace_name: Trajectory file name (with suffix).
            is_const: Constant speed playback. 1 = constant speed at global
                rate, 0 = original speed scaled by *multi*.
            multi: Speed multiplier (valid when is_const=0). Range: [0.25, 2].
            user: User coordinate system index. -1 = use file value.
            tool: Tool coordinate system index. -1 = use file value.

        Returns:
            int: Motion queue ID.
        """
        string = f"StartPath({trace_name:s}"
        params: list[str] = []
        if is_const != -1:
            params.append(f"isConst={is_const:d}")
        if multi != -1:
            params.append(f"multi={multi:f}")
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Relative Motion (Tool / User / Joint)
    # ------------------------------------------------------------------

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
    ) -> int:
        """Relative joint motion along the tool coordinate system.

        Args:
            offset_x: X offset (mm).
            offset_y: Y offset (mm).
            offset_z: Z offset (mm).
            offset_rx: Rx offset (degrees).
            offset_ry: Ry offset (degrees).
            offset_rz: Rz offset (degrees).
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio. -1 = not set.
            cp: Continuous path ratio. -1 = not set.

        Returns:
            int: Motion queue ID.
        """
        string = (
            f"RelMovJTool({offset_x:f},{offset_y:f},{offset_z:f},"
            f"{offset_rx:f},{offset_ry:f},{offset_rz:f}"
        )
        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        if v != -1:
            params.append(f"v={v:d}")
        if cp != -1:
            params.append(f"cp={cp:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

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
    ) -> int:
        """Relative linear motion along the tool coordinate system.

        For 6-axis robots.

        Args:
            offset_x: X offset (mm).
            offset_y: Y offset (mm).
            offset_z: Z offset (mm).
            offset_rx: Rx offset (degrees).
            offset_ry: Ry offset (degrees).
            offset_rz: Rz offset (degrees).
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio, incompatible with *speed*.
            speed: Target speed (mm/s), takes precedence over *v*.
            cp: Continuous path ratio, incompatible with *r*.
            r: Continuous path radius (mm), takes precedence over *cp*.

        Returns:
            int: Motion queue ID.
        """
        string = (
            f"RelMovLTool({offset_x:f},{offset_y:f},{offset_z:f},"
            f"{offset_rx:f},{offset_ry:f},{offset_rz:f}"
        )
        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        self._append_speed_params(params, v, speed, cp, r)
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

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
    ) -> int:
        """Relative joint motion along the user coordinate system.

        Args:
            offset_x: X offset (mm).
            offset_y: Y offset (mm).
            offset_z: Z offset (mm).
            offset_rx: Rx offset (degrees).
            offset_ry: Ry offset (degrees).
            offset_rz: Rz offset (degrees).
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio. -1 = not set.
            cp: Continuous path ratio. -1 = not set.

        Returns:
            int: Motion queue ID.
        """
        string = (
            f"RelMovJUser({offset_x:f},{offset_y:f},{offset_z:f},"
            f"{offset_rx:f},{offset_ry:f},{offset_rz:f}"
        )
        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        if v != -1:
            params.append(f"v={v:d}")
        if cp != -1:
            params.append(f"cp={cp:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

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
    ) -> int:
        """Relative linear motion along the user coordinate system.

        Args:
            offset_x: X offset (mm).
            offset_y: Y offset (mm).
            offset_z: Z offset (mm).
            offset_rx: Rx offset (degrees).
            offset_ry: Ry offset (degrees).
            offset_rz: Rz offset (degrees).
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio, incompatible with *speed*.
            speed: Target speed (mm/s), takes precedence over *v*.
            cp: Continuous path ratio, incompatible with *r*.
            r: Continuous path radius (mm), takes precedence over *cp*.

        Returns:
            int: Motion queue ID.
        """
        string = (
            f"RelMovLUser({offset_x:f},{offset_y:f},{offset_z:f},"
            f"{offset_rx:f},{offset_ry:f},{offset_rz:f}"
        )
        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        self._append_speed_params(params, v, speed, cp, r)
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

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
    ) -> int:
        """Relative joint motion along the joint coordinate system.

        Args:
            offset1..offset6: Joint axis offsets (degrees).
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio. -1 = not set.
            cp: Continuous path ratio. -1 = not set.

        Returns:
            int: Motion queue ID.
        """
        string = (
            f"RelJointMovJ({offset1:f},{offset2:f},{offset3:f},"
            f"{offset4:f},{offset5:f},{offset6:f}"
        )
        params: list[str] = []
        if a != -1:
            params.append(f"a={a:d}")
        if v != -1:
            params.append(f"v={v:d}")
        if cp != -1:
            params.append(f"cp={cp:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

    def rel_point_tool(
        self,
        coordinate_mode: int,
        a1: float,
        b1: float,
        c1: float,
        d1: float,
        e1: float,
        f1: float,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
    ) -> int:
        """Relative point motion in tool coordinate system.

        Args:
            coordinate_mode: 0 = pose, 1 = joint.
            a1..f1: Reference point (6 values).
            x..rz: Offset values (6 values).

        Returns:
            int: Motion queue ID.
        """
        kind = self._pose_or_joint(coordinate_mode)
        string = f"RelPointTool({kind:s}={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}},"
        string = string + "{" + f"{x:f},{y:f},{z:f},{rx:f},{ry:f},{rz:f}" + "}"
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

    def rel_point_user(
        self,
        coordinate_mode: int,
        a1: float,
        b1: float,
        c1: float,
        d1: float,
        e1: float,
        f1: float,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
    ) -> int:
        """Relative point motion in user coordinate system.

        Args:
            coordinate_mode: 0 = pose, 1 = joint.
            a1..f1: Reference point (6 values).
            x..rz: Offset values (6 values).

        Returns:
            int: Motion queue ID.
        """
        kind = self._pose_or_joint(coordinate_mode)
        string = f"RelPointUser({kind:s}={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}},"
        string = string + "{" + f"{x:f},{y:f},{z:f},{rx:f},{ry:f},{rz:f}" + "}"
        string = string + ")"
        return parse_int(self.send_recv_msg(string))

    def rel_joint(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
    ) -> int:
        """Relative joint motion from a reference joint configuration.

        Args:
            j1..j6: Reference joint angles.
            offset1..offset6: Joint offsets.

        Returns:
            int: Motion queue ID.
        """
        string = (
            f"RelJoint({j1:f},{j2:f},{j3:f},{j4:f},{j5:f},{j6:f},"
            f"{{{offset1:f},{offset2:f},{offset3:f},{offset4:f},{offset5:f},{offset6:f}}})"
        )
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # MoveL (pose-only variant)
    # ------------------------------------------------------------------

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
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio, incompatible with *speed*.
            speed: Target speed (mm/s), takes precedence over *v*.
            cp: Continuous path ratio, incompatible with *r*.
            r: Continuous path radius (mm), takes precedence over *cp*.

        Returns:
            int: Motion queue ID.
        """
        string = f"MoveL(pose={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}}"
        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        self._append_speed_params(params, v, speed, cp, r)
        for ii in params:
            string += "," + ii
        string += ")"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Spline (MovS)
    # ------------------------------------------------------------------

    def mov_s(
        self,
        file: Optional[str] = None,
        coordinate_mode: int = -1,
        points: Optional[Sequence[Sequence[float]]] = None,
        user: int = -1,
        tool: int = -1,
        v: int = -1,
        speed: int = -1,
        a: int = -1,
        freq: int = -1,
    ) -> int:
        """Spline motion through multiple points or from a file.

        Either *file* or both *points* + *coordinate_mode* must be provided.

        Args:
            file: Spline data file name.
            coordinate_mode: 0 = pose, 1 = joint (required with *points*).
            points: Sequence of 6-element point lists.
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            v: Velocity ratio, incompatible with *speed*.
            speed: Target speed (mm/s), takes precedence over *v*.
            a: Acceleration ratio. -1 = not set.
            freq: Frequency parameter. -1 = not set.

        Returns:
            int: Motion queue ID.
        """
        string = "MovS("
        if file is not None:
            string += f"file={file:s}"
        elif points is not None and coordinate_mode != -1:
            pts_str = []
            for pt in points:
                if coordinate_mode == 0:
                    pts_str.append("pose={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(*pt))
                elif coordinate_mode == 1:
                    pts_str.append(
                        "joint={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(*pt)
                    )
            string += ",".join(pts_str)
        else:
            logger.error(
                "Invalid MovS parameters. Expected either 'file' or both "
                "'points' and 'coordinateMode'"
            )
            raise ValueError(
                "Invalid MovS parameters. Expected either 'file' or both "
                "'points' and 'coordinateMode'"
            )

        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if v != -1 and speed != -1 or speed != -1:
            params.append(f"speed={speed:d}")
        elif v != -1:
            params.append(f"v={v:d}")
        if a != -1:
            params.append(f"a={a:d}")
        if freq != -1:
            params.append(f"freq={freq:d}")

        if len(params) > 0:
            if file is not None or (points is not None and len(points) > 0):
                string += ","
            string += ",".join(params)

        string += ")"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # RunTo
    # ------------------------------------------------------------------

    def run_to(
        self,
        a1: float,
        b1: float,
        c1: float,
        d1: float,
        e1: float,
        f1: float,
        move_type: int,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
    ) -> None:
        """Move to a target point for single-step execution.

        Args:
            a1..f1: Target point (6 values).
            move_type: 0 = pose (linear), 1 = joint.
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.
            a: Acceleration ratio. -1 = not set.
            v: Velocity ratio. -1 = not set.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        if move_type == 0:
            string = (
                f"RunTo(pose={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}},moveType=0"
            )
        elif move_type == 1:
            string = (
                f"RunTo(joint={{{a1:f},{b1:f},{c1:f},{d1:f},{e1:f},{f1:f}}},moveType=1"
            )
        else:
            logger.error(
                f"Invalid moveType parameter: {move_type}. "
                "Expected 0 (pose) or 1 (joint)"
            )
            raise ValueError(
                f"Invalid moveType parameter: {move_type}. "
                "Expected 0 (pose) or 1 (joint)"
            )

        params: list[str] = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        if v != -1:
            params.append(f"v={v:d}")
        for ii in params:
            string += "," + ii
        string += ")"
        return parse_ack(self.send_recv_msg(string))
