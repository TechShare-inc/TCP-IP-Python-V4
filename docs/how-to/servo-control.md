---
type: how-to
---

# How to Use Servo Control

Servo control (`ServoJ` / `ServoP`) provides low-level joint or Cartesian position control at high frequency. Unlike `MovJ`/`MovL`, servo commands are executed immediately without trajectory planning — you are fully responsible for smooth interpolation.

## ServoJ — Joint Servo

Send target joint angles at regular intervals (typically 8 ms):

```python
from time import sleep

dashboard = robot.dashboard

# Single servo command
dashboard.servo_j(
    j1=0.0, j2=30.0, j3=-30.0, j4=0.0, j5=0.0, j6=0.0,
    t=0.008,          # Interpolation time (seconds)
    ahead_time=30,    # Lookahead time (ms)
    gain=0,           # Proportion gain
)
```

Or via the high-level facade:

```python
robot.servo_j(0.0, 30.0, -30.0, 0.0, 0.0, 0.0)
```

## ServoP — Cartesian Servo

Send target TCP pose at regular intervals:

```python
dashboard.servo_p(
    x=400.0, y=0.0, z=300.0, rx=180.0, ry=0.0, rz=0.0,
    t=0.008,
    ahead_time=30,
    gain=0,
)
```

## Servo Loop Pattern

Servo commands must be sent continuously in a tight loop. A typical pattern:

```python
import math
from time import sleep, time

from dobot_api_v4 import DobotRobot

with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()
    dashboard = robot.dashboard

    # Starting joint position
    base_joints = [0.0, 30.0, -30.0, 0.0, 0.0, 0.0]

    # Oscillate J1 by ±5° at 0.5 Hz for 10 seconds
    t0 = time()
    dt = 0.008  # 8 ms cycle

    while time() - t0 < 10.0:
        elapsed = time() - t0
        offset = 5.0 * math.sin(2 * math.pi * 0.5 * elapsed)

        joints = base_joints.copy()
        joints[0] += offset

        dashboard.servo_j(*joints, t=dt)
        sleep(dt)
```

## Cartesian Servo Loop

```python
import math
from time import sleep, time

from dobot_api_v4 import DobotRobot

with DobotRobot("192.168.1.6") as robot:
    robot.enable_robot()
    dashboard = robot.dashboard

    # Base pose
    base_pose = [400.0, 0.0, 300.0, 180.0, 0.0, 0.0]

    t0 = time()
    dt = 0.008

    while time() - t0 < 10.0:
        elapsed = time() - t0
        # Circle in XY plane, radius 20 mm, 0.2 Hz
        dx = 20.0 * math.cos(2 * math.pi * 0.2 * elapsed)
        dy = 20.0 * math.sin(2 * math.pi * 0.2 * elapsed)

        pose = base_pose.copy()
        pose[0] += dx
        pose[1] += dy

        dashboard.servo_p(*pose, t=dt)
        sleep(dt)
```

## Parameters

| Parameter    | Default | Description                                     |
| ------------ | ------- | ----------------------------------------------- |
| `t`          | 0.008   | Interpolation period in seconds                 |
| `ahead_time` | 30      | Lookahead time in milliseconds                  |
| `gain`       | 0       | Proportion gain (0 = auto)                      |

::: warning
- The servo loop must run at a consistent frequency matching the `t` parameter. Missed cycles cause jerky motion.
- There is no collision detection in servo mode. Ensure your trajectory is safe.
- Start with small amplitudes and low speeds during development.
:::
