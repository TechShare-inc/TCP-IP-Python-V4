"""System and lifecycle commands for Dobot V4 API."""

from ._serialization import _SerializationMixin


class _SystemMixin(_SerializationMixin):
    """Mixin for robot system and lifecycle commands.

    Includes enable/disable, power, emergency stop, script control,
    and other system-level operations.
    """

    def enable_robot(
        self,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
        is_check: int = -1,
    ) -> str:
        """Enable the robot.

        The number of parameters sent depends on which are non-default:
        - 0 params: no load/eccentric settings
        - 1 param: load weight only
        - 4 params: load weight + eccentric XYZ
        - 5 params: load weight + eccentric XYZ + check flag

        Args:
            load: Load weight (kg). Must not exceed model limit.
            center_x: X-direction eccentric distance (mm). Range: [-999, 999].
            center_y: Y-direction eccentric distance (mm). Range: [-999, 999].
            center_z: Z-direction eccentric distance (mm). Range: [-999, 999].
            is_check: Check load after enable. 1=check, 0=no check, -1=omit.

        Returns:
            Raw response string from robot.
        """
        string = "EnableRobot("
        if load != 0:
            string = string + f"{load:f}"
            if center_x != 0 or center_y != 0 or center_z != 0:
                string = string + f",{center_x:f},{center_y:f},{center_z:f}"
                if is_check != -1:
                    string = string + f",{is_check:d}"
        string = string + ")"
        return self.send_recv_msg(string)

    def disable_robot(self) -> str:
        """Disable the robot.

        Returns:
            Raw response string from robot.
        """
        string = "DisableRobot()"
        return self.send_recv_msg(string)

    def clear_error(self) -> str:
        """Clear controller alarm information.

        After clearing, check ``robot_mode()`` to confirm alarm is resolved.
        Some alarms require resolving the cause or restarting the controller.

        Returns:
            Raw response string from robot.
        """
        string = "ClearError()"
        return self.send_recv_msg(string)

    def power_on(self) -> str:
        """Power on the robot.

        Note:
            It takes about 10 seconds for the robot to be enabled after power on.

        Returns:
            Raw response string from robot.
        """
        string = "PowerOn()"
        return self.send_recv_msg(string)

    def run_script(self, project_name: str) -> str:
        """Run a script file.

        Args:
            project_name: Script file name.

        Returns:
            Raw response string from robot.
        """
        string = f"RunScript({project_name:s})"
        return self.send_recv_msg(string)

    def stop_script(self) -> str:
        """Stop the delivered motion command queue or RunScript command.

        Returns:
            Raw response string from robot.
        """
        string = "Stop()"
        return self.send_recv_msg(string)

    def pause_script(self) -> str:
        """Pause the delivered motion command queue or RunScript command.

        Returns:
            Raw response string from robot.
        """
        string = "Pause()"
        return self.send_recv_msg(string)

    def resume(self) -> str:
        """Continue the paused motion command queue or RunScript command.

        Returns:
            Raw response string from robot.
        """
        string = "Continue()"
        return self.send_recv_msg(string)

    def emergency_stop(self, mode: int) -> str:
        """Emergency stop the robot.

        After emergency stop, the robot arm will be disabled and alarm.
        Release the E-Stop and clear alarms to re-enable.

        Args:
            mode: E-Stop operation mode. 1=press E-Stop, 0=release E-Stop.

        Returns:
            Raw response string from robot.
        """
        string = f"EmergencyStop({mode:d})"
        return self.send_recv_msg(string)

    def brake_control(self, axis_id: int, value: int) -> str:
        """Control the brake of a specified joint.

        Joints automatically brake when stationary. Use this to switch on
        the brake for manual dragging while disabled.

        Can only be used when the robot arm is disabled.

        Args:
            axis_id: Joint ID. 1=J1, 2=J2, ... 6=J6.
            value: Brake status. 0=switch off (no drag), 1=switch on (draggable).

        Returns:
            Raw response string from robot.
        """
        string = f"BrakeControl({axis_id:d},{value:d})"
        return self.send_recv_msg(string)

    def request_control(self) -> str:
        """Request control of the robot.

        Note:
            The request may be approved or denied.

        Returns:
            Raw response string from robot.
        """
        string = "RequestControl()"
        return self.send_recv_msg(string)

    def reset_robot(self) -> str:
        """Reset the robot.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("ResetRobot()")

    def tcp_send_and_parse(self, cmd: str) -> str:
        """Send a raw TCP command and parse the response.

        Args:
            cmd: Command string to send.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg(f'TcpSendAndParse("{cmd:s}")')

    def sleep(self, count: int) -> str:
        """Sleep (delay) command in the motion queue.

        Args:
            count: Sleep duration in milliseconds.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg(f"Sleep({count:d})")

