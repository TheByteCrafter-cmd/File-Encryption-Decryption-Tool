"""
Settings View Business Logic Controller.

Manages loading and saving configuration parameters from SettingsModel and updating theme settings.
"""

from gui.models.settings_model import SettingsModel
from gui.utils.theme_manager import ThemeManager
from gui.views.settings_view import SettingsView
from gui.widgets.dialogs import ModernDialog


class SettingsController:
    """
    Controller managing user configuration settings.
    """

    def __init__(self, view: SettingsView, settings_model: SettingsModel) -> None:
        self.view = view
        self.settings_model = settings_model

        # Wire Up Event Callback
        self.view.on_save_click = self.save_settings

        # Load values into view
        self.load_settings()

    def load_settings(self) -> None:
        """Populates UI controls from model values."""
        theme = str(self.settings_model.get("theme_mode", "System"))
        self.view.theme_combo.set(theme)

        outdir = str(self.settings_model.get("default_output_dir", ""))
        self.view.outdir_entry.delete(0, "end")
        self.view.outdir_entry.insert(0, outdir)

        auto_open = bool(self.settings_model.get("auto_open_output_dir", False))
        if auto_open:
            self.view.auto_open_switch.select()
        else:
            self.view.auto_open_switch.deselect()

        chunk_bytes = int(self.settings_model.get("chunk_size", 65536))
        if chunk_bytes == 65536:
            self.view.chunk_combo.set("64 KB (Default)")
        elif chunk_bytes == 131072:
            self.view.chunk_combo.set("128 KB")
        elif chunk_bytes == 262144:
            self.view.chunk_combo.set("256 KB")
        elif chunk_bytes == 1048576:
            self.view.chunk_combo.set("1 MB")

    def save_settings(self) -> None:
        """Persists updated UI values to SettingsModel."""
        theme = self.view.theme_combo.get()
        outdir = self.view.outdir_entry.get()
        auto_open = bool(self.view.auto_open_switch.get())
        chunk_str = self.view.chunk_combo.get()

        chunk_bytes = 65536
        if "128 KB" in chunk_str:
            chunk_bytes = 131072
        elif "256 KB" in chunk_str:
            chunk_bytes = 262144
        elif "1 MB" in chunk_str:
            chunk_bytes = 1048576

        self.settings_model.set("theme_mode", theme)
        self.settings_model.set("default_output_dir", outdir)
        self.settings_model.set("auto_open_output_dir", auto_open)
        self.settings_model.set("chunk_size", chunk_bytes)

        # Update Theme Runtime
        ThemeManager.initialize_theme(theme)

        ModernDialog(
            master=self.view.winfo_toplevel(),
            title="Settings Saved",
            message="Application settings have been updated successfully!",
            dialog_type="success",
        )
