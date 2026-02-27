"""Unit tests for dobot_api_v4.robot module (DobotRobot façade)."""

from unittest.mock import MagicMock, patch

import pytest

from dobot_api_v4.robot import DobotRobot


@pytest.mark.unit
class TestDobotRobotDelegation:
    """Tests for __getattr__-based delegation to dashboard."""

    def _make_robot(self) -> DobotRobot:
        """Create a DobotRobot with mocked connections."""
        with (
            patch("dobot_api_v4.robot.DobotApiDashboard") as mock_dash,
            patch("dobot_api_v4.robot.RobotErrorMonitor"),
        ):
            robot = DobotRobot.__new__(DobotRobot)
            robot.ip = "127.0.0.1"
            robot.dashboard = mock_dash()
            robot.errors = MagicMock()
            robot._language = "en"
            robot._feedback = None
            robot._feedback_30005 = None
            robot._feedback_30006 = None
        return robot

    def test_delegates_to_dashboard(self):
        """robot.enable_robot should call dashboard.enable_robot."""
        robot = self._make_robot()
        robot.dashboard.enable_robot = MagicMock(return_value=None)
        robot.enable_robot()
        robot.dashboard.enable_robot.assert_called_once()

    def test_delegates_args_and_kwargs(self):
        """Arguments should pass through to dashboard."""
        robot = self._make_robot()
        robot.dashboard.mov_j = MagicMock(return_value=42)
        result = robot.mov_j(1, 2, 3, 4, 5, 6, coordinate_mode=0)
        robot.dashboard.mov_j.assert_called_once_with(
            1, 2, 3, 4, 5, 6, coordinate_mode=0
        )
        assert result == 42

    def test_private_attrs_raise_attribute_error(self):
        """Underscore-prefixed names should not delegate."""
        robot = self._make_robot()
        with pytest.raises(AttributeError):
            _ = robot._nonexistent

    def test_own_methods_take_priority(self):
        """Methods defined on DobotRobot should not delegate."""
        robot = self._make_robot()
        # close() is defined on DobotRobot, not delegated
        assert callable(robot.close)
        # check that it's the real method, not a dashboard attr
        assert "close" in type(robot).__dict__

    def test_nonexistent_dashboard_attr_raises(self):
        """Non-existent dashboard method should raise AttributeError."""
        robot = self._make_robot()
        robot.dashboard.totally_nonexistent = None
        del robot.dashboard.totally_nonexistent
        with pytest.raises(AttributeError):
            robot.totally_nonexistent()


@pytest.mark.unit
class TestDobotRobotLifecycle:
    """Tests for DobotRobot lifecycle methods (without real connections)."""

    def test_close_closes_dashboard(self):
        from dobot_api_v4.robot import DobotRobot

        with (
            patch("dobot_api_v4.robot.DobotApiDashboard") as mock_dash,
            patch("dobot_api_v4.robot.RobotErrorMonitor"),
        ):
            robot = DobotRobot.__new__(DobotRobot)
            robot.ip = "127.0.0.1"
            robot.dashboard = mock_dash()
            robot.errors = MagicMock()
            robot._language = "en"
            robot._feedback = None
            robot._feedback_30005 = None
            robot._feedback_30006 = None

            robot.close()
            robot.dashboard.close.assert_called_once()

    def test_context_manager(self):
        from dobot_api_v4.robot import DobotRobot

        with (
            patch("dobot_api_v4.robot.DobotApiDashboard"),
            patch("dobot_api_v4.robot.RobotErrorMonitor"),
        ):
            robot = DobotRobot.__new__(DobotRobot)
            robot.ip = "127.0.0.1"
            robot.dashboard = MagicMock()
            robot.errors = MagicMock()
            robot._language = "en"
            robot._feedback = None
            robot._feedback_30005 = None
            robot._feedback_30006 = None

            with robot:
                pass
            robot.dashboard.close.assert_called_once()

    def test_lazy_feedback_not_created_until_accessed(self):
        from dobot_api_v4.robot import DobotRobot

        robot = DobotRobot.__new__(DobotRobot)
        robot.ip = "127.0.0.1"
        robot._feedback = None
        robot._feedback_30005 = None
        robot._feedback_30006 = None

        assert robot._feedback is None
        assert robot._feedback_30005 is None
        assert robot._feedback_30006 is None


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
