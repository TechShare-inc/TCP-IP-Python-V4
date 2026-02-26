#!/usr/bin/env python3
"""Basic demo — connect, enable, query status, and disconnect.

Demonstrates:
- Context-managed ``DobotRobot`` connection
- Enabling/disabling the robot
- Querying robot mode and TCP pose
- Reading typed feedback data
"""

from dobot_api_v4 import DobotRobot

ROBOT_IP = "192.168.5.1"


def main() -> None:
    with DobotRobot(ROBOT_IP) as robot:
        # Enable the robot (blocks until servo is ready)
        ack = robot.enable_robot()
        print(f"enable_robot → command_id={ack.command_id}")

        # Query current robot mode (5 = IDLE after enable)
        mode = robot.robot_mode()
        print(f"robot_mode   → {mode.value}")

        # Query current TCP pose
        pose = robot.get_pose()
        print(
            f"get_pose     → x={pose.x:.2f}, y={pose.y:.2f}, z={pose.z:.2f}, "
            f"rx={pose.rx:.2f}, ry={pose.ry:.2f}, rz={pose.rz:.2f}"
        )

        # Read one feedback packet (port 30004, 8 ms cycle)
        data = robot.feedback_data()
        if data is not None:
            print(f"feedback     → enable={data.enable_status}, "
                  f"mode={data.robot_mode}, "
                  f"q_actual={tuple(round(q, 2) for q in data.q_actual)}")

        # Disable when finished
        robot.disable_robot()
        print("Robot disabled.")


if __name__ == "__main__":
    main()
