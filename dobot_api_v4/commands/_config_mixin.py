"""Configuration commands for Dobot V4 API."""

from ._serialization import _SerializationMixin


class _ConfigMixin(_SerializationMixin):
    """Mixin for robot configuration commands.

    Includes speed/acceleration settings, coordinate system management,
    payload, collision detection, drag settings, safety features, and offsets.
    """

    def speed_factor(self, speed: int) -> str:
        """Set the global speed ratio.

        Actual jog speed = jog setting * global speed ratio.
        Actual playback speed = motion command ratio * playback setting * global speed ratio.

        Args:
            speed: Global speed ratio. Range: [1, 100].

        Returns:
            Raw response string from robot.
        """
        string = f"SpeedFactor({speed:d})"
        return self.send_recv_msg(string)

    SpeedFactor = speed_factor

    def acc_j(self, speed: int) -> str:
        """Set acceleration ratio of joint motion.

        Defaults to 100 if not set.

        Args:
            speed: Acceleration ratio. Range: [1, 100].

        Returns:
            Raw response string from robot.
        """
        string = f"AccJ({speed:d})"
        return self.send_recv_msg(string)

    AccJ = acc_j

    def acc_l(self, speed: int) -> str:
        """Set acceleration ratio of linear and arc motion.

        Defaults to 100 if not set.

        Args:
            speed: Acceleration ratio. Range: [1, 100].

        Returns:
            Raw response string from robot.
        """
        string = f"AccL({speed:d})"
        return self.send_recv_msg(string)

    AccL = acc_l

    def vel_j(self, speed: int) -> str:
        """Set speed ratio of joint motion.

        Defaults to 100 if not set.

        Args:
            speed: Speed ratio. Range: [1, 100].

        Returns:
            Raw response string from robot.
        """
        string = f"VelJ({speed:d})"
        return self.send_recv_msg(string)

    VelJ = vel_j

    def vel_l(self, speed: int) -> str:
        """Set speed ratio of linear and arc motion.

        Defaults to 100 if not set.

        Args:
            speed: Speed ratio. Range: [1, 100].

        Returns:
            Raw response string from robot.
        """
        string = f"VelL({speed:d})"
        return self.send_recv_msg(string)

    VelL = vel_l

    def cp(self, ratio: int) -> str:
        """Set the continuous path (CP) ratio.

        Controls whether the robot transitions at a right angle or curves
        when passing through intermediate points in multi-point motion.

        Defaults to 0 if not set.

        Args:
            ratio: Continuous path ratio. Range: [0, 100].

        Returns:
            Raw response string from robot.
        """
        string = f"CP({ratio:d})"
        return self.send_recv_msg(string)

    CP = cp

    def user(self, index: int) -> str:
        """Set the global user coordinate system.

        If not set, defaults to User coordinate system 0.

        Args:
            index: User coordinate system index.

        Returns:
            Raw response string from robot.
        """
        string = f"User({index:d})"
        return self.send_recv_msg(string)

    User = user

    def set_user(self, index: int, table: str) -> str:
        """Modify the specified user coordinate system.

        Args:
            index: User coordinate system index. Range: [0, 9].
            table: Coordinate system value, format: ``{x, y, z, rx, ry, rz}``.

        Returns:
            Raw response string from robot.
        """
        string = f"SetUser({index:d},{table:s})"
        return self.send_recv_msg(string)

    SetUser = set_user

    def calc_user(self, index: int, matrix_direction: int, table: str) -> str:
        """Calculate the user coordinate system.

        Args:
            index: User coordinate system index. Range: [0, 9].
            matrix_direction: Calculation method. 1=left multiplication
                (deflect along base), 0=right multiplication (deflect along self).
            table: Coordinate system offset, format: ``{x, y, z, rx, ry, rz}``.

        Returns:
            Raw response string from robot.
        """
        string = f"CalcUser({index:d},{matrix_direction:d},{table:s})"
        return self.send_recv_msg(string)

    CalcUser = calc_user

    def tool(self, index: int) -> str:
        """Set the global tool coordinate system.

        If not set, defaults to Tool coordinate system 0.

        Args:
            index: Tool coordinate system index.

        Returns:
            Raw response string from robot.
        """
        string = f"Tool({index:d})"
        return self.send_recv_msg(string)

    Tool = tool

    def set_tool(self, index: int, table: str) -> str:
        """Modify the specified tool coordinate system.

        Args:
            index: Tool coordinate system index. Range: [0, 9].
            table: Coordinate system value, format: ``{x, y, z, rx, ry, rz}``.

        Returns:
            Raw response string from robot.
        """
        string = f"SetTool({index:d},{table:s})"
        return self.send_recv_msg(string)

    SetTool = set_tool

    def calc_tool(self, index: int, matrix_direction: int, table: str) -> str:
        """Calculate the tool coordinate system.

        Args:
            index: Tool coordinate system index. Range: [0, 9].
            matrix_direction: Calculation method. 1=left multiplication
                (deflect along flange), 0=right multiplication (deflect along self).
            table: Coordinate system offset, format: ``{x, y, z, rx, ry, rz}``.

        Returns:
            Raw response string from robot.
        """
        string = f"CalcTool({index:d},{matrix_direction:d},{table:s})"
        return self.send_recv_msg(string)

    CalcTool = calc_tool

    def set_payload(
        self,
        load: float = 0.0,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        name: str = "F",
    ) -> str:
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

        Returns:
            Raw response string from robot.
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
        return self.send_recv_msg(string)

    SetPayload = set_payload

    def set_collision_level(self, level: int) -> str:
        """Set the collision detection level.

        Args:
            level: Collision detection level. 0=off, 1-5=sensitivity (higher=more sensitive).

        Returns:
            Raw response string from robot.
        """
        string = f"SetCollisionLevel({level:d})"
        return self.send_recv_msg(string)

    SetCollisionLevel = set_collision_level

    def set_back_distance(self, distance: int) -> str:
        """Set the backoff distance after collision detection.

        Args:
            distance: Backoff distance (mm). Range: [0, 50].

        Returns:
            Raw response string from robot.
        """
        string = f"SetBackDistance({distance:d})"
        return self.send_recv_msg(string)

    SetBackDistance = set_back_distance

    def set_post_collision_mode(self, mode: int) -> str:
        """Set the post-collision processing mode.

        Args:
            mode: 0=stop after collision, 1=pause after collision.

        Returns:
            Raw response string from robot.
        """
        string = f"SetPostCollisionMode({mode:d})"
        return self.send_recv_msg(string)

    SetPostCollisionMode = set_post_collision_mode

    def drag_sensitivity(self, index: int, value: int) -> str:
        """Set the drag sensitivity.

        Args:
            index: Axis ID. 1-6=J1-J6, 0=all axes.
            value: Drag sensitivity. Smaller=more force needed. Range: [1, 90].

        Returns:
            Raw response string from robot.
        """
        string = f"DragSensivity({index:d},{value:d})"
        return self.send_recv_msg(string)

    DragSensivity = drag_sensitivity

    def enable_safe_skin(self, status: int) -> str:
        """Switch on or off the SafeSkin.

        Valid only for robot arms equipped with SafeSkin.

        Args:
            status: SafeSkin switch. 0=off, 1=on.

        Returns:
            Raw response string from robot.
        """
        string = f"EnableSafeSkin({status:d})"
        return self.send_recv_msg(string)

    EnableSafeSkin = enable_safe_skin

    def set_safe_skin(self, part: int, status: int) -> str:
        """Set sensitivity for each part of the SafeSkin.

        Valid only for robot arms equipped with SafeSkin.

        Args:
            part: Part to set. 3=forearm, 4-6=J4-J6.
            status: Sensitivity. 0=off, 1=low, 2=middle, 3=high.

        Returns:
            Raw response string from robot.
        """
        string = f"SetSafeSkin({part:d},{status:d})"
        return self.send_recv_msg(string)

    SetSafeSkin = set_safe_skin

    def set_safe_wall_enable(self, index: int, value: int) -> str:
        """Switch on/off the specified safety wall.

        Args:
            index: Safety wall index (must be added in software first). Range: [1, 8].
            value: Switch. 0=off, 1=on.

        Returns:
            Raw response string from robot.
        """
        string = f"SetSafeWallEnable({index:d},{value:d})"
        return self.send_recv_msg(string)

    SetSafeWallEnable = set_safe_wall_enable

    def set_work_zone_enable(self, index: int, value: int) -> str:
        """Switch on/off the specified interference area.

        Args:
            index: Interference area index (must be added in software first). Range: [1, 6].
            value: Switch. 0=off, 1=on.

        Returns:
            Raw response string from robot.
        """
        string = f"SetWorkZoneEnable({index:d},{value:d})"
        return self.send_recv_msg(string)

    SetWorkZoneEnable = set_work_zone_enable

    def offset_para(
        self, x: float, y: float, z: float, rx: float, ry: float, rz: float
    ) -> str:
        """Set offset parameters.

        Args:
            x: X offset (mm).
            y: Y offset (mm).
            z: Z offset (mm).
            rx: RX offset (degrees).
            ry: RY offset (degrees).
            rz: RZ offset (degrees).

        Returns:
            Raw response string from robot.
        """
        string = f"OffsetPara({x:f},{y:f},{z:f},{rx:f},{ry:f},{rz:f})"
        return self.send_recv_msg(string)

    OffsetPara = offset_para

    def set_resume_offset(self, distance: float) -> str:
        """Set the resume offset distance.

        Args:
            distance: Resume offset distance.

        Returns:
            Raw response string from robot.
        """
        string = f"SetResumeOffset({distance:f})"
        return self.send_recv_msg(string)

    SetResumeOffset = set_resume_offset

    def start_rt_offset(self) -> str:
        """Start real-time offset.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("StartRTOffset()")

    StartRTOffset = start_rt_offset

    def end_rt_offset(self) -> str:
        """End real-time offset.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("EndRTOffset()")

    EndRTOffset = end_rt_offset
