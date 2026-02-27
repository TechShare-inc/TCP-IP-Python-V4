# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
with [PEP 440](https://peps.python.org/pep-0440/) pre-release tags.

## [4.0.0-alpha.2] — 2026-02-27

### Fixed
- **Documentation overhaul** — removed all references to phantom response
  dataclasses (`AckResponse`, `IntResponse`, `PoseResponse`, `ErrorIdResponse`)
  that never existed in the source code. All docs now describe actual return
  types: `None`, `int`, `Pose`, `tuple[int, ...]`.
- **Version alignment** — `pyproject.toml`, `package.json`, `__init__.py`, and
  Sphinx `conf.py` all report consistent `4.0.0a2`. Previously some files
  showed `4.1.0`.
- **`@forward_to` decorator docs** — rewritten to describe pure delegation
  (no parsing layer). Mermaid diagrams and code examples match the actual
  implementation.
- **`force-control.md`** — `robot.enable_ft_sensor()` corrected to
  `robot.dashboard.enable_ft_sensor()` (not forwarded on `DobotRobot`).
- **`backward-compat.md`** — clarified that `DobotApiFeedBack` alias is
  available via `dobot_api_v4.feedback` but is not in `__init__.__all__`.
- **`architecture.md`** — corrected Layer 3 description from "response parsing
  into typed dataclasses" to "pure delegation to dashboard methods".
- **`installation.md`** — expected version output updated to `4.0.0a2`.

### Changed
- **README modernized** — Quick Start now uses `DobotRobot` façade with
  `snake_case` methods as the primary example. The old `DobotApiDashboard` +
  PascalCase API is preserved in a collapsible "Legacy API" section.
- **README project structure** — updated to reflect the actual `dobot_api_v4/`
  package layout with commands/ sub-package and all 10 mixins.
- **`docs/index.md` hero features** — "Type-Safe Responses" updated to
  "Type-Safe Returns" describing actual `None`/`int`/`Pose`/`tuple` values.

### Added
- **`CHANGELOG.md`** — this file.
- **`_serialization.py` Sphinx docs** — added `.rst` and included in the
  Sphinx toctree and reference index.

## [4.0.0-alpha.1] — 2026-02-01

### Added
- Mixin-based dashboard architecture — 10 command mixins composed into
  `DobotApiDashboard` via multiple inheritance.
- `DobotRobot` high-level façade with `@forward_to` decorator for ~25
  commonly-used commands.
- `AlarmI18n` class for offline multi-language alarm translation (10 languages).
- `RobotErrorMonitor` with HTTP-based alarm retrieval on port 22000.
- `DobotApiFeedback` for binary feedback data on ports 30004/30005/30006.
- `FeedbackData` frozen dataclass and numpy-based `FeedbackDtype`.
- `Pose` dataclass for 6-DOF positions.
- PascalCase backward-compatibility aliases for all commands.
- Full unit test suite for all 10 mixins, parse utilities, serialization,
  feedback, and robot forwarding.
- VitePress documentation site with getting-started, how-to, tutorial,
  explanation, and reference sections.
- Sphinx autodoc pipeline generating Markdown API reference pages.
- Four example programs: `basic_demo.py`, `basic_move.py`,
  `error_handling.py`, `i18n_demo.py`.
