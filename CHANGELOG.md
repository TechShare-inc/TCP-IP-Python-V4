# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
with [PEP 440](https://peps.python.org/pep-0440/) pre-release tags.

## [4.0.0-alpha.2] — `7ef2b55`

### Added
- **`@forward_to` pure-delegation decorator** (`_forward.py`) — rewrote the
  decorator to perform pure delegation to `self.dashboard` instead of
  parsing through response dataclasses.  Methods on `DobotRobot` now return
  typed values directly from the dashboard mixin layer (`cd6dd2d`).
- **Expanded `DobotRobot` commands** — added forwarded methods for
  `run_script`, `brake_control`, `request_control`, `user`, `tool`,
  `set_payload`, `set_collision_level`, `arc`, `circle`, relative motion
  commands, and force/digital/analog I/O commands.  `DobotRobot` grew from
  ~289 to ~750 lines (`edf2aa0`).
- **`commands/_parse.py` module** — consolidated all response-parsing logic
  into a single module with `parse_response`, `parse_ack`, `parse_int`,
  `parse_pose`, `parse_error_ids`, and `DobotApiError`.  Added Sphinx RST
  and included in the toctree (`38387ab`).
- **V4 brace-command wire format** — `parse_response` now handles
  `error_code,{payload},CommandName();` format in addition to the classic
  3-field and legacy brace formats (`974e3a9`).
- **`basic_move.py` example** — new example demonstrating joint-state
  reading and motion offsets (`6b2c9bc`).
- **`CHANGELOG.md`** — this file (`38af71b`).
- **`_serialization.py` Sphinx docs** — added `.rst` and included in the
  Sphinx toctree and reference index (`38af71b`).

### Changed
- **README modernized** — Quick Start now uses `DobotRobot` façade with
  `snake_case` methods as the primary example; old `DobotApiDashboard` +
  PascalCase API preserved in a collapsible "Legacy API" section.  Updated
  project structure table to match the actual layout (`38af71b`).
- **Documentation overhaul** — removed all references to phantom response
  dataclasses (`AckResponse`, `IntResponse`, `PoseResponse`,
  `ErrorIdResponse`).  Rewrote `forward-decorator.md`, `architecture.md`,
  `backward-compat.md`, `installation.md`, `quick-start.md`,
  `first-program.md`, `facade-vs-dashboard.md`, `force-control.md`,
  `docs/index.md`, and `reference/index.md` to describe actual return types
  and the pure-delegation pattern (`38af71b`).
- **Examples rewritten** — `basic_demo.py`, `error_handling.py`, and
  `i18n_demo.py` updated for the new typed-return API style (`e778d72`).
- **Version alignment** — `pyproject.toml`, `package.json`, `__init__.py`,
  and Sphinx `conf.py` all report consistent `4.0.0a2` (`38af71b`).

### Fixed
- **Socket closure** — `DobotApi.close()` now uses `contextlib.suppress`
  for safe socket shutdown, preventing exceptions on already-closed
  sockets (`5874419`).
- **Motion command return values** — motion methods now return the queue
  command ID as `int` instead of raw strings (`b5fd4ed`).

### Removed
- **`responses.py` module** — deleted along with `AckResponse`,
  `IntResponse`, `PoseResponse`, `ErrorIdResponse` dataclasses.  All
  parsing moved to `commands/_parse.py` (`38387ab`).
- **PascalCase backward-compat aliases** — removed from all 10 command
  mixins, `dashboard.py` re-export shim, `DobotApiFeedBack` alias in
  `feedback.py`, and `MyType` alias in `base.py`.  The `snake_case` API is
  now the only API (`2a03585`).
- **`examples/main.py`** — removed obsolete entry-point script (`e778d72`).
- **Old unit tests** — `test_responses.py` and per-mixin test stubs
  (`test_check.py`, `test_config.py`, etc.) replaced by `test_parse.py`
  and expanded `test_robot.py` (`38387ab`).

## [4.0.0-alpha.1] — `94f0a2f`

### Added
- **Mixin-based dashboard architecture** — 10 command mixins
  (`_system_mixin.py`, `_config_mixin.py`, `_motion_mixin.py`,
  `_io_mixin.py`, `_query_mixin.py`, `_force_mixin.py`,
  `_modbus_mixin.py`, `_conveyor_mixin.py`, `_weld_mixin.py`,
  `_check_mixin.py`) composed into `DobotApiDashboard` via multiple
  inheritance.
- **`DobotRobot` high-level façade** with `@forward_to` decorator
  delegating ~25 commands through response dataclass parsing.
- **`responses.py`** with `AckResponse`, `IntResponse`, `PoseResponse`,
  `ErrorIdResponse` dataclasses and `parse_response` dispatcher.
- **`AlarmI18n`** class for offline multi-language alarm translation
  (10 languages: EN, ZH, JA, KO, DE, FR, ES, RU, VI, ZH-Hant).
- **`RobotErrorMonitor`** with HTTP-based alarm retrieval on port 22000.
- **`DobotApiFeedback`** for binary feedback data on ports
  30004/30005/30006.
- **`FeedbackData`** frozen dataclass and numpy-based `FeedbackDtype`.
- **`Pose`** dataclass for 6-DOF positions.
- **PascalCase backward-compatibility aliases** for all commands.
- **Unit test suite** for all 10 mixins, response parsing, serialization,
  feedback, and robot forwarding.
- **VitePress documentation site** with getting-started, how-to, tutorial,
  explanation, and reference sections.
- **Sphinx autodoc pipeline** generating Markdown API reference pages.
- **Example programs** — `basic_demo.py`, `error_handling.py`,
  `i18n_demo.py`.
- **`set_robot_ip.py`** utility script for static IP / DHCP configuration.
- **`build-docs.ps1` / `build-docs.sh`** — Sphinx + VitePress build
  scripts.
