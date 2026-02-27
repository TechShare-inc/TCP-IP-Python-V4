"""Shared test fixtures for dobot_api_v4 tests."""

from typing import Callable
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from dobot_api_v4.base import DobotApi
from dobot_api_v4.commands.dashboard import DobotApiDashboard
from dobot_api_v4.dtypes import FeedbackDtype
from dobot_api_v4.feedback import DobotApiFeedback

# ---------------------------------------------------------------------------
# DobotApi with patched socket
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_base() -> DobotApi:
    """Return a ``DobotApi`` whose ``__init__`` is bypassed (no real socket).

    The socket attribute is set to a ``MagicMock`` so send/recv can be
    configured per test.
    """
    with patch.object(DobotApi, "__init__", lambda self, *a, **kw: None):
        api = DobotApi.__new__(DobotApi)
        api.ip = "127.0.0.1"
        api.port = 29999
        api.socket_dobot = MagicMock()
        api._global_lock = __import__("threading").Lock()
        return api


# ---------------------------------------------------------------------------
# DobotApiDashboard that captures sent commands
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_dashboard() -> tuple[DobotApiDashboard, list[str]]:
    """Return ``(dashboard, sent)`` where *sent* collects command strings.

    ``send_recv_msg`` is replaced with a spy that appends the command
    string to *sent* and returns a generic success response.
    """
    sent: list[str] = []

    with patch.object(DobotApi, "__init__", lambda self, *a, **kw: None):
        dashboard = DobotApiDashboard.__new__(DobotApiDashboard)
        dashboard.ip = "127.0.0.1"
        dashboard.port = 29999
        dashboard.socket_dobot = MagicMock()
        dashboard._global_lock = __import__("threading").Lock()

    # Commands whose mixin methods call parse_pose (need 6 floats).
    _POSE_COMMANDS = frozenset(
        {
            "GetPose",
            "GetAngle",
            "PositiveKin",
            "InverseKin",
            "InverseSolution",
            "GetForce",
            "GetStartPose",
            "GetTrayPoint",
        }
    )

    def _fake_send_recv(string: str) -> str:
        sent.append(string)
        cmd_name = string.split("(", 1)[0]
        if cmd_name in _POSE_COMMANDS:
            return "0,1,0.0,0.0,0.0,0.0,0.0,0.0;"
        return "0,1,0;"

    dashboard.send_recv_msg = _fake_send_recv  # type: ignore[assignment]
    return dashboard, sent


# ---------------------------------------------------------------------------
# DobotApiFeedback with mock socket
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_feedback() -> DobotApiFeedback:
    """Return a ``DobotApiFeedback`` with a mocked socket."""
    with patch.object(DobotApi, "__init__", lambda self, *a, **kw: None):
        fb = DobotApiFeedback.__new__(DobotApiFeedback)
        fb.ip = "127.0.0.1"
        fb.port = 30004
        fb.socket_dobot = MagicMock()
        fb._global_lock = __import__("threading").Lock()
        fb._feedback_dtype = None
        fb.last_recv_time = 0.0
        return fb


# ---------------------------------------------------------------------------
# Feedback buffer factory
# ---------------------------------------------------------------------------


@pytest.fixture()
def feedback_buffer_factory() -> Callable[..., bytes]:
    """Return a callable that builds valid 1440-byte feedback buffers.

    Usage::

        buf = feedback_buffer_factory(robot_mode=5, speed_scaling=80.0)
    """

    def _factory(**overrides: object) -> bytes:
        arr = np.zeros(1, dtype=FeedbackDtype)
        for key, val in overrides.items():
            arr[key] = val
        return arr.tobytes()

    return _factory
