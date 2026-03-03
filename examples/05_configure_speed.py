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

from dobot_api_v4 import DobotRobot

ROBOT_IP = "192.168.5.1"

# Conservative defaults — safe for first-time users (all unit: %)
SPEED_FACTOR_SAFE: int = 30
ACC_SAFE: int = 30
VEL_SAFE: int = 30


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


def main() -> None:
    """Demonstrate safe, full, and restored speed profiles."""
    with DobotRobot(ROBOT_IP) as robot:
        print("Applying conservative (safe) speed profile:")
        apply_speed_profile(robot, speed=SPEED_FACTOR_SAFE, acc=ACC_SAFE, vel=VEL_SAFE)

        # Motion commands would go here — they will run at 30 % speed.

        print("\nApplying full-speed profile:")
        apply_speed_profile(robot, speed=100, acc=100, vel=100)

        # Motion commands at full speed would go here.

        print("\nRestoring conservative profile before releasing control:")
        apply_speed_profile(robot, speed=SPEED_FACTOR_SAFE, acc=ACC_SAFE, vel=VEL_SAFE)


if __name__ == "__main__":
    main()
