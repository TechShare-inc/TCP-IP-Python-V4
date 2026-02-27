"""Atomic response-parsing helpers for Dobot TCP text responses.

This module is the single place where raw TCP reply strings are cracked
open, validated, and converted to domain-level Python values.

Public API
----------
- :func:`parse_response` — low-level: raw string → ``(command_id, payload)``
- :func:`parse_ack`       — validates success; returns ``None``
- :func:`parse_int`       — extracts a single ``int`` payload
- :func:`parse_pose`      — extracts a 6-DOF :class:`~dobot_api_v4.dtypes.Pose`
- :func:`parse_error_ids` — extracts active alarm IDs as ``tuple[int, ...]``
- :class:`DobotApiError`  — raised on any non-zero error code
"""

from __future__ import annotations

import re

from ..dtypes import Pose

# ---------------------------------------------------------------------------
# Exception
# ---------------------------------------------------------------------------


class DobotApiError(Exception):
    """Raised when the robot returns a non-zero error code.

    Attributes:
        error_code: The numeric error code from the response.
        command_id: The command ID (0 when not present in the wire format).
        message: Human-readable description.
        raw: The original unmodified response string.
    """

    def __init__(self, error_code: int, command_id: int, message: str, raw: str) -> None:
        self.error_code = error_code
        self.command_id = command_id
        self.message = message
        self.raw = raw
        super().__init__(message)


# ---------------------------------------------------------------------------
# Wire-format regexes (compiled once at import time)
# ---------------------------------------------------------------------------

# V4 brace format: "error_code,{payload},CommandName();"
_RE_BRACE_CMD = re.compile(r"^(-?\d+),\{([^}]*)\},(.+)$")

# Classic 3-field format: "error_code,command_id,payload;"
_RE_3FIELD = re.compile(r"^(-?\d+),(\d+),(.*)$")

# Legacy brace-payload format: "error_code,{payload};"
_RE_BRACE = re.compile(r"^(-?\d+),\{(.*)\}$")


# ---------------------------------------------------------------------------
# Low-level parser
# ---------------------------------------------------------------------------


def parse_response(raw: str) -> tuple[int, str]:
    """Parse a raw TCP response into *(command_id, payload)*.

    Three wire formats are recognised (tried in order):

    1. **V4 brace** — ``"error_code,{payload},CommandName();"``
    2. **3-field**  — ``"error_code,command_id,payload;"``
    3. **Legacy brace** — ``"error_code,{payload};"``

    Args:
        raw: Raw response string from the robot (may include trailing
            semicolons and whitespace).

    Returns:
        A ``(command_id, payload)`` tuple.  *command_id* is ``0`` for
        formats that do not include one.  *payload* is the remaining
        data string after header fields have been stripped.

    Raises:
        DobotApiError: If the error code is non-zero.
        ValueError: If the response does not match any known format.
    """
    cleaned = raw.strip().rstrip(";").strip()

    # --- V4 brace format ---
    m = _RE_BRACE_CMD.match(cleaned)
    if m:
        error_code = int(m.group(1))
        payload = m.group(2)
        cmd_echo = m.group(3)
        command_id = 0

        if error_code != 0:
            raise DobotApiError(
                error_code=error_code,
                command_id=command_id,
                message=(f"Robot returned error code {error_code} for {cmd_echo}: {payload}"),
                raw=raw,
            )
        return command_id, payload

    # --- Classic 3-field format ---
    m = _RE_3FIELD.match(cleaned)
    if m:
        error_code = int(m.group(1))
        command_id = int(m.group(2))
        payload = m.group(3)

        if error_code != 0:
            raise DobotApiError(
                error_code=error_code,
                command_id=command_id,
                message=(
                    f"Robot returned error code {error_code} for command {command_id}: {payload}"
                ),
                raw=raw,
            )
        return command_id, payload

    # --- Legacy brace format ---
    m = _RE_BRACE.match(cleaned)
    if m:
        error_code = int(m.group(1))
        payload = m.group(2)
        command_id = 0

        if error_code != 0:
            raise DobotApiError(
                error_code=error_code,
                command_id=command_id,
                message=f"Robot returned error code {error_code}: {payload}",
                raw=raw,
            )
        return command_id, payload

    raise ValueError(f"Unrecognized response format: {raw!r}")


# ---------------------------------------------------------------------------
# Atomic helpers
# ---------------------------------------------------------------------------


def parse_ack(raw: str) -> None:
    """Parse an acknowledgement response; raise on non-zero error code.

    Args:
        raw: Raw TCP response string.

    Raises:
        DobotApiError: If the robot returned a non-zero error code.
    """
    parse_response(raw)


def parse_int(raw: str) -> int:
    """Parse a response carrying a single integer value.

    Args:
        raw: Raw TCP response string.

    Returns:
        The integer value from the response payload.

    Raises:
        DobotApiError: If the robot returned a non-zero error code.
    """
    _, payload = parse_response(raw)
    return int(payload.strip()) if payload.strip() else 0


def parse_pose(raw: str) -> Pose:
    """Parse a response carrying a 6-DOF pose.

    Args:
        raw: Raw TCP response string.

    Returns:
        A :class:`~dobot_api_v4.dtypes.Pose` instance.

    Raises:
        DobotApiError: If the robot returned a non-zero error code.
        ValueError: If the payload does not contain at least 6 floats.
    """
    _, payload = parse_response(raw)
    parts = [float(x.strip()) for x in payload.split(",")]
    if len(parts) < 6:
        raise ValueError(f"Pose requires 6 floats, got {len(parts)}: {payload!r}")
    return Pose(
        x=parts[0],
        y=parts[1],
        z=parts[2],
        rx=parts[3],
        ry=parts[4],
        rz=parts[5],
    )


def parse_error_ids(raw: str) -> tuple[int, ...]:
    """Parse a response carrying active error IDs.

    Args:
        raw: Raw TCP response string.

    Returns:
        Tuple of non-zero error IDs (may be empty).

    Raises:
        DobotApiError: If the robot returned a non-zero error code.
    """
    _, payload = parse_response(raw)
    if not payload.strip():
        return ()
    return tuple(int(x.strip()) for x in payload.split(",") if x.strip() and int(x.strip()) != 0)
