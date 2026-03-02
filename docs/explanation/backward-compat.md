---
type: explanation
---

# Backward Compatibility Strategy

The SDK maintains backward compatibility with earlier Dobot Python SDKs through PascalCase method aliases and class name aliases.

## PascalCase Method Aliases

Every command method has two names:

```python
# Primary (new code should use this)
dashboard.enable_robot()

# Alias (backward compatible)
dashboard.EnableRobot()
```

Both call the exact same function. The alias is implemented as a simple assignment at the end of each mixin:

```python
class _SystemMixin:
    def enable_robot(self, ...):
        ...

    def disable_robot(self, ...):
        ...

    # Backward-compat aliases
    EnableRobot = enable_robot
    DisableRobot = disable_robot
```

### Why Keep Both?

1. **Migration path**: Existing codebases using the V3 SDK can upgrade to V4 without immediately renaming every method call.
2. **Protocol alignment**: PascalCase names match the protocol command names (`EnableRobot()`, `MovJ()`, `GetPose()`), which can be helpful when reading protocol documentation.
3. **Zero cost**: Aliases are just additional references to the same function object — no wrapper, no performance overhead.

### Recommendation

Use `snake_case` in new code. It follows Python conventions (PEP 8) and is the primary name that appears in docstrings, type stubs, and documentation.

## Class Name Aliases

Similar backward-compat aliases exist at the class level:

| Primary Name        | Alias                    | Reason                            |
| ------------------- | ------------------------ | --------------------------------- |
| `DobotApiFeedback`  | `DobotApiFeedBack`       | Old SDK used inconsistent casing  |

Both names are available in the `dobot_api_v4.feedback` module. The primary name `DobotApiFeedback` is exported in `__init__.__all__`:

```python
from dobot_api_v4 import DobotApiFeedback         # primary
from dobot_api_v4.feedback import DobotApiFeedBack  # alias (not in __all__)
```

## Method Name Mapping

The `PROTOCOL_FIELD_MAP` in `dtypes.py` provides a mapping from old PascalCase field names to new `snake_case` names for feedback data fields:

```python
PROTOCOL_FIELD_MAP = {
    "DigitalInputs": "digital_inputs",
    "RobotMode": "robot_mode",
    "QActual": "q_actual",
    ...
}
```

This is useful when migrating code that accessed feedback data using the old field names.

## When Will Aliases Be Removed?

Currently there is no deprecation timeline. The aliases add negligible maintenance burden (a single line per method) and significantly ease migration. If removal is ever planned, a deprecation warning period will be announced first.
