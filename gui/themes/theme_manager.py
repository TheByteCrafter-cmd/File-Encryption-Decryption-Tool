"""
Windows 11 Commercial Design Theme System.

Defines exact color palette tokens (#2563EB Primary, #22C55E Success, #EF4444 Danger,
#F59E0B Warning, #7C3AED Purple, #0F172A Dark, #F8FAFC Light) and handles dark/light mode switching.
"""

from typing import Dict

import customtkinter as ctk
import darkdetect


class ThemeColors:
    """Commercial Windows 11 Fluent Design color tokens."""

    # Brand & Accent Colors
    PRIMARY: str = "#2563EB"
    PRIMARY_HOVER: str = "#1D4ED8"
    SUCCESS: str = "#22C55E"
    SUCCESS_HOVER: str = "#16A34A"
    DANGER: str = "#EF4444"
    DANGER_HOVER: str = "#DC2626"
    WARNING: str = "#F59E0B"
    PURPLE: str = "#7C3AED"

    # Light Theme Colors (#F8FAFC Light background, White cards, #E2E8F0 borders)
    LIGHT_BG: str = "#F8FAFC"
    LIGHT_CARD: str = "#FFFFFF"
    LIGHT_CARD_HOVER: str = "#F1F5F9"
    LIGHT_BORDER: str = "#E2E8F0"
    LIGHT_TEXT: str = "#0F172A"
    LIGHT_SUBTEXT: str = "#64748B"

    # Dark Theme Colors (#0F172A Dark background, #1E293B cards, #334155 borders)
    DARK_BG: str = "#0F172A"
    DARK_CARD: str = "#1E293B"
    DARK_CARD_HOVER: str = "#334155"
    DARK_BORDER: str = "#334155"
    DARK_TEXT: str = "#F8FAFC"
    DARK_SUBTEXT: str = "#94A3B8"


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
                "card_hover": ThemeColors.DARK_CARD_HOVER,
                "border": ThemeColors.DARK_BORDER,
                "text": ThemeColors.DARK_TEXT,
                "subtext": ThemeColors.DARK_SUBTEXT,
                "primary": ThemeColors.PRIMARY,
                "primary_hover": ThemeColors.PRIMARY_HOVER,
                "success": ThemeColors.SUCCESS,
                "danger": ThemeColors.DANGER,
                "warning": ThemeColors.WARNING,
                "purple": ThemeColors.PURPLE,
            }
        else:
            return {
                "bg": ThemeColors.LIGHT_BG,
                "card": ThemeColors.LIGHT_CARD,
                "card_hover": ThemeColors.LIGHT_CARD_HOVER,
                "border": ThemeColors.LIGHT_BORDER,
                "text": ThemeColors.LIGHT_TEXT,
                "subtext": ThemeColors.LIGHT_SUBTEXT,
                "primary": ThemeColors.PRIMARY,
                "primary_hover": ThemeColors.PRIMARY_HOVER,
                "success": ThemeColors.SUCCESS,
                "danger": ThemeColors.DANGER,
                "warning": ThemeColors.WARNING,
                "purple": ThemeColors.PURPLE,
            }
