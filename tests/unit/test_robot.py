"""Unit tests for dobot_api_v4.robot module (DobotRobot façade).

Tests cover:
- ``@forward_to``-based delegation (call routing, args, return values,
  metadata, signatures, and return-type annotations).
- Lifecycle helpers (close, reconnect, context-manager).
- Lazy feedback properties.
- The fact that non-forwarded dashboard methods are *not* accessible
  directly on ``DobotRobot`` (no ``__getattr__`` fallback).
- ``DobotApiDashboard`` MRO sanity checks.
"""

import inspect
from unittest.mock import MagicMock

import pytest

from dobot_api_v4.dtypes import Pose
from dobot_api_v4.robot import DobotRobot

# -- Exhaustive list of every @forward_to method on DobotRobot ----------

FORWARDED_SYSTEM = [
    "enable_robot",
    "disable_robot",
    "clear_error",
    "power_on",
    "emergency_stop",
    "reset_robot",
    "sleep",
]

FORWARDED_CONFIG = [
    "speed_factor",
    "acc_j",
    "acc_l",
    "vel_j",
    "vel_l",
    "cp",
    "user",
    "tool",
]

FORWARDED_QUERY = [
    "robot_mode",
    "get_angle",
    "get_pose",
    "get_error_id",
    "positive_kin",
    "inverse_kin",
    "get_current_command_id",
    "start_drag",
    "stop_drag",
]

FORWARDED_MOTION = [
    "mov_j",
    "mov_l",
    "servo_j",
    "servo_p",
    "arc",
    "circle",
    "move_jog",
    "move_l",
]

FORWARDED_IO = ["do_output", "get_do", "di", "ao"]

FORWARDED_FORCE = ["get_force", "fc_off"]

ALL_FORWARDED = (
    FORWARDED_SYSTEM
    + FORWARDED_CONFIG
    + FORWARDED_QUERY
    + FORWARDED_MOTION
    + FORWARDED_IO
    + FORWARDED_FORCE
)

# Expected return-type annotations for every forwarded method.
EXPECTED_RETURN_TYPES: dict[str, type] = {
    # System — all None
    **{n: type(None) for n in FORWARDED_SYSTEM},
    # Config — all None
    **{n: type(None) for n in FORWARDED_CONFIG},
    # Query
    "robot_mode": int,
    "get_angle": Pose,
    "get_pose": Pose,
    "get_error_id": tuple,  # tuple[int, ...]
    "positive_kin": Pose,
    "inverse_kin": Pose,
    "get_current_command_id": int,
    "start_drag": type(None),
    "stop_drag": type(None),
    # Motion
    "mov_j": int,
    "mov_l": int,
    "servo_j": int,
    "servo_p": int,
    "arc": int,
    "circle": int,
    "move_jog": type(None),
    "move_l": int,
    # IO
    "do_output": type(None),
    "get_do": int,
    "di": int,
    "ao": type(None),
    # Force
    "get_force": Pose,
    "fc_off": type(None),
}


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
# @forward_to delegation
# ======================================================================


@pytest.mark.unit
class TestForwardToDelegation:
    """Verify that @forward_to-decorated methods delegate to dashboard."""

    def test_forwarded_method_calls_dashboard(self):
        """robot.enable_robot() should call dashboard.enable_robot()."""
        robot = _make_robot()
        robot.dashboard.enable_robot = MagicMock(return_value=None)
        robot.enable_robot()
        robot.dashboard.enable_robot.assert_called_once()

    def test_forwarded_method_passes_positional_and_keyword_args(self):
        """Positional and keyword args should pass through unchanged."""
        robot = _make_robot()
        robot.dashboard.mov_j = MagicMock(return_value=42)
        result = robot.mov_j(1, 2, 3, 4, 5, 6, coordinate_mode=0)
        robot.dashboard.mov_j.assert_called_once_with(
            1, 2, 3, 4, 5, 6, coordinate_mode=0
        )
        assert result == 42

    def test_forwarded_method_returns_int(self):
        """Methods forwarding int-returning dashboard methods propagate the value."""
        robot = _make_robot()
        robot.dashboard.robot_mode = MagicMock(return_value=5)
        assert robot.robot_mode() == 5

    def test_forwarded_method_returns_pose(self):
        """Methods forwarding Pose-returning dashboard methods propagate the object."""
        robot = _make_robot()
        pose = Pose(x=1.0, y=2.0, z=3.0, rx=4.0, ry=5.0, rz=6.0)
        robot.dashboard.get_pose = MagicMock(return_value=pose)
        assert robot.get_pose() is pose

    def test_forwarded_method_returns_tuple(self):
        """Methods forwarding tuple-returning dashboard methods propagate the tuple."""
        robot = _make_robot()
        robot.dashboard.get_error_id = MagicMock(return_value=(10, 20))
        assert robot.get_error_id() == (10, 20)

    def test_forwarded_method_returns_none(self):
        """None-returning forwarded methods work correctly."""
        robot = _make_robot()
        robot.dashboard.disable_robot = MagicMock(return_value=None)
        assert robot.disable_robot() is None


