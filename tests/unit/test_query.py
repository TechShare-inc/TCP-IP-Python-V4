"""Unit tests for dobot_api_v4.commands._query_mixin module."""

import pytest


@pytest.mark.unit
class TestQueryMixin:
    """Tests verifying exact protocol strings for query commands."""

    def test_robot_mode(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.robot_mode()
        assert sent[-1] == "RobotMode()"

    def test_get_angle(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_angle()
        assert sent[-1] == "GetAngle()"

    def test_get_pose_no_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_pose()
        assert sent[-1] == "GetPose()"

    def test_get_pose_with_user_and_tool(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_pose(user=0, tool=0)
        assert sent[-1] == "GetPose(user=0,tool=0)"

    def test_get_error_id(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_error_id()
        assert sent[-1] == "GetErrorID()"

    def test_positive_kin_basic(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.positive_kin(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        assert "PositiveKin(" in sent[-1]

    def test_inverse_kin_basic(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.inverse_kin(100.0, 200.0, 300.0, 0.0, 90.0, 0.0)
        assert "InverseKin(" in sent[-1]

    def test_get_current_command_id(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_current_command_id()
        assert sent[-1] == "GetCurrentCommandID()"

    def test_start_drag(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.start_drag()
        assert sent[-1] == "StartDrag()"

    def test_stop_drag(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.stop_drag()
        assert sent[-1] == "StopDrag()"

    def test_path_recovery(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.path_recovery()
        assert sent[-1] == "PathRecovery()"

    def test_path_recovery_stop(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.path_recovery_stop()
        assert sent[-1] == "PathRecoveryStop()"

    def test_path_recovery_status(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.path_recovery_status()
        assert sent[-1] == "PathRecoveryStatus()"

    def test_log_export_usb(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.log_export_usb(1)
        assert sent[-1] == "LogExportUSB(1)"

    def test_get_export_status(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_export_status()
        assert sent[-1] == "GetExportStatus()"
