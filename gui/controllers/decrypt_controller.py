"""
Decrypt View Business Logic Controller.

Coordinates asynchronous single and batch file decryption dispatches to the Phase 1 FileDecryptor backend
on background worker threads, handles real-time progress panel updates, queue controls, logs to HistoryModel,
and triggers popups.
"""

import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Optional

from encryption.aes_decrypt import FileDecryptor
from encryption.utils import IntegrityVerificationError, InvalidFileFormatError, logger
from gui.models.history_model import HistoryModel
from gui.models.job_model import Job, JobQueue
from gui.models.settings_model import SettingsModel
from gui.views.decrypt_view import DecryptView
from gui.widgets.dialogs import ModernDialog


class DecryptController:
    """
    Controller managing decryption view workflow, batch queue, and background worker threads.
    """

    def __init__(
        self,
        view: DecryptView,
        history_model: HistoryModel,
        settings_model: SettingsModel,
        on_operation_complete: Optional[Callable[[], None]] = None,
    ) -> None:
        self.view = view
        self.history_model = history_model
        self.settings_model = settings_model
        self.on_operation_complete = on_operation_complete
        self.last_output_path: Optional[Path] = None
        self.job_queue = JobQueue()

        # Wire Up View Event Callbacks
        self.view.on_decrypt_click = self.start_decryption
        self.view.drop_zone.on_batch_selected = self.on_batch_files_selected

        # Wire Up Queue Panel Button Callbacks
        self.view.queue_panel.on_pause_click = self.pause_batch
        self.view.queue_panel.on_resume_click = self.resume_batch
        self.view.queue_panel.on_cancel_click = self.cancel_batch
        self.view.queue_panel.on_clear_click = self.clear_queue

    def on_batch_files_selected(self, files: List[Path]) -> None:
        """Handler called when drop zone selects batch of files."""
        password = self.view.password_meter.get_password()
        for idx, f in enumerate(files):
            job = Job(
                id=f"dec_{int(time.time())}_{idx}",
                input_path=f,
                mode="Decrypt",
                password=password,
                total_bytes=f.stat().st_size if f.exists() else 0,
            )
            self.job_queue.add_job(job)
        self._refresh_queue_ui()

    def start_decryption(self) -> None:
        """Validates inputs and dispatches batch decryption worker thread."""
        target_files = self.view.drop_zone.selected_files or (
            [self.view.drop_zone.selected_file]
            if self.view.drop_zone.selected_file
            else []
        )
        password = self.view.password_meter.get_password()

        if not target_files:
            ModernDialog(
                master=self.view.winfo_toplevel(),
                title="No File Selected",
                message="Please select or drag & drop encrypted (.enc) file(s) to decrypt.",
                dialog_type="warning",
            )
            return

        if not password:
            ModernDialog(
                master=self.view.winfo_toplevel(),
                title="Password Required",
                message="Please enter the password to decrypt the file(s).",
                dialog_type="warning",
            )
            return

        # Pre-flight File Validations
        for f in target_files:
            if not f.exists():
                ModernDialog(
                    master=self.view.winfo_toplevel(),
                    title="File Not Found",
                    message=f"Encrypted file does not exist:\n{f.name}",
                    dialog_type="error",
                )
                return
            if f.suffix.lower() != ".enc":
                ModernDialog(
                    master=self.view.winfo_toplevel(),
                    title="Invalid File Extension",
                    message=f"Target file does not have a .enc extension:\n{f.name}",
                    dialog_type="warning",
                )
                return
            if not os.access(f, os.R_OK):
                ModernDialog(
                    master=self.view.winfo_toplevel(),
                    title="Permission Denied",
                    message=f"Cannot read file due to missing permissions:\n{f.name}",
                    dialog_type="error",
                )
                return

        # Reset Queue and populate
        self.job_queue.clear()
        for idx, f in enumerate(target_files):
            job = Job(
                id=f"dec_{int(time.time())}_{idx}",
                input_path=f,
                mode="Decrypt",
                password=password,
                total_bytes=f.stat().st_size,
            )
            self.job_queue.add_job(job)

        self._refresh_queue_ui()
        self.view.hide_shortcuts()
        self.view.set_processing_state(True)

        # Dispatch Background Batch Worker Thread
        thread = threading.Thread(target=self._worker_batch_decrypt, daemon=True)
        thread.start()

    def pause_batch(self) -> None:
        """Pauses active batch processing."""
        self.job_queue.pause_all()
        self._refresh_queue_ui()

    def resume_batch(self) -> None:
        """Resumes active batch processing."""
        self.job_queue.resume_all()
        self._refresh_queue_ui()

    def cancel_batch(self) -> None:
        """Cancels active batch processing."""
        self.job_queue.cancel_all()
        self._refresh_queue_ui()

    def clear_queue(self) -> None:
        """Clears completed/cancelled queue items."""
        self.job_queue.clear()
        self._refresh_queue_ui()

    def _refresh_queue_ui(self) -> None:
        """Schedules UI queue panel refresh safely on main thread."""
        self.view.after(
            0, lambda: self.view.queue_panel.update_jobs(self.job_queue.jobs)
        )

    def _worker_batch_decrypt(self) -> None:
        """Background worker loop executing batch queue jobs sequentially."""
        custom_output_dir = (
            Path(self.settings_model.get("default_output_dir"))
            if self.settings_model.get("default_output_dir")
            else None
        )
        chunk_size = int(self.settings_model.get("chunk_size", 65536))

        for job in self.job_queue.jobs:
            if job.is_cancelled():
                job.status = "CANCELLED"
                self._refresh_queue_ui()
                continue

            # Wait while paused
            while job.is_paused() and not job.is_cancelled():
                time.sleep(0.2)

            if job.is_cancelled():
                job.status = "CANCELLED"
                self._refresh_queue_ui()
                continue

            job.status = "PROCESSING"
            self._refresh_queue_ui()

            self.view.after(
                0,
                lambda f=job.input_path.name: self.view.progress_panel.reset(
                    filename=f
                ),
            )

            try:

                def progress_hook(processed: int, total: int) -> None:
                    job.processed_bytes = processed
                    self.view.after(
                        0,
                        lambda: self.view.progress_panel.update_progress(
                            processed, total
                        ),
                    )

                result_path = FileDecryptor.decrypt_file(
                    encrypted_path=job.input_path,
                    password=job.password,
                    output_dir=custom_output_dir,
                    progress_callback=progress_hook,
                    chunk_size=chunk_size,
                )

                job.output_path = result_path
                job.status = "SUCCESS"
                self.last_output_path = result_path
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                self.history_model.add_record(
                    filename=result_path.name,
                    operation="Decrypt",
                    file_size=result_path.stat().st_size,
                    status="SUCCESS",
                    output_path=str(result_path),
                    timestamp=now_str,
                )
            except (IntegrityVerificationError, InvalidFileFormatError) as sec_err:
                logger.error(f"Decryption failed for {job.input_path.name}: {sec_err}")
                job.status = "FAILED"
                job.error_message = str(sec_err)
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                self.history_model.add_record(
                    filename=job.input_path.name,
                    operation="Decrypt",
                    file_size=job.total_bytes,
                    status="FAILED",
                    output_path="",
                    timestamp=now_str,
                )
            except Exception as err:
                logger.error(f"GUI Decrypt Controller caught error: {err}")
                job.status = "FAILED"
                job.error_message = str(err)
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                self.history_model.add_record(
                    filename=job.input_path.name,
                    operation="Decrypt",
                    file_size=job.total_bytes,
                    status="FAILED",
                    output_path="",
                    timestamp=now_str,
                )

            self._refresh_queue_ui()

        # Batch Loop Finished
        self.view.after(0, self._on_batch_complete)

    def _on_batch_complete(self) -> None:
        """Handles post-batch completion UI state updates."""
        self.view.set_processing_state(False)
        if self.on_operation_complete:
            self.on_operation_complete()

        if self.last_output_path:
            self.view.show_shortcuts(
                on_open_folder=lambda: self._open_output_folder(self.last_output_path),
                on_copy_path=lambda: self._copy_path_to_clipboard(
                    self.last_output_path
                ),
            )

            # Auto open output folder if setting enabled
            if self.settings_model.get("auto_open_output_dir", False):
                self._open_output_folder(self.last_output_path)

        ModernDialog(
            master=self.view.winfo_toplevel(),
            title="Batch Processing Completed",
            message="All queued decryption tasks have finished processing.",
            dialog_type="success",
        )

    def _open_output_folder(self, output_path: Path) -> None:
        """Opens output folder in system File Explorer."""
        try:
            folder = output_path.parent if output_path else Path.cwd()
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
