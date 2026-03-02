"""Unit tests for dobot_api_v4.commands._config_mixin module."""

import pytest


@pytest.mark.unit
class TestConfigMixin:
    """Tests verifying exact protocol strings for config commands."""

    def test_speed_factor(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.speed_factor(50)
        assert sent[-1] == "SpeedFactor(50)"

    def test_acc_j(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.acc_j(80)
        assert sent[-1] == "AccJ(80)"

    def test_acc_l(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.acc_l(70)
        assert sent[-1] == "AccL(70)"

    def test_vel_j(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.vel_j(60)
        assert sent[-1] == "VelJ(60)"

    def test_vel_l(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.vel_l(40)
        assert sent[-1] == "VelL(40)"

    def test_cp(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.cp(50)
        assert sent[-1] == "CP(50)"

    def test_user(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.user(1)
        assert sent[-1] == "User(1)"

    def test_set_user(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_user(0, "{0,0,0,0,0,0}")
        assert sent[-1] == "SetUser(0,{0,0,0,0,0,0})"

    def test_calc_user(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.calc_user(0, 1, "{0,0,0,0,0,0}")
        assert sent[-1] == "CalcUser(0,1,{0,0,0,0,0,0})"

    def test_tool(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.tool(2)
        assert sent[-1] == "Tool(2)"

    def test_set_tool(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_tool(1, "{10,20,30,0,0,0}")
        assert sent[-1] == "SetTool(1,{10,20,30,0,0,0})"

    def test_calc_tool(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.calc_tool(1, 0, "{0,0,0,0,0,0}")
        assert sent[-1] == "CalcTool(1,0,{0,0,0,0,0,0})"

    def test_set_payload_no_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_payload()
        assert sent[-1] == "SetPayload()"

    def test_set_payload_with_load(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_payload(load=2.5)
        assert "SetPayload(2.500000" in sent[-1]

    def test_set_collision_level(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_collision_level(3)
        assert sent[-1] == "SetCollisionLevel(3)"

    def test_drag_sensitivity(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.drag_sensitivity(1, 60)
        assert sent[-1] == "DragSensivity(1,60)"

    def test_enable_safe_skin(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.enable_safe_skin(1)
        assert sent[-1] == "EnableSafeSkin(1)"

    def test_set_safe_skin(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_safe_skin(1, 50)
        assert sent[-1] == "SetSafeSkin(1,50)"
