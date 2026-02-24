"""TCP echo/stub server for integration tests."""

import socket
import threading
import time
from typing import Dict, Optional


class StubServer:
    """TCP server that returns prefix-matched responses.

    Usage::

        responses = {"EnableRobot": "0,1,;", "RobotMode": "0,1,5;"}
        with StubServer("127.0.0.1", 0, responses) as srv:
            # connect to srv.address
            ...
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 0,
        response_map: Optional[Dict[str, str]] = None,
        default_response: str = "0,1,;",
    ) -> None:
        self.host = host
        self.port = port
        self.response_map = response_map or {}
        self.default_response = default_response
        self._server_socket: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False

    @property
    def address(self) -> tuple:
        """Return ``(host, port)`` the server is listening on."""
        if self._server_socket is None:
            raise RuntimeError("Server not started")
        return self._server_socket.getsockname()

    def start(self) -> None:
        """Bind and start accepting connections in a background thread."""
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(5)
        self._server_socket.settimeout(0.5)
        self._running = True
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the server and close all connections."""
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        if self._server_socket is not None:
            try:
                self._server_socket.close()
            except OSError:
                pass

    def __enter__(self) -> "StubServer":
        self.start()
        return self

    def __exit__(self, *exc_info) -> None:
        self.stop()

    def _serve(self) -> None:
        """Accept and handle connections."""
        while self._running:
            try:
                conn, addr = self._server_socket.accept()  # type: ignore[union-attr]
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(target=self._handle, args=(conn,), daemon=True).start()

    def _handle(self, conn: socket.socket) -> None:
        """Handle one client connection."""
        conn.settimeout(1.0)
        try:
            while self._running:
                try:
                    data = conn.recv(4096)
                except socket.timeout:
                    continue
                if not data:
                    break
                cmd = data.decode("utf-8", errors="replace").strip()
                response = self._match_response(cmd)
                conn.sendall(response.encode("utf-8"))
        finally:
            try:
                conn.close()
            except OSError:
                pass

    def _match_response(self, cmd: str) -> str:
        """Find first matching response by prefix."""
        for prefix, resp in self.response_map.items():
            if cmd.startswith(prefix):
                return resp
        return self.default_response


class DelayedStubServer(StubServer):
    """Stub server that adds a configurable delay before responding."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 0,
        response_map: Optional[Dict[str, str]] = None,
        default_response: str = "0,1,;",
        delay: float = 0.1,
    ) -> None:
        super().__init__(host, port, response_map, default_response)
        self.delay = delay

    def _match_response(self, cmd: str) -> str:
        time.sleep(self.delay)
        return super()._match_response(cmd)


class FragmentedStubServer(StubServer):
    """Stub server that sends responses in multiple fragments."""

    def _handle(self, conn: socket.socket) -> None:
        conn.settimeout(1.0)
        try:
            while self._running:
                try:
                    data = conn.recv(4096)
                except socket.timeout:
                    continue
                if not data:
                    break
                cmd = data.decode("utf-8", errors="replace").strip()
                response = self._match_response(cmd)
                # Send in 1-byte chunks
                for byte in response.encode("utf-8"):
                    conn.sendall(bytes([byte]))
                    time.sleep(0.001)
        finally:
            try:
                conn.close()
            except OSError:
                pass


class GarbageStubServer(StubServer):
    """Stub server that inserts garbage bytes before the real response."""

    def _match_response(self, cmd: str) -> str:
        garbage = "\x00\xff\xfe"
        return garbage + super()._match_response(cmd)
