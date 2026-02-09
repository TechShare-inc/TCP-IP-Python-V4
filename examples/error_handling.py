#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Updated for V4.0.0: Compatible with new package structure

RobotErrorMonitor Usage Example
Demonstrates how to use the RobotErrorMonitor class for robot alarm monitoring.

Note: RobotErrorMonitor uses logger for all output. Configure DOBOT_LOG_LEVEL
environment variable to control verbosity (DEBUG, INFO, WARNING, ERROR).
"""

from dobot_api import RobotErrorMonitor
import json


def main():
    """Main function - Demonstrate various usage methods"""

    print("=== RobotErrorMonitor Usage Example ===")
    print("Note: Error information is logged. Check console for logger output.\\n")

    # Create monitor instance
    monitor = RobotErrorMonitor(robot_ip="192.168.200.1", dashboard_port=29999)

    # Connect to robot (optional - only needed if you want to use TCP commands)
    print("1. Connecting to robot...")
    if not monitor.connect():
        print(
            "   Note: TCP connection failed, but HTTP error monitoring still works\\n"
        )

    try:
        # 2. Basic usage - Check current errors
        print("2. Checking current error information...")
        has_errors = monitor.check_errors("zh_cn")
        print(f"   Check completed. Errors found: {has_errors}\\n")

        # 3. Multi-language support
        print("3. Multi-language support demonstration:")
        languages = {
            "zh_cn": "Simplified Chinese",
            "en": "English",
            "ja": "Japanese",
        }

        for lang_code, lang_name in languages.items():
            print(f"   Checking in {lang_name} ({lang_code})...")
            monitor.check_errors(lang_code)

        print()

        # 4. Save error log
        print("4. Saving error log to file...")
        monitor.save_error_log()
        print()

        # 5. Get raw data
        print("5. Getting raw JSON data:")
        raw_data = monitor.get_error_info("zh_cn")
        if raw_data:
            print("   Raw data retrieved successfully:")
            print(json.dumps(raw_data, ensure_ascii=False, indent=2))
        else:
            print("   No data retrieved or connection failed.")
        print()

        # 6. Optional: Start continuous monitoring (uncomment to enable)
        print("6. Continuous monitoring available (commented out by default)")
        print("   Uncomment the following lines to enable:")
        print("   # monitor.monitor_errors(interval=10, language='zh_cn')")

    finally:
        # Disconnect (if connected)
        print("\\nDisconnecting from robot...")
        monitor.disconnect()
        print("Example completed.")


if __name__ == "__main__":
    main()