# ======================================================================
# @forward_to metadata & signatures
# ======================================================================


@pytest.mark.unit
class TestForwardToMetadata:
    """Verify that @forward_to attaches correct metadata and preserves signatures."""

    @pytest.mark.parametrize("name", ALL_FORWARDED)
    def test_forwarded_method_exists(self, name: str):
        """Every expected forwarded method should exist on DobotRobot."""
        assert hasattr(DobotRobot, name), f"DobotRobot.{name} missing"

    @pytest.mark.parametrize("name", ALL_FORWARDED)
    def test_forward_target_metadata(self, name: str):
        """Each forwarded method should have __forward_target__ == 'dashboard'."""
        method = getattr(DobotRobot, name)
        assert getattr(method, "__forward_target__", None) == "dashboard"

    @pytest.mark.parametrize("name", ALL_FORWARDED)
    def test_forward_method_name_metadata(self, name: str):
        """__forward_method__ should match the method's own name."""
        method = getattr(DobotRobot, name)
        assert getattr(method, "__forward_method__", None) == name

    @pytest.mark.parametrize("name", ALL_FORWARDED)
    def test_forward_return_type_metadata(self, name: str):
        """__forward_return_type__ should be set and match expectations."""
        method = getattr(DobotRobot, name)
        expected = EXPECTED_RETURN_TYPES[name]
        actual = getattr(method, "__forward_return_type__", None)
        assert actual is expected, f"{name}: expected {expected}, got {actual}"

    @pytest.mark.parametrize("name", ALL_FORWARDED)
    def test_forwarded_method_has_docstring(self, name: str):
        """Every forwarded method should have a non-empty docstring."""
        method = getattr(DobotRobot, name)
        assert method.__doc__, f"DobotRobot.{name} has no docstring"

    @pytest.mark.parametrize("name", ALL_FORWARDED)
    def test_signature_has_return_annotation(self, name: str):
        """inspect.signature should include a return annotation."""
        sig = inspect.signature(getattr(DobotRobot, name))
        assert (
            sig.return_annotation is not inspect.Parameter.empty
        ), f"DobotRobot.{name} has no return annotation"

    def test_enable_robot_signature_has_explicit_params(self):
        """enable_robot should expose load, center_x/y/z, is_check params."""
        sig = inspect.signature(DobotRobot.enable_robot)
        param_names = list(sig.parameters.keys())
        assert "self" in param_names
        assert "load" in param_names
        assert "center_x" in param_names
        assert "center_y" in param_names
        assert "center_z" in param_names
        assert "is_check" in param_names

    def test_mov_j_signature_has_coordinate_mode(self):
        """mov_j should expose coordinate_mode as a required parameter."""
        sig = inspect.signature(DobotRobot.mov_j)
        param = sig.parameters["coordinate_mode"]
        assert param.default is inspect.Parameter.empty  # required, no default


# ======================================================================
# No __getattr__ fallback
# ======================================================================


@pytest.mark.unit
class TestNoGetAttrFallback:
    """Verify that non-forwarded dashboard methods are NOT accessible directly."""

    def test_non_forwarded_method_raises_attribute_error(self):
        """A dashboard method not in the forwarded set should not be accessible."""
        robot = _make_robot()
        with pytest.raises(AttributeError):
            robot.set_payload(1.0, 0, 0, 0)  # type: ignore[attr-defined]

    def test_non_forwarded_method_accessible_via_dashboard(self):
        """The same method should still work through robot.dashboard."""
        robot = _make_robot()
        robot.dashboard.set_payload = MagicMock(return_value=None)
        robot.dashboard.set_payload(1.0, 0, 0, 0)
        robot.dashboard.set_payload.assert_called_once_with(1.0, 0, 0, 0)

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
        # _feedback is None — close should not crash
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
