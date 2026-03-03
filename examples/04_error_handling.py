#!/usr/bin/env python3
"""Error handling and recovery example.

Demonstrates how to detect, inspect, and recover from robot errors using
``DobotRobot`` convenience helpers and the ``DobotApiError`` exception.
Also shows how to save a timestamped JSON error log to the working directory.

Difficulty: Intermediate
Prerequisites: 03_basic_motion.py

See also:
- docs/how-to/error-handling-reconnect.md
- docs/tutorial/error-monitoring.md
"""

from __future__ import annotations

from dobot_api_v4 import DobotApiError, DobotRobot

ROBOT_IP = "192.168.5.1"


def demo_api_error(robot: DobotRobot) -> None:
    """Catch and inspect a ``DobotApiError`` from ``enable_robot``."""
    print("--- DobotApiError ---")
    try:
        robot.enable_robot()
    except DobotApiError as exc:
        print(f"  error_code : {exc.error_code}")
        print(f"  command_id : {exc.command_id}")
        print(f"  message    : {exc.message}")
        print(f"  raw        : {exc.raw}")
    else:
        print("  enable_robot() succeeded — robot is now enabled.")


def demo_error_ids(robot: DobotRobot) -> None:
    """Query active alarm IDs directly from the dashboard."""
    print("\n--- Active error IDs ---")
    ids = robot.get_error_id()
    if ids:
        print(f"  {len(ids)} active error(s): {ids}")
    else:
        print("  No active errors.")


def demo_check_and_clear(robot: DobotRobot) -> None:
    """Use the high-level check / clear helpers on ``DobotRobot``."""
    print("\n--- check_errors / clear_robot_error ---")
    has_errors = robot.check_errors()
    print(f"  Errors present       : {has_errors}")
    if has_errors:
        still_has = robot.clear_robot_error()
        print(f"  Errors after clear   : {still_has}")


def demo_save_log(robot: DobotRobot) -> None:
    """Save a JSON error log to the working directory."""
    print("\n--- Save error log ---")
    # Defaults to a timestamped filename, e.g. robot_errors_20260303_123456.json
    robot.errors.save_error_log(language="en")
    print("  Error log saved to working directory.")


def demo_reconnect(robot: DobotRobot) -> None:
    """Reconnect all active connections and confirm robot is reachable."""
    print("\n--- Reconnect ---")
    robot.reconnect()
    mode = robot.robot_mode()
    print(f"  robot_mode after reconnect: {mode}")


def main() -> None:
    """Run all error-handling demonstrations in sequence."""
    with DobotRobot(ROBOT_IP) as robot:
        demo_api_error(robot)
        demo_error_ids(robot)
        demo_check_and_clear(robot)
        demo_save_log(robot)
        demo_reconnect(robot)

    print("\nAll error-handling demos complete.")


if __name__ == "__main__":
    main()
