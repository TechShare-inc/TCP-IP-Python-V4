"""Modbus and register commands for Dobot V4 API."""

from ._serialization import _SerializationMixin


class _ModbusMixin(_SerializationMixin):
    """Mixin for Modbus communication and internal register commands.

    Includes Modbus TCP/RTU master creation, coil/holding/input register
    read/write, and internal Boolean/Int/Float register access.
    """

    # ------------------------------------------------------------------
    # Modbus Connection
    # ------------------------------------------------------------------

    def modbus_create(self, ip: str, port: int, slave_id: int, is_rtu: int = -1) -> str:
        """Create Modbus master and establish connection with the slave.

        Supports connecting to at most 5 devices.

        Args:
            ip: Slave IP address.
            port: Slave port.
            slave_id: Slave ID.
            is_rtu: Communication mode. 0 or omitted: ModbusTCP,
                1: ModbusRTU. -1 means not set.

        Returns:
            Raw response string from robot.
        """
        string = f"ModbusCreate({ip:s},{port:d},{slave_id:d}"
        params = []
        if is_rtu != -1:
            params.append(f"{is_rtu:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.send_recv_msg(string)

    def modbus_rtu_create(
        self,
        slave_id: int,
        baud: int,
        parity: str = "",
        data_bit: int = 8,
        stop_bit: int = -1,
    ) -> str:
        """Create Modbus RTU master via RS485 and connect to slave.

        Supports connecting to at most 5 devices.

        Args:
            slave_id: Slave ID.
            baud: Baud rate of RS485 interface.
            parity: Parity bit. ``"O"`` = odd, ``"E"`` = even,
                ``"N"`` = none. ``"E"`` by default if omitted.
            data_bit: Data bit length. Default: 8.
            stop_bit: Stop bit length. Range: {1, 2}. -1 means not set.

        Returns:
            Raw response string from robot.
        """
        string = f"ModbusRTUCreate({slave_id:d},{baud:d}"
        params = []
        if parity != "":
            params.append(f"{parity:s}")
        if data_bit != 8:
            params.append(f"{data_bit:d}")
        if stop_bit != -1:
            params.append(f"{stop_bit:d}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.send_recv_msg(string)

    def modbus_close(self, index: int) -> str:
        """Disconnect from Modbus slave and release the master.

        Args:
            index: Master index.

        Returns:
            Raw response string from robot.
        """
        string = f"ModbusClose({index:d})"
        return self.send_recv_msg(string)

    # ------------------------------------------------------------------
    # Modbus Registers
    # ------------------------------------------------------------------

    def get_in_bits(self, index: int, addr: int, count: int) -> str:
        """Read discrete input (contact register) values from Modbus slave.

        Args:
            index: Master index.
            addr: Starting address of the contact register.
            count: Number of contact registers. Range: [1, 16].

        Returns:
            Raw response string from robot.
        """
        string = f"GetInBits({index:d},{addr:d},{count:d})"
        return self.send_recv_msg(string)

    def get_in_regs(self, index: int, addr: int, count: int, val_type: str = "") -> str:
        """Read input register values from Modbus slave.

        Args:
            index: Master index.
            addr: Starting address of the input register.
            count: Number of input registers. Range: [1, 4].
            val_type: Data type. ``"U16"``, ``"U32"``, ``"F32"``, ``"F64"``.
                Default: ``"U16"`` if omitted.

        Returns:
            Raw response string from robot.
        """
        string = f"GetInRegs({index:d},{addr:d},{count:d}"
        params = []
        if val_type != "":
            params.append(f"{val_type:s}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.send_recv_msg(string)

    def get_coils(self, index: int, addr: int, count: int) -> str:
        """Read coil register values from Modbus slave.

        Args:
            index: Master index.
            addr: Starting address of the coil register.
            count: Number of coil registers. Range: [1, 16].

        Returns:
            Raw response string from robot.
        """
        string = f"GetCoils({index:d},{addr:d},{count:d})"
        return self.send_recv_msg(string)

    def set_coils(self, index: int, addr: int, count: int, val_tab: str) -> str:
        """Write values to coil registers on Modbus slave.

        Args:
            index: Master index.
            addr: Starting address of the coil register.
            count: Number of values to write. Range: [1, 16].
            val_tab: Values to write, e.g. ``"{1,0,1}"``.

        Returns:
            Raw response string from robot.
        """
        string = f"SetCoils({index:d},{addr:d},{count:d},{val_tab:s})"
        return self.send_recv_msg(string)

    def get_hold_regs(
        self, index: int, addr: int, count: int, val_type: str = ""
    ) -> str:
        """Read holding register values from Modbus slave.

        Args:
            index: Master index.
            addr: Starting address of the holding register.
            count: Number of holding registers. Range: [1, 4].
            val_type: Data type. ``"U16"``, ``"U32"``, ``"F32"``, ``"F64"``.
                Default: ``"U16"`` if omitted.

        Returns:
            Raw response string from robot.
        """
        string = f"GetHoldRegs({index:d},{addr:d},{count:d}"
        params = []
        if val_type != "":
            params.append(f"{val_type:s}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.send_recv_msg(string)

    def set_hold_regs(
        self, index: int, addr: int, count: int, val_tab: str, val_type: str = ""
    ) -> str:
        """Write values to holding registers on Modbus slave.

        Args:
            index: Master index.
            addr: Starting address of the holding register.
            count: Number of values to write. Range: [1, 4].
            val_tab: Values to write, e.g. ``"{6000,300}"``.
            val_type: Data type. ``"U16"``, ``"U32"``, ``"F32"``, ``"F64"``.
                Default: ``"U16"`` if omitted.

        Returns:
            Raw response string from robot.
        """
        string = f"SetHoldRegs({index:d},{addr:d},{count:d},{val_tab:s}"
        params = []
        if val_type != "":
            params.append(f"{val_type:s}")
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.send_recv_msg(string)

    # ------------------------------------------------------------------
    # Internal Registers (Input)
    # ------------------------------------------------------------------

    def get_input_bool(self, address: int) -> str:
        """Get bool value from the specified input register address.

        Args:
            address: Register address. Range: [0, 63].

        Returns:
            Raw response string from robot.
        """
        string = f"GetInputBool({address:d})"
        return self.send_recv_msg(string)

    def get_input_int(self, address: int) -> str:
        """Get int value from the specified input register address.

        Args:
            address: Register address. Range: [0, 23].

        Returns:
            Raw response string from robot.
        """
        string = f"GetInputInt({address:d})"
        return self.send_recv_msg(string)

    def get_input_float(self, address: int) -> str:
        """Get float value from the specified input register address.

        Args:
            address: Register address. Range: [0, 23].

        Returns:
            Raw response string from robot.
        """
        string = f"GetInputFloat({address:d})"
        return self.send_recv_msg(string)

    # ------------------------------------------------------------------
    # Internal Registers (Output)
    # ------------------------------------------------------------------

    def get_output_bool(self, address: int) -> str:
        """Get bool value from the specified output register address.

        Args:
            address: Register address. Range: [0, 63].

        Returns:
            Raw response string from robot.
        """
        string = f"GetOutputBool({address:d})"
        return self.send_recv_msg(string)

    def get_output_int(self, address: int) -> str:
        """Get int value from the specified output register address.

        Args:
            address: Register address. Range: [0, 23].

        Returns:
            Raw response string from robot.
        """
        string = f"GetOutputInt({address:d})"
        return self.send_recv_msg(string)

    def get_output_float(self, address: int) -> str:
        """Get float value from the specified output register address.

        Args:
            address: Register address. Range: [0, 23].

        Returns:
            Raw response string from robot.
        """
        string = f"GetOutputFloat({address:d})"
        return self.send_recv_msg(string)

    def set_output_bool(self, address: int, value: int) -> str:
        """Set bool value at the specified output register address.

        Args:
            address: Register address. Range: [0, 63].
            value: Value to set (0 or 1).

        Returns:
            Raw response string from robot.
        """
        string = f"SetOutputBool({address:d},{value:d})"
        return self.send_recv_msg(string)

    def set_output_int(self, address: int, value: int) -> str:
        """Set int value at the specified output register address.

        Args:
            address: Register address. Range: [0, 23].
            value: Integer value to set.

        Returns:
            Raw response string from robot.
        """
        string = f"SetOutputInt({address:d},{value:d})"
        return self.send_recv_msg(string)

    def set_output_float(self, address: int, value: float) -> str:
        """Set float value at the specified output register address.

        Args:
            address: Register address. Range: [0, 23].
            value: Float value to set.

        Returns:
            Raw response string from robot.
        """
        string = f"SetOutputFloat({address:d},{value:d})"
        return self.send_recv_msg(string)

