"""
PyInstaller-compatible Resource Loader Utility.

Resolves absolute resource file paths for both development mode and single-file PyInstaller EXEs (sys._MEIPASS).
"""

import sys
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image

import config


class ResourceLoader:
    """
    Utility for loading application assets safely in development and PyInstaller environments.
    """

    @staticmethod
    def get_resource_path(relative_path: str) -> Path:
        """
        Get absolute path to resource, works for dev and for PyInstaller.

        Args:
            relative_path: Relative path string (e.g. 'assets/icons/lock.png').

        Returns:
            Path: Absolute resolved filesystem path.
        """
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_path = Path(getattr(sys, "_MEIPASS"))
        else:
            base_path = config.BASE_DIR

        return (base_path / relative_path).resolve()

    @staticmethod
    def load_pil_image(
        relative_path: str, size: Optional[Tuple[int, int]] = None
    ) -> Optional[Image.Image]:
        """
        Loads PIL Image safely.

        Args:
            relative_path: Relative asset path.
            size: Optional resize tuple (width, height).

        Returns:
            Image.Image or None if file missing.
        """
        target_path = ResourceLoader.get_resource_path(relative_path)
        if not target_path.exists():
            return None

        try:
            img = Image.open(target_path)
            if size:
                return img.resize(size, Image.Resampling.LANCZOS)
            return img
        except Exception:
            return None
