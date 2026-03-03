#!/usr/bin/env python3
"""Connect and query example.

Opens a connection to the robot inside a context manager, queries the
current robot mode and TCP pose, then disconnects cleanly.  No motion is
commanded — this is the simplest possible interaction with the robot.

Difficulty: Beginner
Prerequisites: dobot_api_v4 installed; robot reachable at ROBOT_IP

See also:
- docs/tutorial/first-program.md
- docs/getting-started/quick-start.md
"""

from __future__ import annotations

from dobot_api_v4 import DobotRobot, Pose

ROBOT_IP = "192.168.5.1"


def print_pose(label: str, pose: Pose) -> None:
    """Print a labelled Pose on one line.

    Args:
        label: Short description printed before the values.
        pose: The 6-DOF pose to display.
    """
    print(
        f"{label}: x={pose.x:.2f}  y={pose.y:.2f}  z={pose.z:.2f}  "
        f"rx={pose.rx:.2f}  ry={pose.ry:.2f}  rz={pose.rz:.2f}"
    )


def main() -> None:
    """Connect, query robot mode and pose, then disconnect."""
    with DobotRobot(ROBOT_IP) as robot:
        # Robot mode integer codes:
        #   1=INIT  4=DISABLED  5=ENABLE  7=RUNNING  9=ERROR
        mode = robot.robot_mode()
        print(f"robot_mode   → {mode}")

        # TCP position in the active user coordinate system
        tcp_pose = robot.get_pose()
        print_pose("TCP pose  ", tcp_pose)

        # Joint angles (degrees)
        joint_pose = robot.get_angle()
        print_pose("Joint pos ", joint_pose)


if __name__ == "__main__":
    main()
