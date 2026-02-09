"""
Base classes and types for Dobot API V4

This module contains the core TCP communication class and feedback data structures.
"""

import socket
import numpy as np
import threading
from time import sleep
from typing import Any, Optional
from loguru import logger

# Port Feedback Structure for V4
MyType = np.dtype(
    [
        (
            "len",
            np.uint16,
        ),
        ("reserve", np.byte, (6,)),
        (
            "DigitalInputs",
            np.uint64,
        ),
        (
            "DigitalOutputs",
            np.uint64,
        ),
        (
            "RobotMode",
            np.uint64,
        ),
        (
            "TimeStamp",
            np.uint64,
        ),
        (
            "RunTime",
            np.uint64,
        ),
        (
            "TestValue",
            np.uint64,
        ),
        ("reserve2", np.byte, (8,)),
        (
            "SpeedScaling",
            np.float64,
        ),
        ("reserve3", np.byte, (16,)),
        (
            "VRobot",
            np.float64,
        ),
        (
            "IRobot",
            np.float64,
        ),
        (
            "ProgramState",
            np.float64,
        ),
        (
            "SafetyOIn",
            np.uint16,
        ),
        (
            "SafetyOOut",
            np.uint16,
        ),
        ("reserve4", np.byte, (76,)),
        ("QTarget", np.float64, (6,)),
        ("QDTarget", np.float64, (6,)),
        ("QDDTarget", np.float64, (6,)),
        ("ITarget", np.float64, (6,)),
        ("MTarget", np.float64, (6,)),
        ("QActual", np.float64, (6,)),
        ("QDActual", np.float64, (6,)),
        ("IActual", np.float64, (6,)),
        ("ActualTCPForce", np.float64, (6,)),
        ("ToolVectorActual", np.float64, (6,)),
        ("TCPSpeedActual", np.float64, (6,)),
        ("TCPForce", np.float64, (6,)),
        ("ToolVectorTarget", np.float64, (6,)),
        ("TCPSpeedTarget", np.float64, (6,)),
        ("MotorTemperatures", np.float64, (6,)),
        ("JointModes", np.float64, (6,)),
        ("VActual", np.float64, (6,)),
        ("HandType", np.byte, (4,)),
        (
            "User",
            np.byte,
        ),
        (
            "Tool",
            np.byte,
        ),
        (
            "RunQueuedCmd",
            np.byte,
        ),
        (
            "PauseCmdFlag",
            np.byte,
        ),
        (
            "VelocityRatio",
            np.byte,
        ),
        (
            "AccelerationRatio",
            np.byte,
        ),
        (
            "reserve5",
            np.byte,
        ),
        (
            "XYZVelocityRatio",
            np.byte,
        ),
        (
            "RVelocityRatio",
            np.byte,
        ),
        (
            "XYZAccelerationRatio",
            np.byte,
        ),
        (
            "RAccelerationRatio",
            np.byte,
        ),
        ("reserve6", np.byte, (2,)),
        (
            "BrakeStatus",
            np.byte,
        ),
        (
            "EnableStatus",
            np.byte,
        ),
        (
            "DragStatus",
            np.byte,
        ),
        (
            "RunningStatus",
            np.byte,
        ),
        (
            "ErrorStatus",
            np.byte,
        ),
        (
            "JogStatusCR",
            np.byte,
        ),
        (
            "CRRobotType",
            np.byte,
        ),
        (
            "DragButtonSignal",
            np.byte,
        ),
        (
            "EnableButtonSignal",
            np.byte,
        ),
        (
            "RecordButtonSignal",
            np.byte,
        ),
        (
            "ReappearButtonSignal",
            np.byte,
        ),
        (
            "JawButtonSignal",
            np.byte,
        ),
        (
            "SixForceOnline",
            np.byte,
        ),
        (
            "CollisionState",
            np.byte,
        ),
        (
            "ArmApproachState",
            np.byte,
        ),
        (
            "J4ApproachState",
            np.byte,
        ),
        (
            "J5ApproachState",
            np.byte,
        ),
        (
            "J6ApproachState",
            np.byte,
        ),
        ("reserve7", np.byte, (61,)),
        (
            "VibrationDisZ",
            np.float64,
        ),
        (
            "CurrentCommandId",
            np.uint64,
        ),
        ("MActual", np.float64, (6,)),
        (
            "Load",
            np.float64,
        ),
        (
            "CenterX",
            np.float64,
        ),
        (
            "CenterY",
            np.float64,
        ),
        (
            "CenterZ",
            np.float64,
        ),
        ("UserValue[6]", np.float64, (6,)),
        ("ToolValue[6]", np.float64, (6,)),
        ("reserve8", np.byte, (8,)),
        ("SixForceValue", np.float64, (6,)),
        ("TargetQuaternion", np.float64, (4,)),
        ("ActualQuaternion", np.float64, (4,)),
        (
            "AutoManualMode",
            np.uint16,
        ),
        (
            "ExportStatus",
            np.uint16,
        ),
        (
            "SafetyState",
            np.byte,
        ),
        ("reserve9", np.byte, (19,)),
    ]
)


