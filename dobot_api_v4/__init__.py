"""
Dobot API V4.0.0 - Python TCP/IP Interface

⚠️ BREAKING CHANGES FROM PREVIOUS VERSIONS:
- Refactored into modular package structure
- All V4 method signatures and features preserved
- Import paths changed: `from dobot_api_v4 import DobotApiDashboard, DobotApiFeedBack, RobotErrorMonitor`

V4 Monolithic Architecture (Original Design):
- DobotApiDashboard: Contains both control AND movement commands (TCP port 29999)
- DobotApiFeedBack: Real-time robot feedback (TCP port 30004)
- RobotErrorMonitor: Error monitoring and diagnostics (HTTP port 22000)
- Single dashboard instance for all operations

Usage Example:
    ```python
    from dobot_api_v4 import DobotApiDashboard, DobotApiFeedBack, RobotErrorMonitor

    dashboard = DobotApiDashboard("192.168.1.6", 29999)
    feed = DobotApiFeedBack("192.168.1.6", 30004)

    monitor = RobotErrorMonitor("192.168.1.6")

    dashboard.EnableRobot()
    dashboard.VelL(50)

    dashboard.MovJ(300, 0, 200, 0, 90, 0, coordinateMode=0)

    error_info = monitor.get_error_info("en")
    if error_info and error_info.get("errMsg"):
        print(f"Found {len(error_info['errMsg'])} errors")

    data = feed.feedBackData()
    print(data['QActual'])
    ```

See MIGRATION_V3_TO_V4.md for detailed API differences.
"""

from .base import DobotApi, MyType
from .dashboard import DobotApiDashboard
from .feedback import DobotApiFeedBack
from .error_monitor import RobotErrorMonitor
from .i18n_manager import AlarmI18n

import os
import sys
from loguru import logger

logger.remove()

log_level = os.environ.get("DOBOT_LOG_LEVEL", "INFO").upper()

logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=log_level,
    colorize=True,
)

__version__ = "4.0.0"
__all__ = [
    "DobotApi",
    "DobotApiDashboard",
    "DobotApiFeedBack",
    "RobotErrorMonitor",
    "MyType",
    "AlarmI18n",
    "logger",
]
