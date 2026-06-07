#!/usr/bin/env python3
"""Power-cycle and enable/disable example.

Demonstrates a full startup sequence: check for errors, clear them if
present, power on the robot, wait for readiness, enable, read the robot
status, and finally disable.  This is the pattern you would use at the
start of any production script to ensure the robot is in a known-good
state before commanding motion.

Difficulty: Intermediate
Prerequisites: 04_error_handling.py; robot reachable and powered off or idle
"""

from __future__ import annotations

import time

from dobot_api_v4 import DobotRobot

ROBOT_IP = "192.168.5.1"

# Seconds to wait after power_on before attempting to enable
POWER_ON_WAIT: float = 20.0

# robot_mode() return values used in this example
_MODE_DISABLED: int = 4
_MODE_ENABLE: int = 5
_MODE_ERROR: int = 9


def check_and_clear_errors(robot: DobotRobot) -> None:
    """Check for active errors and clear them if any are present.

    Args:
        robot: Active ``DobotRobot`` instance.

    Raises:
        RuntimeError: If errors could not be fully cleared.
    """
    print("Checking for active errors …")
    has_errors = robot.check_errors()

    if not has_errors:
        print("  No errors found -- robot is clean.")
        return

    error_ids = robot.get_error_id()
    print(f"  Found error(s): {error_ids}")
    print("  Clearing errors …")
    still_has = robot.clear_robot_error()

    if still_has:
        raise RuntimeError(
            "Errors remain after clearing -- inspect the robot and resolve "
            "hardware issues before retrying."
        )
    print("  All errors cleared successfully.")


def power_on_and_wait(robot: DobotRobot, wait: float = POWER_ON_WAIT) -> None:
    """Power on the robot and wait for it to become ready.

    Args:
        robot: Active ``DobotRobot`` instance.
        wait: Seconds to wait after issuing the power-on command.
    """
    print(f"Powering on (waiting {wait:.0f} s for hardware init) …")
    robot.power_on()
    time.sleep(wait)

    mode = robot.robot_mode()
    print(f"  robot_mode after power-on: {mode}")

    if mode == _MODE_ERROR:
        raise RuntimeError("Robot entered ERROR state after power-on.")


def enable_and_read_status(robot: DobotRobot) -> None:
    """Enable the robot, print its status, then disable it.

    Args:
        robot: Active ``DobotRobot`` instance.
    """
    print("Enabling robot …")
    robot.enable_robot()
    mode = robot.robot_mode()
    print(f"  robot_mode after enable: {mode}")

    if mode == _MODE_ENABLE:
        print("  Robot is ENABLED and ready for motion commands.")
    else:
        print(f"  Unexpected mode {mode} -- expected {_MODE_ENABLE} (ENABLE).")

    print("Disabling robot …")
    robot.disable_robot()
    mode = robot.robot_mode()
    print(f"  robot_mode after disable: {mode}")
    print("  Robot disabled successfully.")


def main() -> None:
    """Run the full power-cycle sequence."""
    with DobotRobot(ROBOT_IP) as robot:
        # Step 1 & 2: Check errors and clear if needed
        check_and_clear_errors(robot)

        # Step 3: Power on and wait for hardware to initialise
        power_on_and_wait(robot)

        # Step 4: Enable -> read status -> disable
        enable_and_read_status(robot)

    print("\nPower-cycle sequence complete.")


if __name__ == "__main__":
    main()
