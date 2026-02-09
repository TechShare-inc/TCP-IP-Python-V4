"""
Dobot API V4.0.0 - Python TCP/IP Interface

⚠️ BREAKING CHANGES FROM PREVIOUS VERSIONS:
- Refactored into modular package structure
- Separated DobotApiMove class for movement commands (V3-style architecture)
- All V4 method signatures and features preserved
- Import paths changed: `from dobot_api import DobotApiDashboard, DobotApiMove, DobotApiFeedBack`

Usage Example:
    ```python
    from dobot_api import DobotApiDashboard, DobotApiMove, DobotApiFeedBack

    # Connect (V3 pattern: separate dashboard and move instances)
    dashboard = DobotApiDashboard("192.168.1.6", 29999)
    move = DobotApiMove("192.168.1.6", 29999)  # Same port, separate API
    feed = DobotApiFeedBack("192.168.1.6", 30004)

    # Control commands through dashboard
    dashboard.EnableRobot()
    dashboard.VelL(50)

    # Movement commands through move instance
    move.MovJ(300, 0, 200, 0, 90, 0, coordinateMode=0)  # coordinateMode: 0=pose, 1=joint

    # Read feedback
    data = feed.feedBackData()
    print(data['QActual'])  # V4 uses PascalCase
    ```

See MIGRATION_V3_TO_V4.md for detailed API differences.
"""

from .base import DobotApi, MyType
from .dashboard import DobotApiDashboard
from .move import DobotApiMove
from .feedback import DobotApiFeedBack
from .utils import alarmAlarmJsonFile

__version__ = "4.0.0"
__all__ = [
    "DobotApi",
    "DobotApiDashboard",
    "DobotApiMove",
    "DobotApiFeedBack",
    "MyType",
    "alarmAlarmJsonFile",
]
