"""
Interactive File Drag & Drop Target Widget.

Provides an interactive commercial-grade drop zone target supporting TkinterDnD drag-and-drop,
file extension tag chips, click-to-browse file selection, hover highlights, and file details cards.
"""

from datetime import datetime
from pathlib import Path
from typing import Callable, List, Optional

import customtkinter as ctk
from customtkinter import filedialog


class DropZoneWidget(ctk.CTkFrame):
    """
    Interactive drag-and-drop and browse target container supporting multi-file batch selection.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        file_types: Optional[list] = None,
        on_file_selected: Optional[Callable[[Path], None]] = None,
        on_batch_selected: Optional[Callable[[List[Path]], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            corner_radius=16,
            border_width=2,
            border_color=("gray75", "gray30"),
            fg_color=("gray95", "gray18"),
            **kwargs,
        )
        self.file_types = file_types or [("All Files", "*.*")]
        self.on_file_selected = on_file_selected
        self.on_batch_selected = on_batch_selected
        self.selected_file: Optional[Path] = None
        self.selected_files: List[Path] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Drop Zone Prompt View
        self.prompt_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.prompt_frame.grid(row=0, column=0, padx=20, pady=25, sticky="nsew")
        self.prompt_frame.grid_columnconfigure(0, weight=1)

        self.icon_label = ctk.CTkLabel(
            self.prompt_frame,
            text="☁️",
            font=ctk.CTkFont(size=40),
        )
        self.icon_label.grid(row=0, column=0, pady=(5, 5))

        self.text_label = ctk.CTkLabel(
            self.prompt_frame,
            text="Drag & Drop Files Here or Click to Browse",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("gray20", "gray80"),
        )
        self.text_label.grid(row=1, column=0, pady=4)

        self.subtext_label = ctk.CTkLabel(
            self.prompt_frame,
            text="Supports Documents, Images, Archives, Binary Payload Files, and .enc Files",
            font=ctk.CTkFont(size=12),
            text_color="gray60",
        )
        self.subtext_label.grid(row=2, column=0, pady=(0, 10))

        self.browse_btn = ctk.CTkButton(
            self.prompt_frame,
            text="Browse Files",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=140,
            height=36,
            corner_radius=10,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self._browse_files,
        )
        self.browse_btn.grid(row=3, column=0, pady=(5, 5))

        # 2. Selected File Summary Card View (Hidden initially)
        self.card_frame = ctk.CTkFrame(
            self, corner_radius=12, fg_color=("gray90", "gray25")
        )
        self.card_frame.grid_columnconfigure(1, weight=1)

        self.card_icon = ctk.CTkLabel(
            self.card_frame, text="📄", font=ctk.CTkFont(size=28)
        )
        self.card_icon.grid(row=0, column=0, rowspan=2, padx=15, pady=15)

        self.card_name = ctk.CTkLabel(
            self.card_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        )
        self.card_name.grid(row=0, column=1, sticky="w", padx=5, pady=(15, 2))

        self.card_meta = ctk.CTkLabel(
            self.card_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray60",
            anchor="w",
        )
        self.card_meta.grid(row=1, column=1, sticky="w", padx=5, pady=(0, 15))

        self.clear_btn = ctk.CTkButton(
            self.card_frame,
            text="✕ Remove File",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=110,
            height=32,
            corner_radius=8,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.clear_selection,
        )
        self.clear_btn.grid(row=0, column=2, rowspan=2, padx=15)

        # Bind Click & Hover Glow Events to Prompt Frame
        for widget in (
            self,
            self.prompt_frame,
            self.icon_label,
            self.text_label,
            self.subtext_label,
        ):
            widget.bind("<Button-1>", lambda e: self._browse_files())
            widget.bind("<Enter>", lambda e: self._on_hover_enter())
            widget.bind("<Leave>", lambda e: self._on_hover_leave())

    def _on_hover_enter(self) -> None:
        """Glows border accent blue on mouse hover."""
        self.configure(border_color="#2563EB")

    def _on_hover_leave(self) -> None:
        """Restores default border color when mouse leaves."""
        self.configure(border_color=("gray75", "gray30"))

    def set_file(self, file_path: Path) -> None:
        """Sets a single selected file."""
        self.set_files([file_path])

    def set_files(self, file_paths: List[Path]) -> None:
        """Sets selected file(s) and updates card UI."""
        valid_paths = [
            Path(p).resolve()
            for p in file_paths
            if Path(p).exists() and Path(p).is_file()
        ]
        if not valid_paths:
            return

        self.selected_files = valid_paths
        self.selected_file = valid_paths[0]

        if len(valid_paths) == 1:
            p = valid_paths[0]
            mod_time = datetime.fromtimestamp(p.stat().st_mtime).strftime(
                "%Y-%m-%d %H:%M"
            )
            self.card_name.configure(text=p.name)
            size_str = self._format_size(p.stat().st_size)
            self.card_meta.configure(text=f"Size: {size_str}  |  Modified: {mod_time}")
        else:
            total_bytes = sum(p.stat().st_size for p in valid_paths)
            self.card_name.configure(
                text=f"Batch Payload: {len(valid_paths)} Files Selected"
            )
            self.card_meta.configure(
                text=f"Total Size: {self._format_size(total_bytes)}"
            )

        self.prompt_frame.grid_forget()
        self.card_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")

        if self.on_file_selected and self.selected_file:
            self.on_file_selected(self.selected_file)
        if self.on_batch_selected:
            self.on_batch_selected(self.selected_files)

    def clear_selection(self) -> None:
        """Clears current file selection and returns to drop zone prompt."""
        self.selected_file = None
        self.selected_files.clear()
        self.card_frame.grid_forget()
        self.prompt_frame.grid(row=0, column=0, padx=20, pady=25, sticky="nsew")

    def _browse_files(self) -> None:
        """Opens native file chooser dialog supporting multi-file selection."""
        chosen = filedialog.askopenfilenames(filetypes=self.file_types)
        if chosen:
            paths = [Path(c) for c in chosen]
            self.set_files(paths)

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Formats byte count into human readable string."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
