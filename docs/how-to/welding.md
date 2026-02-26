---
type: how-to
---

# How to Set Up Welding Operations

The weld mixin provides commands for arc welding with arc tracking, weave patterns, and speed control.

## Prerequisites

- A welding torch is mounted and connected.
- The welding power source is configured.
- The workpiece and welding parameters are set up.

## Arc Tracking

Arc tracking adjusts the weld path in real-time based on arc voltage/current feedback.

### Start Arc Tracking

```python
dashboard = robot.dashboard

# Set arc tracking parameters
dashboard.arc_track_params(
    # Parameters depend on welding configuration
)

# Start arc tracking
dashboard.arc_track_start()
```

### Set Arc Track Offset

```python
dashboard.set_arc_track_offset(0.5, 0.0)  # Offset values
```

### End Arc Tracking

```python
dashboard.arc_track_end()
```

## Weave Patterns

Weave patterns create oscillating motions perpendicular to the weld path.

### Start Weave

```python
# Configure weave parameters
dashboard.weave_params(
    # Weave amplitude, frequency, and other parameters
)

# Start weave pattern
dashboard.weave_start()
```

### End Weave

```python
dashboard.weave_end()
```

## Weld Arc Speed Control

Control welding speed dynamically during a weld:

```python
# Start weld with arc speed control
dashboard.weld_arc_speed_start()

# Set arc speed
dashboard.weld_arc_speed(10.0)  # mm/s

# End weld arc speed control
dashboard.weld_arc_speed_end()
```

## Start Weld Weave

```python
dashboard.weld_weave_start()
```

## Relative Weld Motions

Perform welding with relative positioning:

```python
# Linear weld with relative end point
dashboard.rel_point_weld_line(
    10, 0, 0, 0, 0, 0  # Relative offset from current position
)

# Arc weld with relative points
dashboard.rel_point_weld_arc(
    5, 5, 0, 0, 0, 0,   # Relative intermediate point
    10, 0, 0, 0, 0, 0,  # Relative end point
)
```

## Practical Example: Simple Weld Seam

```python
from dobot_api_v4 import DobotRobot
from time import sleep

with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()
    robot.speed_factor(20)
    dashboard = robot.dashboard

    # Move to weld start position
    dashboard.mov_l(400, 0, 50, 180, 0, 0, coordinate_mode=1)
    sleep(2)

    # Start welding arc
    dashboard.weld_arc_speed_start()
    dashboard.weld_arc_speed(8.0)  # 8 mm/s weld speed

    # Weld along a line
    dashboard.mov_l(400, 100, 50, 180, 0, 0, coordinate_mode=1)
    sleep(5)

    # End weld
    dashboard.weld_arc_speed_end()

    # Retract
    dashboard.mov_l(400, 100, 150, 180, 0, 0, coordinate_mode=1)
```

::: warning
Welding operations require proper safety equipment and procedures. Always test in a safe environment first.
:::
