---
type: how-to
---

# How to Use Force Control

Ensure the robot has a force/torque sensor and it is properly calibrated before using force control features.

## Enable the Force/Torque Sensor

```python
dashboard = robot.dashboard

# Enable the sensor (status=1)
dashboard.enable_ft_sensor(1)

# Disable the sensor (status=0)
dashboard.enable_ft_sensor(0)
```

Or via the high-level facade (through the dashboard):

```python
robot.dashboard.enable_ft_sensor(1)
```

## Read Force/Torque Values

Via the dashboard:

```python
result = dashboard.get_force()
print(f"Force values: {result}")
```

Or via feedback data:

```python
data = robot.feedback_data()
if data:
    print(f"Force/Torque: {data.six_force_value}")
    # Returns (Fx, Fy, Fz, Mx, My, Mz) in N and N·m
```

## Zero the Sensor (Home)

```python
dashboard.six_force_home()
```

## Force Compliance (FC) Mode

FC mode allows the robot to comply with external forces along specified axes.

### Enable FC Mode

```python
# Set force control mode per axis
# Parameters: mode for Fx, Fy, Fz, Mx, My, Mz
# 0 = position control, 1 = force control
dashboard.fc_force_mode(0, 0, 1, 0, 0, 0)  # Force control on Z-axis only
```

### Set Target Force

```python
# Set target force values (N and N·m)
dashboard.fc_set_force(0, 0, -10, 0, 0, 0)  # 10N downward on Z
```

### Set Stiffness

```python
# Stiffness for each axis (higher = stiffer)
dashboard.fc_set_stiffness(1000, 1000, 500, 100, 100, 100)
```

### Set Damping

```python
# Damping coefficients for each axis
dashboard.fc_set_damping(50, 50, 50, 10, 10, 10)
```

### Set Force Deviation Limits

```python
dashboard.fc_set_deviation(1.0, 1.0, 2.0, 5.0, 5.0, 5.0)
```

### Set Force Limits

```python
dashboard.fc_set_force_limit(50, 50, 50, 20, 20, 20)
```

### Set Mass Compensation

```python
dashboard.fc_set_mass(0.5)  # End-effector mass in kg
```

### Set Force Speed Limit

```python
dashboard.fc_set_force_speed_limit(100)  # mm/s
```

### Turn Off FC Mode

```python
dashboard.fc_off()
# Or via facade:
robot.fc_off()
```

## Force Drive Mode

Force drive mode applies constant force/velocity along axes:

```python
# Enable force drive mode
dashboard.force_drive_mode(1)

# Set force drive speed per axis
dashboard.force_drive_speed(0, 0, -5, 0, 0, 0)  # Move down at 5 mm/s
```

## Practical Example: Force-Controlled Insertion

```python
from dobot_api_v4 import DobotRobot
from time import sleep

with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()
    dashboard = robot.dashboard

    # Enable force sensor
    dashboard.enable_ft_sensor(1)
    sleep(0.5)
    dashboard.six_force_home()
    sleep(0.5)

    # Move above insertion point
    dashboard.mov_l(400, 0, 100, 180, 0, 0, coordinate_mode=1)
    sleep(2)

    # Enable FC mode on Z-axis with 10N downward force
    dashboard.fc_force_mode(0, 0, 1, 0, 0, 0)
    dashboard.fc_set_force(0, 0, -10, 0, 0, 0)
    dashboard.fc_set_stiffness(1000, 1000, 200, 100, 100, 100)

    # Wait for insertion
    sleep(3)

    # Turn off FC mode
    dashboard.fc_off()
    dashboard.enable_ft_sensor(0)
```

::: warning
Always test force control with low force values first. Incorrect force parameters can damage the robot, workpiece, or end-effector.
:::
