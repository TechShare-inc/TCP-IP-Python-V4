#!/usr/bin/env python3
"""Basic demo showing DobotRobot high-level façade usage.

This example demonstrates:
- Connecting via DobotRobot (unified entry point)
- Enabling the robot
- Reading feedback data in a background thread
- Running simple motion commands
"""

import re
import threading
from time import sleep

from dobot_api_v4 import DobotRobot


class DobotDemo:
    """Simple demo wrapper around the V4 API."""

    def __init__(self, ip: str) -> None:
        self.ip = ip
        self._lock = threading.Lock()

        # Feedback snapshot values
        self.robot_mode: int = -1
        self.current_command_id: int = 0
        self.digital_inputs: int = -1
        self.digital_outputs: int = -1

    def start(self) -> None:
        """Connect, enable, and begin the feedback loop."""
        self.robot = DobotRobot(self.ip)
        dashboard = self.robot.dashboard

        result = dashboard.enable_robot()
        if self.parse_result_id(result)[0] != 0:
            print("Enable failed: Check if port 29999 is occupied")
            return
        print("Enable successful")

        feed_thread = threading.Thread(target=self._read_feedback, daemon=True)
        feed_thread.start()


        while True:
            with self._lock:
                di = self.digital_inputs
                do = self.digital_outputs
                mode = self.robot_mode
            print(f"DI: {di}  2DI: {bin(di)}  16: {hex(di)}")
            print(f"DO: {do}  2DO: {bin(do)}  16: {hex(do)}")
            print(f"robot mode: {mode}")
            sleep(2)

    def _read_feedback(self) -> None:
        """Background thread: continuously read feedback data."""
        feedback = self.robot.feedback  # lazy connect to port 30004
        while True:
            data = feedback.raw_feedback_data()
            if data is not None and hex(int(data["test_value"][0])) == "0x123456789abcdef":
                with self._lock:
                    self.robot_mode = int(data["robot_mode"][0])
                    self.digital_inputs = int(data["digital_inputs"][0])
                    self.digital_outputs = int(data["digital_outputs"][0])
                    self.current_command_id = int(data["current_command_id"][0])

    def run_point(self, point_list: list) -> None:
        """Move to a point and wait for completion."""
        result = self.robot.dashboard.mov_j(*point_list, coordinate_mode=0)
        print(f"mov_j: {result}")
        ids = self.parse_result_id(result)
        print(ids)
        current_id = ids[1]
        print(f"Command ID: {current_id}")

        while True:
            with self._lock:
                mode = self.robot_mode
                cmd_id = self.current_command_id
            if mode == 5 and cmd_id == current_id:
                print("Motion completed")
                break
            sleep(0.1)

    @staticmethod
    def parse_result_id(value_recv) -> list:
        """Parse integer values from a robot response string."""
        if "Not Tcp" in str(value_recv):
            print("Control Mode Is Not Tcp")
            return [1]
        return [int(num) for num in re.findall(r"-?\d+", str(value_recv))] or [2]

    def close(self) -> None:
        """Clean up connections."""
        self.robot.close()
