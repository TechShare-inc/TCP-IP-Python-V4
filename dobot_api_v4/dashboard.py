"""Backward-compatibility re-export shim.

Import DobotApiDashboard from here or from dobot_api_v4.commands.dashboard.
"""

from .commands.dashboard import DobotApiDashboard

__all__ = ["DobotApiDashboard"]
