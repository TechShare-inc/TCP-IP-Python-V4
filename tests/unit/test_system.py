"""Unit tests for dobot_api_v4.commands._system_mixin module."""

import pytest


@pytest.mark.unit
class TestSystemMixin:
    """Tests verifying exact protocol strings for system commands."""

    def test_enable_robot_no_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.enable_robot()
        assert sent[-1] == "EnableRobot()"

    def test_enable_robot_with_load(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.enable_robot(load=1.5)
        assert sent[-1] == "EnableRobot(1.500000)"

    def test_enable_robot_with_load_and_center(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.enable_robot(load=2.0, center_x=0.1, center_y=0.2, center_z=0.3)
        assert sent[-1] == "EnableRobot(2.000000,0.100000,0.200000,0.300000)"

    def test_enable_robot_with_all_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.enable_robot(load=1.0, center_x=0.1, center_y=0.2, center_z=0.3, is_check=1)
        assert sent[-1] == "EnableRobot(1.000000,0.100000,0.200000,0.300000,1)"

    def test_disable_robot(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.disable_robot()
        assert sent[-1] == "DisableRobot()"

    def test_clear_error(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.clear_error()
        assert sent[-1] == "ClearError()"

    def test_power_on(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.power_on()
        assert sent[-1] == "PowerOn()"

    def test_run_script(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.run_script("test_project")
        assert sent[-1] == "RunScript(test_project)"

    def test_stop_script(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.stop_script()
        assert sent[-1] == "Stop()"

    def test_pause_script(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.pause_script()
        assert sent[-1] == "Pause()"

    def test_resume(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.resume()
        assert sent[-1] == "Continue()"

    def test_emergency_stop(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.emergency_stop(1)
        assert sent[-1] == "EmergencyStop(1)"

    def test_brake_control(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.brake_control(1, 1)
        assert sent[-1] == "BrakeControl(1,1)"

    def test_request_control(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.request_control()
        assert sent[-1] == "RequestControl()"

    def test_reset_robot(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.reset_robot()
        assert sent[-1] == "ResetRobot()"

    def test_tcp_send_and_parse(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.tcp_send_and_parse("TestCmd")
        assert sent[-1] == 'TcpSendAndParse("TestCmd")'

    def test_sleep(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.sleep(1000)
        assert sent[-1] == "Sleep(1000)"
