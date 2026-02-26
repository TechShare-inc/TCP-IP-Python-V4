---
type: how-to
---

# How to Configure Speed, Acceleration, and Coordinate Systems

## Set Global Speed Factor

The speed factor scales all motion commands (1–100%):

```python
robot.speed_factor(50)  # 50% of maximum speed
```

## Set Joint Acceleration and Velocity

```python
robot.acc_j(80)   # Joint acceleration ratio (1–100)
robot.vel_j(60)   # Joint velocity ratio (1–100)
```

## Set Linear Acceleration and Velocity

```python
robot.acc_l(80)   # Linear acceleration ratio (1–100)
robot.vel_l(60)   # Linear velocity ratio (1–100)
```

## Set Continuous Path Rate

The CP parameter controls blend radius between consecutive motions:

```python
robot.cp(50)  # Continuous path ratio (1–100)
```

## Configure User Coordinate System

A user coordinate system defines a reference frame for Cartesian motions.

```python
dashboard = robot.dashboard

# Define user coordinate 1 with origin at (400, 100, 0) and no rotation
dashboard.set_user(1, 400, 100, 0, 0, 0, 0)

# Activate user coordinate 1
dashboard.user(1)
```

To calculate a user coordinate from three points:

```python
# Calibrate user coordinate from three reference points
dashboard.calc_user(
    1,                        # User index
    0,                        # Method (0 = three-point)
    400, 100, 0, 0, 0, 0,    # Point 1 (origin)
    500, 100, 0, 0, 0, 0,    # Point 2 (X-axis direction)
    400, 200, 0, 0, 0, 0,    # Point 3 (XY-plane)
)
```

## Configure Tool Coordinate System

A tool coordinate system defines the Tool Center Point (TCP).

```python
# Define tool coordinate 1
dashboard.set_tool(1, 0, 0, 100, 0, 0, 0)

# Activate tool coordinate 1
dashboard.tool(1)
```

## Set Payload

Configure end-effector weight and center of gravity:

```python
# Weight = 1.5 kg, center of gravity offset (x=0, y=0, z=50) mm
dashboard.set_payload(1.5, 0, 0, 50)
```

## Configure Collision Detection

```python
# Set collision detection level (0 = off, 1–5 = increasing sensitivity)
dashboard.set_collision_level(3)

# Set backoff distance after collision (mm)
dashboard.set_back_distance(5.0)

# Set behavior after collision: 0 = stop, 1 = pause
dashboard.set_post_collision_mode(0)
```

## Configure Drag Sensitivity

Set drag teach sensitivity per axis:

```python
dashboard.drag_sensitivity(
    50, 50, 50, 50, 50, 50  # Sensitivity for J1–J6 (1–100)
)
```

## Configure SafeSkin

```python
# Enable SafeSkin
dashboard.enable_safe_skin(1)

# Configure SafeSkin sensitivity for specific parts
dashboard.set_safe_skin(1, 50)  # Part index, sensitivity
```

## Configure Safety Wall and Work Zone

```python
# Enable/disable safety wall
dashboard.set_safe_wall_enable(1)  # 1 = enable, 0 = disable

# Enable/disable interference work zone
dashboard.set_work_zone_enable(1)  # 1 = enable, 0 = disable
```
