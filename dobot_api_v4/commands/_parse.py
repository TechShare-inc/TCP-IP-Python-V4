"""Response parsing helpers for dashboard mixins.

Each helper calls :func:`~dobot_api_v4.responses.parse_response` with the
appropriate response dataclass and extracts a domain-level return value.
Keeping converters here (instead of inlining ``parse_response`` in 150+
mixin methods) makes it easy to adjust the parsing logic in one place.
"""

from ..dtypes import Pose
from ..responses import (
    AckResponse,
    ErrorIdResponse,
    IntResponse,
    PoseResponse,
    parse_response,
)


def parse_ack(raw: str) -> None:
    """Parse an acknowledgement response; raise on non-zero error code.

    Args:
        raw: Raw TCP response string.

    Raises:
        DobotApiError: If the robot returned a non-zero error code.
    """
    parse_response(raw, AckResponse)


def parse_int(raw: str) -> int:
    """Parse a response carrying a single integer value.

    Args:
        raw: Raw TCP response string.

    Returns:
        The integer value from the response payload.

    Raises:
        DobotApiError: If the robot returned a non-zero error code.
    """
    return parse_response(raw, IntResponse).value


def parse_pose(raw: str) -> Pose:
    """Parse a response carrying a 6-DOF pose.

    Args:
        raw: Raw TCP response string.

    Returns:
        A :class:`~dobot_api_v4.dtypes.Pose` instance.

    Raises:
        DobotApiError: If the robot returned a non-zero error code.
    """
    r = parse_response(raw, PoseResponse)
    return Pose(x=r.x, y=r.y, z=r.z, rx=r.rx, ry=r.ry, rz=r.rz)


def parse_error_ids(raw: str) -> tuple[int, ...]:
    """Parse a response carrying active error IDs.

    Args:
        raw: Raw TCP response string.

    Returns:
        Tuple of non-zero error IDs (may be empty).

    Raises:
        DobotApiError: If the robot returned a non-zero error code.
    """
    return parse_response(raw, ErrorIdResponse).error_ids
