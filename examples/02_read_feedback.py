#!/usr/bin/env python3
"""Read feedback data example.

Reads one real-time feedback packet from port 30004 using the
``DobotRobot.feedback_data()`` convenience method and prints a selection
of typed fields.  The feedback connection is created lazily on first
access — no extra setup is required beyond a ``DobotRobot`` instance.

Difficulty: Beginner
Prerequisites: 01_connect.py

See also:
- docs/tutorial/reading-feedback.md
"""

from __future__ import annotations

from dobot_api_v4 import DobotRobot, FeedbackData

ROBOT_IP = "192.168.5.1"


def print_feedback(data: FeedbackData) -> None:
    """Print a concise summary of key FeedbackData fields.

    Args:
        data: Typed feedback packet returned by ``feedback_data()``.
    """
    joints = tuple(round(q, 2) for q in data.q_actual)
    tcp = tuple(round(v, 2) for v in data.tool_vector_actual)

    print(f"  robot_mode      : {data.robot_mode}")
    print(f"  enable_status   : {data.enable_status}")
    print(f"  speed_scaling   : {data.speed_scaling:.1f} %")
    print(f"  q_actual (°)    : {joints}")
    print(f"  TCP position    : {tcp}")
    print(f"  error_status    : {data.error_status}")


def main() -> None:
    """Read one feedback packet and display selected fields."""
    with DobotRobot(ROBOT_IP) as robot:
        data = robot.feedback_data()
        if data is None:
            print("No feedback data received — is the robot powered on?")
            return
        print_feedback(data)


if __name__ == "__main__":
    main()
