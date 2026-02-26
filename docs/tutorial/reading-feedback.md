---
type: tutorial
---

# Reading Real-Time Feedback

In this tutorial, you will learn how to read and interpret the real-time feedback data streamed by the Dobot V4 controller. The feedback system provides 65+ fields covering joint angles, TCP pose, forces, temperatures, I/O states, and more.

## Prerequisites

- The SDK is [installed](../getting-started/installation.md).
- The robot is powered on and connected.

## Step 1 — Understand the Feedback Ports

The robot streams binary data on three ports:

| Port  | Cycle Time | Use Case                        |
| ----- | ---------- | ------------------------------- |
| 30004 | 8 ms       | High-frequency control loops    |
| 30005 | 200 ms     | General monitoring              |
| 30006 | Configurable | Custom applications           |

Each packet is 1440 bytes, containing all robot state information.

## Step 2 — Read Feedback as a Typed Dataclass

The simplest approach uses `DobotRobot.feedback_data()`, which returns a `FeedbackData` dataclass:

```python
from dobot_api_v4 import DobotRobot

with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()

    data = robot.feedback_data()
    if data:
        print(f"Robot mode:      {data.robot_mode}")
        print(f"Joint angles:    {data.q_actual}")
        print(f"TCP position:    {data.tool_vector_actual}")
        print(f"Joint currents:  {data.i_actual}")
        print(f"Motor temps:     {data.motor_temperatures}")
        print(f"Speed scaling:   {data.speed_scaling}")
        print(f"Enable status:   {data.enable_status}")
        print(f"Error status:    {data.error_status}")
```

**Expected Output:**

> ```
> Robot mode:      5
> Joint angles:    (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
> TCP position:    (350.0, 0.0, 300.0, 180.0, 0.0, 0.0)
> Joint currents:  (0.1, 0.2, 0.15, 0.05, 0.05, 0.02)
> Motor temps:     (25.0, 26.0, 25.5, 24.0, 24.5, 23.0)
> Speed scaling:   50.0
> Enable status:   1
> Error status:    0
> ```

## Step 3 — Read Raw Numpy Data

For performance-critical applications, use `raw_feedback_data()` which returns a numpy structured array without the overhead of creating a dataclass:

```python
import numpy as np
from dobot_api_v4 import DobotRobot

with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()

    raw = robot.raw_feedback_data()
    if raw is not None:
        # Access fields by name from the structured array
        mode = int(raw["robot_mode"][0])
        joints = raw["q_actual"][0]
        tcp = raw["tool_vector_actual"][0]

        print(f"Mode: {mode}")
        print(f"J1={joints[0]:.2f}, J2={joints[1]:.2f}, J3={joints[2]:.2f}")
        print(f"X={tcp[0]:.2f}, Y={tcp[1]:.2f}, Z={tcp[2]:.2f}")
```

**Expected Output:**

> ```
> Mode: 5
> J1=0.00, J2=0.00, J3=0.00
> X=350.00, Y=0.00, Z=300.00
> ```

## Step 4 — Continuous Feedback Loop

In a real application, you typically read feedback in a loop. Here is a pattern using a background thread with a shared lock:

```python
import threading
from time import sleep

from dobot_api_v4 import DobotRobot, FeedbackData

robot = DobotRobot("192.168.1.6")
robot.enable_robot()

latest_data: FeedbackData | None = None
lock = threading.Lock()


def feedback_loop() -> None:
    global latest_data
    while True:
        data = robot.feedback_data()
        if data:
            with lock:
                latest_data = data
        sleep(0.008)


thread = threading.Thread(target=feedback_loop, daemon=True)
thread.start()

# Main loop: use feedback data
try:
    for _ in range(10):
        with lock:
            snapshot = latest_data
        if snapshot:
            print(
                f"Mode={snapshot.robot_mode}  "
                f"Pos=({snapshot.tool_vector_actual[0]:.1f}, "
                f"{snapshot.tool_vector_actual[1]:.1f}, "
                f"{snapshot.tool_vector_actual[2]:.1f})  "
                f"CmdID={snapshot.current_command_id}"
            )
        sleep(1)
finally:
    robot.close()
```

## Step 5 — Use Different Feedback Ports

Access the 200 ms or configurable feedback ports via properties:

```python
with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()

    # 200 ms cycle (port 30005) — good for UI updates
    data_200ms = robot.feedback_30005.feedback_data()

    # Configurable cycle (port 30006)
    data_config = robot.feedback_30006.feedback_data()
```

::: tip
Feedback connections are created **lazily** — no socket is opened until you first access the property. This saves resources when you only need the dashboard connection.
:::

## Key Feedback Fields

| Field                  | Type              | Description                          |
| ---------------------- | ----------------- | ------------------------------------ |
| `robot_mode`           | `int`             | Current mode (5 = idle, 7 = running) |
| `q_actual`             | `tuple[float, ...]` | Actual joint angles (degrees)      |
| `tool_vector_actual`   | `tuple[float, ...]` | Actual TCP pose (x, y, z, rx, ry, rz) |
| `motor_temperatures`   | `tuple[float, ...]` | Motor temperatures (°C)            |
| `digital_inputs`       | `int`             | Digital input bitmask                |
| `digital_outputs`      | `int`             | Digital output bitmask               |
| `current_command_id`   | `int`             | ID of latest completed command       |
| `enable_status`        | `int`             | 1 = enabled, 0 = disabled           |
| `error_status`         | `int`             | 1 = error present, 0 = no error     |
| `collision_state`      | `int`             | 1 = collision detected               |
| `six_force_value`      | `tuple[float, ...]` | Force/torque sensor values (N/Nm) |

For the complete list of all 65+ fields, see the [Feedback Fields Reference](../reference/feedback-fields.md).

## What's Next

- [Error Monitoring & Alarms](./error-monitoring.md) — detect and diagnose errors
- [Your First Robot Program](./first-program.md) — combine feedback with motion
- [Feedback Fields Reference](../reference/feedback-fields.md) — all fields documented
