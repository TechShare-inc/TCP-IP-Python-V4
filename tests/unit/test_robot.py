"""Unit tests for dobot_api_v4.robot module (DobotRobot façade).

Tests cover:
- Lifecycle helpers (close, reconnect, context-manager).
- Lazy feedback properties.
- The fact that non-existent methods are *not* accessible directly on
  ``DobotRobot`` (no ``__getattr__`` fallback).
- ``DobotApiDashboard`` MRO sanity checks.
"""

from unittest.mock import MagicMock

import pytest

from dobot_api_v4.robot import DobotRobot

# -- Shared fixture -----------------------------------------------------


def _make_robot() -> DobotRobot:
    """Create a ``DobotRobot`` with mocked connections."""
    robot = DobotRobot.__new__(DobotRobot)
    robot.ip = "127.0.0.1"
    robot.dashboard = MagicMock()  # type: ignore[assignment]
    robot.errors = MagicMock()
    robot._language = "en"
    robot._feedback = None
    robot._feedback_30005 = None
    robot._feedback_30006 = None
    return robot


# ======================================================================
# No __getattr__ fallback
# ======================================================================


@pytest.mark.unit
class TestNoGetAttrFallback:
    """Verify that non-forwarded dashboard methods are NOT accessible directly."""

    def test_nonexistent_method_raises_attribute_error(self):
        """A method that doesn't exist anywhere should not be accessible."""
        robot = _make_robot()
        with pytest.raises(AttributeError):
            robot.this_method_does_not_exist_anywhere()  # type: ignore[attr-defined]

    def test_dashboard_accessible_directly_via_robot(self):
        """Forwarded dashboard methods are callable directly on DobotRobot."""
        robot = _make_robot()
        robot.dashboard.enable_robot = MagicMock(return_value=None)
        robot.enable_robot()
        robot.dashboard.enable_robot.assert_called_once()

    def test_no_getattr_on_class(self):
        """DobotRobot should not define __getattr__."""
        assert "__getattr__" not in DobotRobot.__dict__

    def test_own_methods_take_priority(self):
        """Methods defined directly on DobotRobot are not forwarded."""
        assert "close" in DobotRobot.__dict__
        assert "reconnect" in DobotRobot.__dict__
        assert "check_errors" in DobotRobot.__dict__
        assert "clear_robot_error" in DobotRobot.__dict__
        assert "feedback_data" in DobotRobot.__dict__


# ======================================================================
# Lifecycle
# ======================================================================


@pytest.mark.unit
class TestDobotRobotLifecycle:
    """Tests for DobotRobot lifecycle methods (without real connections)."""

    def test_close_closes_dashboard(self):
        robot = _make_robot()
        robot.close()
        robot.dashboard.close.assert_called_once()  # type: ignore[attr-defined]

    def test_close_closes_active_feedback(self):
        robot = _make_robot()
        mock_fb = MagicMock()
        robot._feedback = mock_fb
        robot.close()
        mock_fb.close.assert_called_once()

    def test_close_skips_inactive_feedback(self):
        robot = _make_robot()
        # _feedback is None -- close should not crash
        robot.close()

    def test_context_manager_calls_close(self):
        robot = _make_robot()
        with robot:
            pass
        robot.dashboard.close.assert_called_once()  # type: ignore[attr-defined]

    def test_reconnect_reconnects_dashboard(self):
        robot = _make_robot()
        robot.reconnect()
        robot.dashboard.reconnect.assert_called_once()  # type: ignore[attr-defined]

    def test_reconnect_reconnects_active_feedback(self):
        robot = _make_robot()
        mock_fb = MagicMock()
        robot._feedback = mock_fb
        robot.reconnect()
        mock_fb.reconnect.assert_called_once()

    def test_lazy_feedback_not_created_until_accessed(self):
        robot = _make_robot()
        assert robot._feedback is None
        assert robot._feedback_30005 is None
        assert robot._feedback_30006 is None


# ======================================================================
# Error convenience
# ======================================================================


@pytest.mark.unit
class TestDobotRobotErrorConvenience:
    """Tests for check_errors / clear_robot_error composite methods."""

    def test_check_errors_delegates_to_error_monitor(self):
        robot = _make_robot()
        robot.errors.check_errors = MagicMock(return_value=True)
        assert robot.check_errors() is True
        robot.errors.check_errors.assert_called_once_with("en")

    def test_check_errors_respects_language_override(self):
        robot = _make_robot()
        robot.errors.check_errors = MagicMock(return_value=False)
        robot.check_errors(language="zh_CN")
        robot.errors.check_errors.assert_called_once_with("zh_CN")

    def test_clear_robot_error_clears_then_checks(self):
        robot = _make_robot()
        robot.dashboard.clear_error = MagicMock(return_value=None)
        robot.errors.check_errors = MagicMock(return_value=False)
        result = robot.clear_robot_error()
        robot.dashboard.clear_error.assert_called_once()
        robot.errors.check_errors.assert_called_once_with("en")
        assert result is False


# ======================================================================
# Dashboard MRO (unchanged)
# ======================================================================


@pytest.mark.unit
class TestDobotRobotMRO:
    """Tests for the composed DobotApiDashboard MRO."""

    def test_dashboard_has_all_mixin_methods(self):
        from dobot_api_v4.commands.dashboard import DobotApiDashboard

        # System
        assert hasattr(DobotApiDashboard, "enable_robot")
        assert hasattr(DobotApiDashboard, "disable_robot")
        assert hasattr(DobotApiDashboard, "clear_error")

        # Config
        assert hasattr(DobotApiDashboard, "speed_factor")
        assert hasattr(DobotApiDashboard, "acc_j")

        # IO
        assert hasattr(DobotApiDashboard, "do_output")
        assert hasattr(DobotApiDashboard, "di")

        # Modbus
        assert hasattr(DobotApiDashboard, "modbus_create")
        assert hasattr(DobotApiDashboard, "get_output_float")

        # Query
        assert hasattr(DobotApiDashboard, "robot_mode")
        assert hasattr(DobotApiDashboard, "get_pose")

        # Motion
        assert hasattr(DobotApiDashboard, "mov_j")
        assert hasattr(DobotApiDashboard, "mov_l")

        # Force
        assert hasattr(DobotApiDashboard, "enable_ft_sensor")
        assert hasattr(DobotApiDashboard, "fc_off")

        # Conveyor
        assert hasattr(DobotApiDashboard, "cnv_init")

        # Weld
        assert hasattr(DobotApiDashboard, "weave_start")

        # Check
        assert hasattr(DobotApiDashboard, "check_mov_j")

    def test_method_count_at_least_80(self):
        from dobot_api_v4.commands.dashboard import DobotApiDashboard

        methods = [
            m
            for m in dir(DobotApiDashboard)
            if not m.startswith("_") and callable(getattr(DobotApiDashboard, m))
        ]
        assert len(methods) >= 80, f"Expected >= 80 methods, got {len(methods)}"
