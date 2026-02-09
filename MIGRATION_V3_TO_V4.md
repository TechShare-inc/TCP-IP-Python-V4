# Migration Guide: V3 to V4 API Differences

This document provides a comprehensive comparison of Dobot API V3 and V4, highlighting breaking changes, new features, and migration strategies.

## Table of Contents
- [Architecture Changes](#architecture-changes)
- [Port Changes](#port-changes)
- [MyType Feedback Structure](#mytype-feedback-structure)
- [Method Signature Changes](#method-signature-changes)
- [V4 New Features](#v4-new-features)
- [V3-Only Methods (Deprecated)](#v3-only-methods-deprecated)
- [Migration Examples](#migration-examples)
- [Breaking Changes Summary](#breaking-changes-summary)

---

## Architecture Changes

### Class Structure

**V3:** Two separate API classes
```python
from dobot_api import DobotApiDashboard, DobotApiMove

dashboard = DobotApiDashboard(ip, 29999)  # Control commands
move = DobotApiMove(ip, 29999)            # Movement commands (separate class)
```

**V4 (Monolithic):** Single unified API class
```python
from dobot_api import DobotApiDashboard

dashboard = DobotApiDashboard(ip, 29999)  # All commands in one class
# Movement commands now called directly on dashboard:
dashboard.MovJ(300, 0, 200, 0, 90, 0, coordinateMode=0)
```

**Note:** V4 simplifies the architecture by combining control and movement commands into a single `DobotApiDashboard` class. This is the original V4 monolithic design (commit 65a19c9e), providing a simpler, more straightforward API surface.

**Key Benefits:**
- Single connection instance for all operations
- Simplified initialization (no need to create separate move instance)
- Consistent interface for all robot commands
- Reduced complexity in application code

---

## Port Changes

| Port  | V3 Usage           | V4 Usage                      |
|-------|--------------------|-------------------------------|
| 29999 | ✓ Dashboard/Move   | ✓ Dashboard/Move              |
| 30003 | ✓ Supported        | ❌ **REMOVED**                |
| 30004 | ✓ Feedback         | ✓ Feedback                    |
| 30005 | ❌ Not supported   | ✓ **NEW** Feedback (V4-only) |

### Breaking Change
**Port 30003 is removed in V4.** Use port 30004 or 30005 for feedback instead.

---

## MyType Feedback Structure

### Field Naming Convention Change

**V3:** snake_case
```python
data = feedback.feedBackData()
joint1 = data['q_actual'][0][0]
digital_in = data['digital_input_bits'][0]
```

**V4:** PascalCase
```python
data = feedback.feedBackData()
joint1 = data['QActual'][0][0]
digital_in = data['DigitalInputs'][0]
```

### Type Changes
- `len`: `int64` (V3) → `uint16` (V4)

### Removed Fields (V3 → V4)
- `jerk_ratio`, `xyz_jerk_ratio`, `r_jerk_ratio`
- `trace_index`
- `elbow_position`, `elbow_velocity`
- `tool_accelerometer_values`

### New Fields (V4 Only)
- `RunTime`, `CollisionState`
- `ArmApproachState`, `J4ApproachState`, `J5ApproachState`, `J6ApproachState`
- `VibrationDisZ`, `CurrentCommandId`
- `AutoManualMode`, `ExportStatus`, `SafetyState`

---

## Method Signature Changes

### EnableRobot
```python
# V3
EnableRobot(load=0.0, centerX=0.0, centerY=0.0, centerZ=0.0)

# V4
EnableRobot(load=0.0, centerX=0.0, centerY=0.0, centerZ=0.0, isCheck=-1)
```
**Change:** Added `isCheck` parameter to verify load after enabling.

---

### EmergencyStop
```python
# V3
EmergencyStop()  # No parameters

# V4
EmergencyStop(mode)  # mode: 1=press, 0=release
```
**Breaking Change:** Now requires `mode` parameter.

---

### Speed Commands Renamed
```python
# V3
SpeedJ(speed)  # Set joint speed ratio
SpeedL(speed)  # Set linear speed ratio

# V4
VelJ(speed)    # Renamed for clarity
VelL(speed)    # Renamed for clarity
```
**Breaking Change:** Method names changed.

---

### SetPayload (formerly PayLoad)
```python
# V3
PayLoad(weight, inertia)  # 2 parameters

# V4
SetPayload(load=0.0, X=0.0, Y=0.0, Z=0.0, name='F')
```
**Breaking Change:** Completely different signature. Supports eccentric coordinates or preset names.

---

### GetPose
```python
# V3
GetPose()  # No parameters

# V4
GetPose(user=-1, tool=-1)  # Optional coordinate system selection
```
**Enhancement:** Added coordinate system parameters.

---

### MovJ - MAJOR CHANGE
```python
# V3 (DobotApiMove class)
MovJ(x, y, z, rx, ry, rz, *dynParams)
# Dynamic params as strings: "SpeedL=80", "AccL=50"

# V4 (DobotApiDashboard class - monolithic)
MovJ(a1, b1, c1, d1, e1, f1, coordinateMode, 
     user=-1, tool=-1, a=-1, v=-1, cp=-1)
```

**Breaking Changes:**
1. Added **required** `coordinateMode` parameter:
   - `0` = Cartesian pose (x, y, z, rx, ry, rz)
   - `1` = Joint angles (j1, j2, j3, j4, j5, j6)
2. Named parameters replace dynamic strings
3. Generic parameter names (a1-f1) work for both modes

**Usage:**
```python
# Cartesian mode
dashboard.MovJ(300, 0, 200, 0, 90, 0, coordinateMode=0)

# Joint mode
dashboard.MovJ(0, 0, 90, 0, 90, 0, coordinateMode=1)
```

---

### MovL - MAJOR CHANGE
```python
# V3
MovL(x, y, z, rx, ry, rz, *dynParams)

# V4
MovL(a1, b1, c1, d1, e1, f1, coordinateMode,
     user=-1, tool=-1, a=-1, v=-1, speed=-1, cp=-1, r=-1)
```
**Breaking Changes:** Same as MovJ, plus added `speed` and `r` (blend radius) parameters.

---

### JointMovJ (Deprecated)
```python
# V3
JointMovJ(j1, j2, j3, j4, j5, j6, *dynParams)

# V4 - Use MovJ with coordinateMode=1
MovJ(j1, j2, j3, j4, j5, j6, coordinateMode=1, ...)
```
**Breaking Change:** `JointMovJ` removed. Use `MovJ(coordinateMode=1)` instead.

---

### ServoJ
```python
# V3
ServoJ(j1, j2, j3, j4, j5, j6, t=0.1, lookahead_time=50, gain=500)

# V4
ServoJ(J1, J2, J3, J4, J5, J6, t=-1.0, aheadtime=-1.0, gain=-1.0)
```
**Breaking Change:** `lookahead_time` → `aheadtime`. Different default values.

---

### Arc
```python
# V3
Arc(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, *dynParams)

# V4
Arc(a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2,
    coordinateMode, user=-1, tool=-1, a=-1, v=-1, speed=-1, cp=-1, r=-1)
```
**Breaking Change:** Added `coordinateMode` parameter.

---

### Circle3 → Circle
```python
# V3
Circle3(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, count, *dynParams)

# V4
Circle(a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2, 
       coordinateMode, count, user=-1, tool=-1, ...)
```
**Breaking Change:** Renamed and added `coordinateMode`.

---

### MovLIO / MovJIO
```python
# V3
MovLIO(x, y, z, a, b, c, *dynParams)
# dynParams: tuples like (Mode, Distance, Index, Status)

# V4
MovLIO(a1, b1, c1, d1, e1, f1, coordinateMode, 
       Mode, Distance, Index, Status,
       user=-1, tool=-1, ...)
```
**Breaking Change:** IO parameters are now individual required parameters, not tuples.

---

### ResetRobot vs Stop
```python
# V3
ResetRobot()  # Stop robot motion

# V4
Stop()        # Stop motion queue
Pause()       # Pause motion queue
Continue()    # Resume motion queue
ResetRobot()  # Different behavior (system reset)
```
**Breaking Change:** Use `Stop()` to halt motion, not `ResetRobot()`.

---

## V4 New Features

### Force Control (V4 Only)
```python
dashboard.EnableFTSensor(1)              # Enable force sensor
dashboard.SixForceHome()                  # Zero force sensor
move.FCForceMode(x, y, z, rx, ry, rz)   # Start force control
move.FCSetForceLimit(...)                # Set force limits
move.FCOff()                             # Exit force control
```

### Kinematics (V4 Only)
```python
# Forward kinematics
dashboard.PositiveKin(J1, J2, J3, J4, J5, J6, user, tool)

# Inverse kinematics
dashboard.InverseKin(X, Y, Z, Rx, Ry, Rz, ...)
```

### Enhanced IO Operations
```python
dashboard.DOInstant(index, status)       # Immediate DO (non-queued)
dashboard.GetDO(index)                   # Read DO status
dashboard.DOGroup(*indices)              # Set multiple DOs
dashboard.DIGroup(*indices)              # Read multiple DIs
```

### Collision Detection Enhancement
```python
dashboard.SetCollisionLevel(level)       # Sensitivity: 0-5
dashboard.SetBackDistance(distance)      # Collision backoff distance
dashboard.SetPostCollisionMode(mode)     # Post-collision behavior
```

### SafeSkin Support (V4 Only)
```python
dashboard.EnableSafeSkin(1)              # Enable SafeSkin
dashboard.SetSafeSkin(part, status)      # Configure zones
```

### Conveyor Tracking (V4 Only)
```python
move.CnvInit(traceName, ...)             # Initialize tracking
move.CnvMovL(...)                        # Track on conveyor (linear)
move.CnvMovC(...)                        # Track on conveyor (arc)
```

### Welding Features (V4 Only)
```python
dashboard.WeaveStart()                   # Start weaving
dashboard.WeaveParams(...)               # Configure weave pattern
dashboard.ArcTrackStart()                # Start arc tracking
dashboard.WeldArcSpeed(speed)            # Set welding speed
```

### Advanced Motion
```python
dashboard.RunTo(pose, moveType, ...)     # Single motion command
dashboard.MovS(file, ...)                # Spline motion
dashboard.CheckMovJ(...)                 # Validate motion before execution
```

### Tool Configuration
```python
dashboard.SetTool485(baud, parity, ...)  # Configure RS485
dashboard.SetToolPower(status, ...)      # Control tool power
dashboard.SetToolMode(mode, type, ...)   # Set tool mode
```

---

## V3-Only Methods (Deprecated in V4)

The following V3 methods do not exist in V4:

### Control Commands
- `RobotMode()` → Different implementation in V4
- `SetArmOrientation(r, d, n, cfg)` → Removed
- `LimZ(value)` → Removed
- `Arch(index)` → Removed (gate parameter)
- `StopScript()` → Use `Stop()`
- `PauseScript()` → Use `Pause()`
- `ContinueScript()` → Use `Continue()`
- `LoadSwitch(offset)` → Removed
- `wait(t)` → Use `Sleep(t)`
- `pause()` → Use `Pause()`

### Movement Commands
- `JointMovJ(...)` → Use `MovJ(coordinateMode=1)`
- `RelMovJ/RelMovL(...)` → Use `RelJointMovJ` or `RelMovJUser/RelMovLUser`
- `Circle3(...)` → Renamed to `Circle()`
- `StartTrace(trace_name)` → Use `StartPath()`
- `StartFCTrace(trace_name)` → Removed
- `Sync()` → Removed/Internal
- `Jump()` → Removed (was marked "pending" in V3)

---

## Migration Examples

### Example 1: Basic Setup

**V3 Code:**
```python
from dobot_api import DobotApiDashboard, DobotApiMove, DobotApiFeedBack

ip = "192.168.1.6"
dashboard = DobotApiDashboard(ip, 29999)
move = DobotApiMove(ip, 29999)
feedback = DobotApiFeedBack(ip, 30003)  # Port 30003

dashboard.EnableRobot()
dashboard.SpeedL(50)
dashboard.PayLoad(1.5, 0.1)
```

**V4 Code:**
```python
from dobot_api import DobotApiDashboard, DobotApiMove, DobotApiFeedBack

ip = "192.168.1.6"
dashboard = DobotApiDashboard(ip, 29999)
move = DobotApiMove(ip, 29999)
feedback = DobotApiFeedBack(ip, 30004)  # Port 30004 or 30005

dashboard.EnableRobot()
dashboard.VelL(50)                      # SpeedL → VelL
dashboard.SetPayload(1.5, 0.0, 0.0, 0.0)  # New signature
```

---

### Example 2: Movement Commands

**V3 Code:**
```python
# Cartesian movement
move.MovJ(300, 0, 200, 0, 90, 0, "User=0", "Tool=0")

# Joint movement
move.JointMovJ(0, 0, 90, 0, 90, 0)

# Relative movement
move.RelMovJ(10, 0, 0, 0, 0, 0)
```

**V4 Code:**
```python
# Cartesian movement (coordinateMode=0)
dashboard.MovJ(300, 0, 200, 0, 90, 0, coordinateMode=0, user=0, tool=0)

# Joint movement (coordinateMode=1)
dashboard.MovJ(0, 0, 90, 0, 90, 0, coordinateMode=1)

# Relative movement (use specific methods)
dashboard.RelJointMovJ(10, 0, 0, 0, 0, 0)  # Joint space
dashboard.RelMovJUser(10, 0, 0, 0, 0, 0)   # User frame
```

---

### Example 3: Feedback Reading

**V3 Code:**
```python
data = feedback.feedBackData()
joint_pos = data['q_actual'][0]
digital_in = data['digital_input_bits'][0]
robot_mode = data['robot_mode'][0]
```

**V4 Code:**
```python
data = feedback.feedBackData()
joint_pos = data['QActual'][0]          # PascalCase
digital_in = data['DigitalInputs'][0]   # PascalCase
robot_mode = data['RobotMode'][0]       # PascalCase
```

---

### Example 4: Emergency Stop

**V3 Code:**
```python
dashboard.EmergencyStop()  # Single call
```

**V4 Code:**
```python
dashboard.EmergencyStop(1)  # 1 = press emergency stop
# ...
dashboard.EmergencyStop(0)  # 0 = release emergency stop
```

---

### Example 5: Servo Commands

**V3 Code:**
```python
move.ServoJ(0, 0, 90, 0, 90, 0, lookahead_time=50, gain=500)
```

**V4 Code:**
```python
dashboard.ServoJ(0, 0, 90, 0, 90, 0, aheadtime=50.0, gain=500.0)  # Parameter renamed
```

---

## Breaking Changes Summary

| Category | Breaking Change |
|----------|----------------|
| **Architecture** | Monolithic class structure (all commands in DobotApiDashboard) |
| **Ports** | 30003 removed → use 30004/30005 |
| **Feedback Fields** | snake_case → PascalCase |
| **Movement** | Added required `coordinateMode` parameter (0=pose, 1=joint) |
| **Movement** | `JointMovJ` removed → use `MovJ(coordinateMode=1)` |
| **Speed Methods** | `SpeedJ/SpeedL` → `VelJ/VelL` |
| **Payload** | `PayLoad(weight, inertia)` → `SetPayload(load, X, Y, Z, name)` |
| **Emergency** | `EmergencyStop()` → `EmergencyStop(mode)` requires parameter |
| **Parameters** | Dynamic string params → Named keyword arguments |
| **ServoJ** | `lookahead_time` → `aheadtime` |
| **Relative Motion** | `RelMovJ/Rel MovL` → `RelJointMovJ/RelMovJUser/RelMovLUser` |
| **Stop Motion** | `ResetRobot()` for stop → `Stop()` |
| **Circle** | `Circle3()` → `Circle()` |
| **Error Handling** | Parameter validation now raises `ValueError` instead of returning empty string |
| **Logging** | Print statements replaced with structured logging (loguru) |

---

## Logging and Error Handling

### Structured Logging with Loguru

**V4** now uses [loguru](https://github.com/Delgan/loguru) for structured logging instead of print statements.

**Benefits:**
- Structured, timestamped log messages
- Configurable log levels (DEBUG, INFO, WARNING, ERROR)
- Colored output for better readability
- Easy filtering and formatting

**Configuration:**

```python
from dobot_api import DobotApiDashboard, logger

# Default log level is INFO
dashboard = DobotApiDashboard("192.168.1.6", 29999)

# Configure log level via environment variable
# Set before importing dobot_api:
import os
os.environ["DOBOT_LOG_LEVEL"] = "DEBUG"  # Options: DEBUG, INFO, WARNING, ERROR

# Or customize logger directly:
logger.remove()  # Remove default handler
logger.add(sys.stderr, level="WARNING")  # Add custom handler
logger.add("robot_logs.log", rotation="10 MB")  # Log to file
```

**Log Levels:**
- **ERROR**: Connection failures, parameter validation errors
- **WARNING**: Socket cleanup issues, reconnection attempts
- **INFO**: Successful connections, reconnections (default)
- **DEBUG**: Detailed operation information

### Parameter Validation Changes

**BREAKING CHANGE:** Invalid parameters now raise `ValueError` exceptions instead of silently failing.

**Previous behavior (silent failure):**
```python
# Would print "coordinateMode param is wrong" and return empty string
result = dashboard.MovJ(100, 0, 200, 0, 90, 0, coordinateMode=2)  # Invalid
# result == ""
```

**New behavior (raises exception):**
```python
try:
    result = dashboard.MovJ(100, 0, 200, 0, 90, 0, coordinateMode=2)  # Invalid
except ValueError as e:
    # ValueError: Invalid coordinateMode parameter: 2. Expected 0 (pose) or 1 (joint)
    print(f"Error: {e}")
```

**Affected methods:**
- `MovJ`, `MovL`, `MovLIO`, `MovJIO` - invalid `coordinateMode`
- `Arc`, `Circle`, `ArcIO` - invalid `coordinateMode`
- `MovS` - invalid parameters (must provide either `file` or both `points` and `coordinateMode`)
- `RunTo` - invalid `moveType`

**Migration action:** Add try-except blocks around movement commands if your code previously relied on empty string returns.

---

## Feature Comparison Table

| Feature | V3 | V4 | Notes |
|---------|----|----|-------|
| Basic Motion (MovJ/MovL/Arc) | ✓ | ✓ | V4 requires `coordinateMode` |
| Servo Motion | ✓ | ✓ | Parameter name change |
| IO Control | ✓ | ✓ | V4 has more granular commands |
| Force Control | ❌ | ✓ | Completely new in V4 |
| Kinematics (FK/IK) | ❌ | ✓ | New in V4 |
| Coordinate Frames | Basic | Advanced | V4 adds CalcUser/CalcTool |
| Collision Detection | Basic | Advanced | V4 adds sensitivity/backoff |
| SafeSkin Support | ❌ | ✓ | New in V4 |
| Conveyor Tracking | ❌ | ✓ | New in V4 |
| Welding Features | ❌ | ✓ | Arc tracking, weaving |
| Trajectory Playback | Basic | Advanced | V4 adds speed control |
| Error Reporting | Basic | Advanced | V4 multi-language |

---

## Migration Checklist

- [ ] Update imports: `from dobot_api import DobotApiDashboard, DobotApiMove, DobotApiFeedBack`
- [ ] Change feedback port from 30003 to 30004 or 30005
- [ ] Add `coordinateMode` parameter to all MovJ/MovL/Arc/Circle calls
- [ ] Replace `SpeedJ/SpeedL` with `VelJ/VelL`
- [ ] Update `PayLoad()` to `SetPayload()` with new signature
- [ ] Add `mode` parameter to `EmergencyStop()`
- [ ] Replace `JointMovJ()` calls with `MovJ(coordinateMode=1)`
- [ ] Update feedback field access to PascalCase (e.g., `q_actual` → `QActual`)
- [ ] Change `lookahead_time` to `aheadtime` in ServoJ calls
- [ ] Replace `ResetRobot()` with `Stop()` for stopping motion
- [ ] Update relative motion methods to new variants
- [ ] **Add try-except blocks for movement commands** (parameter validation now raises `ValueError`)
- [ ] **Configure logging level** if needed (default INFO, use `DOBOT_LOG_LEVEL` env var)
- [ ] Test all force control, kinematics, and V4-specific features if used

---

## Additional Resources

- See [README.md](README.md) for installation and quick start
- See [examples/](examples/) for working code samples
- Refer to Dobot official documentation for detailed command specifications

---

**Document Version:** 1.0  
**Created:** February 9, 2026  
**Compatible with:** Dobot API V4.0.0
