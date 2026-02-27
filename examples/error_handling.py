#!/usr/bin/env python3
"""Error handling demo — DobotApiError, error checking, and reconnection.

Demonstrates:
- Catching ``DobotApiError`` raised by dashboard methods
- Querying active error IDs via ``get_error_id()``
- Using ``check_errors()`` / ``clear_robot_error()`` helpers
- Saving an error log to disk
- Reconnecting after a connection loss
"""

from dobot_api_v4 import DobotApiError, DobotRobot

ROBOT_IP = "192.168.5.1"


def demo_catch_api_error(robot: DobotRobot) -> None:
    """Show how to catch and inspect a DobotApiError."""
    print("--- DobotApiError handling ---")
    try:
        # Any dashboard method may raise DobotApiError if the robot
        # returns a non-zero error code.
        robot.enable_robot()
    except DobotApiError as exc:
        print(f"  error_code : {exc.error_code}")
        print(f"  command_id : {exc.command_id}")
        print(f"  message    : {exc.message}")
        print(f"  raw        : {exc.raw}")
    else:
        print("  Robot enabled without errors.")


def demo_query_errors(robot: DobotRobot) -> None:
    """Query and display active error IDs."""
    print("\n--- Active error IDs ---")
    error_ids = robot.get_error_id()
    if error_ids:
        print(f"  {len(error_ids)} error(s): {error_ids}")
    else:
        print("  No active errors.")


def demo_check_and_clear(robot: DobotRobot) -> None:
    """Use the convenience helpers on DobotRobot."""
    print("\n--- check_errors / clear_robot_error ---")

    has_errors = robot.check_errors()
    print(f"  Errors present: {has_errors}")

    if has_errors:
        still_has = robot.clear_robot_error()
        print(f"  After clear, errors remain: {still_has}")


def demo_error_log(robot: DobotRobot) -> None:
    """Save the current error log to a JSON file."""
    print("\n--- Error log ---")
    robot.errors.save_error_log()
    print("  Error log saved (see working directory).")


def demo_reconnect(robot: DobotRobot) -> None:
    """Demonstrate reconnecting all active connections."""
    print("\n--- Reconnect ---")
    robot.reconnect()
    print("  Reconnected successfully.")

    mode = robot.robot_mode()
    print(f"  robot_mode after reconnect → {mode}")


def main() -> None:
    with DobotRobot(ROBOT_IP) as robot:
        demo_catch_api_error(robot)
        demo_query_errors(robot)
        demo_check_and_clear(robot)
        demo_error_log(robot)
        demo_reconnect(robot)

    print("\nAll error-handling demos complete.")


if __name__ == "__main__":
    main()
