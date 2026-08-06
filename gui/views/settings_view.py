"""
Settings Page View Frame.

Provides UI controls for theme mode selection, default output directory picker,
chunk size customization, auto-open output toggles, and settings persistence.
"""

from typing import Callable, Optional

import customtkinter as ctk
from customtkinter import filedialog

import config


class SettingsView(ctk.CTkFrame):
    """
    Application Settings page view frame.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_save_click: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, corner_radius=12, fg_color="transparent", **kwargs)
        self.on_save_click = on_save_click

        self.grid_columnconfigure(0, weight=1)

        # Header Title
        self.title_label = ctk.CTkLabel(
            self,
            text="⚙️ Application Settings",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Card Container
        self.card_frame = ctk.CTkFrame(
            self, corner_radius=12, fg_color=("gray90", "gray20")
        )
        self.card_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.card_frame.grid_columnconfigure(1, weight=1)

        # 1. Theme Setting
        self.lbl_theme = ctk.CTkLabel(
            self.card_frame,
            text="Appearance Theme",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.lbl_theme.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.theme_combo = ctk.CTkOptionMenu(
            self.card_frame, values=["System", "Dark", "Light"], width=180
        )
        self.theme_combo.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="e")

        # 2. Output Directory Setting
        self.lbl_outdir = ctk.CTkLabel(
            self.card_frame,
            text="Default Output Directory",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.lbl_outdir.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.outdir_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.outdir_frame.grid(row=1, column=1, padx=20, pady=10, sticky="e")

        self.outdir_entry = ctk.CTkEntry(self.outdir_frame, width=220)
        self.outdir_entry.grid(row=0, column=0, padx=(0, 8))

        self.btn_browse = ctk.CTkButton(
            self.outdir_frame, text="Browse", width=80, command=self._browse_dir
        )
        self.btn_browse.grid(row=0, column=1)

        # 3. Chunk Size Setting
        self.lbl_chunk = ctk.CTkLabel(
            self.card_frame,
            text="Streaming Chunk Size",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.lbl_chunk.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.chunk_combo = ctk.CTkOptionMenu(
            self.card_frame,
            values=["64 KB (Default)", "128 KB", "256 KB", "1 MB"],
            width=180,
        )
        self.chunk_combo.grid(row=2, column=1, padx=20, pady=10, sticky="e")

        # 4. Auto Open Output Directory Toggle
        self.lbl_auto_open = ctk.CTkLabel(
            self.card_frame,
            text="Auto Open Output Folder",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.lbl_auto_open.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="w")

        self.auto_open_switch = ctk.CTkSwitch(self.card_frame, text="")
        self.auto_open_switch.grid(row=3, column=1, padx=20, pady=(10, 20), sticky="e")

        # Save Settings Button
        self.save_btn = ctk.CTkButton(
            self,
            text="💾 Save Settings",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.on_save_click,
        )
        self.save_btn.grid(row=2, column=0, sticky="ew")

    def _browse_dir(self) -> None:
        chosen = filedialog.askdirectory()
        if chosen:
            self.outdir_entry.delete(0, "end")
            self.outdir_entry.insert(0, chosen)
