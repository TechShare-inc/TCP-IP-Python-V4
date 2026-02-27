#!/usr/bin/env python3
"""I18n alarm demo — multi-language alarm lookup and live error enrichment.

Demonstrates:
- Offline alarm translation via ``AlarmI18n``
- Language switching and auto-detection of alarm type
- Using ``DobotRobot.check_errors()`` with a language override
- Enriching live error data with translated descriptions
"""

from dobot_api_v4 import AlarmI18n, DobotRobot

ROBOT_IP = "192.168.5.1"


# --------------------------------------------------------------------------
# Offline demos (no robot connection required)
# --------------------------------------------------------------------------


def demo_basic_lookup() -> None:
    """Look up a controller and servo alarm in English."""
    print("--- Basic alarm lookup (English) ---")
    i18n = AlarmI18n(default_language="en")

    alarm = i18n.get_controller_alarm(16)
    print(f"  Controller #16: {alarm['description']}")

    alarm = i18n.get_servo_alarm(8752)
    print(f"  Servo #8752   : {alarm['description']}")


def demo_language_switching() -> None:
    """Show the same alarm in several languages."""
    print("\n--- Alarm #16 in multiple languages ---")
    i18n = AlarmI18n("en")

    for code, name in [
        ("en", "English"),
        ("zh_CN", "中文"),
        ("ja", "日本語"),
        ("de", "Deutsch"),
        ("ko", "한국어"),
    ]:
        i18n.set_language(code)
        alarm = i18n.get_controller_alarm(16)
        print(f"  [{name:7s}] {alarm['description']}")


def demo_auto_detection() -> None:
    """Auto-detect alarm type (controller vs servo) by ID range."""
    print("\n--- Auto-detection by ID ---")
    i18n = AlarmI18n("en")

    for alarm_id in [16, 100, 8752, 12816]:
        alarm = i18n.get_alarm(alarm_id)
        print(f"  ID {alarm_id:5d} -> {alarm['type']:10s} | {alarm['description'][:60]}")


def demo_supported_languages() -> None:
    """List every supported language code."""
    print("\n--- Supported languages ---")
    for lang in AlarmI18n.get_supported_languages():
        print(f"  {lang}")


# --------------------------------------------------------------------------
# Live demo (requires robot connection)
# --------------------------------------------------------------------------


def demo_live_error_check() -> None:
    """Connect to the robot and check errors in two languages."""
    print("\n--- Live error check via DobotRobot ---")
    with DobotRobot(ROBOT_IP, language="en") as robot:
        has_errors = robot.check_errors()
        print(f"  Errors (en)   : {has_errors}")

        has_errors = robot.check_errors(language="zh_CN")
        print(f"  Errors (zh_CN): {has_errors}")


def main() -> None:
    demo_basic_lookup()
    demo_language_switching()
    demo_auto_detection()
    demo_supported_languages()

    # Uncomment the line below when connected to a real robot:
    # demo_live_error_check()

    print("\nI18n demo complete.")


if __name__ == "__main__":
    main()
