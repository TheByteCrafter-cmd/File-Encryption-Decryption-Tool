"""
Theme Management and Color Palette Subsystem.

Defines Windows 11 Fluent and VSCode inspired color palettes and handles dynamic mode switching
with darkdetect system theme detection.
"""

from typing import Dict

import customtkinter as ctk
import darkdetect


class ThemeColors:
    """Windows 11 Fluent & VSCode dark/light theme color constants."""

    PRIMARY: str = "#0078D4"  # Windows Accent Blue
    PRIMARY_HOVER: str = "#106EBE"  # Hover Blue
    SUCCESS: str = "#107C41"  # Fluent Green
    WARNING: str = "#FCE100"  # Fluent Yellow
    ERROR: str = "#D13438"  # Fluent Red

    # Dark Mode Palette
    DARK_BG: str = "#181818"
    DARK_CARD: str = "#202020"
    DARK_BORDER: str = "#2D2D2D"
    DARK_TEXT: str = "#FFFFFF"
    DARK_SUBTEXT: str = "#A0A0A0"

    # Light Mode Palette
    LIGHT_BG: str = "#F3F3F3"
    LIGHT_CARD: str = "#FFFFFF"
    LIGHT_BORDER: str = "#E5E5E5"
    LIGHT_TEXT: str = "#1F1F1F"
    LIGHT_SUBTEXT: str = "#606060"


class ThemeManager:
    """
    Manages CustomTkinter theme settings and system theme synchronization.
    """

    @staticmethod
    def initialize_theme(theme_mode: str = "System") -> None:
        """Sets CustomTkinter appearance mode ('System', 'Dark', 'Light')."""
        ctk.set_appearance_mode(theme_mode)
        ctk.set_default_color_theme("blue")

    @staticmethod
    def get_effective_mode(mode: str) -> str:
        """Resolves 'System' mode into actual 'Dark' or 'Light' via darkdetect."""
        if mode == "System":
            detected = darkdetect.theme()
            return detected if detected in ("Dark", "Light") else "Dark"
        return mode if mode in ("Dark", "Light") else "Dark"

    @staticmethod
    def get_colors(mode: str = "System") -> Dict[str, str]:
        """Returns active theme color dictionary based on effective appearance mode."""
        effective = ThemeManager.get_effective_mode(mode)
        if effective == "Dark":
            return {
                "bg": ThemeColors.DARK_BG,
                "card": ThemeColors.DARK_CARD,
                "border": ThemeColors.DARK_BORDER,
                "text": ThemeColors.DARK_TEXT,
                "subtext": ThemeColors.DARK_SUBTEXT,
                "primary": ThemeColors.PRIMARY,
                "primary_hover": ThemeColors.PRIMARY_HOVER,
                "success": ThemeColors.SUCCESS,
                "warning": ThemeColors.WARNING,
                "error": ThemeColors.ERROR,
            }
        else:
            return {
                "bg": ThemeColors.LIGHT_BG,
                "card": ThemeColors.LIGHT_CARD,
                "border": ThemeColors.LIGHT_BORDER,
                "text": ThemeColors.LIGHT_TEXT,
                "subtext": ThemeColors.LIGHT_SUBTEXT,
                "primary": ThemeColors.PRIMARY,
                "primary_hover": ThemeColors.PRIMARY_HOVER,
                "success": ThemeColors.SUCCESS,
                "warning": ThemeColors.WARNING,
                "error": ThemeColors.ERROR,
            }
