---
layout: home

hero:
  name: Dobot V4 Python SDK
  text: Control Dobot Robots over TCP/IP
  tagline: Typed responses, real-time feedback, 10 command categories, and multi-language alarm support.
  actions:
    - theme: brand
      text: Get Started
      link: /getting-started/installation
    - theme: alt
      text: API Reference
      link: /reference/
    - theme: alt
      text: GitHub
      link: https://github.com/Dobot-Arm/TCP-IP-Python-V4

features:
  - icon: 🤖
    title: Unified Facade
    details: DobotRobot provides a single entry point — connect, enable, move, and monitor with one object.
  - icon: 📡
    title: Real-Time Feedback
    details: Read joint angles, TCP pose, forces, and 60+ fields at 8 ms resolution via binary feedback ports.
  - icon: 🔧
    title: 10 Command Categories
    details: System, Config, Motion, I/O, Query, Force, Modbus, Conveyor, Weld, and Check — all with snake_case methods.
  - icon: 🌍
    title: Multi-Language Alarms
    details: Alarm descriptions in 10 languages (EN, ZH, JA, KO, DE, FR, ES, RU, VI) with automatic detection.
  - icon: 🛡️
    title: Type-Safe Returns
    details: DobotRobot methods return typed Python values — None, int, Pose, or tuple — not raw strings.
  - icon: ⚡
    title: Python 3.9+
    details: Modern Python with full type annotations, Google-style docstrings, and loguru logging.
---

## Quick Example

```python
from dobot_api_v4 import DobotRobot

with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()
    robot.speed_factor(50)

    # Joint motion
    robot.mov_j(0, 0, 0, 0, 0, 0, coordinate_mode=0)

    # Read current pose
    pose = robot.get_pose()
    print(f"Position: x={pose.x}, y={pose.y}, z={pose.z}")

    # Read real-time feedback
    data = robot.feedback_data()
    if data:
        print(f"Robot mode: {data.robot_mode}")
        print(f"Joint angles: {data.q_actual}")
```
