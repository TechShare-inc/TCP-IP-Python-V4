---
type: reference
---

# Port Reference

The Dobot V4 controller exposes five network ports for different communication purposes.

## Overview

| Port  | Protocol    | Direction       | Class                | Purpose                        |
| ----- | ----------- | --------------- | -------------------- | ------------------------------ |
| 29999 | TCP (text)  | Request/Reply   | `DobotApiDashboard`  | Dashboard commands             |
| 30004 | TCP (binary)| Server → Client | `DobotApiFeedback`   | Real-time feedback (8 ms)      |
| 30005 | TCP (binary)| Server → Client | `DobotApiFeedback`   | Real-time feedback (200 ms)    |
| 30006 | TCP (binary)| Server → Client | `DobotApiFeedback`   | Real-time feedback (configurable) |
| 22000 | HTTP (JSON) | Request/Reply   | `RobotErrorMonitor`  | Error/alarm information        |

## Port 29999 — Dashboard

- **Protocol**: Line-oriented text over TCP.
- **Command format**: `CommandName(param1,param2,...)`
- **Response format**: `error_code,{payload};` or `error_code,command_id,value;`
- **Threading**: Thread-safe — `send_recv_msg()` is protected by a lock.
- **Multiplexing**: Only one active request at a time per connection.
- **Used by**: `DobotApiDashboard`, and `DobotRobot` (which delegates via `@forward_to`).

## Port 30004 — 8 ms Feedback

- **Protocol**: Binary push stream over TCP.
- **Packet size**: 1440 bytes per cycle.
- **Cycle time**: 8 ms (125 Hz).
- **Use case**: High-frequency control loops, servo commanding, real-time monitoring.
- **Access**: `robot.feedback` (lazy connection on `DobotRobot`).

## Port 30005 — 200 ms Feedback

- **Protocol**: Same binary format as 30004.
- **Packet size**: 1440 bytes per cycle.
- **Cycle time**: 200 ms (5 Hz).
- **Use case**: General monitoring, UI updates, logging.
- **Access**: `robot.feedback_30005`.

## Port 30006 — Configurable Feedback

- **Protocol**: Same binary format as 30004.
- **Packet size**: 1440 bytes per cycle.
- **Cycle time**: Configurable via the controller.
- **Use case**: Custom applications with specific update rate requirements.
- **Access**: `robot.feedback_30006`.

## Port 22000 — Error Monitor

- **Protocol**: HTTP GET returning JSON.
- **Endpoint**: `http://{ip}:22000/`
- **Content**: Current error/alarm information with alarm IDs.
- **Use case**: Periodic error polling, alarm logging.
- **Access**: `RobotErrorMonitor(robot_ip)`, or `robot.errors` on `DobotRobot`.

## Firewall Notes

Ensure the following ports are open between the client machine and the robot controller:

- **TCP outbound**: 29999, 30004, 30005, 30006
- **HTTP outbound**: 22000

If you only use `DobotRobot` with default settings, port 29999 is opened immediately. Feedback ports (30004–30006) are opened on demand when first accessed.
