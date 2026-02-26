---
type: how-to
---

# How to Perform Relative Motions

Relative motion commands move the robot by an offset from its current position, rather than to an absolute target. Three reference frames are available: tool, user, and joint.

## Relative Motion in Tool Frame

Move relative to the current tool (end-effector) orientation:

```python
dashboard = robot.dashboard

# Joint-interpolated relative motion in tool frame
dashboard.rel_mov_j_tool(
    10, 0, 0, 0, 0, 0,    # Offset: 10 mm along tool X-axis
    user=0, tool=0,
)

# Linear relative motion in tool frame
dashboard.rel_mov_l_tool(
    0, 0, -50, 0, 0, 0,   # Offset: 50 mm downward in tool Z
    user=0, tool=0,
)
```

## Relative Motion in User Frame

Move relative to the current position expressed in a user coordinate system:

```python
# Joint-interpolated relative motion in user frame
dashboard.rel_mov_j_user(
    0, 100, 0, 0, 0, 0,   # Offset: 100 mm along user Y-axis
    user=0, tool=0,
)

# Linear relative motion in user frame
dashboard.rel_mov_l_user(
    50, 0, 0, 0, 0, 0,    # Offset: 50 mm along user X-axis
    user=0, tool=0,
)
```

## Relative Joint Motion

Move joints by angular offsets:

```python
# Move J1 by +10° and J2 by -5° from current position
dashboard.rel_joint_mov_j(
    10, -5, 0, 0, 0, 0,
)
```

## Relative Point Commands

These commands specify an offset and return the calculated target point:

```python
# Calculate target point from tool-frame offset
result = dashboard.rel_point_tool(10, 0, 0, 0, 0, 0, user=0, tool=0)

# Calculate target point from user-frame offset
result = dashboard.rel_point_user(0, 50, 0, 0, 0, 0, user=0, tool=0)

# Calculate target point from joint offset
result = dashboard.rel_joint(5, 0, 0, 0, 0, 0)
```

## Practical Example: Grid Pattern

Trace a 3×3 grid using relative motions in the user frame:

```python
from dobot_api_v4 import DobotRobot
from time import sleep

STEP_X = 50   # mm between grid points in X
STEP_Y = 50   # mm between grid points in Y

with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()
    robot.speed_factor(30)
    dashboard = robot.dashboard

    # Move to starting corner
    dashboard.mov_l(300, -50, 200, 180, 0, 0, coordinate_mode=1)
    sleep(2)

    for row in range(3):
        for col in range(3):
            print(f"Grid point ({row}, {col})")
            sleep(1)

            if col < 2:
                # Move right along X
                dashboard.rel_mov_l_user(STEP_X, 0, 0, 0, 0, 0, user=0, tool=0)
                sleep(1.5)

        if row < 2:
            # Move to next row: back to start of row, then forward in Y
            dashboard.rel_mov_l_user(-STEP_X * 2, STEP_Y, 0, 0, 0, 0, user=0, tool=0)
            sleep(1.5)
```

::: tip
Relative motions are especially useful when the absolute position is unknown or when working with a calibrated user coordinate system.
:::
