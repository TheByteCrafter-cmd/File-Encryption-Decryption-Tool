"""
Settings and Window State Persistence Model.

Loads and persists window geometry, position, active page, theme preference,
default output paths, chunk sizes, and GUI settings to output/settings.json.
"""

import json
from pathlib import Path
from typing import Any, Dict

import config


class SettingsModel:
    """
    Manages persistent GUI settings and window state.
    """

    SETTINGS_FILE: Path = config.OUTPUT_DIR / "settings.json"

    DEFAULT_SETTINGS: Dict[str, Any] = {
        "theme_mode": "System",
        "default_output_dir": str(config.OUTPUT_DIR),
        "chunk_size": config.CHUNK_SIZE,
        "auto_open_output_dir": False,
        "remember_last_dir": True,
        "history_limit": 500,
        "last_page": "home",
        "window_width": 1100,
        "window_height": 700,
        "window_x": None,
        "window_y": None,
    }

    def __init__(self) -> None:
        self.settings: Dict[str, Any] = self.DEFAULT_SETTINGS.copy()
        self.load()

    def load(self) -> None:
        """Loads settings from JSON file if present."""
        if self.SETTINGS_FILE.exists():
            try:
                data = json.loads(self.SETTINGS_FILE.read_text(encoding="utf-8"))
                self.settings.update(data)
            except Exception:
                pass

    def save(self) -> None:
        """Saves current settings dict to JSON file."""
        try:
            config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            self.SETTINGS_FILE.write_text(
                json.dumps(self.settings, indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a setting value and persist."""
        self.settings[key] = value
        self.save()
