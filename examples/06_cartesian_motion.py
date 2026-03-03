#!/usr/bin/env python3
"""Cartesian linear motion example.

Demonstrates TCP linear motion via ``mov_l`` with Cartesian coordinate
mode.  The current TCP pose is read first and used as both the reference
and the return target, so the robot always comes back to its starting
position regardless of where it happens to be.

Difficulty: Intermediate
Prerequisites: 03_basic_motion.py, 05_configure_speed.py

See also:
- docs/how-to/configure-speed-and-coords.md
- docs/how-to/motion-checking.md
"""

from __future__ import annotations

import time

from dobot_api_v4 import DobotRobot, Pose

ROBOT_IP = "192.168.5.1"

# Vertical (Z-axis) lift distance in mm
Z_LIFT_MM: float = 20.0

# Robot mode constants
_MODE_ENABLE: int = 5
_MODE_RUNNING: int = 7
_MODE_SINGLE_MOVE: int = 8
_MODE_ERROR: int = 9


def wait_for_idle(robot: DobotRobot, timeout: float = 30.0) -> bool:
    """Block until the robot returns to ENABLE state after a move.

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


def move_to_pose(robot: DobotRobot, pose: Pose, label: str) -> None:
    """Issue a MovL (Cartesian) command and wait for completion.

    Args:
        robot: Active ``DobotRobot`` instance.
        pose: Target TCP pose (Cartesian, ``coordinate_mode=0``).
        label: Human-readable description for console output.
    """
    qid = robot.mov_l(pose.x, pose.y, pose.z, pose.rx, pose.ry, pose.rz, coordinate_mode=0)
    print(f"MovL {label}  →  queue_id={qid}")
    assert wait_for_idle(robot), f"Move to '{label}' timed out."


def main() -> None:
    """Read origin, lift Z by Z_LIFT_MM, then return to origin."""
    with DobotRobot(ROBOT_IP) as robot:
        if robot.check_errors():
            still_has = robot.clear_robot_error()
            if still_has:
                print("Could not clear all errors — check robot status.")
                return

        robot.enable_robot()

        # Conservative Cartesian speed settings
        robot.speed_factor(30)
        robot.acc_l(30)
        robot.vel_l(30)
        print("Robot enabled, conservative speed profile applied.")

        # Capture current TCP pose as origin
        origin = robot.get_pose()
        print(
            f"Origin: x={origin.x:.2f}  y={origin.y:.2f}  z={origin.z:.2f}  "
            f"rx={origin.rx:.2f}  ry={origin.ry:.2f}  rz={origin.rz:.2f}"
        )

        # Lift Z
        lifted = Pose(
            x=origin.x,
            y=origin.y,
            z=origin.z + Z_LIFT_MM,
            rx=origin.rx,
            ry=origin.ry,
            rz=origin.rz,
        )
        move_to_pose(robot, lifted, f"z+{Z_LIFT_MM} mm")

        # Return to origin
        move_to_pose(robot, origin, "origin")

        robot.disable_robot()
        print("Robot disabled.")


if __name__ == "__main__":
    main()
