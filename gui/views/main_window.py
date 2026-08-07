"""
Main Application Window Shell View.

Provides commercial Windows 11 Fluent Design UI layout with floating sidebar card,
header bar with live status indicators, theme controls, and keyboard shortcuts.
"""

from typing import Callable, Dict, Optional

import customtkinter as ctk

import config
from gui.models.settings_model import SettingsModel
from gui.utils.theme_manager import ThemeManager


class MainWindow(ctk.CTk):
    """
    Main application shell window with Windows 11 Fluent floating card layout.
    """

    MIN_WIDTH: int = 1050
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

        # Configure Grid Layout (Floating Sidebar + Container)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Navigation & View Callback Hooks
        self.nav_callbacks: Dict[str, Callable[[], None]] = {}
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}

        # 1. Header Bar
        self._build_header()

        # 2. Floating Sidebar Navigation Card
        self._build_sidebar()

        # 3. Dynamic Page View Container
        self.container_frame = ctk.CTkFrame(
            self, corner_radius=16, fg_color=("gray95", "gray15")
        )
        self.container_frame.grid(
            row=1, column=1, sticky="nsew", padx=(10, 15), pady=(10, 15)
        )
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.container_frame.grid_rowconfigure(0, weight=1)

        # Window Close & Save Geometry Bindings
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._bind_keyboard_shortcuts()

    def _build_header(self) -> None:
        """Constructs top header bar with active view title, status badge, and theme toggle."""
        self.header_frame = ctk.CTkFrame(
            self, height=54, corner_radius=12, fg_color=("gray90", "gray20")
        )
        self.header_frame.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=(15, 5)
        )
        self.header_frame.grid_columnconfigure(1, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            text=" 🔐 ",
            font=ctk.CTkFont(size=22),
        )
        self.logo_label.grid(row=0, column=0, padx=(15, 5), pady=10)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=config.APP_NAME,
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.title_label.grid(row=0, column=1, sticky="w", padx=5, pady=10)

        # Engine Active Status Badge
        self.status_badge = ctk.CTkLabel(
            self.header_frame,
            text="● Engine Active",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#16A34A",
        )
        self.status_badge.grid(row=0, column=2, padx=(0, 15), pady=10)

        # Theme Switcher Control
        current_theme = str(self.settings_model.get("theme_mode", "System"))
        self.theme_switch = ctk.CTkOptionMenu(
            self.header_frame,
            values=["System", "Dark", "Light"],
            command=self._on_theme_change,
            width=100,
        )
        self.theme_switch.set(current_theme)
        self.theme_switch.grid(row=0, column=3, padx=(0, 15), pady=10)

    def _build_sidebar(self) -> None:
        """Constructs left floating navigation sidebar card."""
        self.sidebar_frame = ctk.CTkFrame(
            self, width=220, corner_radius=16, fg_color=("gray90", "gray20")
        )
        self.sidebar_frame.grid(
            row=1, column=0, sticky="nsew", padx=(15, 5), pady=(10, 15)
        )
        self.sidebar_frame.grid_rowconfigure(
            7, weight=1
        )  # Push version badge to bottom

        # Brand Header
        brand_lbl = ctk.CTkLabel(
            self.sidebar_frame,
            text="FEDT Security",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w",
        )
        brand_lbl.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

        pages = [
            ("home", "🏠  Dashboard", "Ctrl+O"),
            ("encrypt", "🔒  Encrypt File", "Ctrl+E"),
            ("decrypt", "🔓  Decrypt File", "Ctrl+D"),
            ("history", "📜  Audit History", "Ctrl+H"),
            ("settings", "⚙️  Settings", "Ctrl+,"),
            ("about", "ℹ️  About Engine", "F1"),
        ]

        for i, (page_key, label, shortcut) in enumerate(pages, start=1):
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=label,
                anchor="w",
                font=ctk.CTkFont(size=13),
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray75", "gray30"),
                height=38,
                corner_radius=10,
                command=lambda k=page_key: self._on_nav_click(k),
            )
            btn.grid(row=i, column=0, padx=10, pady=4, sticky="ew")
            self.nav_buttons[page_key] = btn

        # App Version Footer Badge
        self.version_badge = ctk.CTkLabel(
            self.sidebar_frame,
            text=f"v{config.APP_VERSION}",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
        )
        self.version_badge.grid(row=8, column=0, padx=10, pady=15, sticky="s")

    def register_nav_callback(
        self, page_key: str, callback: Callable[[], None]
    ) -> None:
        """Registers callback handler for page switching."""
        self.nav_callbacks[page_key] = callback

    def set_active_page(self, page_key: str) -> None:
        """Highlights active sidebar navigation button with Fluent active pill styling."""
        for key, btn in self.nav_buttons.items():
            if key == page_key:
                btn.configure(
                    fg_color=("#2563EB", "#2563EB"),
                    text_color="#FFFFFF",
                    font=ctk.CTkFont(size=13, weight="bold"),
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=("gray10", "gray90"),
                    font=ctk.CTkFont(size=13, weight="normal"),
                )

    def set_page_title(self, title: str) -> None:
        """Updates header title bar text."""
        self.title_label.configure(text=title)

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
        """Saves window geometry and settings before exiting."""
        try:
            self.settings_model.set("window_width", self.winfo_width())
            self.settings_model.set("window_height", self.winfo_height())
            self.settings_model.save()
        except Exception:
            pass
        self.destroy()
