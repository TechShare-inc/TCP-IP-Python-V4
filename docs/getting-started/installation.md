---
type: how-to
---

# Installation

## Requirements

- **Python** 3.9 or later (3.9, 3.10, 3.11, 3.12 are tested)
- **Network access** to the Dobot V4 robot controller (default IP: `192.168.1.6`)
- **Ports**: 29999 (dashboard), 30004/30005/30006 (feedback), 22000 (error monitor)

## Install from PyPI

```bash
pip install dobot-api-v4
```

## Install from Source (Editable)

Clone the repository and install in editable mode:

```bash
git clone https://github.com/Dobot-Arm/TCP-IP-Python-V4.git
cd TCP-IP-Python-V4
pip install -e .
```

## Install with Development Dependencies

```bash
pip install -e ".[dev]"
```

This adds `pytest`, `pytest-cov`, `pytest-mock`, and `mypy`.

## Install with Documentation Dependencies

```bash
pip install -e ".[docs]"
```

This adds `sphinx`, `myst-parser`, `sphinx-autodoc2`, and `sphinx-markdown-builder`.

## Verify Installation

```bash
python -c "import dobot_api_v4; print(dobot_api_v4.__version__)"
```

**Expected Output:**

> ```
> 4.1.0
> ```

## Logging Configuration

The SDK uses [loguru](https://github.com/Delgan/loguru) for logging. Control the log level with the `DOBOT_LOG_LEVEL` environment variable:

```bash
# Show debug messages
export DOBOT_LOG_LEVEL=DEBUG   # Linux/macOS
set DOBOT_LOG_LEVEL=DEBUG      # Windows cmd
$env:DOBOT_LOG_LEVEL = "DEBUG" # PowerShell
```

Valid levels: `DEBUG`, `INFO` (default), `WARNING`, `ERROR`, `CRITICAL`.

## Next Steps

Proceed to the [Quick Start](./quick-start.md) to connect to your first robot.
