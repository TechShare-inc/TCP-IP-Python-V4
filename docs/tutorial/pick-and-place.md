---
type: tutorial
---

# Pick-and-Place Workflow

In this tutorial, we will build a complete pick-and-place program that combines motion commands with digital I/O to control a gripper. This is one of the most common industrial robot workflows.

## Prerequisites

- The SDK is [installed](../getting-started/installation.md).
- The robot is powered on and connected.
- A gripper is connected to Digital Output index 1 (DO1): HIGH = close, LOW = open.

## Workflow Overview

```
1. Home position
2. Move above pick location
3. Descend to pick height
4. Close gripper (DO1 = HIGH)
5. Lift to safe height
6. Move above place location
7. Descend to place height
8. Open gripper (DO1 = LOW)
9. Lift to safe height
10. Return home
```

## Step 1 — Define Positions

```python
# All positions in Cartesian coordinates (x, y, z, rx, ry, rz)
HOME       = (350.0,   0.0, 300.0, 180.0, 0.0, 0.0)
PICK_ABOVE = (400.0, 100.0, 200.0, 180.0, 0.0, 0.0)
PICK_DOWN  = (400.0, 100.0,  50.0, 180.0, 0.0, 0.0)
PLACE_ABOVE= (400.0,-100.0, 200.0, 180.0, 0.0, 0.0)
PLACE_DOWN = (400.0,-100.0,  50.0, 180.0, 0.0, 0.0)

GRIPPER_DO = 1    # Digital output index for the gripper
COORD_MODE = 1    # 1 = Cartesian coordinate mode
```

## Step 2 — Helper Functions

```python
import threading
from time import sleep

from dobot_api_v4 import DobotRobot

current_mode = -1
current_cmd_id = 0

def start_feedback(robot: DobotRobot) -> None:
    """Start a background feedback thread."""
    global current_mode, current_cmd_id

    def loop():
        global current_mode, current_cmd_id
        while True:
            data = robot.feedback_data()
            if data:
                current_mode = data.robot_mode
                current_cmd_id = data.current_command_id
            sleep(0.008)

    threading.Thread(target=loop, daemon=True).start()
    sleep(0.5)  # Wait for first data


def wait_arrive(cmd_id: int) -> None:
    """Block until the robot reports completion of the given command."""
    while True:
        if current_mode == 5 and current_cmd_id >= cmd_id:
            return
        sleep(0.05)


def move_and_wait(robot: DobotRobot, pos: tuple) -> None:
    """Move to a Cartesian position and wait for arrival."""
    result = robot.dashboard.mov_l(*pos, coordinate_mode=COORD_MODE)
    # Parse the command ID from the raw response
    import re
    ids = [int(n) for n in re.findall(r"-?\d+", str(result))]
    if len(ids) >= 2:
        wait_arrive(ids[1])


def gripper(robot: DobotRobot, close: bool) -> None:
    """Control the gripper via digital output."""
    robot.dashboard.do_output(GRIPPER_DO, int(close))
    sleep(0.5)  # Wait for gripper to actuate
```

## Step 3 — Main Pick-and-Place Routine

```python
def pick_and_place(robot: DobotRobot) -> None:
    """Execute one pick-and-place cycle."""

    print("Moving to home...")
    move_and_wait(robot, HOME)

    # --- Pick ---
    print("Approaching pick location...")
    move_and_wait(robot, PICK_ABOVE)

    print("Descending to pick...")
    move_and_wait(robot, PICK_DOWN)

    print("Closing gripper...")
    gripper(robot, close=True)

    print("Lifting with part...")
    move_and_wait(robot, PICK_ABOVE)

    # --- Place ---
    print("Moving to place location...")
    move_and_wait(robot, PLACE_ABOVE)

    print("Descending to place...")
    move_and_wait(robot, PLACE_DOWN)

    print("Opening gripper...")
    gripper(robot, close=False)

    print("Lifting...")
    move_and_wait(robot, PLACE_ABOVE)

    # --- Home ---
    print("Returning home...")
    move_and_wait(robot, HOME)

    print("Cycle complete!")
```

## Step 4 — Run the Program

```python
def main() -> None:
    with DobotRobot("192.168.1.6") as robot:
        robot.enable_robot()
        robot.speed_factor(30)

        start_feedback(robot)

        # Open gripper initially
        gripper(robot, close=False)

        # Run 3 cycles
        for i in range(3):
            print(f"\n=== Cycle {i + 1} ===")
            pick_and_place(robot)

        print("\nAll cycles complete.")


if __name__ == "__main__":
    main()
```

**Expected Output:**

> ```
> === Cycle 1 ===
> Moving to home...
> Approaching pick location...
> Descending to pick...
> Closing gripper...
> Lifting with part...
> Moving to place location...
> Descending to place...
> Opening gripper...
> Lifting...
> Returning home...
> Cycle complete!
>
> === Cycle 2 ===
> ...
> ```

## Variations

### Using MovJ Instead of MovL

Replace `mov_l` with `mov_j` for joint-interpolated motion (faster for large moves but non-linear path):

```python
result = robot.dashboard.mov_j(*pos, coordinate_mode=COORD_MODE)
```

### Using User Coordinate System

Set up a user coordinate system aligned to the work surface:

```python
# Define user coordinate (origin at pick station)
robot.dashboard.set_user(1, 400, 100, 0, 0, 0, 0)
robot.dashboard.user(1)
```

Then use positions relative to that coordinate system.

## What's Next

- [How to Use Digital & Analog I/O](../how-to/use-digital-analog-io.md) — detailed I/O guide
- [How to Configure Speed & Coordinates](../how-to/configure-speed-and-coords.md) — tuning motion parameters
- [Relative Motion](../how-to/relative-motion.md) — move in tool or user frame
