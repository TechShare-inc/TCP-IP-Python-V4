---
type: reference
---

# Glossary

Key terms and abbreviations used throughout this documentation.

## A

**Alarm**
: An error or warning condition reported by the robot controller. Alarms have numeric IDs and are categorized as controller alarms or servo alarms.

**Arc (motion)**
: A circular motion through three points (start, intermediate, end). See `arc()` in the motion commands.

## C

**Command ID**
: A sequential integer assigned to each queued command. Used to track whether a specific command has completed by comparing against `current_command_id` in feedback data.

**Continuous Path (CP)**
: A motion mode where the robot blends between consecutive waypoints without stopping at each one. The CP ratio controls the blend radius.

**Controller Alarm**
: An alarm originating from the robot's main controller (as opposed to individual servo drives). Usually has lower ID numbers.

**Coordinate Mode**
: Specifies how position values are interpreted: `0` = joint coordinates (degrees), `1` = Cartesian coordinates (mm and degrees).

## D

**Dashboard**
: The command interface on TCP port 29999. The term comes from the Dobot protocol naming. All robot commands are sent through this port.

**Drag Mode**
: A mode where the robot's joints are free to be moved by hand, used for teaching positions.

## E

**Emergency Stop (E-Stop)**
: An immediate halt of all robot motion. Can be triggered via hardware button or software command.

## F

**Facade**
: The `DobotRobot` class, which provides a simplified, unified interface over the underlying dashboard, feedback, and error monitor components.

**FC Mode (Force Compliance)**
: A control mode where the robot complies with external forces along specified axes, useful for assembly tasks like insertion and polishing.

**Feedback**
: Binary data packets streamed by the robot at fixed intervals (8 ms, 200 ms, or configurable) containing the full robot state.

**Forward Decorator (`@forward_to`)**
: A Python decorator used in `DobotRobot` that delegates method calls to the dashboard and parses raw string responses into typed dataclasses.

## I

**I18n (Internationalization)**
: Support for multiple languages. The SDK includes alarm descriptions in 10 languages via YAML locale files and the `AlarmI18n` class.

## J

**Jog**
: Manual control mode where the robot moves along a single axis at a time, typically used for setup and calibration.

**Joint Coordinates**
: Robot position expressed as individual joint angles (J1–J6) in degrees.

## M

**Mixin**
: A Python class that provides a group of related methods, composed via multiple inheritance. The SDK uses 10 mixins to organize ~155 dashboard commands.

**Modbus**
: An industrial communication protocol. The Dobot controller can act as a Modbus TCP or RTU master to communicate with PLCs and sensors.

## P

**PascalCase Alias**
: A backward-compatible method name (e.g., `EnableRobot`) that maps to the primary `snake_case` name (e.g., `enable_robot`). Present on all dashboard commands.

**Payload**
: The weight and center of gravity of the end-effector and workpiece attached to the robot flange.

## S

**SafeSkin**
: A collision sensing skin that can be attached to the robot body for enhanced safety.

**Servo Control**
: Low-level position control mode (`ServoJ`/`ServoP`) where the application sends target positions at a fixed frequency (typically 125 Hz).

**Servo Alarm**
: An alarm from an individual joint servo drive. Usually has higher ID numbers than controller alarms.

## T

**TCP (Tool Center Point)**
: The reference point at the end of the robot tool, defined by the tool coordinate system. Position commands typically refer to the TCP location.

**TCP (Transmission Control Protocol)**
: The network protocol used for dashboard commands (port 29999) and binary feedback (ports 30004–30006). Context determines which meaning applies.

**Tool Coordinate System**
: A coordinate frame attached to the robot's end-effector (tool). Defines where the TCP is relative to the robot flange.

## U

**User Coordinate System**
: A custom reference frame defined by the user, typically aligned to a workpiece or fixture. Cartesian motions can be expressed in any user coordinate system.

## W

**Weave Pattern**
: An oscillating motion perpendicular to the weld path, used in welding to improve weld bead quality and coverage.
