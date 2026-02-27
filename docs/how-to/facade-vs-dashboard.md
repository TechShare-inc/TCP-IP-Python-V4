---
type: how-to
---

# How to Choose Between DobotRobot and DobotApiDashboard

The SDK offers two levels of API. Choose based on your needs.

## DobotRobot — High-Level Facade

**Use when:** You want typed return values, automatic resource management, and a simple interface.

```python
from dobot_api_v4 import DobotRobot

with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()               # → None
    pose = robot.get_pose()            # → Pose
    mode = robot.robot_mode()          # → int

    print(f"x={pose.x}, y={pose.y}")   # Typed field access
    print(f"mode={mode}")
```

**Advantages:**

- Context manager for automatic cleanup
- Methods return typed Python values (`None`, `int`, `Pose`, `tuple`)
- Lazy feedback connections (only created when accessed)
- Built-in error monitor via HTTP
- Convenience methods: `check_errors()`, `clear_robot_error()`, `feedback_data()`

**Limitations:**

- Only a subset of dashboard commands are forwarded (~25 commonly used methods)
- Cannot customize connection parameters

## DobotApiDashboard — Full Command Set

**Use when:** You need access to all ~155 commands, or when `DobotRobot` doesn't expose the specific command you need.

```python
from dobot_api_v4 import DobotApiDashboard

dashboard = DobotApiDashboard("192.168.1.6", 29999)

result = dashboard.enable_robot()      # → raw string
result = dashboard.get_pose()          # → raw string "0,1,350.0,0.0,300.0,..."
result = dashboard.cnv_init()          # → raw string (not available on DobotRobot)
result = dashboard.modbus_create(...)  # → raw string (not available on DobotRobot)

dashboard.close()
```

**Advantages:**

- All ~155 commands available across 10 categories
- Direct control over the protocol
- Both `snake_case` and `PascalCase` naming

**Limitations:**

- Returns raw strings — you must parse responses yourself
- No automatic resource management (no context manager)
- No feedback or error monitor — you must create those separately

## Mixing Both

The best approach is often to use `DobotRobot` as the main entry point and access the dashboard directly when needed:

```python
from dobot_api_v4 import DobotRobot

with DobotRobot("192.168.1.6") as robot:
    # High-level: typed responses
    robot.enable_robot()
    pose = robot.get_pose()

    # Low-level: access any dashboard command
    robot.dashboard.modbus_create("192.168.1.100", 502, 1)
    robot.dashboard.cnv_init()
    robot.dashboard.set_collision_level(3)

    # Feedback is still available
    data = robot.feedback_data()
```

## Decision Guide

| Criterion                    | DobotRobot          | DobotApiDashboard       |
| ---------------------------- | -------------------- | ----------------------- |
| Typed responses              | Yes                  | No (raw strings)        |
| Command coverage             | ~25 common commands  | All ~155 commands       |
| Context manager              | Yes                  | No                      |
| Feedback integration         | Built-in (lazy)      | Separate class needed   |
| Error monitoring             | Built-in (HTTP)      | Separate class needed   |
| Modbus, Conveyor, Weld, etc. | Via `robot.dashboard`| Direct                  |
| Best for                     | Most applications    | Specialized/low-level   |

::: tip
Start with `DobotRobot`. If you need a command that isn't forwarded, access it via `robot.dashboard.method_name()` — you get the best of both worlds.
:::
