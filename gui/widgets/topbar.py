"""
Windows 11 Glassmorphism Top Bar Component.

Features current page title, Engine Status badge (● AES-256-GCM ACTIVE),
Theme Switcher OptionMenu, Settings shortcut button, and Notification indicator icon.
"""

from typing import Callable, Optional

import customtkinter as ctk

import config
from gui.themes.theme_manager import ThemeManager


class TopBarWidget(ctk.CTkFrame):
    """
    Glassmorphism top header bar widget.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_theme_change: Callable[[str], None],
        on_settings_click: Optional[Callable[[], None]] = None,
        initial_theme: str = "System",
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            height=54,
            corner_radius=16,
            fg_color=("gray90", "#1E293B"),
            border_width=1,
            border_color=("gray80", "#334155"),
            **kwargs,
        )
        self.on_theme_change = on_theme_change
        self.on_settings_click = on_settings_click

        self.grid_columnconfigure(1, weight=1)

        # Page Title Label
        self.title_label = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=1, sticky="w", padx=20, pady=10)

        # Engine Active Status Badge (● AES-256-GCM ACTIVE)
        self.engine_badge = ctk.CTkFrame(
            self, corner_radius=10, fg_color=("#DCFCE7", "#064E3B")
        )
        self.engine_badge.grid(row=0, column=2, padx=(0, 15), pady=10)

        self.engine_text = ctk.CTkLabel(
            self.engine_badge,
            text="● AES-256-GCM ACTIVE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#16A34A", "#4ADE80"),
        )
        self.engine_text.grid(row=0, column=0, padx=12, pady=4)

        # Notification Badge Icon
        self.notif_btn = ctk.CTkButton(
            self,
            text="🔔",
            width=36,
            height=36,
            corner_radius=10,
            fg_color="transparent",
            hover_color=("gray80", "#334155"),
            text_color=("gray10", "#F8FAFC"),
        )
        self.notif_btn.grid(row=0, column=3, padx=(0, 10), pady=10)

        # Theme Switcher Dropdown
        self.theme_switch = ctk.CTkOptionMenu(
            self,
            values=["System", "Dark", "Light"],
            command=self.on_theme_change,
            width=100,
            height=34,
            corner_radius=10,
            fg_color="#2563EB",
            button_color="#1D4ED8",
            button_hover_color="#1E40AF",
        )
        self.theme_switch.set(initial_theme)
        self.theme_switch.grid(row=0, column=4, padx=(0, 15), pady=10)

        # Settings Shortcut Button
        if self.on_settings_click:
            self.settings_btn = ctk.CTkButton(
                self,
                text="⚙️",
                width=36,
                height=36,
                corner_radius=10,
                fg_color="transparent",
                hover_color=("gray80", "#334155"),
                text_color=("gray10", "#F8FAFC"),
                command=self.on_settings_click,
            )
            self.settings_btn.grid(row=0, column=5, padx=(0, 15), pady=10)

    def set_title(self, title: str) -> None:
        """Updates header page title label."""
        self.title_label.configure(text=title)
