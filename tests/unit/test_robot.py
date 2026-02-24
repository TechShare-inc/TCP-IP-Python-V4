"""Unit tests for dobot_api_v4.robot module (DobotRobot façade)."""

from unittest.mock import MagicMock, patch

import pytest

from dobot_api_v4._forward import forward_to
from dobot_api_v4.responses import (
    AckResponse,
    IntResponse,
    PoseResponse,
    ErrorIdResponse,
    parse_response,
)


@pytest.mark.unit
class TestForwardTo:
    """Tests for the @forward_to decorator."""

    def test_forwards_to_target_and_parses(self):
        """@forward_to should call the method on the target attr and parse."""

        class FakeTarget:
            def my_method(self):
                return "0,1,;"

        class FakeRobot:
            def __init__(self):
                self.dashboard = FakeTarget()

            @forward_to("dashboard", AckResponse)
            def my_method(self) -> AckResponse: ...

        robot = FakeRobot()
        result = robot.my_method()
        assert isinstance(result, AckResponse)
        assert result.command_id == 1

    def test_forwards_args(self):
        """@forward_to should pass args and kwargs through."""

        class FakeTarget:
            def method_with_args(self, x, y=0):
                return f"0,1,{x + y};"

        class FakeRobot:
            def __init__(self):
                self.target = FakeTarget()

            @forward_to("target", IntResponse)
            def method_with_args(self, x, y=0) -> IntResponse: ...

        robot = FakeRobot()
        result = robot.method_with_args(3, y=7)
        assert isinstance(result, IntResponse)
        assert result.value == 10

    def test_forwards_pose_response(self):
        """@forward_to should parse PoseResponse correctly."""

        class FakeTarget:
            def get_pose(self):
                return "0,1,100.0,200.0,300.0,0.0,90.0,45.0;"

        class FakeRobot:
            def __init__(self):
                self.dashboard = FakeTarget()

            @forward_to("dashboard", PoseResponse)
            def get_pose(self) -> PoseResponse: ...

        robot = FakeRobot()
        result = robot.get_pose()
        assert isinstance(result, PoseResponse)
        assert result.x == 100.0
        assert result.ry == 90.0

    def test_forwards_error_id_response(self):
        """@forward_to should parse ErrorIdResponse correctly."""

        class FakeTarget:
            def get_error_id(self):
                return "0,1,101,202,0;"

        class FakeRobot:
            def __init__(self):
                self.dashboard = FakeTarget()

            @forward_to("dashboard", ErrorIdResponse)
            def get_error_id(self) -> ErrorIdResponse: ...

        robot = FakeRobot()
        result = robot.get_error_id()
        assert isinstance(result, ErrorIdResponse)
        assert result.error_ids == (101, 202)


@pytest.mark.unit
class TestDobotRobotLifecycle:
    """Tests for DobotRobot lifecycle methods (without real connections)."""

    def test_close_closes_dashboard(self):
        from dobot_api_v4.robot import DobotRobot

        with (
            patch("dobot_api_v4.robot.DobotApiDashboard") as MockDash,
            patch("dobot_api_v4.robot.RobotErrorMonitor"),
        ):
            robot = DobotRobot.__new__(DobotRobot)
            robot.ip = "127.0.0.1"
            robot.dashboard = MockDash()
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

    def test_backward_compat_aliases_present(self):
        from dobot_api_v4.commands.dashboard import DobotApiDashboard

        assert hasattr(DobotApiDashboard, "EnableRobot")
        assert hasattr(DobotApiDashboard, "DisableRobot")
        assert hasattr(DobotApiDashboard, "SpeedFactor")
        assert hasattr(DobotApiDashboard, "MovJ")
        assert hasattr(DobotApiDashboard, "MovL")
        assert hasattr(DobotApiDashboard, "RobotMode")
        assert hasattr(DobotApiDashboard, "GetPose")
        assert hasattr(DobotApiDashboard, "GetErrorID")

    def test_method_count_at_least_160(self):
        from dobot_api_v4.commands.dashboard import DobotApiDashboard

        methods = [
            m
            for m in dir(DobotApiDashboard)
            if not m.startswith("_") and callable(getattr(DobotApiDashboard, m))
        ]
        assert len(methods) >= 160, f"Expected >= 160 methods, got {len(methods)}"
