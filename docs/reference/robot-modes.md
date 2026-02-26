---
type: reference
---

# Robot Modes

The `robot_mode` field in feedback data indicates the current operating state of the robot. Read it via:

```python
data = robot.feedback_data()
if data:
    print(f"Mode: {data.robot_mode}")
```

Or via the dashboard command:

```python
mode = robot.robot_mode()
print(f"Mode: {mode.value}")
```

## Mode Values

| Value | Name             | Description                                         |
| ----- | ---------------- | --------------------------------------------------- |
| 1     | **INIT**         | Initializing — controller is starting up            |
| 2     | **BRAKE_OPEN**   | Brakes are being released                           |
| 3     | **DISABLED**     | Robot is disabled (powered but not enabled)          |
| 4     | **ENABLE**       | Robot is being enabled (transition state)            |
| 5     | **IDLE**         | Robot is enabled and idle — ready for commands       |
| 6     | **DRAG**         | Drag teach mode active                              |
| 7     | **RUNNING**      | Executing a motion command                          |
| 8     | **PAUSE**        | Motion is paused (can be resumed)                    |
| 9     | **ERROR**        | Error/fault state — check alarms                     |
| 10    | **JOG**          | Jog mode active                                     |
| 11    | **EMERGENCY_STOP** | Emergency stop triggered                          |

## Common Patterns

### Wait for Motion Complete

The most common pattern is to wait for the robot to return to IDLE (mode 5) after issuing a motion command:

```python
from time import sleep

result = robot.mov_j(0, 30, -30, 0, 0, 0, coordinate_mode=0)
target_id = result.command_id

while True:
    data = robot.feedback_data()
    if data and data.robot_mode == 5 and data.current_command_id >= target_id:
        print("Motion complete")
        break
    sleep(0.1)
```

### Check if Robot is Ready

```python
data = robot.feedback_data()
if data and data.robot_mode == 5:
    print("Robot is ready for commands")
elif data and data.robot_mode == 9:
    print("Robot is in error state — clear errors first")
```

### Detect Emergency Stop

```python
data = robot.feedback_data()
if data and data.robot_mode == 11:
    print("Emergency stop is active!")
```
