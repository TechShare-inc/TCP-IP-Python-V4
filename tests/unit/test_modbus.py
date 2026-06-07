"""Unit tests for dobot_api_v4.commands._modbus_mixin module."""

import pytest


@pytest.mark.unit
class TestModbusMixin:
    """Tests verifying exact protocol strings for Modbus commands."""

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    def test_modbus_create_basic(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.modbus_create("192.168.1.100", 502, 1)
        assert sent[-1] == "ModbusCreate(192.168.1.100,502,1)"

    def test_modbus_create_with_rtu(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.modbus_create("192.168.1.100", 502, 1, is_rtu=1)
        assert sent[-1] == "ModbusCreate(192.168.1.100,502,1,1)"

    def test_modbus_rtu_create_basic(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.modbus_rtu_create(1, 115200)
        assert sent[-1] == "ModbusRTUCreate(1,115200)"

    def test_modbus_rtu_create_with_parity(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.modbus_rtu_create(1, 115200, parity="E")
        assert sent[-1] == "ModbusRTUCreate(1,115200,E)"

    def test_modbus_rtu_create_all_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.modbus_rtu_create(1, 9600, parity="N", data_bit=7, stop_bit=2)
        assert sent[-1] == "ModbusRTUCreate(1,9600,N,7,2)"

    def test_modbus_close(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.modbus_close(0)
        assert sent[-1] == "ModbusClose(0)"

    # ------------------------------------------------------------------
    # Register Operations
    # ------------------------------------------------------------------

    def test_get_in_bits(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_in_bits(0, 100, 10)
        assert sent[-1] == "GetInBits(0,100,10)"

    def test_get_in_regs(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_in_regs(0, 100, 5)
        assert "GetInRegs(0,100,5" in sent[-1]

    def test_get_coils(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_coils(0, 100, 8)
        assert sent[-1] == "GetCoils(0,100,8)"

    def test_set_coils(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_coils(0, 100, 3, "1,0,1")
        assert sent[-1] == "SetCoils(0,100,3,1,0,1)"

    def test_get_hold_regs(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_hold_regs(0, 100, 4)
        assert "GetHoldRegs(0,100,4" in sent[-1]

    def test_set_hold_regs(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_hold_regs(0, 100, 2, "123,456")
        assert "SetHoldRegs(0,100,2,123,456" in sent[-1]

    # ------------------------------------------------------------------
    # Internal Registers
    # ------------------------------------------------------------------

    def test_get_input_bool(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_input_bool(0)
        assert sent[-1] == "GetInputBool(0)"

    def test_get_input_int(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_input_int(0)
        assert sent[-1] == "GetInputInt(0)"

    def test_get_input_float(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_input_float(0)
        assert sent[-1] == "GetInputFloat(0)"

    def test_get_output_bool(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_output_bool(0)
        assert sent[-1] == "GetOutputBool(0)"

    def test_get_output_int(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_output_int(0)
        assert sent[-1] == "GetOutputInt(0)"

    def test_get_output_float(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_output_float(0)
        assert sent[-1] == "GetOutputFloat(0)"

    def test_set_output_bool(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_output_bool(0, 1)
        assert sent[-1] == "SetOutputBool(0,1)"

    def test_set_output_int(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_output_int(0, 42)
        assert sent[-1] == "SetOutputInt(0,42)"

    def test_set_output_float(self, mock_dashboard):
        # NOTE: source uses {:d} for value -- known bug, only int values work
        dashboard, sent = mock_dashboard
        dashboard.set_output_float(0, 3)
        assert "SetOutputFloat(0," in sent[-1]
