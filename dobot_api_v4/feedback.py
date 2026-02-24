"""
Feedback module for Dobot API V4

This module provides real-time robot status feedback.
"""

import numpy as np
import time
from .base import DobotApi
from .dtypes import FeedbackDtype, FeedbackData
from loguru import logger
from typing import Optional


class DobotApiFeedback(DobotApi):
    """
    Feedback interface for receiving robot status data.

    Connect to port 30004 (8ms), 30005 (200ms), or 30006 (configurable)
    for real-time feedback.
    """

    def __init__(self, ip: str, port: int, *args) -> None:
        """
        Initialize feedback connection.

        Args:
            ip: Robot IP address.
            port: Feedback port (30004, 30005, or 30006).
            *args: Additional positional arguments forwarded to DobotApi.
        """
        super().__init__(ip, port, *args)
        self._feedback_dtype: Optional[np.ndarray] = None
        self.last_recv_time: float = time.perf_counter()

    def raw_feedback_data(self) -> Optional[np.ndarray]:
        """Return robot status data as a numpy structured array.

        Reads 1440 bytes of feedback data and parses into a structured
        numpy array using ``FeedbackDtype``.

        Returns:
            Numpy structured array with robot state, or ``None`` if the
            data is invalid or the socket is not connected.

        Raises:
            Exception: If data packets are missing after retries.
        """
        if self.socket_dobot is None:
            return None

        self.socket_dobot.setblocking(True)
        current_recv_time = time.perf_counter()
        temp = self.socket_dobot.recv(144000)

        if len(temp) > 1440:
            temp = self.socket_dobot.recv(144000)

        i = 0
        if len(temp) < 1440:
            while i < 5:
                temp = self.socket_dobot.recv(144000)
                if len(temp) > 1440:
                    break
                i += 1
            if i >= 5:
                raise Exception("Missing data packets, please check network")

        interval = (
            current_recv_time - self.last_recv_time
        ) * 1000  # Convert to milliseconds
        self.last_recv_time = current_recv_time

        data = temp[0:1440]
        self._feedback_dtype = None

        if len(data) == 1440:
            self._feedback_dtype = np.frombuffer(data, dtype=FeedbackDtype)

        return self._feedback_dtype

    # Backward-compat alias
    feedBackData = raw_feedback_data

    def feedback_data(self) -> Optional[FeedbackData]:
        """Return robot status data as a typed ``FeedbackData`` dataclass.

        Convenience wrapper around :meth:`raw_feedback_data` that converts
        the numpy array into a frozen dataclass with Python-native types.

        Returns:
            ``FeedbackData`` instance, or ``None`` if no valid data.
        """
        arr = self.raw_feedback_data()
        if arr is None:
            return None
        return FeedbackData.from_numpy(arr)


# Backward-compat alias
DobotApiFeedBack = DobotApiFeedback
