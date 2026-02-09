"""
Internationalization manager for robot alarm messages.

This module provides the AlarmI18n class for managing multi-language
alarm translations using python-i18n library with YAML locale files.
"""

import i18n
from pathlib import Path
from typing import Optional, Dict, Any, List
from loguru import logger


class AlarmI18n:
    """
    Internationalization manager for robot alarm messages.

    Provides easy access to translated alarm descriptions, causes,
    and solutions with automatic fallback to English for missing translations.

    Example:
        >>> i18n_manager = AlarmI18n(default_language='en')
        >>> alarm = i18n_manager.get_controller_alarm(16)
        >>> print(alarm['description'])
        'The planned point is closed to the shoulder singularity point'

        >>> i18n_manager.set_language('zh_CN')
        >>> alarm = i18n_manager.get_controller_alarm(16)
        >>> print(alarm['description'])
        '规划位置接近肩奇异点'
    """

    # Supported languages
    SUPPORTED_LANGUAGES = [
        "en",
        "zh_CN",
        "zh_Hant",
        "ja",
        "de",
        "ko",
        "vi",
        "es",
        "ru",
        "fr",
    ]

    # Language aliases for backward compatibility
    LANGUAGE_ALIASES = {
        "zh_cn": "zh_CN",  # Case normalization
        "zh_hant": "zh_Hant",  # Case normalization
        "kr": "ko",  # Korean code fix
    }

    # Alarm ID ranges for automatic type detection
    SERVO_ID_MIN = 8000  # Servo alarms start from 8000+

    def __init__(self, default_language: str = "en"):
        """
        Initialize i18n manager.

        Args:
            default_language: Default language code (e.g., 'en', 'zh_CN')

        Raises:
            ValueError: If default_language is not supported
        """
        self._initialized = False
        self._setup_i18n()
        self.set_language(default_language)
        logger.debug(f"AlarmI18n initialized with language: {default_language}")

    def _setup_i18n(self):
        """Configure python-i18n library with locale files."""
        if self._initialized:
            return

        locale_path = Path(__file__).parent / "locales"

        if not locale_path.exists():
            logger.warning(f"Locales directory not found at {locale_path}")
            return

        i18n.load_path.append(str(locale_path))
        i18n.set("file_format", "yml")
        i18n.set("fallback", "en")
        i18n.set("error_on_missing_translation", False)
        i18n.set("skip_locale_root_data", True)  # Files are named alarms.{locale}.yml

        self._initialized = True
        logger.debug(f"I18n configured with locale path: {locale_path}")

    def set_language(self, language: str) -> None:
        """
        Set active language for translations.

        Automatically normalizes language codes (e.g., 'zh_cn' -> 'zh_CN', 'kr' -> 'ko').

        Args:
            language: Language code (e.g., 'en', 'zh_CN', 'zh_cn', 'kr')

        Raises:
            ValueError: If language is not supported

        Example:
            >>> i18n_manager.set_language('zh_CN')  # Standard format
            >>> i18n_manager.set_language('zh_cn')  # Auto-normalized to zh_CN
            >>> i18n_manager.set_language('kr')     # Auto-converted to ko
        """
        # Normalize language code
        original_language = language
        language = self.LANGUAGE_ALIASES.get(language.lower(), language)

        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {original_language} (normalized to {language}). "
                f"Supported languages: {', '.join(self.SUPPORTED_LANGUAGES)}"
            )

        i18n.set("locale", language)

        if original_language != language:
            logger.debug(f"Language normalized: {original_language} -> {language}")

    def get_current_language(self) -> str:
        """
        Get currently active language code.

        Returns:
            Current language code (e.g., 'en', 'zh_CN')
        """
        return i18n.get("locale")

    def get_alarm(
        self,
        alarm_id: int,
        alarm_type: Optional[str] = None,
        field: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get alarm information by ID.

        Args:
            alarm_id: Alarm ID number
            alarm_type: 'controller' or 'servo'. If None, auto-detects based on ID range.
            field: Specific field ('description', 'cause', 'solution', 'level')
                   If None, returns all fields

        Returns:
            Dictionary with alarm information. Example:
            {
                'id': 16,
                'description': 'The planned point is closed to the shoulder singularity point',
                'cause': '',
                'solution': 'Reselect the movement points...',
                'level': 5
            }

        Example:
            >>> alarm = i18n_manager.get_alarm(16)  # Auto-detects controller type
            >>> alarm = i18n_manager.get_alarm(8752, alarm_type='servo')
            >>> desc = i18n_manager.get_alarm(16, field='description')
        """
        # Auto-detect alarm type if not specified
        if alarm_type is None:
            alarm_type = "servo" if alarm_id >= self.SERVO_ID_MIN else "controller"

        base_key = f"alarms.{alarm_type}.{alarm_id}"

        if field:
            key = f"{base_key}.{field}"
            value = i18n.t(key, default="")
            return {field: value}

        # Return all fields
        description = i18n.t(f"{base_key}.description", default="Unknown error")
        cause = i18n.t(f"{base_key}.cause", default="")
        solution = i18n.t(f"{base_key}.solution", default="Contact technical support")

        # Level is an integer, handle it specially
        try:
            level_val = i18n.t(f"{base_key}.level")
            level = (
                int(level_val)
                if isinstance(level_val, (int, float, str)) and str(level_val).isdigit()
                else 0
            )
        except (TypeError, ValueError):
            level = 0

        return {
            "id": alarm_id,
            "type": alarm_type,
            "description": description,
            "cause": cause,
            "solution": solution,
            "level": level,
        }

    def get_controller_alarm(self, alarm_id: int) -> Dict[str, Any]:
        """
        Get controller alarm by ID.

        Shortcut method for getting controller-specific alarms.

        Args:
            alarm_id: Controller alarm ID (typically 16-4193)

        Returns:
            Dictionary with alarm information

        Example:
            >>> alarm = i18n_manager.get_controller_alarm(16)
            >>> print(alarm['description'])
        """
        return self.get_alarm(alarm_id, alarm_type="controller")

    def get_servo_alarm(self, alarm_id: int) -> Dict[str, Any]:
        """
        Get servo alarm by ID.

        Shortcut method for getting servo-specific alarms.

        Args:
            alarm_id: Servo alarm ID (typically 8000+)

        Returns:
            Dictionary with alarm information

        Example:
            >>> alarm = i18n_manager.get_servo_alarm(8752)
            >>> print(alarm['description'])
        """
        return self.get_alarm(alarm_id, alarm_type="servo")

    def format_alarm(
        self,
        alarm_id: int,
        alarm_type: Optional[str] = None,
        include_cause: bool = True,
    ) -> str:
        """
        Format alarm as human-readable string.

        Args:
            alarm_id: Alarm ID number
            alarm_type: 'controller' or 'servo'. If None, auto-detects.
            include_cause: Whether to include cause field (if not empty)

        Returns:
            Formatted multi-line string

        Example:
            >>> print(i18n_manager.format_alarm(16))
            ID 16 [Level 5]: The planned point is closed to the shoulder singularity point
              Solution: Reselect the movement points or The joint interpolation command is used near the singularity point
        """
        alarm = self.get_alarm(alarm_id, alarm_type)

        lines = [f"ID {alarm['id']} [Level {alarm['level']}]: {alarm['description']}"]

        if include_cause and alarm["cause"]:
            lines.append(f"  Cause: {alarm['cause']}")

        if alarm["solution"]:
            lines.append(f"  Solution: {alarm['solution']}")

        return "\n".join(lines)

    def enrich_alarm_data(self, alarm_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich alarm data from robot with localized translations.

        This is useful when you receive alarm IDs from the robot
        and want to add translated descriptions/solutions.

        Args:
            alarm_data: Dictionary with at least 'id' key, may have 'mode', 'date', 'time'

        Returns:
            Enriched dictionary with translation fields added

        Example:
            >>> robot_alarm = {'id': 16, 'mode': 'error', 'date': '2026-02-09', 'time': '10:30:00'}
            >>> enriched = i18n_manager.enrich_alarm_data(robot_alarm)
            >>> print(enriched)
            {
                'id': 16,
                'mode': 'error',
                'date': '2026-02-09',
                'time': '10:30:00',
                'description': 'The planned point is closed...',
                'cause': '',
                'solution': 'Reselect the movement points...',
                'level': 5,
                'type': 'controller'
            }
        """
        alarm_id = alarm_data.get("id")
        if alarm_id is None:
            logger.warning("Alarm data missing 'id' field, cannot enrich")
            return alarm_data

        # Get translation
        translation = self.get_alarm(alarm_id)

        # Merge: original data + translations
        enriched = {**alarm_data, **translation}

        return enriched

    @classmethod
    def get_supported_languages(cls) -> List[str]:
        """
        Get list of supported language codes.

        Returns:
            List of language codes

        Example:
            >>> langs = AlarmI18n.get_supported_languages()
            >>> print(langs)
            ['en', 'zh_CN', 'zh_Hant', 'ja', 'de', 'ko', 'vi', 'es', 'ru', 'fr']
        """
        return cls.SUPPORTED_LANGUAGES.copy()

    @classmethod
    def normalize_language_code(cls, language: str) -> str:
        """
        Normalize language code to standard format.

        Args:
            language: Language code (any casing, may use aliases)

        Returns:
            Normalized language code

        Raises:
            ValueError: If language is not recognized

        Example:
            >>> AlarmI18n.normalize_language_code('zh_cn')
            'zh_CN'
            >>> AlarmI18n.normalize_language_code('kr')
            'ko'
        """
        normalized = cls.LANGUAGE_ALIASES.get(language.lower(), language)

        if normalized not in cls.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language} (normalized to {normalized})"
            )

        return normalized
