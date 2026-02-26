---
type: explanation
---

# Internationalization (i18n) Design

The SDK supports alarm descriptions in 10 languages. This page explains the design decisions behind the i18n system.

## Why i18n for Alarms?

Dobot robots are deployed worldwide. When a robot reports alarm ID `16`, the operator needs to understand what went wrong and how to fix it — in their own language. The SDK provides offline translation of alarm codes into human-readable descriptions and solutions.

## Architecture

```
dobot_api_v4/
└── locales/
    ├── alarms.en.yml       # English
    ├── alarms.zh_CN.yml    # Simplified Chinese
    ├── alarms.zh_Hant.yml  # Traditional Chinese
    ├── alarms.ja.yml       # Japanese
    ├── alarms.ko.yml       # Korean
    ├── alarms.de.yml       # German
    ├── alarms.fr.yml       # French
    ├── alarms.es.yml       # Spanish
    ├── alarms.ru.yml       # Russian
    └── alarms.vi.yml       # Vietnamese
```

Each YAML file contains two sections:

```yaml
controller:
  "16":
    level: warning
    description: "Description text..."
    solution: "Solution text..."
  "17":
    ...

servo:
  "8752":
    description: "Description text..."
    solution: "Solution text..."
```

## Why YAML?

- **Human-editable**: Translators can edit YAML files without programming knowledge.
- **Structured**: Supports nested keys (alarm ID → fields) naturally.
- **Widely supported**: YAML is a standard format with tooling in every language.

Alternatives considered:
- **JSON**: More verbose for multi-line strings. No comments.
- **gettext (.po)**: Standard for app i18n but overkill for a lookup table of alarm descriptions.
- **Hardcoded dictionaries**: The V3 SDK used this approach — it was impossible to maintain across languages.

## The AlarmI18n Class

`AlarmI18n` wraps the `python-i18n` library and provides:

1. **Language selection**: `set_language("ja")` switches all subsequent lookups.
2. **Auto-detection**: `get_alarm(id)` determines whether an ID is a controller or servo alarm based on the numeric range.
3. **Formatted output**: `format_alarm(id)` returns a pre-formatted multi-line string.
4. **Data enrichment**: `enrich_alarm_data(dict)` takes raw robot data and adds translated fields.

## Language Code Normalization

Users provide language codes in various formats. The SDK normalizes them:

| User Input   | Normalized    | Locale File          |
| ------------ | ------------- | -------------------- |
| `en`         | `en`          | `alarms.en.yml`      |
| `zh_cn`      | `zh_CN`       | `alarms.zh_CN.yml`   |
| `zh-CN`      | `zh_CN`       | `alarms.zh_CN.yml`   |
| `zh_tw`      | `zh_Hant`     | `alarms.zh_Hant.yml` |
| `zh-Hant`    | `zh_Hant`     | `alarms.zh_Hant.yml` |
| `ja`         | `ja`          | `alarms.ja.yml`      |

This prevents common mistakes with case and separator variations.

## Controller vs. Servo Alarms

Dobot alarm IDs are divided into two namespaces:

- **Controller alarms**: Lower ID numbers, reported by the main controller.
- **Servo alarms**: Higher ID numbers, reported by individual joint servo drives.

The `get_alarm()` method auto-detects the type based on the ID range. If you know the type, use `get_controller_alarm()` or `get_servo_alarm()` directly to avoid ambiguity.

## Offline Operation

`AlarmI18n` requires no robot connection. The YAML files are bundled with the package and loaded at instantiation time. This enables:

- Building alarm lookup UIs without a robot
- Translating alarm IDs from stored logs
- Testing alarm handling in CI environments

## Integration with RobotErrorMonitor

`RobotErrorMonitor` retrieves alarm IDs from the robot via HTTP. It can optionally use `AlarmI18n` to enrich the raw data with translations:

```python
monitor = RobotErrorMonitor("192.168.1.6")
i18n = AlarmI18n("en")

raw = monitor.get_error_info("en")
if raw:
    for alarm in raw:
        details = i18n.get_alarm(alarm["id"])
        print(f"{details['description']}: {details['solution']}")
```

## Adding a New Language

To add a new language (e.g., Portuguese):

1. Create `dobot_api_v4/locales/alarms.pt.yml` following the structure of existing files.
2. Translate all controller and servo alarm entries.
3. The `AlarmI18n` class will automatically detect and load the new file.
4. Update `pyproject.toml` to include the new `.yml` in package data (already covered by the `locales/*.yml` glob).
