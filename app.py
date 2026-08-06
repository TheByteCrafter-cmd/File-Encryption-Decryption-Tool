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

import config
from gui.controllers.decrypt_controller import DecryptController
from gui.controllers.encrypt_controller import EncryptController
from gui.controllers.history_controller import HistoryController
from gui.controllers.main_controller import MainController
from gui.models.history_model import HistoryModel
from gui.models.settings_model import SettingsModel
from gui.views.decrypt_view import DecryptView
from gui.views.encrypt_view import EncryptView
from gui.views.history_view import HistoryView
from gui.views.home_view import HomeView
from gui.views.main_window import MainWindow


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
    )
    stats = history_model.get_stats()
    home_view.update_stats(
        stats["encrypted_count"], stats["decrypted_count"], stats["total_bytes"]
    )
    main_controller.register_view("home", home_view)

    encrypt_view = EncryptView(master=app.container_frame)
    encrypt_controller = EncryptController(
        view=encrypt_view,
        history_model=history_model,
        settings_model=settings_model,
    )
    main_controller.register_view("encrypt", encrypt_view)

    decrypt_view = DecryptView(master=app.container_frame)
    decrypt_controller = DecryptController(
        view=decrypt_view,
        history_model=history_model,
        settings_model=settings_model,
    )
    main_controller.register_view("decrypt", decrypt_view)

    history_view = HistoryView(master=app.container_frame)
    history_controller = HistoryController(
        view=history_view,
        history_model=history_model,
    )
    main_controller.register_view("history", history_view)

    # Create Placeholder Views for Remaining Tabs
    for page_key in ["settings", "about"]:
        view = ctk.CTkFrame(app.container_frame, corner_radius=10)
        view.grid_columnconfigure(0, weight=1)
        view.grid_rowconfigure(0, weight=1)

        label = ctk.CTkLabel(
            view,
            text=f"Loading {page_key.capitalize()} View...",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        label.grid(row=0, column=0, padx=20, pady=20)
        main_controller.register_view(page_key, view)

    # Restore last open page or default to home
    last_page = str(settings_model.get("last_page", "home"))
    main_controller.show_page(last_page)

    app.mainloop()


if __name__ == "__main__":
    main()
