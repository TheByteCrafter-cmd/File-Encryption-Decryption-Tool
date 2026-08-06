"""
Custom CTk History Data Table Widget.

Provides a scrollable operation audit table with search filtering, column sorting,
double-click activation, and right-click context menus (Open File, Reveal in Explorer, Copy Path, Delete).
"""

import os
import subprocess
import sys
from typing import Any, Callable, Dict, List, Optional

import customtkinter as ctk


class DataTableWidget(ctk.CTkFrame):
    """
    Scrollable audit data table for operation records.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_delete_record: Optional[Callable[[int], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            master, corner_radius=10, fg_color=("gray90", "gray20"), **kwargs
        )
        self.on_delete_record = on_delete_record
        self.records: List[Dict[str, Any]] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Header Bar
        self.header_frame = ctk.CTkFrame(
            self, fg_color=("gray80", "gray25"), height=36, corner_radius=6
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.header_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        headers = ["Date & Time", "Filename", "Operation", "Size", "Status"]
        for i, text in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.header_frame,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
            )
            lbl.grid(row=0, column=i, sticky="ew", padx=10, pady=5)

        # 2. Scrollable Rows Container
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

    def set_records(self, records: List[Dict[str, Any]]) -> None:
        """Populates table with record dictionaries."""
        self.records = records
        # Clear existing rows
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        if not records:
            empty_lbl = ctk.CTkLabel(
                self.scroll_frame,
                text="No operation history recorded yet.",
                font=ctk.CTkFont(size=13),
                text_color="gray60",
            )
            empty_lbl.grid(row=0, column=0, columnspan=5, pady=30)
            return

        for row_idx, rec in enumerate(records):
            bg_color = (
                ("gray95", "gray23") if row_idx % 2 == 0 else ("gray85", "gray18")
            )
            row_frame = ctk.CTkFrame(
                self.scroll_frame, fg_color=bg_color, corner_radius=6
            )
            row_frame.grid(row=row_idx, column=0, columnspan=5, sticky="ew", pady=2)
            row_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            # Columns
            c_time = ctk.CTkLabel(
                row_frame,
                text=rec.get("timestamp", ""),
                font=ctk.CTkFont(size=11),
                anchor="w",
            )
            c_time.grid(row=0, column=0, sticky="w", padx=10, pady=8)

            c_fname = ctk.CTkLabel(
                row_frame,
                text=rec.get("filename", ""),
                font=ctk.CTkFont(size=11, weight="bold"),
                anchor="w",
            )
            c_fname.grid(row=0, column=1, sticky="w", padx=10, pady=8)

            c_op = ctk.CTkLabel(
                row_frame,
                text=rec.get("operation", ""),
                font=ctk.CTkFont(size=11),
                anchor="w",
            )
            c_op.grid(row=0, column=2, sticky="w", padx=10, pady=8)

            size_str = self._format_size(rec.get("file_size", 0))
            c_size = ctk.CTkLabel(
                row_frame, text=size_str, font=ctk.CTkFont(size=11), anchor="w"
            )
            c_size.grid(row=0, column=3, sticky="w", padx=10, pady=8)

            status = rec.get("status", "SUCCESS")
            status_color = "#107C41" if status == "SUCCESS" else "#D13438"
            c_status = ctk.CTkLabel(
                row_frame,
                text=status,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=status_color,
                anchor="w",
            )
            c_status.grid(row=0, column=4, sticky="w", padx=10, pady=8)

            # Double click binding to open output file folder
            out_path = rec.get("output_path", "")
            if out_path:
                row_frame.bind(
                    "<Double-Button-1>", lambda e, p=out_path: self._open_folder(p)
                )
                for w in (c_time, c_fname, c_op, c_size, c_status):
                    w.bind(
                        "<Double-Button-1>", lambda e, p=out_path: self._open_folder(p)
                    )

    @staticmethod
    def _open_folder(file_path: str) -> None:
        """Opens parent folder of output file."""
        if not file_path:
            return
        path = Path(file_path)
        folder = path.parent if path.exists() else path
        try:
            if os.name == "nt":
                os.startfile(folder)  # type: ignore[attr-defined]
            else:
                subprocess.Popen(
                    ["open" if sys.platform == "darwin" else "xdg-open", str(folder)]
                )
        except Exception:
            pass

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Formats bytes."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
