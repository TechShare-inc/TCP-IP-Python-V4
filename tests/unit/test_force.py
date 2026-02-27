"""Unit tests for dobot_api_v4.commands._force_mixin module."""

import pytest


@pytest.mark.unit
class TestForceMixin:
    """Tests verifying exact protocol strings for force commands."""

    def test_enable_ft_sensor(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.enable_ft_sensor(1)
        assert sent[-1] == "EnableFTSensor(1)"

    def test_disable_ft_sensor(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.enable_ft_sensor(0)
        assert sent[-1] == "EnableFTSensor(0)"

    def test_six_force_home(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.six_force_home()
        assert sent[-1] == "SixForceHome()"

    def test_get_force_no_tool(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_force()
        assert sent[-1] == "GetForce()"

    def test_get_force_with_tool(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_force(tool=1)
        assert sent[-1] == "GetForce(1)"

    def test_force_drive_mode(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.force_drive_mode(1, 0, 1, 0, 0, 0)
        cmd = sent[-1]
        assert cmd.startswith("ForceDriveMode({1,0,1,0,0,0}")

    def test_force_drive_mode_with_user(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.force_drive_mode(1, 1, 1, 0, 0, 0, user=0)
        cmd = sent[-1]
        assert cmd == "ForceDriveMode({1,1,1,0,0,0},0)"

    def test_force_drive_speed(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.force_drive_speed(50)
        assert sent[-1] == "ForceDriveSpeed(50)"

    def test_fc_force_mode(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.fc_force_mode(
            1,
            0,
            1,
            0,
            0,
            0,  # direction flags
            0,
            0,
            10,
            0,
            0,
            0,  # force values
        )
        cmd = sent[-1]
        assert "FCForceMode(" in cmd

    def test_fc_off(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.fc_off()
        assert sent[-1] == "FCOff()"

    def test_fc_set_mass(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.fc_set_mass(1, 1, 1, 1, 1, 1)
        assert "FCSetMass(" in sent[-1]

    def test_fc_set_stiffness(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.fc_set_stiffness(1, 1, 1, 1, 1, 1)
        assert "FCSetStiffness(" in sent[-1]

    def test_fc_set_damping(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.fc_set_damping(1, 1, 1, 1, 1, 1)
        assert "FCSetDamping(" in sent[-1]

    def test_fc_set_force_speed_limit(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.fc_set_force_speed_limit(100, 100, 100, 50, 50, 50)
        assert "FCSetForceSpeedLimit(" in sent[-1]

    def test_fc_collision_switch(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.fc_collision_switch(1)
        assert sent[-1] == "FCCollisionSwitch(enable=1)"

    def test_set_fc_collision(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_fc_collision(1.0, 50.0)
        assert "SetFCCollision(" in sent[-1]
        assert "1.000000" in sent[-1]
        assert "50.000000" in sent[-1]
