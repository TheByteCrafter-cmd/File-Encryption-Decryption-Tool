"""
Decrypt View Business Logic Controller.

Coordinates asynchronous file decryption dispatches to the Phase 1 FileDecryptor backend on background
worker threads, handles real-time progress panel updates, logs to HistoryModel, and triggers popups.
"""

import os
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

from encryption.aes_decrypt import FileDecryptor
from encryption.utils import IntegrityVerificationError, InvalidFileFormatError, logger
from gui.models.history_model import HistoryModel
from gui.models.settings_model import SettingsModel
from gui.views.decrypt_view import DecryptView
from gui.widgets.dialogs import ModernDialog


class DecryptController:
    """
    Controller managing decryption view workflow and background worker thread.
    """

    def __init__(
        self,
        view: DecryptView,
        history_model: HistoryModel,
        settings_model: SettingsModel,
    ) -> None:
        self.view = view
        self.history_model = history_model
        self.settings_model = settings_model
        self.last_output_path: Optional[Path] = None

        # Wire Up View Event Callbacks
        self.view.on_decrypt_click = self.start_decryption

    def start_decryption(self) -> None:
        """Validates inputs and dispatches decryption worker thread."""
        target_file = self.view.drop_zone.selected_file
        password = self.view.password_meter.get_password()

        if not target_file:
            ModernDialog(
                master=self.view.winfo_toplevel(),
                title="No File Selected",
                message="Please select or drag & drop an encrypted (.enc) file to decrypt.",
                dialog_type="warning",
            )
            return

        if not password:
            ModernDialog(
                master=self.view.winfo_toplevel(),
                title="Password Required",
                message="Please enter the password to decrypt the file.",
                dialog_type="warning",
            )
            return

        # Prepare UI State
        self.view.hide_shortcuts()
        self.view.set_processing_state(True)
        self.view.progress_panel.reset(filename=target_file.name)

        # Dispatch Background Worker Thread
        thread = threading.Thread(
            target=self._worker_decrypt,
            args=(target_file, password),
            daemon=True,
        )
        thread.start()

    def _worker_decrypt(self, input_file: Path, password: str) -> None:
        """Background thread executing streaming decryption."""
        try:
            custom_output_dir = (
                Path(self.settings_model.get("default_output_dir"))
                if self.settings_model.get("default_output_dir")
                else None
            )

            # Callback wrapper updating UI safely on main thread
            def progress_hook(processed: int, total: int) -> None:
                self.view.after(
                    0,
                    lambda: self.view.progress_panel.update_progress(processed, total),
                )

            result_path = FileDecryptor.decrypt_file(
                encrypted_path=input_file,
                password=password,
                output_dir=custom_output_dir,
                progress_callback=progress_hook,
                chunk_size=int(self.settings_model.get("chunk_size")),
            )

            self.last_output_path = result_path
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Log to History Model
            self.history_model.add_record(
                filename=result_path.name,
                operation="Decrypt",
                file_size=result_path.stat().st_size,
                status="SUCCESS",
                output_path=str(result_path),
                timestamp=now_str,
            )

            # Schedule UI Success Callback
            self.view.after(0, lambda: self._on_decryption_success(result_path))

        except (IntegrityVerificationError, InvalidFileFormatError) as sec_err:
            logger.error(f"Decryption failed: {sec_err}")
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history_model.add_record(
                filename=input_file.name,
                operation="Decrypt",
                file_size=input_file.stat().st_size if input_file.exists() else 0,
                status="FAILED",
                output_path="",
                timestamp=now_str,
            )
            self.view.after(0, lambda: self._on_decryption_error(str(sec_err)))

        except Exception as err:
            logger.error(f"GUI Decrypt Controller caught error: {err}")
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history_model.add_record(
                filename=input_file.name,
                operation="Decrypt",
                file_size=input_file.stat().st_size if input_file.exists() else 0,
                status="FAILED",
                output_path="",
                timestamp=now_str,
            )
            self.view.after(0, lambda: self._on_decryption_error(str(err)))

    def _on_decryption_success(self, output_path: Path) -> None:
        """Handles post-decryption UI success updates."""
        self.view.set_processing_state(False)

        self.view.show_shortcuts(
            on_open_folder=lambda: self._open_output_folder(output_path),
            on_copy_path=lambda: self._copy_path_to_clipboard(output_path),
        )

        ModernDialog(
            master=self.view.winfo_toplevel(),
            title="Decryption Completed",
            message=f"File decrypted successfully!\nOriginal filename restored:\n{output_path.name}",
            dialog_type="success",
        )

        # Auto open output folder if setting enabled
        if self.settings_model.get("auto_open_output_dir", False):
            self._open_output_folder(output_path)

    def _on_decryption_error(self, error_msg: str) -> None:
        """Handles post-decryption UI error updates."""
        self.view.set_processing_state(False)
        ModernDialog(
            master=self.view.winfo_toplevel(),
            title="Decryption Failed",
            message=f"Could not decrypt file:\n{error_msg}",
            dialog_type="error",
            details=error_msg,
        )

    def _open_output_folder(self, output_path: Path) -> None:
        """Opens output folder in system File Explorer."""
        try:
            folder = output_path.parent
            if os.name == "nt":
                os.startfile(folder)  # type: ignore[attr-defined]
            else:
                subprocess.Popen(
                    ["open" if sys.platform == "darwin" else "xdg-open", str(folder)]
                )
        except Exception as err:
            logger.warning(f"Unable to open file explorer: {err}")

    def _copy_path_to_clipboard(self, output_path: Path) -> None:
        """Copies output path string to clipboard."""
        self.view.clipboard_clear()
        self.view.clipboard_append(str(output_path))
        ModernDialog(
            master=self.view.winfo_toplevel(),
            title="Path Copied",
            message="Restored file path copied to clipboard!",
            dialog_type="info",
        )
