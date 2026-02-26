---
type: how-to
---

# How to Handle Errors and Reconnect

## Catch DobotApiError

All SDK methods can raise `DobotApiError` when the robot returns an error response:

```python
from dobot_api_v4 import DobotRobot, DobotApiError

with DobotRobot("192.168.1.6") as robot:
    try:
        robot.enable_robot()
        robot.mov_j(0, 30, -30, 0, 0, 0, coordinate_mode=0)
    except DobotApiError as e:
        print(f"Robot error: {e}")
```

## Check and Clear Errors

```python
with DobotRobot("192.168.1.6") as robot:
    # Check if errors exist
    has_errors = robot.check_errors()

    if has_errors:
        # Clear errors
        robot.clear_error()

        # Verify errors are cleared
        still_has_errors = robot.clear_robot_error()
        if still_has_errors:
            print("Errors persist after clearing — manual intervention needed.")
        else:
            print("Errors cleared successfully.")
```

## Reconnect After Connection Loss

If the TCP connection drops (network issue, robot reboot), use `reconnect()`:

```python
import socket
from dobot_api_v4 import DobotRobot

robot = DobotRobot("192.168.1.6")

try:
    robot.enable_robot()
    # ... do work ...
except (ConnectionError, socket.error, OSError) as e:
    print(f"Connection lost: {e}")
    print("Attempting to reconnect...")

    try:
        robot.reconnect()
        print("Reconnected successfully.")

        # Re-enable after reconnect
        robot.enable_robot()
    except Exception as reconnect_err:
        print(f"Reconnect failed: {reconnect_err}")
finally:
    robot.close()
```

## Automatic Retry Pattern

A practical retry wrapper for production code:

```python
import socket
from time import sleep
from dobot_api_v4 import DobotRobot

def with_retry(robot: DobotRobot, func, *args, max_retries=3, delay=2.0):
    """Execute a robot command with automatic reconnect on failure."""
    for attempt in range(max_retries):
        try:
            return func(*args)
        except (ConnectionError, socket.error, OSError) as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                sleep(delay)
                try:
                    robot.reconnect()
                    robot.enable_robot()
                except Exception:
                    pass
    raise ConnectionError(f"Failed after {max_retries} attempts")


# Usage
with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()

    # This will retry up to 3 times on connection failure
    result = with_retry(robot, robot.get_pose)
    print(f"Pose: ({result.x}, {result.y}, {result.z})")
```

## Reset the Robot

If the robot enters a fault state that `clear_error` cannot resolve:

```python
robot.dashboard.reset_robot()
```

## Emergency Stop

For immediate halt in dangerous situations:

```python
# Emergency stop (mode=0: stop, mode=1: resume-able)
robot.emergency_stop(mode=0)
```

::: warning
After an emergency stop with `mode=0`, the robot must be power-cycled or reset before it can be re-enabled.
:::
