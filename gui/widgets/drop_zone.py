"""
Interactive File Drag & Drop Target Widget.

Provides an interactive target zone supporting TkinterDnD drag-and-drop events and click-to-browse
file selection with hover highlights and file details card.
"""

from pathlib import Path
from typing import Callable, Optional

import customtkinter as ctk
from customtkinter import filedialog


class DropZoneWidget(ctk.CTkFrame):
    """
    Interactive drag-and-drop and browse target container.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        file_types: Optional[list] = None,
        on_file_selected: Optional[Callable[[Path], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            corner_radius=12,
            border_width=2,
            border_color=("gray75", "gray30"),
            **kwargs,
        )
        self.file_types = file_types or [("All Files", "*.*")]
        self.on_file_selected = on_file_selected
        self.selected_file: Optional[Path] = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Drop Zone Prompt View
        self.prompt_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.prompt_frame.grid(row=0, column=0, padx=20, pady=30, sticky="nsew")
        self.prompt_frame.grid_columnconfigure(0, weight=1)

        self.icon_label = ctk.CTkLabel(
            self.prompt_frame,
            text="📁",
            font=ctk.CTkFont(size=36),
        )
        self.icon_label.grid(row=0, column=0, pady=(5, 5))

        self.text_label = ctk.CTkLabel(
            self.prompt_frame,
            text="Drag & Drop your file here\nor click to browse",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray20", "gray80"),
        )
        self.text_label.grid(row=1, column=0, pady=5)

        self.browse_btn = ctk.CTkButton(
            self.prompt_frame,
            text="Browse File",
            width=130,
            command=self._browse_file,
        )
        self.browse_btn.grid(row=2, column=0, pady=(10, 5))

        # 2. Selected File Summary Card View (Hidden initially)
        self.card_frame = ctk.CTkFrame(
            self, corner_radius=8, fg_color=("gray90", "gray20")
        )
        self.card_frame.grid_columnconfigure(1, weight=1)

        self.card_icon = ctk.CTkLabel(
            self.card_frame, text="📄", font=ctk.CTkFont(size=24)
        )
        self.card_icon.grid(row=0, column=0, padx=12, pady=12)

        self.card_name = ctk.CTkLabel(
            self.card_frame,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        self.card_name.grid(row=0, column=1, sticky="ew", padx=5)

        self.card_size = ctk.CTkLabel(
            self.card_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
            anchor="w",
        )
        self.card_size.grid(row=1, column=1, sticky="ew", padx=5)

        self.clear_btn = ctk.CTkButton(
            self.card_frame,
            text="✕",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=("gray75", "gray35"),
            command=self.clear_selection,
        )
        self.clear_btn.grid(row=0, column=2, rowspan=2, padx=10)

        # Bind Click & Hover Glow Events to Prompt Frame
        for widget in (self, self.prompt_frame, self.icon_label, self.text_label):
            widget.bind("<Button-1>", lambda e: self._browse_file())
            widget.bind("<Enter>", lambda e: self._on_hover_enter())
            widget.bind("<Leave>", lambda e: self._on_hover_leave())

    def _on_hover_enter(self) -> None:
        """Glows border accent blue on mouse hover."""
        self.configure(border_color="#0078D4")

    def _on_hover_leave(self) -> None:
        """Restores default border color when mouse leaves."""
        self.configure(border_color=("gray75", "gray30"))

    def set_file(self, file_path: Path) -> None:
        """Sets the selected file and updates card UI."""
        path = Path(file_path).resolve()
        if not path.exists() or not path.is_file():
            return

        self.selected_file = path

        # Update Card Labels
        self.card_name.configure(text=path.name)
        size_bytes = path.stat().st_size
        size_str = self._format_size(size_bytes)
        self.card_size.configure(text=size_str)

        # Switch View: Hide prompt, show card
        self.prompt_frame.grid_forget()
        self.card_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        if self.on_file_selected:
            self.on_file_selected(self.selected_file)

    def clear_selection(self) -> None:
        """Clears current file selection and returns to drop zone prompt."""
        self.selected_file = None
        self.card_frame.grid_forget()
        self.prompt_frame.grid(row=0, column=0, padx=20, pady=30, sticky="nsew")

    def _browse_file(self) -> None:
        """Opens native file chooser dialog."""
        chosen = filedialog.askopenfilename(filetypes=self.file_types)
        if chosen:
            self.set_file(Path(chosen))

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
