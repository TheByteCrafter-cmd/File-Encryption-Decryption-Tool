"""
Main Application Controller.

Manages top-level navigation, view lifecycle transitions, keyboard shortcut routing,
and shell header state synchronization.
"""

from typing import Callable, Dict

import customtkinter as ctk

from gui.models.settings_model import SettingsModel
from gui.views.main_window import MainWindow


class MainController:
    """
    Controller responsible for application navigation and view orchestration.
    """

    def __init__(self, main_window: MainWindow, settings_model: SettingsModel) -> None:
        self.window = main_window
        self.settings_model = settings_model
        self.views: Dict[str, ctk.CTkFrame] = {}

        # Register Navigation Callback Handlers
        for page_key in ["home", "encrypt", "decrypt", "history", "settings", "about"]:
            self.window.register_nav_callback(
                page_key, self._make_nav_callback(page_key)
            )

    def _make_nav_callback(self, page_key: str) -> Callable[[], None]:
        """Creates a type-safe navigation callback for target page_key."""
        return lambda: self.show_page(page_key)

    def register_view(self, page_key: str, view_frame: ctk.CTkFrame) -> None:
        """Registers a page view frame into the controller container."""
        self.views[page_key] = view_frame

    def show_page(self, page_key: str) -> None:
        """Switches active page view frame."""
        if page_key not in self.views:
            return

        # Hide all view frames
        for frame in self.views.values():
            frame.grid_forget()

        # Display target view frame
        target_view = self.views[page_key]
        target_view.grid(row=0, column=0, sticky="nsew")

        # Update Sidebar & Header Title
        self.window.set_active_page(page_key)
        self.settings_model.set("last_page", page_key)

        titles = {
            "home": "Dashboard Overview",
            "encrypt": "Encrypt File (AES-256-GCM)",
            "decrypt": "Decrypt File (AES-256-GCM)",
            "history": "Operation Audit History",
            "settings": "Application Settings",
            "about": "About & Specifications",
        }
        self.window.set_page_title(titles.get(page_key, "Secure File Tool"))
