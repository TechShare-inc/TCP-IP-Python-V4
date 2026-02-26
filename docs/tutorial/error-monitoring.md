---
type: tutorial
---

# Error Monitoring & Alarms

In this tutorial, you will learn how to monitor robot errors using the `RobotErrorMonitor` and translate alarm codes into human-readable messages using `AlarmI18n`.

## Prerequisites

- The SDK is [installed](../getting-started/installation.md).
- The robot is powered on and reachable.

## Step 1 — Check for Errors

The `RobotErrorMonitor` class communicates with the robot's HTTP error endpoint on port 22000. When using `DobotRobot`, an error monitor is automatically created.

```python
from dobot_api_v4 import DobotRobot

with DobotRobot("192.168.1.6") as robot:
    has_errors = robot.check_errors()
    print(f"Errors present: {has_errors}")
```

**Expected Output:**

> ```
> Errors present: False
> ```

## Step 2 — Use RobotErrorMonitor Directly

For more control, use `RobotErrorMonitor` standalone:

```python
from dobot_api_v4 import RobotErrorMonitor

monitor = RobotErrorMonitor(robot_ip="192.168.1.6")

# Check errors in English (default)
has_errors = monitor.check_errors("en")
print(f"Errors: {has_errors}")

# Check errors in Chinese
has_errors_zh = monitor.check_errors("zh_cn")
print(f"Errors (Chinese): {has_errors_zh}")
```

**Expected Output:**

> ```
> Errors: False
> Errors (Chinese): False
> ```

## Step 3 — Get Raw Error Data

For programmatic access to error information:

```python
import json
from dobot_api_v4 import RobotErrorMonitor

monitor = RobotErrorMonitor(robot_ip="192.168.1.6")

raw_data = monitor.get_error_info("en")
if raw_data:
    print(json.dumps(raw_data, indent=2, ensure_ascii=False))
else:
    print("No errors or connection failed.")
```

## Step 4 — Save Error Logs

Export error logs to a file for later analysis:

```python
from dobot_api_v4 import RobotErrorMonitor

monitor = RobotErrorMonitor(robot_ip="192.168.1.6")
monitor.save_error_log("robot_errors.log", language="en")
```

## Step 5 — Translate Alarm Codes with AlarmI18n

`AlarmI18n` translates numeric alarm IDs into descriptions and solutions in 10 languages. It works offline — no robot connection needed.

```python
from dobot_api_v4 import AlarmI18n

i18n = AlarmI18n(default_language="en")

# Look up a controller alarm
alarm = i18n.get_controller_alarm(16)
print(f"Alarm #{alarm['id']}")
print(f"Level: {alarm['level']}")
print(f"Description: {alarm['description']}")
print(f"Solution: {alarm['solution']}")
```

**Expected Output:**

> ```
> Alarm #16
> Level: warning
> Description: ...
> Solution: ...
> ```

## Step 6 — Switch Languages Dynamically

```python
from dobot_api_v4 import AlarmI18n

i18n = AlarmI18n("en")

languages = ["en", "zh_CN", "ja", "de", "ko"]

for lang in languages:
    i18n.set_language(lang)
    alarm = i18n.get_controller_alarm(16)
    print(f"[{lang:5s}] {alarm['description']}")
```

**Expected Output:**

> ```
> [en   ] ...
> [zh_CN] ...
> [ja   ] ...
> [de   ] ...
> [ko   ] ...
> ```

## Step 7 — Auto-Detect Alarm Type

The `get_alarm()` method automatically detects whether an ID is a controller or servo alarm based on the ID range:

```python
from dobot_api_v4 import AlarmI18n

i18n = AlarmI18n("en")

for alarm_id in [16, 100, 8752, 12816]:
    alarm = i18n.get_alarm(alarm_id)
    print(f"ID {alarm_id:5d} → Type: {alarm['type']:10s} | {alarm['description'][:50]}")
```

## Step 8 — Combine Error Monitor with I18n

Here is a practical pattern that checks for errors and provides translated details:

```python
from dobot_api_v4 import DobotRobot, AlarmI18n

i18n = AlarmI18n("en")

with DobotRobot("192.168.1.6") as robot:
    # Get error IDs from the robot
    error_resp = robot.get_error_id()

    if error_resp.error_ids:
        print(f"Found {len(error_resp.error_ids)} error(s):")
        for eid in error_resp.error_ids:
            alarm = i18n.get_alarm(eid)
            print(f"  [{alarm['type']}] #{eid}: {alarm['description']}")
            print(f"    Solution: {alarm['solution']}")
    else:
        print("No errors.")

    # Clear errors if any
    robot.clear_error()
```

## Supported Languages

| Code      | Language           |
| --------- | ------------------ |
| `en`      | English            |
| `zh_CN`   | Simplified Chinese |
| `zh_Hant` | Traditional Chinese|
| `ja`      | Japanese           |
| `ko`      | Korean             |
| `de`      | German             |
| `fr`      | French             |
| `es`      | Spanish            |
| `ru`      | Russian            |
| `vi`      | Vietnamese         |

## What's Next

- [Pick-and-Place Workflow](./pick-and-place.md) — combine motion with I/O
- [How to Use Multi-Language Alarms](../how-to/multi-language-alarms.md) — advanced alarm usage
- [Error Handling & Reconnect](../how-to/error-handling-reconnect.md) — handle connection failures
