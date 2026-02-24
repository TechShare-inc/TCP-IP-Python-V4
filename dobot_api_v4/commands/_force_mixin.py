"""Force control commands for Dobot V4 API."""

from ._serialization import _SerializationMixin


class _ForceMixin(_SerializationMixin):
    """Mixin for force/torque sensor and force-control commands.

    Includes force sensor enable, force reading, force-drive mode,
    force-compliance (FC) mode, and related parameter settings.
    """

    # ------------------------------------------------------------------
    # Sensor Control
    # ------------------------------------------------------------------

    def enable_ft_sensor(self, status: int) -> str:
        """Enable or disable the force/torque sensor.

        Args:
            status: 0 = disable, 1 = enable.

        Returns:
            Raw response string from robot.
        """
        string = "EnableFTSensor({:d})".format(status)
        return self.send_recv_msg(string)

    EnableFTSensor = enable_ft_sensor

    def six_force_home(self) -> str:
        """Zero (home) the six-axis force sensor.

        Returns:
            Raw response string from robot.
        """
        string = "SixForceHome()"
        return self.send_recv_msg(string)

    SixForceHome = six_force_home

    def get_force(self, tool: int = -1) -> str:
        """Get current force/torque sensor readings.

        Args:
            tool: Tool coordinate system index. -1 = not set (default frame).

        Returns:
            Raw response string from robot.
        """
        if tool == -1:
            string = "GetForce()"
        else:
            string = "GetForce({:d})".format(tool)
        return self.send_recv_msg(string)

    GetForce = get_force

    # ------------------------------------------------------------------
    # Force Drive Mode
    # ------------------------------------------------------------------

    def force_drive_mode(
        self,
        x: int,
        y: int,
        z: int,
        rx: int,
        ry: int,
        rz: int,
        user: int = -1,
    ) -> str:
        """Set force-drive mode axes.

        Args:
            x: X-axis force drive flag.
            y: Y-axis force drive flag.
            z: Z-axis force drive flag.
            rx: Rx-axis force drive flag.
            ry: Ry-axis force drive flag.
            rz: Rz-axis force drive flag.
            user: User coordinate system. -1 = not set.

        Returns:
            Raw response string from robot.
        """
        string = (
            "ForceDriveMode("
            + "{"
            + "{:d},{:d},{:d},{:d},{:d},{:d}".format(x, y, z, rx, ry, rz)
            + "}"
        )
        if user != -1:
            string = string + ",{:d}".format(user)
        string = string + ")"
        return self.send_recv_msg(string)

    ForceDriveMode = force_drive_mode

    def force_drive_speed(self, speed: int) -> str:
        """Set the force-drive speed.

        Args:
            speed: Force drive speed value.

        Returns:
            Raw response string from robot.
        """
        string = "ForceDriveSpeed({:d})".format(speed)
        return self.send_recv_msg(string)

    ForceDriveSpeed = force_drive_speed

    # ------------------------------------------------------------------
    # Force Compliance (FC) Mode
    # ------------------------------------------------------------------

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
    ) -> str:
        """Set force-compliance mode parameters.

        Args:
            x..rz: Axis compliance flags (6 values).
            fx..frz: Target force/torque values (6 values).
            reference: Reference frame. -1 = not set.
            user: User coordinate system. -1 = not set.
            tool: Tool coordinate system. -1 = not set.

        Returns:
            Raw response string from robot.
        """
        string = (
            "FCForceMode("
            + "{"
            + "{:d},{:d},{:d},{:d},{:d},{:d}".format(x, y, z, rx, ry, rz)
            + "},"
            + "{"
            + "{:d},{:d},{:d},{:d},{:d},{:d}".format(fx, fy, fz, frx, fry, frz)
            + "}"
        )
        params: list[str] = []
        if reference != -1:
            params.append("reference={:d}".format(reference))
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.send_recv_msg(string)

    FCForceMode = fc_force_mode

    def fc_set_deviation(
        self,
        x: int,
        y: int,
        z: int,
        rx: int,
        ry: int,
        rz: int,
        control_type: int = -1,
    ) -> str:
        """Set maximum deviation for force-compliance mode.

        Args:
            x..rz: Maximum deviation per axis (6 values).
            control_type: Control type. -1 = not set.

        Returns:
            Raw response string from robot.
        """
        string = (
            "FCSetDeviation("
            + "{"
            + "{:d},{:d},{:d},{:d},{:d},{:d}".format(x, y, z, rx, ry, rz)
            + "}"
        )
        if control_type != -1:
            string = string + ",{:d}".format(control_type)
        string = string + ")"
        return self.send_recv_msg(string)

    FCSetDeviation = fc_set_deviation

    def fc_set_force_limit(
        self, x: int, y: int, z: int, rx: int, ry: int, rz: int
    ) -> str:
        """Set force limits for force-compliance mode.

        Args:
            x..rz: Force limit per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetForceLimit(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.send_recv_msg(string)

    FCSetForceLimit = fc_set_force_limit

    def fc_set_mass(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> str:
        """Set virtual mass for force-compliance mode.

        Args:
            x..rz: Virtual mass per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetMass(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.send_recv_msg(string)

    FCSetMass = fc_set_mass

    def fc_set_stiffness(
        self, x: int, y: int, z: int, rx: int, ry: int, rz: int
    ) -> str:
        """Set stiffness for force-compliance mode.

        Args:
            x..rz: Stiffness per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetStiffness(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.send_recv_msg(string)

    FCSetStiffness = fc_set_stiffness

    def fc_set_damping(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> str:
        """Set damping for force-compliance mode.

        Args:
            x..rz: Damping per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetDamping(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.send_recv_msg(string)

    FCSetDamping = fc_set_damping

    def fc_off(self) -> str:
        """Turn off force-compliance mode.

        Returns:
            Raw response string from robot.
        """
        string = "FCOff()"
        return self.send_recv_msg(string)

    FCOff = fc_off

    def fc_set_force_speed_limit(
        self, x: int, y: int, z: int, rx: int, ry: int, rz: int
    ) -> str:
        """Set speed limits under force-compliance mode.

        Args:
            x..rz: Speed limit per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetForceSpeedLimit(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.send_recv_msg(string)

    FCSetForceSpeedLimit = fc_set_force_speed_limit

    def fc_set_force(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> str:
        """Set target force for force-compliance mode.

        Args:
            x..rz: Target force/torque per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetForce(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.send_recv_msg(string)

    FCSetForce = fc_set_force

    def fc_collision_switch(self, enable: int) -> str:
        """Enable or disable force-compliance collision detection.

        Args:
            enable: 0 = disable, 1 = enable.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("FCCollisionSwitch(enable={:d})".format(enable))

    FCCollisionSwitch = fc_collision_switch

    def set_fc_collision(self, force: float, torque: float) -> str:
        """Set force-compliance collision detection thresholds.

        Args:
            force: Force collision threshold.
            torque: Torque collision threshold.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("SetFCCollision({:f},{:f})".format(force, torque))

    SetFCCollision = set_fc_collision
