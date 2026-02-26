# Code Style

This page defines the code-style rules enforced across the `dobot_api_v4` codebase.
All contributors — human and AI — must follow these conventions.

## Python Version

- Target: **Python 3.9+** (`requires-python = ">=3.9"`).
- Use `from __future__ import annotations` only when necessary; prefer
  `typing` imports available in 3.9.

## Formatting & Linting

All style enforcement is configured in `pyproject.toml` — no standalone config
files (`.flake8`, `tox.ini`, etc.) are allowed.

| Tool | Purpose | Command |
|------|---------|---------|
| **Ruff** (lint) | Lint and auto-fix | `uv run ruff check .` |
| **Ruff** (format) | Code formatting | `uv run ruff format .` |
| **mypy** (strict) | Static type checking | `uv run mypy dobot_api_v4` |

### Ruff rules

```toml
[tool.ruff]
target-version = "py39"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "SIM"]
```

| Rule Set | Scope |
|----------|-------|
| `E`, `W` | pycodestyle errors & warnings |
| `F` | pyflakes |
| `I` | isort (import ordering) |
| `N` | pep8-naming |
| `UP` | pyupgrade (modern syntax) |
| `B` | flake8-bugbear |
| `A` | flake8-builtins |
| `SIM` | flake8-simplify |

### mypy configuration

```toml
[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
warn_unused_configs = true
warn_unused_ignores = true
no_implicit_reexport = true
```

## Naming Conventions

### Modules

All `.py` files use `snake_case` — e.g., `error_monitor.py`, `i18n_manager.py`.

### Classes

| Rule | Example |
|------|---------|
| `PascalCase`, one capital per word boundary | `DobotApiFeedback`, `RobotErrorMonitor` |
| No mid-word capitals | `Feedback` not `FeedBack`; `Payload` not `PayLoad` |
| Acronyms ≤ 2 chars: uppercase | `DobotApi`, `MovJIO` |
| Acronyms ≥ 3 chars: title-case | `TcpSpeed` not `TCPSpeed` |

### Methods & Functions

| Rule | Example |
|------|---------|
| All public/private methods | `snake_case` |
| Protected methods | `_snake_case` (single underscore) |
| Protocol commands | `snake_case` mapped from PascalCase wire name |

### Parameters & Variables

| Rule | Example |
|------|---------|
| All `snake_case` | `center_x`, `offset_z`, `is_rtu` |
| Booleans: `is_`, `has_`, `should_`, `can_` prefix | `is_rtu`, `is_enabled` |
| Private instance variables | `_snake_case` (single underscore) |
| Never `camelCase` | `robotMode` → `robot_mode` |

### Constants

`UPPER_SNAKE_CASE` — e.g., `SERVO_ID_MIN`, `SUPPORTED_LANGUAGES`, `PROTOCOL_FIELD_MAP`.

### Type Aliases

`PascalCase` and descriptive — e.g., `FeedbackDtype`, `DynParam`, `ToolDynParam`.

## Backward-Compatibility Aliases

Every `snake_case` public method that maps to a PascalCase protocol name must
have a class-level alias so legacy code continues to work:

```python
def enable_robot(self, ...) -> str:
    """Enable the robot."""
    ...

# Backward-compat alias
EnableRobot = enable_robot
```

The alias is a simple assignment **immediately** after the method definition.
No wrapper functions, no `__getattr__` magic.

## Type Annotations

- **All public APIs** must have full type annotations (parameters + return).
- Use `from typing import Optional, Union, Any` for 3.9 compatibility when
  needed.
- Autodoc renders type hints via `autodoc_typehints = "description"`.

```python
def get_alarm(
    self,
    alarm_id: int,
    alarm_type: Optional[str] = None,
    field: Optional[str] = None,
) -> dict[str, Any]:
```

## Docstrings

All public APIs use **Google-style docstrings** with these sections
(when applicable): `Args:`, `Returns:`, `Raises:`, `Example:` / `Usage::`.

```python
def speed_factor(self, speed: int) -> str:
    """Set global speed factor.

    Args:
        speed: Rate value in range 1-100.

    Returns:
        Raw response string from robot.

    Usage::

        dashboard.speed_factor(40)
    """
```

::: tip
For docstrings that include code examples, use the `Usage::` block
(reStructuredText literal block) rather than `Example:` with `>>>` doctest
syntax. This ensures compatibility with `sphinx-markdown-builder`.
:::

## Protocol Command Strings

Command strings sent over TCP use `str.format()` or f-strings with explicit
format specifiers — **never** bare f-string interpolation without a format spec:

```python
# Correct — explicit format specifiers
string = f"EnableRobot({load:f},{center_x:f},{center_y:f},{center_z:f})"

# Correct — using _build_cmd helper
return self.send_recv_msg(self._build_cmd("SpeedFactor", speed))

# Wrong — bare interpolation (no format control)
string = f"EnableRobot({load})"
```

The `_build_cmd` and `_fmt` methods in `_SerializationMixin` handle formatting
automatically for most commands.

## Imports

Import order is enforced by Ruff's `I` (isort) rule set:

1. **Standard library** (`os`, `sys`, `typing`, …)
2. **Third-party** (`numpy`, `loguru`, `i18n`, …)
3. **Local** (relative imports: `from .base import ...`, `from ._serialization import ...`)

```python
"""System and lifecycle commands for Dobot V4 API."""

from ._serialization import _SerializationMixin
```

## Logging

- Use `loguru.logger` — configured in `__init__.py`, controlled by
  `DOBOT_LOG_LEVEL` environment variable.
- Log levels:

| Level | Usage |
|-------|-------|
| `debug` | Wire data, command strings |
| `info` | Lifecycle transitions (startup, shutdown, connections) |
| `warning` | Unimplemented methods, missing locale files |
| `error` | Alarm details, exception context |

```python
from loguru import logger

logger.debug(f"Sending command: {command}")
logger.info("Dashboard connected on port 29999")
```

## Editor Settings

| File Type | Indentation | Line Ending |
|-----------|-------------|-------------|
| Python (`.py`) | 4 spaces | LF |
| YAML / JSON | 2 spaces | LF |
| Markdown (`.md`) | 2 spaces | LF |
| TypeScript (`.ts`) | 2 spaces | LF |

All files must end with a final newline.

## File Organization

- **No** `setup.py`, `setup.cfg`, or `requirements*.txt` —
  `pyproject.toml` is the single source of metadata.
- **No** standalone tool config files — all tool config lives in `pyproject.toml`.
- Scripts directory uses `.ps1` (PowerShell) and `.sh` (Bash) files.
- Auto-generated files (e.g., `docs/reference/api/*.md`) must not be manually
  edited.
