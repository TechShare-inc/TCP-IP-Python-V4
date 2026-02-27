"""Digital and analog I/O commands for Dobot V4 API."""

from ._parse import parse_ack, parse_int
from ._serialization import _SerializationMixin


class _IOMixin(_SerializationMixin):
    """Mixin for digital/analog I/O and tool interface commands.

    Includes digital output (DO), digital input (DI), analog output (AO),
    analog input (AI), tool I/O, and tool RS485/power/mode settings.
    """

    # ------------------------------------------------------------------
    # Digital Output
    # ------------------------------------------------------------------

    def do_output(self, index: int, status: int, time: int = -1) -> None:
        """Set the status of digital output port (queue command).

        Args:
            index: DO index.
            status: DO status. 1: ON, 0: OFF.
            time: Continuous output time in ms. Range: [25, 60000].
                If set, the system automatically inverts the DO after the
                specified time. -1 means not set.

        Returns:
            Raw response string from robot.
        """
        string = f"DO({index:d},{status:d}"
        params = []
        if time != -1:
            params.append(f"{time:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def do_instant(self, index: int, status: int) -> None:
        """Set the status of digital output port (immediate command).

        Args:
            index: DO index.
            status: DO status. 1: ON, 0: OFF.

        Returns:
            Raw response string from robot.
        """
        string = f"DOInstant({index:d},{status:d})"
        return parse_ack(self.send_recv_msg(string))

    def get_do(self, index: int) -> int:
        """Get the status of digital output port.

        Args:
            index: DO index.

        Returns:
            Raw response string from robot.
        """
        string = f"GetDO({index:d})"
        return parse_int(self.send_recv_msg(string))

    def do_group(self, *index_value: int) -> None:
        """Set the status of multiple digital output ports (queue command).

        Args:
            *index_value: Alternating index and value pairs.
                Example: ``do_group(4, 1, 6, 0)`` sets DO_4=ON, DO_6=OFF.

        Returns:
            Raw response string from robot.
        """
        string = f"DOGroup({index_value[0]:d}"
        for ii in index_value[1:]:
            string = string + "," + str(ii)
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def get_do_group(self, *index_value: int) -> str:
        """Get the status of multiple digital output ports.

        Args:
            *index_value: Indices of DO ports to query.
                Example: ``get_do_group(1, 2)`` gets status of DO_1 and DO_2.

        Returns:
            Raw response string from robot.
        """
        string = f"GetDOGroup({index_value[0]:d}"
        for ii in index_value[1:]:
            string = string + "," + str(ii)
        string = string + ")"
        return self.send_recv_msg(string)

    def do_group_dec(self, group: int, value: int) -> None:
        """Set digital output group using decimal encoding.

        Args:
            group: DO group index.
            value: Decimal-encoded value for the group.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg(f"DOGroupDEC({group:d},{value:d})"))

    def get_do_group_dec(self, group: int, value: int) -> str:
        """Get digital output group status using decimal encoding.

        Args:
            group: DO group index.
            value: Decimal-encoded query value.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg(f"GetDOGroupDEC({group:d},{value:d})")

    # ------------------------------------------------------------------
    # Tool Digital Output
    # ------------------------------------------------------------------

    def tool_do(self, index: int, status: int) -> None:
        """Set the status of tool digital output port (queue command).

        Args:
            index: Tool DO index.
            status: Tool DO status. 1: ON, 0: OFF.

        Returns:
            Raw response string from robot.
        """
        string = f"ToolDO({index:d},{status:d})"
        return parse_ack(self.send_recv_msg(string))

    def tool_do_instant(self, index: int, status: int) -> None:
        """Set the status of tool digital output port (immediate command).

        Args:
            index: Tool DO index.
            status: Tool DO status. 1: ON, 0: OFF.

        Returns:
            Raw response string from robot.
        """
        string = f"ToolDOInstant({index:d},{status:d})"
        return parse_ack(self.send_recv_msg(string))

    def get_tool_do(self, index: int) -> int:
        """Get the status of tool digital output port.

        Args:
            index: Tool DO index.

        Returns:
            Raw response string from robot.
        """
        string = f"GetToolDO({index:d})"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Analog Output
    # ------------------------------------------------------------------

    def ao(self, index: int, value: float) -> None:
        """Set the value of analog output port (queue command).

        Args:
            index: AO index.
            value: AO output. Voltage range: [0, 10] V; current range: [4, 20] mA.

        Returns:
            Raw response string from robot.
        """
        string = f"AO({index:d},{value:f})"
        return parse_ack(self.send_recv_msg(string))

    def ao_instant(self, index: int, value: float) -> None:
        """Set the value of analog output port (immediate command).

        Args:
            index: AO index.
            value: AO output. Voltage range: [0, 10] V; current range: [4, 20] mA.

        Returns:
            Raw response string from robot.
        """
        string = f"AOInstant({index:d},{value:f})"
        return parse_ack(self.send_recv_msg(string))

    def get_ao(self, index: int) -> str:
        """Get the value of analog output port.

        Args:
            index: AO index.

        Returns:
            Raw response string from robot.
        """
        string = f"GetAO({index:d})"
        return self.send_recv_msg(string)

    # ------------------------------------------------------------------
    # Digital Input
    # ------------------------------------------------------------------

    def di(self, index: int) -> int:
        """Get the status of digital input port.

        Args:
            index: DI index.

        Returns:
            Raw response string from robot.
        """
        string = f"DI({index:d})"
        return parse_int(self.send_recv_msg(string))

    def di_group(self, *index_value: int) -> str:
        """Get the status of multiple digital input ports.

        Args:
            *index_value: Indices of DI ports to query.
                Example: ``di_group(4, 6, 2, 7)`` gets status of DI_4, DI_6,
                DI_2, and DI_7.

        Returns:
            Raw response string from robot.
        """
        string = f"DIGroup({index_value[0]:d}"
        for ii in index_value[1:]:
            string = string + "," + str(ii)
        string = string + ")"
        return self.send_recv_msg(string)

    def di_group_dec(self, group: int, value: int) -> str:
        """Get digital input group status using decimal encoding.

        Args:
            group: DI group index.
            value: Decimal-encoded query value.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg(f"DIGroupDEC({group:d},{value:d})")

    # ------------------------------------------------------------------
    # Tool Digital / Analog Input
    # ------------------------------------------------------------------

    def tool_di(self, index: int) -> int:
        """Get the status of tool digital input port.

        Args:
            index: Tool DI index.

        Returns:
            Raw response string from robot.
        """
        string = f"ToolDI({index:d})"
        return parse_int(self.send_recv_msg(string))

    def ai(self, index: int) -> int:
        """Get the value of analog input port.

        Args:
            index: AI index.

        Returns:
            Raw response string from robot.
        """
        string = f"AI({index:d})"
        return parse_int(self.send_recv_msg(string))

    def tool_ai(self, index: int) -> int:
        """Get the value of tool analog input port.

        Note:
            Set the port to analog-input mode via ``set_tool_mode()`` first.

        Args:
            index: Tool AI index.

        Returns:
            Raw response string from robot.
        """
        string = f"ToolAI({index:d})"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Tool RS485 / Power / Mode
    # ------------------------------------------------------------------

    def set_tool_485(
        self,
        baud: int,
        parity: str = "",
        stopbit: int = -1,
        identify: int = -1,
    ) -> None:
        """Set RS485 interface parameters for the end tool.

        Args:
            baud: Baud rate of RS485 interface.
            parity: Parity bit setting. ``"O"`` = odd, ``"E"`` = even,
                ``"N"`` = none. Default ``"N"`` if omitted.
            stopbit: Stop bit length. Range: {1, 2}. -1 means not set.
            identify: Aviation socket selector for multi-socket robots.
                1: aviation 1, 2: aviation 2. -1 means not set.

        Returns:
            Raw response string from robot.
        """
        string = f"SetTool485({baud:d}"
        params = []
        if parity != "":
            params.append(parity)
        if stopbit != -1:
            params.append(f"{stopbit:d}")
            if identify != -1:
                params.append(f"{identify:d}")
        else:
            if identify != -1:
                params.append(f"1,{identify:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def set_tool_power(self, status: int, identify: int = -1) -> None:
        """Set the power status of the end tool.

        Generally used for restarting end power (e.g., re-powering and
        re-initializing the gripper). If calling continuously, keep an
        interval of at least 4 ms.

        Note:
            Not supported on Magician E6 robot.

        Args:
            status: Power status. 0: power off, 1: power on.
            identify: Aviation socket selector for multi-socket robots.
                1: aviation 1, 2: aviation 2. -1 means not set.

        Returns:
            Raw response string from robot.
        """
        string = f"SetToolPower({status:d}"
        params = []
        if identify != -1:
            params.append(f"{identify:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))

    def set_tool_mode(
        self, mode: int, type: int, identify: int = -1
    ) -> None:  # noqa: A002
        """Set the mode of the end multiplex terminal.

        If the AI interface on the end of the robot arm is multiplexed with
        the 485 interface, use this to switch modes. 485 mode by default.

        Note:
            Robots without tool RS485 interface are unaffected.

        Args:
            mode: Mode of the multiplex terminal. 1: 485 mode, 2: AI mode.
            type: When mode is 1, this is invalid. When mode is 2, sets AI mode.
                Single digit = AI1 mode, tens digit = AI2 mode.
                Mode values: 0 = 0-10V voltage, 1 = current, 2 = 0-5V voltage.
            identify: Aviation socket selector for multi-socket robots.
                1: aviation 1, 2: aviation 2. -1 means not set.

        Returns:
            Raw response string from robot.
        """
        string = f"SetToolMode({mode:d},{type:d}"
        params = []
        if identify != -1:
            params.append(f"{identify:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return parse_ack(self.send_recv_msg(string))
