---
type: how-to
---

# How to Use Multi-Language Alarms

The `AlarmI18n` class provides offline translation of alarm codes into 10 languages. It reads YAML locale files bundled with the SDK.

## Basic Setup

```python
from dobot_api_v4 import AlarmI18n

i18n = AlarmI18n(default_language="en")
```

## Look Up a Controller Alarm

```python
alarm = i18n.get_controller_alarm(16)
print(f"ID:          {alarm['id']}")
print(f"Level:       {alarm['level']}")
print(f"Description: {alarm['description']}")
print(f"Solution:    {alarm['solution']}")
```

## Look Up a Servo Alarm

```python
alarm = i18n.get_servo_alarm(8752)
print(f"Description: {alarm['description']}")
print(f"Solution:    {alarm['solution']}")
```

## Auto-Detect Alarm Type

The `get_alarm()` method determines whether an ID is a controller or servo alarm based on its range:

```python
alarm = i18n.get_alarm(16)      # → controller
alarm = i18n.get_alarm(8752)    # → servo
print(f"Type: {alarm['type']}")
```

## Switch Languages Dynamically

```python
for lang in ["en", "zh_CN", "ja", "de", "ko", "fr", "es", "ru", "vi"]:
    i18n.set_language(lang)
    alarm = i18n.get_controller_alarm(16)
    print(f"[{lang:7s}] {alarm['description']}")
```

## Get Current Language

```python
current = i18n.get_current_language()
print(f"Current language: {current}")
```

## Format an Alarm for Display

```python
formatted = i18n.format_alarm(16)
print(formatted)
```

This returns a pre-formatted multi-line string with ID, type, level, description, and solution.

## Enrich Robot Data

Given a raw data dict from the robot, add translated fields:

```python
robot_data = {
    "id": 16,
    "mode": "warning",
    "date": "2026-02-26",
    "time": "14:30:00",
}

enriched = i18n.enrich_alarm_data(robot_data)
print(f"Type:        {enriched['type']}")
print(f"Level:       {enriched['level']}")
print(f"Description: {enriched['description']}")
print(f"Solution:    {enriched['solution']}")
```

## Supported Languages

| Code      | Language            |
| --------- | ------------------- |
| `en`      | English             |
| `zh_CN`   | Simplified Chinese  |
| `zh_Hant` | Traditional Chinese |
| `ja`      | Japanese            |
| `ko`      | Korean              |
| `de`      | German              |
| `fr`      | French              |
| `es`      | Spanish             |
| `ru`      | Russian             |
| `vi`      | Vietnamese          |

## Language Code Normalization

The SDK normalizes common variants automatically:

| Input     | Normalized To |
| --------- | ------------- |
| `zh_cn`   | `zh_CN`       |
| `zh-CN`   | `zh_CN`       |
| `zh_tw`   | `zh_Hant`     |
| `zh-Hant` | `zh_Hant`     |

::: tip
`AlarmI18n` works entirely offline — no robot connection is needed. Use it to build alarm lookup UIs or translate logged alarm IDs after the fact.
:::