class DobotApi:
    """
    Base TCP communication class for Dobot robots.

    Supports ports:
    - 29999: Dashboard and movement commands
    - 30004: Feedback data
    - 30005: Additional feedback (V4-specific)
    """

    def __init__(self, ip: str, port: int, *args) -> None:
        """
        Initialize TCP connection to Dobot robot.

        Args:
            ip: Robot IP address (e.g., "192.168.1.6")
            port: Port number (must be 29999, 30004, or 30005)
            *args: Optional text log widget for UI integration

        Raises:
            ValueError: If port is not in allowed list
            ConnectionError: If unable to establish socket connection
        """
        self.ip: str = ip
        self.port: int = port
        self.socket_dobot: Optional[socket.socket] = None
        self.__globalLock: threading.Lock = threading.Lock()
        self.text_log: Optional[Any] = args[0] if args else None

        # Validate port
        if self.port not in [29999, 30004, 30005]:
            raise ValueError(
                f"Invalid port {self.port}. Must be 29999 (dashboard/movement), "
                f"30004 (feedback), or 30005 (feedback V4-specific)."
            )

        # Establish connection
        try:
            self.socket_dobot = socket.socket()
            self.socket_dobot.connect((self.ip, self.port))
            self.socket_dobot.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 144000)
        except socket.error as e:
            raise ConnectionError(
                f"Unable to establish socket connection to {self.ip}:{self.port}. "
                f"Error: {e}"
            ) from e

    def log(self, text: str) -> None:
        """Log a message to the text widget or console."""
        if self.text_log:
            logger.debug(text)

    def send_data(self, string: str) -> None:
        """
        Send data to the robot over TCP.

        Args:
            string: Command string to send
        """
        try:
            if self.socket_dobot:
                self.socket_dobot.send(str.encode(string, "utf-8"))
        except Exception as e:
            logger.error(f"Send error: {e}. Attempting reconnection...")
            while True:
                try:
                    self.socket_dobot = self.reConnect(self.ip, self.port)
                    if self.socket_dobot:
                        self.socket_dobot.send(str.encode(string, "utf-8"))
                    break
                except Exception:
                    sleep(1)

    def wait_reply(self) -> str:
        """
        Read the return value from robot.

        Returns:
            Response string from robot
        """
        data = b""
        try:
            if self.socket_dobot:
                data = self.socket_dobot.recv(1024)
        except Exception as e:
            logger.error(f"Receive error: {e}. Attempting reconnection...")
            self.socket_dobot = self.reConnect(self.ip, self.port)
        finally:
            data_str = str(data, encoding="utf-8") if data else ""
            return data_str

    def close(self) -> None:
        """Close the TCP socket connection."""
        if self.socket_dobot is not None:
            try:
                self.socket_dobot.shutdown(socket.SHUT_RDWR)
                self.socket_dobot.close()
            except socket.error as e:
                logger.warning(f"Error while closing socket: {e}")

    def sendRecvMsg(self, string: str) -> str:
        """
        Send command and receive response synchronously.

        Args:
            string: Command string to send

        Returns:
            Response string from robot
        """
        with self.__globalLock:
            self.send_data(string)
            recvData = self.wait_reply()
            return recvData

    def __del__(self) -> None:
        """Clean up socket connection on object destruction."""
        self.close()

    def reConnect(self, ip: str, port: int) -> Optional[socket.socket]:
        """
        Attempt to reconnect to the robot.

        Args:
            ip: Robot IP address
            port: Port number

        Returns:
            New socket object or None
        """
        while True:
            try:
                socket_dobot = socket.socket()
                socket_dobot.connect((ip, port))
                logger.info(f"Reconnected to {ip}:{port}")
                return socket_dobot
            except Exception:
                sleep(1)
