"""Unit tests for dobot_api_v4.commands._io_mixin module."""

import pytest


@pytest.mark.unit
class TestIOMixin:
    """Tests verifying exact protocol strings for I/O commands."""

    # ------------------------------------------------------------------
    # Digital Output
    # ------------------------------------------------------------------

    def test_do_output_basic(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.do_output(1, 1)
        assert sent[-1] == "DO(1,1)"

    def test_do_output_with_time(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.do_output(1, 1, time=500)
        assert sent[-1] == "DO(1,1,500)"

    def test_do_instant(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.do_instant(2, 0)
        assert sent[-1] == "DOInstant(2,0)"

    def test_get_do(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_do(3)
        assert sent[-1] == "GetDO(3)"

    def test_do_group(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.do_group(4, 1, 6, 0)
        assert sent[-1] == "DOGroup(4,1,6,0)"

    def test_get_do_group(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_do_group(1, 2, 3)
        assert sent[-1] == "GetDOGroup(1,2,3)"

    # ------------------------------------------------------------------
    # Tool Digital Output
    # ------------------------------------------------------------------

    def test_tool_do(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.tool_do(1, 1)
        assert sent[-1] == "ToolDO(1,1)"

    def test_tool_do_instant(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.tool_do_instant(1, 0)
        assert sent[-1] == "ToolDOInstant(1,0)"

    def test_get_tool_do(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_tool_do(1)
        assert sent[-1] == "GetToolDO(1)"

    # ------------------------------------------------------------------
    # Analog Output / Input
    # ------------------------------------------------------------------

    def test_ao(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.ao(1, 3.14)
        assert "AO(1," in sent[-1]

    def test_ao_instant(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.ao_instant(1, 2.5)
        assert "AOInstant(1," in sent[-1]

    def test_get_ao(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_ao(1)
        assert sent[-1] == "GetAO(1)"

    def test_di(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.di(1)
        assert sent[-1] == "DI(1)"

    def test_di_group(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.di_group(1, 2, 3)
        assert sent[-1] == "DIGroup(1,2,3)"

    def test_tool_di(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.tool_di(1)
        assert sent[-1] == "ToolDI(1)"

    def test_ai(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.ai(1)
        assert sent[-1] == "AI(1)"

    def test_tool_ai(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.tool_ai(1)
        assert sent[-1] == "ToolAI(1)"

    # ------------------------------------------------------------------
    # Tool RS485 / Power / Mode
    # ------------------------------------------------------------------

    def test_set_tool_485(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_tool_485(115200)
        assert "SetTool485(115200" in sent[-1]

    def test_set_tool_power(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_tool_power(1)
        assert sent[-1] == "SetToolPower(1)"

    def test_set_tool_mode(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_tool_mode(1, 0, 0)
        assert sent[-1] == "SetToolMode(1,0,0)"

    # ------------------------------------------------------------------
    # Group DEC
    # ------------------------------------------------------------------

    def test_do_group_dec(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.do_group_dec(1, 3)
        assert "DOGroupDEC(" in sent[-1]

    def test_get_do_group_dec(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_do_group_dec(1, 2)
        assert "GetDOGroupDEC(" in sent[-1]

    def test_di_group_dec(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.di_group_dec(1, 2)
        assert "DIGroupDEC(" in sent[-1]
