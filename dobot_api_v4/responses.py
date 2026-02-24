"""Typed response dataclasses and parser for Dobot TCP text responses."""

import re
from dataclasses import dataclass
from typing import TypeVar


class DobotApiError(Exception):
    """Raised when robot returns non-zero error_code."""

    def __init__(
        self, error_code: int, command_id: int, message: str, raw: str
    ) -> None:
        self.error_code = error_code
        self.command_id = command_id
        self.message = message
        self.raw = raw
        super().__init__(message)


@dataclass(frozen=True)
class AckResponse:
    """Simple acknowledgement - no payload beyond command_id."""

    command_id: int


@dataclass(frozen=True)
class IntResponse:
    """Response carrying a single integer value."""

    command_id: int
    value: int


@dataclass(frozen=True)
class PoseResponse:
    """Response carrying a 6-DOF pose (x, y, z, rx, ry, rz)."""

    command_id: int
    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float


@dataclass(frozen=True)
class ErrorIdResponse:
    """Response carrying a list of active error IDs."""

    command_id: int
    error_ids: tuple[int, ...]


_ResponseT = TypeVar(
    "_ResponseT", AckResponse, IntResponse, PoseResponse, ErrorIdResponse
)

# Regex for standard 3-field format: "error_code,command_id,payload;"
_RE_3FIELD = re.compile(r"^(\d+),(\d+),(.*)$")

# Regex for brace-payload format: "error_code,{payload};"
_RE_BRACE = re.compile(r"^(\d+),\{(.*)\}$")


def parse_response(raw: str, response_type: type[_ResponseT]) -> _ResponseT:
    """Parse raw robot TCP response into a typed dataclass.

    Supports two formats:
    - 3-field: ``"error_code,command_id,payload;"``
    - 2-field (brace): ``"error_code,{brace_payload};"``

    Args:
        raw: Raw response string from robot.
        response_type: Target dataclass type.

    Returns:
        Parsed response dataclass.

    Raises:
        DobotApiError: If error_code is non-zero.
        ValueError: If response format is unrecognized.
    """
    cleaned = raw.strip().rstrip(";").strip()

    # Try 3-field format first
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
                    f"Robot returned error code {error_code}"
                    f" for command {command_id}: {payload}"
                ),
                raw=raw,
            )

        return _build_response(response_type, command_id, payload)

    # Try brace format
    m = _RE_BRACE.match(cleaned)
    if m:
        error_code = int(m.group(1))
        payload = m.group(2)
        # Brace format has no explicit command_id; use 0
        command_id = 0

        if error_code != 0:
            raise DobotApiError(
                error_code=error_code,
                command_id=command_id,
                message=f"Robot returned error code {error_code}: {payload}",
                raw=raw,
            )

        return _build_response(response_type, command_id, payload)

    raise ValueError(f"Unrecognized response format: {raw!r}")


def _build_response(
    response_type: type[_ResponseT], command_id: int, payload: str
) -> _ResponseT:
    """Construct a response dataclass from parsed fields.

    Args:
        response_type: Target dataclass type.
        command_id: Parsed command ID.
        payload: Remaining payload string after error_code and command_id.

    Returns:
        Constructed response instance.
    """
    if response_type is AckResponse:
        return AckResponse(command_id=command_id)  # type: ignore[return-value]

    if response_type is IntResponse:
        value = int(payload.strip()) if payload.strip() else 0
        return IntResponse(command_id=command_id, value=value)  # type: ignore[return-value]

    if response_type is PoseResponse:
        parts = [float(x.strip()) for x in payload.split(",")]
        if len(parts) < 6:
            raise ValueError(
                f"PoseResponse requires 6 floats, got {len(parts)}: {payload!r}"
            )
        return PoseResponse(  # type: ignore[return-value]
            command_id=command_id,
            x=parts[0],
            y=parts[1],
            z=parts[2],
            rx=parts[3],
            ry=parts[4],
            rz=parts[5],
        )

    if response_type is ErrorIdResponse:
        if not payload.strip():
            error_ids: tuple[int, ...] = ()
        else:
            error_ids = tuple(
                int(x.strip())
                for x in payload.split(",")
                if x.strip() and int(x.strip()) != 0
            )
        return ErrorIdResponse(  # type: ignore[return-value]
            command_id=command_id, error_ids=error_ids
        )

    raise TypeError(f"Unsupported response type: {response_type}")
