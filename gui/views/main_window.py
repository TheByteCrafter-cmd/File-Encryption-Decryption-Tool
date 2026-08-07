"""
Main Application Window Shell View.

Integrates SidebarWidget (240px) and TopBarWidget (Glassmorphism header) with
floating container frame and keyboard shortcuts.
"""

from typing import Callable, Dict, Optional

import customtkinter as ctk

import config
from gui.models.settings_model import SettingsModel
from gui.themes.theme_manager import ThemeManager
from gui.widgets.sidebar import SidebarWidget
from gui.widgets.topbar import TopBarWidget


class MainWindow(ctk.CTk):
    """
    Main application shell window with Windows 11 Fluent Floating Card layout.
    """

    MIN_WIDTH: int = 1080
    MIN_HEIGHT: int = 700

    def __init__(self, settings_model: SettingsModel) -> None:
        super().__init__()
        self.settings_model = settings_model

        # Window Metadata & Geometry
        self.title(f"{config.APP_NAME} ({config.APP_VERSION})")
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)

        # Restore window state
        width = int(self.settings_model.get("window_width", 1150))
        height = int(self.settings_model.get("window_height", 720))
        self.geometry(f"{width}x{height}")

        # Initialize Theme
        theme_mode = str(self.settings_model.get("theme_mode", "System"))
        ThemeManager.initialize_theme(theme_mode)

        # Configure Grid Layout (240px Sidebar + Container)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Navigation & View Callback Hooks
        self.nav_callbacks: Dict[str, Callable[[], None]] = {}

        # 1. Top Header Bar
        self.topbar = TopBarWidget(
            self,
            on_theme_change=self._on_theme_change,
            on_settings_click=lambda: self._on_nav_click("settings"),
            initial_theme=theme_mode,
        )
        self.topbar.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=(15, 5)
        )

        # 2. Sidebar Navigation Widget (240px)
        self.sidebar = SidebarWidget(
            self,
            on_nav_click=self._on_nav_click,
        )
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(15, 5), pady=(10, 15))

        # 3. Dynamic Page View Container Frame
        self.container_frame = ctk.CTkFrame(
            self, corner_radius=20, fg_color=("gray95", "#0F172A")
        )
        self.container_frame.grid(
            row=1, column=1, sticky="nsew", padx=(10, 15), pady=(10, 15)
        )
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.container_frame.grid_rowconfigure(0, weight=1)

        # Window Close & Keyboard Bindings
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._bind_keyboard_shortcuts()

    def register_nav_callback(
        self, page_key: str, callback: Callable[[], None]
    ) -> None:
        """Registers callback handler for page switching."""
        self.nav_callbacks[page_key] = callback

    def set_active_page(self, page_key: str) -> None:
        """Highlights active sidebar navigation button and updates header title."""
        self.sidebar.set_active_page(page_key)

        titles = {
            "home": "Dashboard",
            "encrypt": "Encrypt File",
            "decrypt": "Decrypt File",
            "history": "Audit History",
            "settings": "Settings",
            "about": "About Engine",
        }
        self.topbar.set_title(titles.get(page_key, "Dashboard"))

    def set_page_title(self, title: str) -> None:
        """Updates header title bar text."""
        self.topbar.set_title(title)

    def _on_nav_click(self, page_key: str) -> None:
        if page_key in self.nav_callbacks:
            self.nav_callbacks[page_key]()

    def _on_theme_change(self, mode: str) -> None:
        ThemeManager.initialize_theme(mode)
        self.settings_model.set("theme_mode", mode)

    def _bind_keyboard_shortcuts(self) -> None:
        """Binds accessibility keyboard shortcuts."""
        self.bind("<Control-o>", lambda e: self._on_nav_click("home"))
        self.bind("<Control-e>", lambda e: self._on_nav_click("encrypt"))
        self.bind("<Control-d>", lambda e: self._on_nav_click("decrypt"))
        self.bind("<Control-h>", lambda e: self._on_nav_click("history"))
        self.bind("<Control-comma>", lambda e: self._on_nav_click("settings"))
        self.bind("<F1>", lambda e: self._on_nav_click("about"))

    def _on_close(self) -> None:
        """Saves window geometry before exiting."""
        try:
            self.settings_model.set("window_width", self.winfo_width())
            self.settings_model.set("window_height", self.winfo_height())
            self.settings_model.save()
        except Exception:
            pass
        self.destroy()
