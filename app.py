"""
Secure File Encryption & Decryption Tool - Desktop Application Entry Point.

Initializes CustomTkinter / TkinterDnD runtime, loads persistent window state & settings,
instantiates MVC components, and launches the desktop application GUI.
"""

import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import customtkinter as ctk

from encryption.utils import logger
from gui.controllers.decrypt_controller import DecryptController
from gui.controllers.encrypt_controller import EncryptController
from gui.controllers.history_controller import HistoryController
from gui.controllers.main_controller import MainController
from gui.controllers.settings_controller import SettingsController
from gui.models.history_model import HistoryModel
from gui.models.settings_model import SettingsModel
from gui.views.about_view import AboutView
from gui.views.decrypt_view import DecryptView
from gui.views.encrypt_view import EncryptView
from gui.views.history_view import HistoryView
from gui.views.home_view import HomeView
from gui.views.main_window import MainWindow
from gui.views.settings_view import SettingsView
from gui.widgets.dialogs import ModernDialog


def handle_uncaught_exception(exc_type, exc_value, exc_traceback) -> None:
    """Global crash recovery hook logging unhandled exceptions safely."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical(
        "Uncaught Application Exception", exc_info=(exc_type, exc_value, exc_traceback)
    )


sys.excepthook = handle_uncaught_exception


def main() -> None:
    """Launches the desktop GUI application."""
    settings_model = SettingsModel()

    # Create Main Application Shell Window
    app = MainWindow(settings_model=settings_model)
    main_controller = MainController(main_window=app, settings_model=settings_model)

    history_model = HistoryModel()

    # Instantiate Views
    home_view = HomeView(
        master=app.container_frame,
        on_encrypt_click=lambda: main_controller.show_page("encrypt"),
        on_decrypt_click=lambda: main_controller.show_page("decrypt"),
        on_history_click=lambda: main_controller.show_page("history"),
        on_settings_click=lambda: main_controller.show_page("settings"),
    )
    stats = history_model.get_stats()
    home_view.update_stats(
        stats["encrypted_count"], stats["decrypted_count"], stats["total_bytes"]
    )
    home_view.update_recent_files(history_model.records)
    main_controller.register_view("home", home_view)

    history_view = HistoryView(master=app.container_frame)
    history_controller = HistoryController(
        view=history_view,
        history_model=history_model,
    )
    main_controller.register_view("history", history_view)

    def refresh_global_stats() -> None:
        """Refreshes dashboard metrics and history table after operation completion."""
        s = history_model.get_stats()
        home_view.update_stats(
            s["encrypted_count"], s["decrypted_count"], s["total_bytes"]
        )
        home_view.update_recent_files(history_model.records)
        history_controller.refresh()

    encrypt_view = EncryptView(master=app.container_frame)
    encrypt_controller = EncryptController(
        view=encrypt_view,
        history_model=history_model,
        settings_model=settings_model,
        on_operation_complete=refresh_global_stats,
    )
    main_controller.register_view("encrypt", encrypt_view)

    decrypt_view = DecryptView(master=app.container_frame)
    decrypt_controller = DecryptController(
        view=decrypt_view,
        history_model=history_model,
        settings_model=settings_model,
        on_operation_complete=refresh_global_stats,
    )
    main_controller.register_view("decrypt", decrypt_view)

    settings_view = SettingsView(master=app.container_frame)
    settings_controller = SettingsController(
        view=settings_view,
        settings_model=settings_model,
    )
    main_controller.register_view("settings", settings_view)

    about_view = AboutView(master=app.container_frame)
    main_controller.register_view("about", about_view)

    # Restore last open page or default to home
    last_page = str(settings_model.get("last_page", "home"))
    main_controller.show_page(last_page)

    app.mainloop()


if __name__ == "__main__":
    main()
