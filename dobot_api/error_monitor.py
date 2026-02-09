"""
Robot Error Monitor Module

This module provides the RobotErrorMonitor class for monitoring robot alarm information
via HTTP interface (port 22000), separate from the TCP/IP command interface.

The error monitoring system uses HTTP REST API calls to retrieve structured alarm
information with multi-language support.
"""

import json
import time
import urllib.request
import urllib.error
from loguru import logger
from .dashboard import DobotApiDashboard


class RobotErrorMonitor:
    """
    Robot Error Monitor Class
    A class for monitoring robot alarm information via HTTP interface.

    This monitor uses the robot's HTTP REST API (port 22000) to retrieve error
    information, which is fundamentally different from the TCP/IP command protocol
    (port 29999) used by DobotApiDashboard.

    Attributes:
        robot_ip (str): Robot IP address
        dashboard_port (int): Dashboard TCP port (default: 29999)
        dashboard (DobotApiDashboard): TCP command interface (optional)
    """

    def __init__(self, robot_ip="192.168.200.1", dashboard_port=29999):
        """
        Initialize the error monitor.

        Args:
            robot_ip (str): Robot IP address
            dashboard_port (int): Dashboard TCP port for control commands
        """
        self.robot_ip = robot_ip
        self.dashboard_port = dashboard_port
        self.dashboard = None

    def connect(self):
        """
        Connect to robot TCP/IP interface.

        Note: The HTTP error monitoring doesn't require connection, but this
        establishes the TCP interface for control commands if needed.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.dashboard = DobotApiDashboard(self.robot_ip, self.dashboard_port)
            logger.info(
                f"Successfully connected to robot: {self.robot_ip}:{self.dashboard_port}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to connect to robot: {e}")
            return False

    def disconnect(self):
        """Disconnect from robot TCP interface."""
        if self.dashboard:
            self.dashboard.close()
            logger.info("Disconnected from robot")

    def get_error_info(self, language="zh_cn"):
        """
        Get robot alarm information via HTTP interface.

        This method uses HTTP requests (port 22000) to retrieve structured alarm
        information in JSON format with multi-language support.

        Args:
            language (str): Language setting, default is "zh_cn"
                           Supported languages: zh_cn, zh_hant, en, ja, de, vi, es, fr, ko, ru

        Returns:
            dict or None: Returns alarm information dictionary on success, None on error.
                         Alarm information format:
                         {
                             "errMsg": [
                                 {
                                     "id": int,              # Error ID
                                     "level": int,           # Error level
                                     "description": str,     # Error description
                                     "solution": str,        # Solution suggestion
                                     "mode": str,            # Error mode
                                     "date": str,            # Error date
                                     "time": str             # Error time
                                 }
                             ]
                         }

        Example:
            error_info = monitor.get_error_info("en")
            if error_info and "errMsg" in error_info:
                for error in error_info["errMsg"]:
                    print(f"ID: {error['id']}, Description: {error['description']}")
        """
        try:
            # Step 1: Set language preference via POST request
            language_url = f"http://{self.robot_ip}:22000/interface/language"
            language_data = json.dumps({"type": language}).encode("utf-8")
            language_headers = {"Content-Type": "application/json"}

            language_req = urllib.request.Request(
                language_url,
                data=language_data,
                headers=language_headers,
                method="POST",
            )

            with urllib.request.urlopen(language_req, timeout=5) as response:
                response.read()  # Read but don't need to parse response

            # Step 2: Retrieve alarm information via GET request
            alarm_url = f"http://{self.robot_ip}:22000/protocol/getAlarm"
            alarm_req = urllib.request.Request(alarm_url, method="GET")

            with urllib.request.urlopen(alarm_req, timeout=5) as response:
                alarm_data = response.read().decode("utf-8")
                return json.loads(alarm_data)

        except urllib.error.HTTPError as e:
            logger.error(f"GetError: HTTP error {e.code} - {e.reason}")
            return None
        except urllib.error.URLError as e:
            logger.error(f"GetError: Network error - {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"GetError: JSON parsing error - {e}")
            return None
        except Exception as e:
            logger.error(f"GetError: Unexpected error - {e}")
            return None

    def check_errors(self, language="zh_cn"):
        """
        Check and display current error information.

        Args:
            language (str): Display language

        Returns:
            bool: True means there are errors, False means no errors
        """
        error_info = self.get_error_info(language)

        if not error_info or "errMsg" not in error_info:
            logger.warning("Failed to get error information")
            return False

        errors = error_info["errMsg"]

        if not errors:
            logger.info("Robot status normal, no error information")
            return False

        logger.warning(f"Found {len(errors)} error(s)")

        for i, error in enumerate(errors, 1):
            logger.error(
                f"Error {i}: ID={error.get('id', 'N/A')}, "
                f"Level={error.get('level', 'N/A')}, "
                f"Description={error.get('description', 'N/A')}, "
                f"Solution={error.get('solution', 'N/A')}, "
                f"Mode={error.get('mode', 'N/A')}, "
                f"Date={error.get('date', 'N/A')}, "
                f"Time={error.get('time', 'N/A')}"
            )

        return True

    def monitor_errors(self, interval=5, language="zh_cn"):
        """
        Continuously monitor error information.

        Args:
            interval (int): Check interval (seconds)
            language (str): Display language
        """
        logger.info(
            f"Start monitoring robot error information (check every {interval} seconds)"
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

    def save_error_log(self, filename=None, language="zh_cn"):
        """
        Save error information to file.

        Args:
            filename (str): Save filename, default is current timestamp
            language (str): Language setting
        """
        if filename is None:
            filename = f"robot_errors_{time.strftime('%Y%m%d_%H%M%S')}.json"

        error_info = self.get_error_info(language)

        if error_info:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(error_info, f, ensure_ascii=False, indent=2)
                logger.info(f"Error information saved to: {filename}")
            except Exception as e:
                logger.error(f"Failed to save file: {e}")
        else:
            logger.warning("Unable to get error information")
