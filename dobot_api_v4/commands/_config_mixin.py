"""Configuration commands for Dobot V4 API."""

from ._parse import parse_ack
from ._serialization import _SerializationMixin


class _ConfigMixin(_SerializationMixin):
    """Mixin for robot configuration commands.

    Includes speed/acceleration settings, coordinate system management,
    payload, collision detection, drag settings, safety features, and offsets.
    """

    def speed_factor(self, speed: int) -> None:
        """Set the global speed ratio.

        Actual jog speed = jog setting * global speed ratio.
        Actual playback speed = motion command ratio * playback setting * global speed ratio.

        Args:
            speed: Global speed ratio. Range: [1, 100].

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"SpeedFactor({speed:d})"
        return parse_ack(self.send_recv_msg(string))

    def acc_j(self, speed: int) -> None:
        """Set acceleration ratio of joint motion.

        Defaults to 100 if not set.

        Args:
            speed: Acceleration ratio. Range: [1, 100].

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"AccJ({speed:d})"
        return parse_ack(self.send_recv_msg(string))

    def acc_l(self, speed: int) -> None:
        """Set acceleration ratio of linear and arc motion.

        Defaults to 100 if not set.

        Args:
            speed: Acceleration ratio. Range: [1, 100].

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"AccL({speed:d})"
        return parse_ack(self.send_recv_msg(string))

    def vel_j(self, speed: int) -> None:
        """Set speed ratio of joint motion.

        Defaults to 100 if not set.

        Args:
            speed: Speed ratio. Range: [1, 100].

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"VelJ({speed:d})"
        return parse_ack(self.send_recv_msg(string))

    def vel_l(self, speed: int) -> None:
        """Set speed ratio of linear and arc motion.

        Defaults to 100 if not set.

        Args:
            speed: Speed ratio. Range: [1, 100].

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"VelL({speed:d})"
        return parse_ack(self.send_recv_msg(string))

    def cp(self, ratio: int) -> None:
        """Set the continuous path (CP) ratio.

        Controls whether the robot transitions at a right angle or curves
        when passing through intermediate points in multi-point motion.

        Defaults to 0 if not set.

        Args:
            ratio: Continuous path ratio. Range: [0, 100].

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"CP({ratio:d})"
        return parse_ack(self.send_recv_msg(string))

    def user(self, index: int) -> None:
        """Set the global user coordinate system.

        If not set, defaults to User coordinate system 0.

        Args:
            index: User coordinate system index.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"User({index:d})"
        return parse_ack(self.send_recv_msg(string))

    def set_user(self, index: int, table: str) -> None:
        """Modify the specified user coordinate system.

        Args:
            index: User coordinate system index. Range: [0, 9].
            table: Coordinate system value, format: ``{x, y, z, rx, ry, rz}``.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"SetUser({index:d},{table:s})"
        return parse_ack(self.send_recv_msg(string))

    def calc_user(self, index: int, matrix_direction: int, table: str) -> None:
        """Calculate the user coordinate system.

        Args:
            index: User coordinate system index. Range: [0, 9].
            matrix_direction: Calculation method. 1=left multiplication
                (deflect along base), 0=right multiplication (deflect along self).
            table: Coordinate system offset, format: ``{x, y, z, rx, ry, rz}``.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"CalcUser({index:d},{matrix_direction:d},{table:s})"
        return parse_ack(self.send_recv_msg(string))

    def tool(self, index: int) -> None:
        """Set the global tool coordinate system.

        If not set, defaults to Tool coordinate system 0.

        Args:
            index: Tool coordinate system index.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"Tool({index:d})"
        return parse_ack(self.send_recv_msg(string))

    def set_tool(self, index: int, table: str) -> None:
        """Modify the specified tool coordinate system.

        Args:
            index: Tool coordinate system index. Range: [0, 9].
            table: Coordinate system value, format: ``{x, y, z, rx, ry, rz}``.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"SetTool({index:d},{table:s})"
        return parse_ack(self.send_recv_msg(string))

    def calc_tool(self, index: int, matrix_direction: int, table: str) -> None:
        """Calculate the tool coordinate system.

        Args:
            index: Tool coordinate system index. Range: [0, 9].
            matrix_direction: Calculation method. 1=left multiplication
                (deflect along flange), 0=right multiplication (deflect along self).
            table: Coordinate system offset, format: ``{x, y, z, rx, ry, rz}``.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"CalcTool({index:d},{matrix_direction:d},{table:s})"
        return parse_ack(self.send_recv_msg(string))

    def set_payload(
        self,
        load: float = 0.0,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        name: str = "F",
    ) -> None:
        """Set the load of the robot arm.

        Two methods:
        - Direct parameters: ``set_payload(load, x, y, z)``
        - Preset name: ``set_payload(name="my_preset")``

        Args:
            load: Load weight (kg). Must not exceed model limit.
            x: X-axis eccentric coordinate (mm). Range: [-500, 500].
            y: Y-axis eccentric coordinate (mm). Range: [-500, 500].
            z: Z-axis eccentric coordinate (mm). Range: [-500, 500].
            name: Name of preset load parameter group. Default ``"F"`` means unused.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = "SetPayload("
        if name != "F":
            string = string + f"{name:s}"
        else:
            if load != 0:
                string = string + f"{load:f}"
                if x != 0 or y != 0 or z != 0:
                    string = string + f",{x:f},{y:f},{z:f}"
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def set_collision_level(self, level: int) -> None:
        """Set the collision detection level.

        Args:
            level: Collision detection level. 0=off, 1-5=sensitivity (higher=more sensitive).

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"SetCollisionLevel({level:d})"
        return parse_ack(self.send_recv_msg(string))

    def set_back_distance(self, distance: int) -> None:
        """Set the backoff distance after collision detection.

        Args:
            distance: Backoff distance (mm). Range: [0, 50].

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"SetBackDistance({distance:d})"
        return parse_ack(self.send_recv_msg(string))

    def set_post_collision_mode(self, mode: int) -> None:
        """Set the post-collision processing mode.

        Args:
            mode: 0=stop after collision, 1=pause after collision.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"SetPostCollisionMode({mode:d})"
        return parse_ack(self.send_recv_msg(string))

    def drag_sensitivity(self, index: int, value: int) -> None:
        """Set the drag sensitivity.

        Args:
            index: Axis ID. 1-6=J1-J6, 0=all axes.
            value: Drag sensitivity. Smaller=more force needed. Range: [1, 90].

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"DragSensivity({index:d},{value:d})"
        return parse_ack(self.send_recv_msg(string))

    def enable_safe_skin(self, status: int) -> None:
        """Switch on or off the SafeSkin.

        Valid only for robot arms equipped with SafeSkin.

        Args:
            status: SafeSkin switch. 0=off, 1=on.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"EnableSafeSkin({status:d})"
        return parse_ack(self.send_recv_msg(string))

    def set_safe_skin(self, part: int, status: int) -> None:
        """Set sensitivity for each part of the SafeSkin.

        Valid only for robot arms equipped with SafeSkin.

        Args:
            part: Part to set. 3=forearm, 4-6=J4-J6.
            status: Sensitivity. 0=off, 1=low, 2=middle, 3=high.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"SetSafeSkin({part:d},{status:d})"
        return parse_ack(self.send_recv_msg(string))

    def set_safe_wall_enable(self, index: int, value: int) -> None:
        """Switch on/off the specified safety wall.

        Args:
            index: Safety wall index (must be added in software first). Range: [1, 8].
            value: Switch. 0=off, 1=on.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"SetSafeWallEnable({index:d},{value:d})"
        return parse_ack(self.send_recv_msg(string))

    def set_work_zone_enable(self, index: int, value: int) -> None:
        """Switch on/off the specified interference area.

        Args:
            index: Interference area index (must be added in software first). Range: [1, 6].
            value: Switch. 0=off, 1=on.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"SetWorkZoneEnable({index:d},{value:d})"
        return parse_ack(self.send_recv_msg(string))

    def offset_para(self, x: float, y: float, z: float, rx: float, ry: float, rz: float) -> None:
        """Set offset parameters.

        Args:
            x: X offset (mm).
            y: Y offset (mm).
            z: Z offset (mm).
            rx: RX offset (degrees).
            ry: RY offset (degrees).
            rz: RZ offset (degrees).

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"OffsetPara({x:f},{y:f},{z:f},{rx:f},{ry:f},{rz:f})"
        return parse_ack(self.send_recv_msg(string))

    def set_resume_offset(self, distance: float) -> None:
        """Set the resume offset distance.

        Args:
            distance: Resume offset distance.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        string = f"SetResumeOffset({distance:f})"
        return parse_ack(self.send_recv_msg(string))

    def start_rt_offset(self) -> None:
        """Start real-time offset.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        return parse_ack(self.send_recv_msg("StartRTOffset()"))

    def end_rt_offset(self) -> None:
        """End real-time offset.

        Raises:
            DobotApiError: If the robot returned a non-zero error code.
        """
        return parse_ack(self.send_recv_msg("EndRTOffset()"))
