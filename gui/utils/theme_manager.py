"""
Theme Management and Color Palette Subsystem Compatibility Module.

Re-exports ThemeColors and ThemeManager from gui.themes.theme_manager.
"""

from gui.themes.theme_manager import ThemeColors, ThemeManager

__all__ = ["ThemeColors", "ThemeManager"]
