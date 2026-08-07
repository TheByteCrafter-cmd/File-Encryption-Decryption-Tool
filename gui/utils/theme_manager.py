"""
Theme Management and Color Palette Subsystem.

Defines commercial Windows 11 Fluent Design color tokens and handles dynamic mode switching
with darkdetect system theme detection.
"""

from typing import Dict

import customtkinter as ctk
import darkdetect


class ThemeColors:
    """Windows 11 Fluent Design light and dark color palette constants."""

    # Light Theme Palette
    LIGHT_BG: str = "#F5F7FA"
    LIGHT_CARD: str = "#FFFFFF"
    LIGHT_BORDER: str = "#E5E7EB"
    LIGHT_TEXT: str = "#111827"
    LIGHT_SUBTEXT: str = "#6B7280"
    LIGHT_PRIMARY: str = "#2563EB"
    LIGHT_PRIMARY_HOVER: str = "#1D4ED8"
    LIGHT_SUCCESS: str = "#16A34A"
    LIGHT_WARNING: str = "#F59E0B"
    LIGHT_DANGER: str = "#DC2626"

    # Dark Theme Palette
    DARK_BG: str = "#0F172A"
    DARK_CARD: str = "#1E293B"
    DARK_BORDER: str = "#334155"
    DARK_TEXT: str = "#F8FAFC"
    DARK_SUBTEXT: str = "#94A3B8"
    DARK_PRIMARY: str = "#3B82F6"
    DARK_PRIMARY_HOVER: str = "#2563EB"
    DARK_SUCCESS: str = "#22C55E"
    DARK_WARNING: str = "#F59E0B"
    DARK_DANGER: str = "#EF4444"


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
                "primary": ThemeColors.DARK_PRIMARY,
                "primary_hover": ThemeColors.DARK_PRIMARY_HOVER,
                "success": ThemeColors.DARK_SUCCESS,
                "warning": ThemeColors.DARK_WARNING,
                "danger": ThemeColors.DARK_DANGER,
            }
        else:
            return {
                "bg": ThemeColors.LIGHT_BG,
                "card": ThemeColors.LIGHT_CARD,
                "border": ThemeColors.LIGHT_BORDER,
                "text": ThemeColors.LIGHT_TEXT,
                "subtext": ThemeColors.LIGHT_SUBTEXT,
                "primary": ThemeColors.LIGHT_PRIMARY,
                "primary_hover": ThemeColors.LIGHT_PRIMARY_HOVER,
                "success": ThemeColors.LIGHT_SUCCESS,
                "warning": ThemeColors.LIGHT_WARNING,
                "danger": ThemeColors.LIGHT_DANGER,
            }
