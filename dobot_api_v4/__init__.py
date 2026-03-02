"""dobot_api_v4 — Python SDK for Dobot V4 robots."""

import os
import sys

from loguru import logger

from .base import DobotApi
from .commands._parse import (
    DobotApiError,
    parse_ack,
    parse_error_ids,
    parse_int,
    parse_pose,
    parse_response,
)
from .commands.dashboard import DobotApiDashboard
from .dtypes import PROTOCOL_FIELD_MAP, FeedbackData, FeedbackDtype, Pose
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedback
from .i18n_manager import AlarmI18n
from .robot import DobotRobot

__version__ = "4.0.0a2"

__all__ = [
    "DobotRobot",
    "DobotApi",
    "DobotApiDashboard",
    "DobotApiFeedback",
    "RobotErrorMonitor",
    "FeedbackData",
    "FeedbackDtype",
    "Pose",
    "PROTOCOL_FIELD_MAP",
    "AlarmI18n",
    "logger",
    "DobotApiError",
    "parse_response",
    "parse_ack",
    "parse_int",
    "parse_pose",
    "parse_error_ids",
]

# Configure loguru
logger.remove()
_LOG_FMT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)
logger.add(
    sys.stderr,
    format=_LOG_FMT,
    level=os.environ.get("DOBOT_LOG_LEVEL", "INFO").upper(),
    colorize=True,
)
