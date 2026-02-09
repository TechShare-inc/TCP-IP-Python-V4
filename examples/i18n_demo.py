#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I18n Alarm System Demo

Demonstrates the new AlarmI18n class for multi-language alarm translation.
This replaces the old hardcoded JSON approach with a flexible i18n system.
"""

from dobot_api_v4 import AlarmI18n


def demo_basic_usage():
    """Basic alarm retrieval in different languages."""
    print("=" * 70)
    print("DEMO 1: Basic Usage")
    print("=" * 70)

    i18n = AlarmI18n(default_language="en")

    print("\n📋 Controller Alarm #16 (English):")
    alarm = i18n.get_controller_alarm(16)
    print(f"   ID: {alarm['id']}")
    print(f"   Level: {alarm['level']}")
    print(f"   Description: {alarm['description']}")
    print(f"   Solution: {alarm['solution']}")

    print("\n⚙️  Servo Alarm #8752 (English):")
    alarm = i18n.get_servo_alarm(8752)
    print(f"   ID: {alarm['id']}")
    print(f"   Description: {alarm['description']}")
    print(f"   Solution: {alarm['solution'][:80]}...")


def demo_language_switching():
    """Switch between multiple languages dynamically."""
    print("\n" + "=" * 70)
    print("DEMO 2: Language Switching")
    print("=" * 70)

    i18n = AlarmI18n("en")

    languages = [
        ("en", "English"),
        ("zh_CN", "简体中文"),
        ("ja", "日本語"),
        ("de", "Deutsch"),
        ("ko", "한국어"),
    ]

    print("\n🌍 Alarm #16 in Different Languages:\n")

    for lang_code, lang_name in languages:
        i18n.set_language(lang_code)
        alarm = i18n.get_controller_alarm(16)
        print(f"   [{lang_name}] {alarm['description']}")


def demo_auto_detection():
    """Automatic alarm type detection based on ID range."""
    print("\n" + "=" * 70)
    print("DEMO 3: Auto-Detection of Alarm Type")
    print("=" * 70)

    i18n = AlarmI18n("en")

    test_ids = [16, 100, 8752, 12816, 30080]

    print("\n🔍 Auto-detecting alarm types:\n")
    for alarm_id in test_ids:
        alarm = i18n.get_alarm(alarm_id)
        print(
            f"   ID {alarm_id:5d} → {alarm['type']:10s} | {alarm['description'][:50]}..."
        )


def demo_formatted_output():
    """Pretty-print alarms with formatting."""
    print("\n" + "=" * 70)
    print("DEMO 4: Formatted Alarm Output")
    print("=" * 70)

    i18n = AlarmI18n("en")

    print("\n📄 Formatted Alarms:\n")

    for alarm_id in [16, 17, 8752]:
        formatted = i18n.format_alarm(alarm_id)
        print(formatted)
        print()


def demo_enrichment():
    """Enrich robot data with translations."""
    print("=" * 70)
    print("DEMO 5: Enriching Robot Data with Translations")
    print("=" * 70)

    i18n = AlarmI18n("zh_CN")

    robot_data = {"id": 16, "mode": "warning", "date": "2026-02-09", "time": "14:30:00"}

    print("\n📡 Data from Robot:")
    print(f"   {robot_data}")

    enriched = i18n.enrich_alarm_data(robot_data)

    print("\n✨ Enriched with Translations (Chinese):")
    print(f"   ID: {enriched['id']}")
    print(f"   Type: {enriched['type']}")
    print(f"   Level: {enriched['level']}")
    print(f"   Mode: {enriched['mode']}")
    print(f"   Date/Time: {enriched['date']} {enriched['time']}")
    print(f"   Description: {enriched['description']}")
    print(f"   Solution: {enriched['solution']}")


def demo_language_normalization():
    """Show automatic language code normalization."""
    print("\n" + "=" * 70)
    print("DEMO 6: Language Code Normalization")
    print("=" * 70)

    print("\n🔄 Automatic normalization of language codes:\n")

    test_cases = [
        ("zh_cn", "zh_CN"),  # Case normalization
        ("zh_CN", "zh_CN"),  # Already correct
        ("kr", "ko"),  # Korean code fix
        ("ko", "ko"),  # Already correct
        ("en", "en"),  # Standard
    ]

    for input_code, expected in test_cases:
        try:
            normalized = AlarmI18n.normalize_language_code(input_code)
            status = "✓" if normalized == expected else "✗"
            print(
                f"   {status} '{input_code}' → '{normalized}' (expected: '{expected}')"
            )
        except ValueError as e:
            print(f"   ✗ '{input_code}' → ERROR: {e}")


def demo_supported_languages():
    """List all supported languages."""
    print("\n" + "=" * 70)
    print("DEMO 7: Supported Languages")
    print("=" * 70)

    languages = AlarmI18n.get_supported_languages()

    print(f"\n🌐 {len(languages)} Supported Languages:\n")

    lang_names = {
        "en": "English",
        "zh_CN": "简体中文 (Simplified Chinese)",
        "zh_Hant": "繁體中文 (Traditional Chinese)",
        "ja": "日本語 (Japanese)",
        "de": "Deutsch (German)",
        "ko": "한국어 (Korean)",
        "vi": "Tiếng Việt (Vietnamese)",
        "es": "Español (Spanish)",
        "ru": "Русский (Russian)",
        "fr": "Français (French)",
    }

    for lang in languages:
        name = lang_names.get(lang, "Unknown")
        print(f"   • {lang:10s} - {name}")


def main():
    """Run all demos."""
    print("\n")
    print("=" * 70)
    print(" " * 15 + "DOBOT API v4.1 - I18N ALARM SYSTEM DEMO")
    print("=" * 70)
    print()

    try:
        demo_basic_usage()
        demo_language_switching()
        demo_auto_detection()
        demo_formatted_output()
        demo_enrichment()
        demo_language_normalization()
        demo_supported_languages()

        print("\n" + "=" * 70)
        print("✅ All demos completed successfully!")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
