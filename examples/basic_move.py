#!/usr/bin/env python3
"""Basic motion demo — MovJ/MovL with feedback-based completion wait.

Demonstrates:
- Reading the current joint state via feedback
- Computing waypoints as small offsets from the current pose
- Joint (MovJ) and linear (MovL) motion commands
- Polling feedback to detect motion completion
- Using typed ``AckResponse`` return values
"""

import time

from dobot_api_v4 import DobotRobot

ROBOT_IP = "192.168.5.1"

# J1 offset in degrees for the small movements
J1_OFFSET = 5.0


def wait_for_command(robot: DobotRobot, command_id: int = 0, timeout: float = 30.0) -> bool:
    """Block until the robot finishes the current motion.

    Waits for the robot to enter a running state (RUNNING=7 or
    SINGLE_MOVE=8), then waits for it to return to ENABLE/idle (5).
    Returns ``False`` immediately if the robot enters ERROR (9).

    Args:
        robot: Active ``DobotRobot`` instance.
        command_id: Unused — kept for call-site compatibility.
        timeout: Maximum seconds to wait before giving up.

    Returns:
        ``True`` if the motion completed, ``False`` on timeout or error.
    """
    deadline = time.monotonic() + timeout
    saw_running = False
    while time.monotonic() < deadline:
        data = robot.feedback_data()
        if data is not None:
            mode = data.robot_mode
            if mode in (7, 8):          # RUNNING / SINGLE_MOVE
                saw_running = True
            elif saw_running and mode == 5:  # back to ENABLE (idle)
                return True
            elif mode == 9:             # ERROR
                print(f"Robot entered ERROR state (mode=9)")
                return False
        time.sleep(0.05)
    return False


def main() -> None:
    with DobotRobot(ROBOT_IP) as robot:
        # -- Check and clear errors before starting ------------------------
        if robot.check_errors():
            print("Errors detected — clearing...")
            still_has_errors = robot.clear_robot_error()
            if still_has_errors:
                print("ERROR: Could not clear all errors. Aborting.")
                return
            print("Errors cleared.")

        # -- Disable then enable for a clean start -------------------------
        robot.disable_robot()
        print("Robot disabled (clean start).")
        time.sleep(1)

        robot.enable_robot()
        print("Robot enabled.")

        # Configure speed / acceleration
        robot.speed_factor(10)
        robot.acc_j(10)
        robot.vel_j(10)
        print("Speed factor=10, AccJ=10, VelJ=10")

        # -- Read current joint state --------------------------------------
        data = robot.feedback_data()
        assert data is not None, "Failed to read feedback data"
        current_joints = data.q_actual  # tuple of 6 floats (degrees)
        j1, j2, j3, j4, j5, j6 = current_joints
        print(f"Current joints: J1={j1:.2f}, J2={j2:.2f}, J3={j3:.2f}, "
              f"J4={j4:.2f}, J5={j5:.2f}, J6={j6:.2f}")

        # -- MovJ: offset J1 by +J1_OFFSET degrees -------------------------
        ack = robot.mov_j(j1 + J1_OFFSET, j2, j3, j4, j5, j6,
                          coordinate_mode=1)
        print(f"MovJ → J1+{J1_OFFSET}°  (cmd={ack.command_id})")
        assert wait_for_command(robot, ack.command_id), "Timeout waiting for J1+"

        # -- MovJ: offset J1 by -J1_OFFSET degrees -------------------------
        ack = robot.mov_j(j1 - J1_OFFSET, j2, j3, j4, j5, j6,
                          coordinate_mode=1)
        print(f"MovJ → J1-{J1_OFFSET}°  (cmd={ack.command_id})")
        assert wait_for_command(robot, ack.command_id), "Timeout waiting for J1-"

        # -- Return to original pose ----------------------------------------
        ack = robot.mov_j(j1, j2, j3, j4, j5, j6, coordinate_mode=1)
        print(f"MovJ → original  (cmd={ack.command_id})")
        assert wait_for_command(robot, ack.command_id), "Timeout waiting for home"

        robot.disable_robot()
        print("Motion sequence complete. Robot disabled.")


if __name__ == "__main__":
    main()
