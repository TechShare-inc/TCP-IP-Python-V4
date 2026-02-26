# Copilot Instructions for TCP-IP-Python-V4

## Project Overview

This is the Python SDK for Dobot V4 robots, communicating over TCP/IP.

## Architecture

- See `v4-refactoring-spec.md` for the full architecture specification.
- See `REFACTORING_PLAN.md` for the step-by-step execution plan.

## Key Patterns

- **Mixin-based composition**: Dashboard commands are split into 10 mixins
  (`_system_mixin.py`, `_config_mixin.py`, etc.) composed into
  `DobotApiDashboard` via multiple inheritance.
- **snake_case methods** with PascalCase backward-compat aliases (e.g.,
  `enable_robot` + `EnableRobot = enable_robot`).
- **`DobotRobot`** is the unified high-level façade; it delegates to
  `dashboard`, `feedback`, and `errors` sub-objects.
- **`@forward_to` decorator** in `_forward.py` delegates `DobotRobot` methods
  to the dashboard and parses responses into typed dataclasses.
- **Feedback** connections (ports 30004/30005/30006) are lazily created.
- **Error monitoring** uses HTTP on port 22000, not TCP.

## Conventions

- All new code uses Google-style docstrings.
- Type annotations on all public APIs (Python 3.9+).
- Protocol command strings are built with `str.format()`, not f-strings.
- Tests use `pytest` with markers: `unit`, `integration`, `hil`.
