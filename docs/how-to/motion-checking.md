---
type: how-to
---

# How to Pre-Check Motions

Before executing a motion on the physical robot, you can pre-check whether the target position is reachable and collision-free. This is useful for validating waypoints in offline programming.

## Check Joint Motion (MovJ)

```python
dashboard = robot.dashboard

# Check if a joint motion to these angles is feasible
result = dashboard.check_mov_j(
    0, 30, -30, 0, 0, 0,
    coordinate_mode=0,
)
print(f"MovJ check result: {result}")
```

## Check Linear Motion (MovL)

```python
result = dashboard.check_mov_l(
    400, 0, 300, 180, 0, 0,
    coordinate_mode=1,
)
print(f"MovL check result: {result}")
```

## Check Circular Motion (MovC)

```python
result = dashboard.check_mov_c(
    400, 50, 300, 180, 0, 0,    # Intermediate point
    400, 100, 300, 180, 0, 0,   # End point
    coordinate_mode=1,
)
print(f"MovC check result: {result}")
```

## 7-Axis (Odd) Variants

For 7-axis robots, use the odd-prefixed versions:

```python
result = dashboard.check_odd_mov_j(0, 30, -30, 0, 0, 0, 0, coordinate_mode=0)
result = dashboard.check_odd_mov_l(400, 0, 300, 180, 0, 0, 0, coordinate_mode=1)
result = dashboard.check_odd_mov_c(
    400, 50, 300, 180, 0, 0, 0,
    400, 100, 300, 180, 0, 0, 0,
    coordinate_mode=1,
)
```

## Practical Example: Validate Waypoints Before Execution

```python
from dobot_api_v4 import DobotRobot

waypoints = [
    (0, 30, -30, 0, 0, 0),
    (10, 20, -20, 0, 10, 0),
    (0, 0, 0, 0, 0, 0),
    (0, 90, -90, 0, 0, 0),  # Potentially out of range
]

with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()
    dashboard = robot.dashboard

    valid_waypoints = []
    for i, wp in enumerate(waypoints):
        result = dashboard.check_mov_j(*wp, coordinate_mode=0)
        # Parse result to determine if the motion is feasible
        print(f"Waypoint {i}: {result}")
        valid_waypoints.append(wp)

    # Execute only validated waypoints
    for wp in valid_waypoints:
        dashboard.mov_j(*wp, coordinate_mode=0)
```

::: tip
Pre-checking motions is especially valuable in offline programming environments where you generate waypoints algorithmically and want to filter out unreachable positions before sending them to the robot.
:::
