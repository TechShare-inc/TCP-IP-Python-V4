#!/usr/bin/env python3
"""Basic motion demo — MovJ/MovL with feedback-based completion wait.

Demonstrates:
- Setting speed and acceleration parameters
- Joint (MovJ) and linear (MovL) motion commands
- Polling feedback to detect motion completion
- Using typed ``AckResponse`` return values
"""

import time

from dobot_api_v4 import DobotRobot

ROBOT_IP = "192.168.5.1"

# -- Define target waypoints (joint coords, 6-DOF) -------------------------
POINT_A = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
POINT_B = (10.0, -5.0, 10.0, 0.0, 0.0, 0.0)
POINT_C = (-10.0, 5.0, -10.0, 0.0, 0.0, 0.0)


def wait_for_command(robot: DobotRobot, command_id: int, timeout: float = 30.0) -> bool:
    """Block until the robot finishes executing *command_id*.

    Polls ``feedback_data()`` and checks ``current_command_id`` against the
    target while the robot is in IDLE mode (``robot_mode == 5``).

    Args:
        robot: Active ``DobotRobot`` instance.
        command_id: The ``command_id`` returned by a motion command.
        timeout: Maximum seconds to wait before giving up.

    Returns:
        ``True`` if the command completed, ``False`` on timeout.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        data = robot.feedback_data()
        if data is not None:
            if data.robot_mode == 5 and data.current_command_id == command_id:
                return True
        time.sleep(0.05)
    return False


def main() -> None:
    with DobotRobot(ROBOT_IP) as robot:
        robot.enable_robot()
        print("Robot enabled.")

        # Configure speed / acceleration
        robot.speed_factor(50)
        robot.acc_j(50)
        robot.vel_j(50)
        print("Speed factor=50, AccJ=50, VelJ=50")

        # -- Joint motion (MovJ) -------------------------------------------
        ack = robot.mov_j(*POINT_A, coordinate_mode=0)
        print(f"MovJ → POINT_A  (cmd={ack.command_id})")
        assert wait_for_command(robot, ack.command_id), "Timeout waiting for POINT_A"

        ack = robot.mov_j(*POINT_B, coordinate_mode=0)
        print(f"MovJ → POINT_B  (cmd={ack.command_id})")
        assert wait_for_command(robot, ack.command_id), "Timeout waiting for POINT_B"

        # -- Linear motion (MovL) ------------------------------------------
        robot.acc_l(50)
        robot.vel_l(50)
        ack = robot.mov_l(*POINT_C, coordinate_mode=0)
        print(f"MovL → POINT_C  (cmd={ack.command_id})")
        assert wait_for_command(robot, ack.command_id), "Timeout waiting for POINT_C"

        # Return to home
        ack = robot.mov_j(*POINT_A, coordinate_mode=0)
        print(f"MovJ → POINT_A  (cmd={ack.command_id})")
        assert wait_for_command(robot, ack.command_id), "Timeout waiting for home"

        robot.disable_robot()
        print("Motion sequence complete. Robot disabled.")


if __name__ == "__main__":
    main()
