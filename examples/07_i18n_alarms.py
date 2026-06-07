#!/usr/bin/env python3
"""Multi-language alarm lookup example.

Uses ``AlarmI18n`` to translate robot alarm codes into human-readable
descriptions across all ten supported languages -- entirely offline, with
no robot connection required.  Also demonstrates live error enrichment
when connected to a real robot.

Difficulty: Advanced
Prerequisites: 01_connect.py, 04_error_handling.py

See also:
- docs/how-to/multi-language-alarms.md
- docs/explanation/i18n-design.md
"""

from __future__ import annotations

from dobot_api_v4 import AlarmI18n, DobotRobot

ROBOT_IP = "192.168.5.1"


def demo_lookup() -> None:
    """Look up a controller and a servo alarm in English."""
    print("--- Alarm lookup (English) ---")
    i18n = AlarmI18n(default_language="en")

    alarm = i18n.get_controller_alarm(16)
    print(f"  Controller #16  : {alarm['description']}")

    alarm = i18n.get_servo_alarm(8752)
    print(f"  Servo #8752     : {alarm['description']}")


def demo_language_switching() -> None:
    """Print alarm #16 in every supported language."""
    print("\n--- Alarm #16 across all supported languages ---")
    i18n = AlarmI18n("en")
    for lang in AlarmI18n.get_supported_languages():
        i18n.set_language(lang)
        alarm = i18n.get_controller_alarm(16)
        print(f"  [{lang:<7s}]  {alarm['description']}")


def demo_auto_detect() -> None:
    """Auto-detect alarm type (controller vs servo) from the ID range."""
    print("\n--- Auto-detection by ID ---")
    i18n = AlarmI18n("en")
    for alarm_id in (16, 100, 8752, 12816):
        alarm = i18n.get_alarm(alarm_id)
        desc = alarm["description"][:60]
        print(f"  ID {alarm_id:5d}  ->  {alarm['type']:<10s}  |  {desc}")


def demo_live_check() -> None:
    """Connect to the robot and report active errors in two languages.

    This function is called only when ``ROBOT_IP`` is reachable.
    """
    print("\n--- Live error check ---")
    with DobotRobot(ROBOT_IP, language="en") as robot:
        has_en = robot.check_errors()
        print(f"  Errors (en)    : {has_en}")
        has_cn = robot.check_errors(language="zh_CN")
        print(f"  Errors (zh_CN) : {has_cn}")


def main() -> None:
    """Run all offline alarm demos (no robot connection required)."""
    demo_lookup()
    demo_language_switching()
    demo_auto_detect()

    # Uncomment the line below to run the live demo against a real robot:
    demo_live_check()

    print("\nI18n alarm demo complete.")


if __name__ == "__main__":
    main()
