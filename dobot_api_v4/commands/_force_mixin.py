"""Force control commands for Dobot V4 API."""

from ..dtypes import Pose
from ._parse import parse_ack, parse_pose
from ._serialization import _SerializationMixin


class _ForceMixin(_SerializationMixin):
    """Mixin for force/torque sensor and force-control commands.

    Includes force sensor enable, force reading, force-drive mode,
    force-compliance (FC) mode, and related parameter settings.
    """

    # ------------------------------------------------------------------
    # Sensor Control
    # ------------------------------------------------------------------

    def enable_ft_sensor(self, status: int) -> None:
        """Enable or disable the force/torque sensor.

        Args:
            status: 0 = disable, 1 = enable.

        Returns:
            Raw response string from robot.
        """
        string = f"EnableFTSensor({status:d})"
        return parse_ack(self.send_recv_msg(string))

    def six_force_home(self) -> None:
        """Zero (home) the six-axis force sensor.

        Returns:
            Raw response string from robot.
        """
        string = "SixForceHome()"
        return parse_ack(self.send_recv_msg(string))

    def get_force(self, tool: int = -1) -> Pose:
        """Get current force/torque sensor readings.

        Args:
            tool: Tool coordinate system index. -1 = not set (default frame).

        Returns:
            Raw response string from robot.
        """
        string = "GetForce()" if tool == -1 else f"GetForce({tool:d})"
        return parse_pose(self.send_recv_msg(string))

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
    ) -> None:
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
        string = "ForceDriveMode(" + "{" + f"{x:d},{y:d},{z:d},{rx:d},{ry:d},{rz:d}" + "}"
        if user != -1:
            string = string + f",{user:d}"
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def force_drive_speed(self, speed: int) -> None:
        """Set the force-drive speed.

        Args:
            speed: Force drive speed value.

        Returns:
            Raw response string from robot.
        """
        string = f"ForceDriveSpeed({speed:d})"
        return parse_ack(self.send_recv_msg(string))

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
    ) -> None:
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
            + f"{x:d},{y:d},{z:d},{rx:d},{ry:d},{rz:d}"
            + "},"
            + "{"
            + f"{fx:d},{fy:d},{fz:d},{frx:d},{fry:d},{frz:d}"
            + "}"
        )
        params: list[str] = []
        if reference != -1:
            params.append(f"reference={reference:d}")
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def fc_set_deviation(
        self,
        x: int,
        y: int,
        z: int,
        rx: int,
        ry: int,
        rz: int,
        control_type: int = -1,
    ) -> None:
        """Set maximum deviation for force-compliance mode.

        Args:
            x..rz: Maximum deviation per axis (6 values).
            control_type: Control type. -1 = not set.

        Returns:
            Raw response string from robot.
        """
        string = "FCSetDeviation(" + "{" + f"{x:d},{y:d},{z:d},{rx:d},{ry:d},{rz:d}" + "}"
        if control_type != -1:
            string = string + f",{control_type:d}"
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def fc_set_force_limit(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> None:
        """Set force limits for force-compliance mode.

        Args:
            x..rz: Force limit per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetForceLimit(" + f"{x:d},{y:d},{z:d},{rx:d},{ry:d},{rz:d}"
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def fc_set_mass(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> None:
        """Set virtual mass for force-compliance mode.

        Args:
            x..rz: Virtual mass per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetMass(" + f"{x:d},{y:d},{z:d},{rx:d},{ry:d},{rz:d}"
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def fc_set_stiffness(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> None:
        """Set stiffness for force-compliance mode.

        Args:
            x..rz: Stiffness per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetStiffness(" + f"{x:d},{y:d},{z:d},{rx:d},{ry:d},{rz:d}"
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def fc_set_damping(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> None:
        """Set damping for force-compliance mode.

        Args:
            x..rz: Damping per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetDamping(" + f"{x:d},{y:d},{z:d},{rx:d},{ry:d},{rz:d}"
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def fc_off(self) -> None:
        """Turn off force-compliance mode.

        Returns:
            Raw response string from robot.
        """
        string = "FCOff()"
        return parse_ack(self.send_recv_msg(string))

    def fc_set_force_speed_limit(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> None:
        """Set speed limits under force-compliance mode.

        Args:
            x..rz: Speed limit per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetForceSpeedLimit(" + f"{x:d},{y:d},{z:d},{rx:d},{ry:d},{rz:d}"
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def fc_set_force(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> None:
        """Set target force for force-compliance mode.

        Args:
            x..rz: Target force/torque per axis (6 values).

        Returns:
            Raw response string from robot.
        """
        string = "FCSetForce(" + f"{x:d},{y:d},{z:d},{rx:d},{ry:d},{rz:d}"
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def fc_collision_switch(self, enable: int) -> None:
        """Enable or disable force-compliance collision detection.

        Args:
            enable: 0 = disable, 1 = enable.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg(f"FCCollisionSwitch(enable={enable:d})"))

    def set_fc_collision(self, force: float, torque: float) -> None:
        """Set force-compliance collision detection thresholds.

        Args:
            force: Force collision threshold.
            torque: Torque collision threshold.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg(f"SetFCCollision({force:f},{torque:f})"))
