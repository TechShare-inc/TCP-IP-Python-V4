---
type: tutorial
---

# Your First Robot Program

In this tutorial, you will build a complete program that connects to a Dobot V4 robot, enables it, performs motions, monitors feedback in a background thread, and shuts down cleanly.

## Prerequisites

- The SDK is [installed](../getting-started/installation.md).
- The robot is powered on and reachable (e.g., `192.168.1.6`).

## Step 1 — Create the Connection

We use `DobotRobot` as our single entry point. The context manager ensures connections are closed even if an error occurs.

```python
from dobot_api_v4 import DobotRobot

robot = DobotRobot("192.168.1.6")
```

**Expected Output:**

> ```
> 2026-02-26 10:00:00.000 | INFO     | dobot_api_v4.base:__init__:42 - Connected to 192.168.1.6:29999
> ```

## Step 2 — Enable and Configure

```python
# Enable the robot (returns None on success)
robot.enable_robot()

# Set global speed to 30%
robot.speed_factor(30)

# Set joint acceleration and velocity
robot.acc_j(50)
robot.vel_j(50)
```

## Step 3 — Start a Feedback Thread

The feedback connection (port 30004) pushes data every 8 ms. We read it in a background thread to track the robot's state without blocking our main program.

```python
import threading
from time import sleep

current_mode = -1
current_cmd_id = 0

def read_feedback():
    global current_mode, current_cmd_id
    while True:
        data = robot.feedback_data()
        if data:
            current_mode = data.robot_mode
            current_cmd_id = data.current_command_id
        sleep(0.008)  # Match the 8 ms feedback cycle

thread = threading.Thread(target=read_feedback, daemon=True)
thread.start()

# Give it a moment to connect and receive first packet
sleep(0.5)
print(f"Robot mode: {current_mode}")
```

**Expected Output:**

> ```
> Robot mode: 5
> ```

Mode 5 means the robot is idle and ready to accept motion commands. See [Robot Modes](../reference/robot-modes.md) for all values.

## Step 4 — Move to Waypoints

Let's define three waypoints and move through them sequentially. We wait for each motion to complete by monitoring `current_command_id` from the feedback thread.

```python
waypoints = [
    (0, 30, -30, 0, 0, 0),
    (10, 20, -20, 0, 10, 0),
    (0, 0, 0, 0, 0, 0),
]

for i, wp in enumerate(waypoints):
    command_id = robot.mov_j(*wp, coordinate_mode=0)
    print(f"Waypoint {i+1}: command ID {command_id}, moving...")

    # Wait for motion to complete
    while True:
        if current_mode == 5 and current_cmd_id >= command_id:
            break
        sleep(0.1)

    print(f"Waypoint {i+1}: reached.")
```

**Expected Output:**

> ```
> Waypoint 1: command ID 5, moving...
> Waypoint 1: reached.
> Waypoint 2: command ID 6, moving...
> Waypoint 2: reached.
> Waypoint 3: command ID 7, moving...
> Waypoint 3: reached.
> ```

## Step 5 — Read Final Pose

```python
pose = robot.get_pose()
print(f"Final pose: x={pose.x:.1f}, y={pose.y:.1f}, z={pose.z:.1f}")
print(f"Orientation: rx={pose.rx:.1f}, ry={pose.ry:.1f}, rz={pose.rz:.1f}")
```

**Expected Output:**

> ```
> Final pose: x=350.0, y=0.0, z=300.0
> Orientation: rx=180.0, ry=0.0, rz=0.0
> ```

## Step 6 — Clean Up

```python
robot.close()
print("Disconnected.")
```

## Complete Program

```python
#!/usr/bin/env python3
"""First robot program — connect, move, monitor, disconnect."""

import threading
from time import sleep

from dobot_api_v4 import DobotRobot

ROBOT_IP = "192.168.1.6"

current_mode = -1
current_cmd_id = 0


def read_feedback(robot: DobotRobot) -> None:
    global current_mode, current_cmd_id
    while True:
        data = robot.feedback_data()
        if data:
            current_mode = data.robot_mode
            current_cmd_id = data.current_command_id
        sleep(0.008)


def wait_for_command(target_id: int) -> None:
    while True:
        if current_mode == 5 and current_cmd_id >= target_id:
            return
        sleep(0.1)


def main() -> None:
    with DobotRobot(ROBOT_IP) as robot:
        # Enable & configure
        robot.enable_robot()
        robot.speed_factor(30)
        robot.acc_j(50)
        robot.vel_j(50)

        # Start feedback thread
        thread = threading.Thread(target=read_feedback, args=(robot,), daemon=True)
        thread.start()
        sleep(0.5)

        # Move through waypoints
        waypoints = [
            (0, 30, -30, 0, 0, 0),
            (10, 20, -20, 0, 10, 0),
            (0, 0, 0, 0, 0, 0),
        ]
        for i, wp in enumerate(waypoints):
            command_id = robot.mov_j(*wp, coordinate_mode=0)
            print(f"Waypoint {i+1}: moving (cmd {command_id})...")
            wait_for_command(command_id)
            print(f"Waypoint {i+1}: reached.")

        # Final pose
        pose = robot.get_pose()
        print(f"Final: ({pose.x:.1f}, {pose.y:.1f}, {pose.z:.1f})")


if __name__ == "__main__":
    main()
```

## What's Next

- [Reading Real-Time Feedback](./reading-feedback.md) — deep-dive into all 65+ feedback fields
- [Error Monitoring & Alarms](./error-monitoring.md) — detect and diagnose robot errors
- [Pick-and-Place Workflow](./pick-and-place.md) — combine motion with I/O
