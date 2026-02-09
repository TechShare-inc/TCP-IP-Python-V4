"""
Feedback module for Dobot API V4

This module provides real-time robot status feedback.
"""

import numpy as np
import time
from .base import DobotApi, MyType
from typing import Optional


class DobotApiFeedBack(DobotApi):
    """
    Feedback interface for receiving robot status data.

    Connect to port 30004 or 30005 for real-time feedback.
    """

    def __init__(self, ip: str, port: int, *args) -> None:
        """
        Initialize feedback connection.

        Args:
            ip: Robot IP address
            port: Feedback port (30004 or 30005)
            *args: Optional text log widget
        """
        super().__init__(ip, port, *args)
        self.__MyType: Optional[np.ndarray] = None
        self.last_recv_time: float = time.perf_counter()

    def feedBackData(self) -> Optional[np.ndarray]:
        """
        Return robot status data.

        Reads 1440 bytes of feedback data and parses into structured numpy array
        with V4's MyType structure (PascalCase fields: QActual, DigitalInputs, etc.)

        Returns:
            Numpy structured array with robot state, or None if data invalid

        Raises:
            Exception: If data packets are missing after retries
        """
        if self.socket_dobot is None:
            return None

        self.socket_dobot.setblocking(True)  # Set to blocking mode
        data = bytes()
        current_recv_time = time.perf_counter()  # Get current time
        temp = self.socket_dobot.recv(144000)  # Buffer

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
                raise Exception(
                    "接收数据包缺失，请检查网络环境 / Missing data packets, please check network"
                )

        interval = (
            current_recv_time - self.last_recv_time
        ) * 1000  # Convert to milliseconds
        self.last_recv_time = current_recv_time

        data = temp[0:1440]  # Extract 1440 bytes
        self.__MyType = None

        if len(data) == 1440:
            self.__MyType = np.frombuffer(data, dtype=MyType)

        return self.__MyType
