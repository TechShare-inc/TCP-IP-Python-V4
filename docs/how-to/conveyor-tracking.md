---
type: how-to
---

# How to Track Conveyor Objects

Conveyor tracking allows the robot to follow objects on a moving conveyor belt and perform pick operations while the conveyor is running.

## Prerequisites

- An encoder is connected to the robot controller for conveyor position tracking.
- The conveyor coordinate system has been calibrated.

## Initialize Conveyor Tracking

```python
dashboard = robot.dashboard

# Initialize conveyor tracking
# Parameters depend on your conveyor configuration
dashboard.cnv_init()
```

## Start Synchronized Conveyor Tracking

```python
dashboard.start_sync_cnv()
```

## Move Along Conveyor (Linear)

```python
# Linear motion synchronized with conveyor
dashboard.cnv_mov_l(400, 100, 50, 180, 0, 0)
```

## Move Along Conveyor (Circular)

```python
# Circular motion synchronized with conveyor
dashboard.cnv_mov_c(
    400, 100, 50, 180, 0, 0,    # Intermediate point
    400, 200, 50, 180, 0, 0,    # End point
)
```

## Get Conveyor Object Position

```python
result = dashboard.get_cnv_object()
print(f"Object position: {result}")
```

## Set Point Offset

```python
dashboard.set_cnv_point_offset(10, 5, 0)  # X, Y, Z offset in mm
```

## Set Time Compensation

```python
dashboard.set_cnv_time_compensation(0.05)  # Time compensation in seconds
```

## Stop Synchronized Tracking

```python
dashboard.stop_sync_cnv()
```

## Practical Example: Conveyor Pick

```python
from dobot_api_v4 import DobotRobot
from time import sleep

with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()
    robot.speed_factor(50)
    dashboard = robot.dashboard

    # Initialize conveyor
    dashboard.cnv_init()

    # Start synchronization
    dashboard.start_sync_cnv()

    # Wait for object detection (application-specific)
    sleep(1)

    # Get object position
    obj_pos = dashboard.get_cnv_object()

    # Move to object with conveyor sync
    dashboard.cnv_mov_l(400, 100, 50, 180, 0, 0)

    # Pick (close gripper)
    dashboard.do_output(1, 1)
    sleep(0.3)

    # Stop sync and move to place position
    dashboard.stop_sync_cnv()

    dashboard.mov_l(400, -100, 200, 180, 0, 0, coordinate_mode=1)
```

::: tip
Conveyor tracking requires careful calibration of the encoder ratio and conveyor coordinate system. Refer to the Dobot controller documentation for calibration procedures.
:::
