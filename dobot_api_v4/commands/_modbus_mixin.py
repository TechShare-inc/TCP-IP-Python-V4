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
        string = "ModbusCreate({:s},{:d},{:d}".format(ip, port, slave_id)
        params = []
        if is_rtu != -1:
            params.append("{:d}".format(is_rtu))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.send_recv_msg(string)

    ModbusCreate = modbus_create

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
        string = "ModbusRTUCreate({:d},{:d}".format(slave_id, baud)
        params = []
        if parity != "":
            params.append("{:s}".format(parity))
        if data_bit != 8:
            params.append("{:d}".format(data_bit))
        if stop_bit != -1:
            params.append("{:d}".format(stop_bit))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.send_recv_msg(string)

    ModbusRTUCreate = modbus_rtu_create

    def modbus_close(self, index: int) -> str:
        """Disconnect from Modbus slave and release the master.

        Args:
            index: Master index.

        Returns:
            Raw response string from robot.
        """
        string = "ModbusClose({:d})".format(index)
        return self.send_recv_msg(string)

    ModbusClose = modbus_close

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
        string = "GetInBits({:d},{:d},{:d})".format(index, addr, count)
        return self.send_recv_msg(string)

    GetInBits = get_in_bits

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
        string = "GetInRegs({:d},{:d},{:d}".format(index, addr, count)
        params = []
        if val_type != "":
            params.append("{:s}".format(val_type))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.send_recv_msg(string)

    GetInRegs = get_in_regs

    def get_coils(self, index: int, addr: int, count: int) -> str:
        """Read coil register values from Modbus slave.

        Args:
            index: Master index.
            addr: Starting address of the coil register.
            count: Number of coil registers. Range: [1, 16].

        Returns:
            Raw response string from robot.
        """
        string = "GetCoils({:d},{:d},{:d})".format(index, addr, count)
        return self.send_recv_msg(string)

    GetCoils = get_coils

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
        string = "SetCoils({:d},{:d},{:d},{:s})".format(index, addr, count, val_tab)
        return self.send_recv_msg(string)

    SetCoils = set_coils

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
        string = "GetHoldRegs({:d},{:d},{:d}".format(index, addr, count)
        params = []
        if val_type != "":
            params.append("{:s}".format(val_type))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.send_recv_msg(string)

    GetHoldRegs = get_hold_regs

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
        string = "SetHoldRegs({:d},{:d},{:d},{:s}".format(index, addr, count, val_tab)
        params = []
        if val_type != "":
            params.append("{:s}".format(val_type))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.send_recv_msg(string)

    SetHoldRegs = set_hold_regs

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
        string = "GetInputBool({:d})".format(address)
        return self.send_recv_msg(string)

    GetInputBool = get_input_bool

    def get_input_int(self, address: int) -> str:
        """Get int value from the specified input register address.

        Args:
            address: Register address. Range: [0, 23].

        Returns:
            Raw response string from robot.
        """
        string = "GetInputInt({:d})".format(address)
        return self.send_recv_msg(string)

    GetInputInt = get_input_int

    def get_input_float(self, address: int) -> str:
        """Get float value from the specified input register address.

        Args:
            address: Register address. Range: [0, 23].

        Returns:
            Raw response string from robot.
        """
        string = "GetInputFloat({:d})".format(address)
        return self.send_recv_msg(string)

    GetInputFloat = get_input_float

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
        string = "GetOutputBool({:d})".format(address)
        return self.send_recv_msg(string)

    GetOutputBool = get_output_bool

    def get_output_int(self, address: int) -> str:
        """Get int value from the specified output register address.

        Args:
            address: Register address. Range: [0, 23].

        Returns:
            Raw response string from robot.
        """
        string = "GetOutputInt({:d})".format(address)
        return self.send_recv_msg(string)

    GetOutputInt = get_output_int

    def get_output_float(self, address: int) -> str:
        """Get float value from the specified output register address.

        Args:
            address: Register address. Range: [0, 23].

        Returns:
            Raw response string from robot.
        """
        string = "GetOutputFloat({:d})".format(address)
        return self.send_recv_msg(string)

    GetOutputFloat = get_output_float

    def set_output_bool(self, address: int, value: int) -> str:
        """Set bool value at the specified output register address.

        Args:
            address: Register address. Range: [0, 63].
            value: Value to set (0 or 1).

        Returns:
            Raw response string from robot.
        """
        string = "SetOutputBool({:d},{:d})".format(address, value)
        return self.send_recv_msg(string)

    SetOutputBool = set_output_bool

    def set_output_int(self, address: int, value: int) -> str:
        """Set int value at the specified output register address.

        Args:
            address: Register address. Range: [0, 23].
            value: Integer value to set.

        Returns:
            Raw response string from robot.
        """
        string = "SetOutputInt({:d},{:d})".format(address, value)
        return self.send_recv_msg(string)

    SetOutputInt = set_output_int

    def set_output_float(self, address: int, value: float) -> str:
        """Set float value at the specified output register address.

        Args:
            address: Register address. Range: [0, 23].
            value: Float value to set.

        Returns:
            Raw response string from robot.
        """
        string = "SetOutputFloat({:d},{:d})".format(address, value)
        return self.send_recv_msg(string)

    SetOutputFloat = set_output_float
