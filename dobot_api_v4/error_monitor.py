"""Robot error monitor via HTTP interface (port 22000).

This module provides the ``RobotErrorMonitor`` class for monitoring robot alarm
information via the robot's HTTP REST API, separate from the TCP/IP command
interface.  Alarm data is enriched with localized translations from the i18n
system.
"""

import json
import time
import urllib.error
import urllib.request
from typing import Any, Optional

from loguru import logger

from .i18n_manager import AlarmI18n


class RobotErrorMonitor:
    """Monitor robot alarms via the HTTP REST API on port 22000.

    Retrieves structured alarm information and enriches it with
    multi-language translations managed by :class:`AlarmI18n`.

    Attributes:
        robot_ip: Robot IP address.
        i18n: Alarm internationalisation manager instance.
    """

    def __init__(self, robot_ip: str = "192.168.200.1") -> None:
        """Initialize the error monitor.

        Args:
            robot_ip: Robot IP address.
        """
        self.robot_ip: str = robot_ip
        self.i18n: AlarmI18n = AlarmI18n(default_language="en")

    def get_error_info(self, language: str = "zh_CN") -> Optional[dict[str, Any]]:
        """Get robot alarm information via HTTP with local translations.

        Retrieves alarm IDs from the robot via HTTP (port 22000) and enriches
        them with localized translations from the i18n system.

        Args:
            language: Language code.  Supported: ``en``, ``zh_CN``,
                ``zh_Hant``, ``ja``, ``de``, ``ko``, ``vi``, ``es``,
                ``ru``, ``fr``.  Also accepts ``zh_cn``, ``kr``
                (auto-normalised).

        Returns:
            Alarm information dictionary on success, ``None`` on error.
            The dictionary has the form::

                {
                    "errMsg": [
                        {
                            "id": int,
                            "type": str,
                            "level": int,
                            "description": str,
                            "cause": str,
                            "solution": str,
                            "mode": str,
                            "date": str,
                            "time": str,
                        }
                    ]
                }

        Example::

            info = monitor.get_error_info("en")
            if info and "errMsg" in info:
                for err in info["errMsg"]:
                    print(f"ID: {err['id']}, Desc: {err['description']}")
        """
        try:
            self.i18n.set_language(language)

            alarm_url = f"http://{self.robot_ip}:22000/protocol/getAlarm"
            alarm_req = urllib.request.Request(alarm_url, method="GET")

            with urllib.request.urlopen(alarm_req, timeout=5) as response:
                alarm_data = response.read().decode("utf-8")
                robot_response: dict[str, Any] = json.loads(alarm_data)

            if robot_response and "errMsg" in robot_response:
                enriched_alarms: list[dict[str, Any]] = []
                for alarm in robot_response["errMsg"]:
                    enriched = self.i18n.enrich_alarm_data(alarm)
                    enriched_alarms.append(enriched)
                robot_response["errMsg"] = enriched_alarms

            return robot_response

        except urllib.error.HTTPError as e:
            logger.error("GetError: HTTP error {} - {}", e.code, e.reason)
            return None
        except urllib.error.URLError as e:
            logger.error("GetError: Network error - {}", e)
            return None
        except json.JSONDecodeError as e:
            logger.error("GetError: JSON parsing error - {}", e)
            return None
        except Exception as e:
            logger.error("GetError: Unexpected error - {}", e)
            return None

    def check_errors(self, language: str = "zh_cn") -> bool:
        """Check and display current error information.

        Args:
            language: Display language code.

        Returns:
            ``True`` if errors are present, ``False`` otherwise.
        """
        error_info = self.get_error_info(language)

        if not error_info or "errMsg" not in error_info:
            logger.warning("Failed to get error information")
            return False

        errors: list[dict[str, Any]] = error_info["errMsg"]

        if not errors:
            logger.info("Robot status normal, no error information")
            return False

        logger.warning("Found {} error(s)", len(errors))

        for i, error in enumerate(errors, 1):
            logger.error(
                "Error {}: ID={}, Level={}, Description={}, "
                "Solution={}, Mode={}, Date={}, Time={}",
                i,
                error.get("id", "N/A"),
                error.get("level", "N/A"),
                error.get("description", "N/A"),
                error.get("solution", "N/A"),
                error.get("mode", "N/A"),
                error.get("date", "N/A"),
                error.get("time", "N/A"),
            )

        return True

    def monitor_errors(self, interval: int = 5, language: str = "zh_cn") -> None:
        """Continuously monitor error information.

        Blocks until interrupted with ``Ctrl+C``.

        Args:
            interval: Check interval in seconds.
            language: Display language code.
        """
        logger.info(
            "Start monitoring robot error information (check every {} seconds)",
            interval,
        )
        logger.info("Press Ctrl+C to stop monitoring")

        try:
            while True:
                logger.info("Checking error information...")
                has_errors = self.check_errors(language)

                if has_errors:
                    logger.warning("Recommend handling error information immediately!")

                time.sleep(interval)

        except KeyboardInterrupt:
            logger.info("Monitoring stopped")

    def save_error_log(
        self, filename: Optional[str] = None, language: str = "zh_cn"
    ) -> None:
        """Save error information to a JSON file.

        Args:
            filename: Destination path.  Defaults to a timestamped name.
            language: Language code for translations.
        """
        if filename is None:
            filename = "robot_errors_{}.json".format(time.strftime("%Y%m%d_%H%M%S"))

        error_info = self.get_error_info(language)

        if error_info:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(error_info, f, ensure_ascii=False, indent=2)
                logger.info("Error information saved to: {}", filename)
            except Exception as e:
                logger.error("Failed to save file: {}", e)
        else:
            logger.warning("Unable to get error information")
