---
type: reference
---

# Feedback Fields

The `FeedbackData` dataclass contains all fields from the 1440-byte binary feedback packet. Fields are grouped by category.

## Packet Metadata

| Field | Type  | Description                                  |
| ----- | ----- | -------------------------------------------- |
| `len` | `int` | Packet length (bytes)                        |

## Status Scalars

| Field                | Type  | Description                                    |
| -------------------- | ----- | ---------------------------------------------- |
| `digital_inputs`     | `int` | Digital input bitmask (all DI pins)            |
| `digital_outputs`    | `int` | Digital output bitmask (all DO pins)           |
| `robot_mode`         | `int` | Current robot mode (see [Robot Modes](./robot-modes.md)) |
| `time_stamp`         | `int` | Controller timestamp (ms)                      |
| `run_time`           | `int` | Total run time (ms)                            |
| `test_value`         | `int` | Magic value `0x123456789ABCDEF` for validation |
| `speed_scaling`      | `float` | Current speed scaling factor                 |
| `v_robot`            | `float` | Robot velocity                               |
| `i_robot`            | `float` | Robot current                                |
| `program_state`      | `float` | Program execution state                      |
| `safety_o_in`        | `int` | Safety controller input                        |
| `safety_o_out`       | `int` | Safety controller output                       |

## Joint Arrays (6 elements)

| Field                | Type                 | Description                   |
| -------------------- | -------------------- | ----------------------------- |
| `q_target`           | `tuple[float, ...]`  | Target joint angles (°)       |
| `qd_target`          | `tuple[float, ...]`  | Target joint velocities (°/s) |
| `qdd_target`         | `tuple[float, ...]`  | Target joint accelerations    |
| `i_target`           | `tuple[float, ...]`  | Target joint currents (A)     |
| `m_target`           | `tuple[float, ...]`  | Target joint torques (N·m)    |
| `q_actual`           | `tuple[float, ...]`  | Actual joint angles (°)       |
| `qd_actual`          | `tuple[float, ...]`  | Actual joint velocities (°/s) |
| `i_actual`           | `tuple[float, ...]`  | Actual joint currents (A)     |
| `m_actual`           | `tuple[float, ...]`  | Actual joint torques (N·m)    |
| `v_actual`           | `tuple[float, ...]`  | Actual joint voltages (V)     |
| `motor_temperatures` | `tuple[float, ...]`  | Motor temperatures (°C)       |
| `joint_modes`        | `tuple[float, ...]`  | Individual joint modes        |

## TCP (Tool Center Point) Arrays (6 elements)

| Field                | Type                 | Description                            |
| -------------------- | -------------------- | -------------------------------------- |
| `actual_tcp_force`   | `tuple[float, ...]`  | Actual TCP force (Fx,Fy,Fz,Mx,My,Mz)  |
| `tool_vector_actual` | `tuple[float, ...]`  | Actual TCP pose (x,y,z,rx,ry,rz)      |
| `tcp_speed_actual`   | `tuple[float, ...]`  | Actual TCP speed                       |
| `tcp_force`          | `tuple[float, ...]`  | TCP force reading                      |
| `tool_vector_target` | `tuple[float, ...]`  | Target TCP pose                        |
| `tcp_speed_target`   | `tuple[float, ...]`  | Target TCP speed                       |

## Byte-Sized Status Flags

| Field                    | Type  | Description                         |
| ------------------------ | ----- | ----------------------------------- |
| `hand_type`              | `tuple[int, ...]` | End-effector type (4 bytes) |
| `user`                   | `int` | Active user coordinate index        |
| `tool`                   | `int` | Active tool coordinate index        |
| `run_queued_cmd`         | `int` | Running queued command flag         |
| `pause_cmd_flag`         | `int` | Paused command flag                 |
| `velocity_ratio`         | `int` | Current velocity ratio              |
| `acceleration_ratio`     | `int` | Current acceleration ratio          |
| `xyz_velocity_ratio`     | `int` | Cartesian velocity ratio            |
| `r_velocity_ratio`       | `int` | Rotation velocity ratio             |
| `xyz_acceleration_ratio` | `int` | Cartesian acceleration ratio        |
| `r_acceleration_ratio`   | `int` | Rotation acceleration ratio         |
| `brake_status`           | `int` | Brake engaged (1) or released (0)   |
| `enable_status`          | `int` | Robot enabled (1) or disabled (0)   |
| `drag_status`            | `int` | Drag mode active (1) or not (0)     |
| `running_status`         | `int` | Motion running (1) or idle (0)      |
| `error_status`           | `int` | Error present (1) or clear (0)      |
| `jog_status_cr`          | `int` | Jog mode status                     |
| `cr_robot_type`          | `int` | Robot model type identifier         |
| `drag_button_signal`     | `int` | Drag button physical state          |
| `enable_button_signal`   | `int` | Enable button physical state        |
| `record_button_signal`   | `int` | Record button physical state        |
| `reappear_button_signal` | `int` | Reappear button physical state      |
| `jaw_button_signal`      | `int` | Jaw button physical state           |
| `six_force_online`       | `int` | Force sensor connected (1) or not   |
| `collision_state`        | `int` | Collision detected (1) or not       |
| `arm_approach_state`     | `int` | Arm approach warning                |
| `j4_approach_state`      | `int` | J4 approach limit warning           |
| `j5_approach_state`      | `int` | J5 approach limit warning           |
| `j6_approach_state`      | `int` | J6 approach limit warning           |

## Extended Fields

| Field               | Type                 | Description                        |
| ------------------- | -------------------- | ---------------------------------- |
| `vibration_dis_z`   | `float`              | Z-axis vibration displacement      |
| `current_command_id`| `int`                | ID of the latest completed command |
| `load`              | `float`              | Payload weight (kg)                |
| `center_x`          | `float`              | Payload CoG X offset (mm)         |
| `center_y`          | `float`              | Payload CoG Y offset (mm)         |
| `center_z`          | `float`              | Payload CoG Z offset (mm)         |
| `user_coords`       | `tuple[float, ...]`  | Active user coordinate values (6)  |
| `tool_coords`       | `tuple[float, ...]`  | Active tool coordinate values (6)  |
| `six_force_value`   | `tuple[float, ...]`  | Force sensor values (Fx,Fy,Fz,Mx,My,Mz) |
| `target_quaternion` | `tuple[float, ...]`  | Target orientation quaternion (4)  |
| `actual_quaternion` | `tuple[float, ...]`  | Actual orientation quaternion (4)  |
| `auto_manual_mode`  | `int`                | 0 = auto, 1 = manual              |
| `export_status`     | `int`                | Log export status                  |
| `safety_state`      | `int`                | Safety system state                |

## Packet Validation

Each feedback packet contains a `test_value` field with the magic number `0x123456789ABCDEF`. Verify this value to confirm the packet was received and parsed correctly:

```python
data = robot.feedback_data()
if data and data.test_value == 0x123456789ABCDEF:
    print("Valid packet")
```
