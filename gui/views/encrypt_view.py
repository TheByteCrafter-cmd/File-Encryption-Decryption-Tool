"""
Encrypt Page View Frame.

Assembles drop zone target, password entry with strength gauge, real-time progress panel,
action buttons, and post-encryption shortcut button bar.
"""

from pathlib import Path
from typing import Callable, Optional

import customtkinter as ctk

from gui.widgets.drop_zone import DropZoneWidget
from gui.widgets.password_meter import PasswordMeterWidget
from gui.widgets.progress_panel import ProgressPanelWidget


class EncryptView(ctk.CTkFrame):
    """
    File Encryption page view frame.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_encrypt_click: Optional[Callable[[], None]] = None,
        on_generate_password_click: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, corner_radius=12, fg_color="transparent", **kwargs)
        self.on_encrypt_click = on_encrypt_click
        self.on_generate_password_click = on_generate_password_click

        self.grid_columnconfigure(0, weight=1)

        # 1. Page Title Header
        self.header_label = ctk.CTkLabel(
            self,
            text="🔒 Encrypt File",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        self.header_label.grid(row=0, column=0, sticky="w", pady=(0, 15))

        # 2. File Drop Zone Target
        self.drop_zone = DropZoneWidget(
            self,
            file_types=[
                ("All Supported Files", "*.*"),
                ("Documents", "*.pdf;*.docx;*.txt;*.xlsx;*.pptx"),
                ("Images", "*.png;*.jpg;*.jpeg;*.gif"),
                ("Archives", "*.zip;*.rar;*.7z;*.tar;*.gz"),
            ],
        )
        self.drop_zone.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # 3. Password Entry & Strength Meter
        self.password_meter = PasswordMeterWidget(
            self,
            placeholder_text="Enter secret password for AES-256 encryption...",
            on_generate_click=self.on_generate_password_click,
        )
        self.password_meter.grid(row=2, column=0, sticky="ew", pady=(0, 15))

        # 4. Action Button
        self.encrypt_btn = ctk.CTkButton(
            self,
            text="🔒 Encrypt File Now",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=42,
            fg_color="#0078D4",
            hover_color="#106EBE",
            command=self.on_encrypt_click,
        )
        self.encrypt_btn.grid(row=3, column=0, sticky="ew", pady=(0, 15))

        # 5. Real-Time Progress Panel
        self.progress_panel = ProgressPanelWidget(self)
        self.progress_panel.grid(row=4, column=0, sticky="ew", pady=(0, 15))

        # 6. Post-Encryption Shortcut Action Bar (Hidden initially)
        self.shortcuts_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.shortcuts_frame.grid_columnconfigure((0, 1), weight=1)

        self.btn_open_folder = ctk.CTkButton(
            self.shortcuts_frame,
            text="📂 Open Output Folder",
            fg_color=("gray80", "gray30"),
            text_color=("gray10", "gray90"),
        )
        self.btn_open_folder.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.btn_copy_path = ctk.CTkButton(
            self.shortcuts_frame,
            text="📋 Copy Output Path",
            fg_color=("gray80", "gray30"),
            text_color=("gray10", "gray90"),
        )
        self.btn_copy_path.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    def show_shortcuts(
        self, on_open_folder: Callable[[], None], on_copy_path: Callable[[], None]
    ) -> None:
        """Displays post-encryption shortcut button bar."""
        self.btn_open_folder.configure(command=on_open_folder)
        self.btn_copy_path.configure(command=on_copy_path)
        self.shortcuts_frame.grid(row=5, column=0, sticky="ew", pady=(0, 10))

    def hide_shortcuts(self) -> None:
        """Hides post-encryption shortcut button bar."""
        self.shortcuts_frame.grid_forget()

    def set_processing_state(self, is_processing: bool) -> None:
        """Enables/disables buttons during worker thread execution."""
        if is_processing:
            self.encrypt_btn.configure(state="disabled", text="⏳ Encrypting File...")
            self.drop_zone.browse_btn.configure(state="disabled")
        else:
            self.encrypt_btn.configure(state="normal", text="🔒 Encrypt File Now")
            self.drop_zone.browse_btn.configure(state="normal")
