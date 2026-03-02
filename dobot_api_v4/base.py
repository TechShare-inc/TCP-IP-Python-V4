"""
Base classes and types for Dobot API V4

This module contains the core TCP communication class.
Feedback data structures are defined in dtypes.py and re-exported here.
"""

import contextlib
import socket
import threading
from time import sleep
from typing import Any, Optional

from loguru import logger


class DobotApi:
    """
    Base TCP communication class for Dobot robots.

    Supports ports:
    - 29999: Dashboard and movement commands
    - 30004: Feedback data (8ms cycle)
    - 30005: Feedback data (200ms cycle)
    - 30006: Feedback data (configurable cycle)
    """

    _ALLOWED_PORTS = {29999, 30004, 30005, 30006}

    def __init__(self, ip: str, port: int, *args: Any) -> None:
        """
        Initialize TCP connection to Dobot robot.

        Args:
            ip: Robot IP address (e.g., "192.168.1.6")
            port: Port number (must be in {29999, 30004, 30005, 30006})
            *args: Legacy positional args (ignored).

        Raises:
            ValueError: If port is not in allowed set.
            ConnectionError: If unable to establish socket connection.
        """
        self.ip: str = ip
        self.port: int = port
        self.socket_dobot: Optional[socket.socket] = None
        self._global_lock: threading.Lock = threading.Lock()

        if self.port not in self._ALLOWED_PORTS:
            raise ValueError(
                f"Invalid port {self.port}. Must be one of {sorted(self._ALLOWED_PORTS)}."
            )

        try:
            self.socket_dobot = socket.socket()
            self.socket_dobot.connect((self.ip, self.port))
            self.socket_dobot.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 144000)
        except OSError as e:
            raise ConnectionError(
                f"Unable to establish socket connection to {self.ip}:{self.port}. Error: {e}"
            ) from e

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "DobotApi":
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Low-level send / receive
    # ------------------------------------------------------------------

    def send_data(self, string: str) -> None:
        """
        Send data to the robot over TCP.

        Args:
            string: Command string to send.
        """
        try:
            if self.socket_dobot:
                self.socket_dobot.send(str.encode(string, "utf-8"))
        except Exception as e:
            logger.error(f"Send error: {e}. Attempting reconnection...")
            while True:
                try:
                    self.socket_dobot = self.reconnect(self.ip, self.port)
                    if self.socket_dobot:
                        self.socket_dobot.send(str.encode(string, "utf-8"))
                    break
                except Exception:
                    sleep(1)

    def wait_reply(self) -> str:
        """
        Read the return value from robot.

        Returns:
            Response string from robot.
        """
        data = b""
        try:
            if self.socket_dobot:
                data = self.socket_dobot.recv(1024)
        except Exception as e:
            logger.error(f"Receive error: {e}. Attempting reconnection...")
            self.socket_dobot = self.reconnect(self.ip, self.port)
        data_str = str(data, encoding="utf-8") if data else ""
        return data_str

    def close(self) -> None:
        """Close the TCP socket connection."""
        if self.socket_dobot is not None:
            with contextlib.suppress(OSError):
                self.socket_dobot.shutdown(socket.SHUT_RDWR)
            with contextlib.suppress(OSError):
                self.socket_dobot.close()
            self.socket_dobot = None

    # ------------------------------------------------------------------
    # Send + receive (thread-safe)
    # ------------------------------------------------------------------

    def send_recv_msg(self, string: str) -> str:
        """
        Send command and receive response synchronously (thread-safe).

        Args:
            string: Command string to send.

        Returns:
            Response string from robot.
        """
        with self._global_lock:
            self.send_data(string)
            recv_data = self.wait_reply()
            return recv_data

    # ------------------------------------------------------------------
    # Reconnection
    # ------------------------------------------------------------------

    def reconnect(
        self, ip: Optional[str] = None, port: Optional[int] = None
    ) -> Optional[socket.socket]:
        """
        Attempt to reconnect to the robot.

        Args:
            ip: Robot IP address (defaults to ``self.ip``).
            port: Port number (defaults to ``self.port``).

        Returns:
            New socket object or None.
        """
        ip = ip or self.ip
        port = port or self.port
        while True:
            try:
                socket_dobot = socket.socket()
                socket_dobot.connect((ip, port))
                logger.info(f"Reconnected to {ip}:{port}")
                return socket_dobot
            except Exception:
                sleep(1)

    def __del__(self) -> None:
        """Clean up socket connection on object destruction."""
        self.close()
