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
print(f"Mode: {mode}")
```

## Mode Values

| Value | Name             | Description                                         |
| ----- | ---------------- | --------------------------------------------------- |
| 1     | **INIT**         | Initialized — controller is starting up             |
| 2     | **BRAKE_OPEN**   | Brake switched on                                   |
| 3     | **POWEROFF**     | Power-off status                                    |
| 4     | **DISABLED**     | Disabled (no brake switched on)                     |
| 5     | **ENABLE**       | Enabled and idle — ready for commands               |
| 6     | **BACKDRIVE**    | Drag teach mode active                              |
| 7     | **RUNNING**      | Running status (project, TCP queue)                 |
| 8     | **SINGLE_MOVE**  | Single motion status (jog, RunTo)                   |
| 9     | **ERROR**        | Uncleared alarms (highest priority)                 |
| 10    | **PAUSE**        | Pause status                                        |
| 11    | **COLLISION**    | Collision status                                    |

## Common Patterns

### Wait for Motion Complete

The most common pattern is to wait for the robot to return to IDLE (mode 5) after issuing a motion command:

```python
from time import sleep

target_id = robot.mov_j(0, 30, -30, 0, 0, 0, coordinate_mode=0)

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
