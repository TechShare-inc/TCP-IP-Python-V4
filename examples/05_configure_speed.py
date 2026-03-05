#!/usr/bin/env python3
"""Speed and acceleration configuration example.

Shows how to tune the global speed ratio (``speed_factor``) and the
per-axis acceleration/velocity limits before issuing motion commands.
All settings are robot-global and persist for the duration of the
connection unless explicitly changed.

Difficulty: Intermediate
Prerequisites: 03_basic_motion.py

See also:
- docs/how-to/configure-speed-and-coords.md
"""

from __future__ import annotations

import time

from dobot_api_v4 import DobotRobot

ROBOT_IP = "192.168.5.1"

# Conservative defaults — safe for first-time users (all unit: %)
SPEED_FACTOR_SAFE: int = 30
ACC_SAFE: int = 30
VEL_SAFE: int = 30

# Small J1 offset (degrees) used to show the speed difference
J1_SWING: float = 5.0

# Robot mode constants
_MODE_ENABLE: int = 5
_MODE_RUNNING: int = 7
_MODE_SINGLE_MOVE: int = 8
_MODE_ERROR: int = 9


def apply_speed_profile(robot: DobotRobot, *, speed: int, acc: int, vel: int) -> None:
    """Apply a uniform speed/acc/vel profile to both joint and linear motion.

    Sets SpeedFactor, AccJ, AccL, VelJ, and VelL to the provided values.

    Args:
        robot: Active ``DobotRobot`` instance.
        speed: Global speed ratio for ``speed_factor()``. Range: [1, 100].
        acc: Acceleration ratio applied to both ``acc_j`` and ``acc_l``.
        vel: Velocity ratio applied to both ``vel_j`` and ``vel_l``.
    """
    robot.speed_factor(speed)
    robot.acc_j(acc)
    robot.acc_l(acc)
    robot.vel_j(vel)
    robot.vel_l(vel)
    print(f"  speed_factor={speed}  acc_j/l={acc}  vel_j/l={vel}")


def wait_for_idle(robot: DobotRobot, timeout: float = 30.0) -> bool:
    """Block until the robot finishes moving and returns to ENABLE state.

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


def swing_j1(robot: DobotRobot, label: str) -> None:
    """Move J1 forward then back by ``J1_SWING`` degrees using relative moves.

    Args:
        robot: Active ``DobotRobot`` instance.
        label: Profile name printed before each move for comparison.
    """
    qid = robot.rel_joint_mov_j(J1_SWING, 0, 0, 0, 0, 0)
    print(f"  [{label}] RelJointMovJ J1+{J1_SWING}°  →  queue_id={qid}")
    assert wait_for_idle(robot), f"[{label}] J1+ move timed out."

    qid = robot.rel_joint_mov_j(-J1_SWING, 0, 0, 0, 0, 0)
    print(f"  [{label}] RelJointMovJ J1-{J1_SWING}°  →  queue_id={qid}")
    assert wait_for_idle(robot), f"[{label}] J1- move timed out."


def main() -> None:
    """Demonstrate safe, full, and restored speed profiles with motion."""
    with DobotRobot(ROBOT_IP) as robot:
        # Clear lingering errors before enabling
        if robot.check_errors():
            still_has = robot.clear_robot_error()
            if still_has:
                print("Could not clear all errors — check robot status.")
                return

        robot.enable_robot()
        print("Robot enabled.\n")

        print("Applying conservative (safe) speed profile:")
        apply_speed_profile(robot, speed=SPEED_FACTOR_SAFE, acc=ACC_SAFE, vel=VEL_SAFE)
        swing_j1(robot, label="safe")

        print("\nApplying full-speed profile:")
        apply_speed_profile(robot, speed=100, acc=100, vel=100)
        swing_j1(robot, label="full")

        print("\nRestoring conservative profile before releasing control:")
        apply_speed_profile(robot, speed=SPEED_FACTOR_SAFE, acc=ACC_SAFE, vel=VEL_SAFE)

        robot.disable_robot()
        print("\nRobot disabled — done.")


if __name__ == "__main__":
    main()
