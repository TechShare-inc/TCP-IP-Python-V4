---
type: tutorial
---

# Quick Start

In this tutorial, we will connect to a Dobot V4 robot, enable it, read its pose, and perform a simple motion.

## Prerequisites

- The SDK is [installed](./installation.md).
- The robot controller is powered on and reachable at its IP address (e.g., `192.168.1.6`).
- Port 29999 is not occupied by another client.

## Step 1 — Connect to the Robot

```python
from dobot_api_v4 import DobotRobot

robot = DobotRobot("192.168.1.6")
```

This creates a TCP connection to port 29999 (dashboard) and an HTTP connection to port 22000 (error monitor). Feedback connections are created lazily when first accessed.

**Expected Output:**

> ```
> 2026-02-26 10:00:00.000 | INFO     | dobot_api_v4.base:__init__:42 - Connected to 192.168.1.6:29999
> ```

## Step 2 — Enable the Robot

```python
result = robot.enable_robot()
print(result)
```

**Expected Output:**

> ```
> AckResponse(command_id=1)
> ```

## Step 3 — Set Speed and Read Pose

```python
robot.speed_factor(50)  # 50% global speed

pose = robot.get_pose()
print(f"x={pose.x:.2f}, y={pose.y:.2f}, z={pose.z:.2f}")
print(f"rx={pose.rx:.2f}, ry={pose.ry:.2f}, rz={pose.rz:.2f}")
```

**Expected Output:**

> ```
> x=350.00, y=0.00, z=300.00
> rx=180.00, ry=0.00, rz=0.00
> ```

The actual values depend on your robot's current position.

## Step 4 — Move the Robot

```python
# Joint motion to a target position (joint coordinates, coordinate_mode=0)
result = robot.mov_j(0, 30, -30, 0, 0, 0, coordinate_mode=0)
print(f"Motion started, command ID: {result.command_id}")
```

**Expected Output:**

> ```
> Motion started, command ID: 2
> ```

## Step 5 — Read Feedback Data

```python
data = robot.feedback_data()
if data:
    print(f"Robot mode: {data.robot_mode}")
    print(f"Joint angles: {data.q_actual}")
    print(f"TCP position: {data.tool_vector_actual}")
```

**Expected Output:**

> ```
> Robot mode: 5
> Joint angles: (0.0, 30.0, -30.0, 0.0, 0.0, 0.0)
> TCP position: (350.0, 0.0, 250.0, 180.0, 0.0, 0.0)
> ```

## Step 6 — Close the Connection

```python
robot.close()
```

## Complete Example

Here is the full program using a context manager for automatic cleanup:

```python
from dobot_api_v4 import DobotRobot

with DobotRobot("192.168.1.6") as robot:
    # Enable
    robot.enable_robot()
    robot.speed_factor(50)

    # Read pose
    pose = robot.get_pose()
    print(f"Current pose: ({pose.x:.1f}, {pose.y:.1f}, {pose.z:.1f})")

    # Move
    result = robot.mov_j(0, 30, -30, 0, 0, 0, coordinate_mode=0)
    print(f"Motion command ID: {result.command_id}")

    # Read feedback
    data = robot.feedback_data()
    if data:
        print(f"Robot mode: {data.robot_mode}")
```

## What's Next

- [Your First Robot Program](../tutorial/first-program.md) — a more complete tutorial with threaded feedback
- [Architecture Overview](./architecture.md) — understand the connection model and layered design
- [API Reference](../reference/) — browse all available commands
