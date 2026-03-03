#!/usr/bin/env python3
"""Basic joint motion example.

Enables the robot, reads the current joint configuration from feedback,
offsets J1 forward then backward, and returns to the starting pose.  A
feedback-based helper polls ``robot_mode`` so each command is confirmed
complete before the next one begins — the same synchronisation pattern
used in all subsequent motion examples.

Difficulty: Intermediate
Prerequisites: 02_read_feedback.py; robot in a safe, unobstructed position

See also:
- docs/tutorial/pick-and-place.md
- docs/how-to/motion-checking.md
"""

from __future__ import annotations

import time

from dobot_api_v4 import DobotRobot

ROBOT_IP = "192.168.5.1"

# Degrees to offset J1 for the demonstration swing
J1_OFFSET: float = 5.0

# Robot mode constants (robot_mode() return values)
_MODE_ENABLE: int = 5
_MODE_RUNNING: int = 7
_MODE_SINGLE_MOVE: int = 8
_MODE_ERROR: int = 9


def wait_for_idle(robot: DobotRobot, timeout: float = 30.0) -> bool:
    """Block until the robot finishes moving and returns to ENABLE state.

    Polls ``robot.feedback_data()`` every 50 ms.  Waits for the robot to
    enter RUNNING or SINGLE_MOVE mode, then waits for it to drop back to
    ENABLE (idle).

    Args:
        robot: Active ``DobotRobot`` instance.
        timeout: Maximum seconds to wait before giving up.

    Returns:
        ``True`` when idle, ``False`` on timeout or ERROR.
    """
    deadline = time.monotonic() + timeout
    saw_moving = False
    while time.monotonic() < deadline:
        data = robot.feedback_data()
        if data is not None:
            mode = data.robot_mode
            if mode in (_MODE_RUNNING, _MODE_SINGLE_MOVE):
                saw_moving = True
            elif saw_moving and mode == _MODE_ENABLE:
                return True
            elif mode == _MODE_ERROR:
                print("Robot entered ERROR state — aborting.")
                return False
        time.sleep(0.05)
    print("Timeout: motion did not complete in time.")
    return False


def main() -> None:
    """Enable, swing J1 ±J1_OFFSET degrees, return home, then disable."""
    with DobotRobot(ROBOT_IP) as robot:
        # Clear lingering errors before enabling
        if robot.check_errors():
            still_has = robot.clear_robot_error()
            if still_has:
                print("Could not clear all errors — check robot status.")
                return

        robot.enable_robot()
        print("Robot enabled.")

        # Read starting joints from the first feedback packet
        data = robot.feedback_data()
        assert data is not None, "Failed to read initial feedback."
        j1, j2, j3, j4, j5, j6 = data.q_actual
        print(f"Start joints (°): {tuple(round(v, 2) for v in (j1, j2, j3, j4, j5, j6))}")

        # Move J1 forward
        qid = robot.mov_j(j1 + J1_OFFSET, j2, j3, j4, j5, j6, coordinate_mode=1)
        print(f"MovJ J1+{J1_OFFSET}°  →  queue_id={qid}")
        assert wait_for_idle(robot), "J1+ move timed out."

        # Move J1 backward
        qid = robot.mov_j(j1 - J1_OFFSET, j2, j3, j4, j5, j6, coordinate_mode=1)
        print(f"MovJ J1-{J1_OFFSET}°  →  queue_id={qid}")
        assert wait_for_idle(robot), "J1- move timed out."

        # Return to the starting configuration
        qid = robot.mov_j(j1, j2, j3, j4, j5, j6, coordinate_mode=1)
        print(f"MovJ home       →  queue_id={qid}")
        assert wait_for_idle(robot), "Home move timed out."

        robot.disable_robot()
        print("Robot disabled.")


if __name__ == "__main__":
    main()
