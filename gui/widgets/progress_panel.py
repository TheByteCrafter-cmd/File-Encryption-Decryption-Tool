"""
Advanced Real-Time Progress Panel Widget.

Displays custom CTk progress bar, percentage indicator, active target filename,
processed MB / total MB, real-time transfer speed (MB/s), elapsed time, and ETA calculations.
"""

import time
from typing import Optional

import customtkinter as ctk


class ProgressPanelWidget(ctk.CTkFrame):
    """
    Advanced real-time progress panel widget with transfer metrics.
    """

    def __init__(self, master: ctk.CTkBaseClass, **kwargs) -> None:
        super().__init__(
            master, corner_radius=10, fg_color=("gray90", "gray20"), **kwargs
        )

        self.grid_columnconfigure(0, weight=1)
        self.start_time: Optional[float] = None
        self.last_time: Optional[float] = None
        self.last_bytes: int = 0

        # 1. Filename & Percentage Header Row
        self.header_row = ctk.CTkFrame(self, fg_color="transparent")
        self.header_row.grid(row=0, column=0, sticky="ew", padx=15, pady=(12, 5))
        self.header_row.grid_columnconfigure(0, weight=1)

        self.filename_label = ctk.CTkLabel(
            self.header_row,
            text="Ready",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        self.filename_label.grid(row=0, column=0, sticky="ew")

        self.percent_label = ctk.CTkLabel(
            self.header_row,
            text="0%",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#0078D4",
        )
        self.percent_label.grid(row=0, column=1, sticky="e")

        # 2. Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, height=10, corner_radius=5)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        self.progress_bar.set(0.0)

        # 3. Metrics Details Footer Row (Processed MB / Speed / ETA)
        self.metrics_row = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_row.grid(row=2, column=0, sticky="ew", padx=15, pady=(5, 12))
        self.metrics_row.grid_columnconfigure(1, weight=1)

        self.bytes_label = ctk.CTkLabel(
            self.metrics_row,
            text="0.0 MB / 0.0 MB",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
        )
        self.bytes_label.grid(row=0, column=0, sticky="w")

        self.speed_eta_label = ctk.CTkLabel(
            self.metrics_row,
            text="Speed: 0 MB/s | ETA: --",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
        )
        self.speed_eta_label.grid(row=0, column=1, sticky="e")

    def reset(self, filename: str = "Ready") -> None:
        """Resets progress panel counters and timers."""
        self.start_time = time.time()
        self.last_time = self.start_time
        self.last_bytes = 0

        self.filename_label.configure(text=filename)
        self.percent_label.configure(text="0%")
        self.progress_bar.set(0.0)
        self.bytes_label.configure(text="0.0 MB / 0.0 MB")
        self.speed_eta_label.configure(text="Speed: 0 MB/s | ETA: --")

    def update_progress(self, processed_bytes: int, total_bytes: int) -> None:
        """
        Updates progress bar, percentage, MB/s speed, and ETA.
        """
        if self.start_time is None:
            self.start_time = time.time()
            self.last_time = self.start_time

        now = time.time()
        ratio = (processed_bytes / total_bytes) if total_bytes > 0 else 1.0
        percent_str = f"{int(ratio * 100)}%"

        self.progress_bar.set(ratio)
        self.percent_label.configure(text=percent_str)

        proc_mb = processed_bytes / (1024 * 1024)
        total_mb = total_bytes / (1024 * 1024)
        self.bytes_label.configure(text=f"{proc_mb:.1f} MB / {total_mb:.1f} MB")

        # Calculate Transfer Speed & ETA
        elapsed = now - self.start_time
        if elapsed > 0 and processed_bytes > 0:
            speed_bps = processed_bytes / elapsed
            speed_mbps = speed_bps / (1024 * 1024)

            remaining_bytes = total_bytes - processed_bytes
            eta_seconds = (remaining_bytes / speed_bps) if speed_bps > 0 else 0

            speed_str = f"{speed_mbps:.1f} MB/s"
            eta_str = f"{int(eta_seconds)}s" if eta_seconds < 3600 else "> 1h"
            self.speed_eta_label.configure(text=f"Speed: {speed_str} | ETA: {eta_str}")
