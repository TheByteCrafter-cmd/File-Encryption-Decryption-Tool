"""
Operation History Page View Frame.

Displays searchable data table of past encryption and decryption audit records,
search filter entry, clear history button, and Export CSV/JSON action buttons.
"""

from typing import Callable, Optional

import customtkinter as ctk

from gui.widgets.data_table import DataTableWidget


class HistoryView(ctk.CTkFrame):
    """
    Operation Audit History page view frame.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_clear_click: Optional[Callable[[], None]] = None,
        on_export_csv_click: Optional[Callable[[], None]] = None,
        on_export_json_click: Optional[Callable[[], None]] = None,
        on_search_change: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, corner_radius=12, fg_color="transparent", **kwargs)
        self.on_clear_click = on_clear_click
        self.on_export_csv_click = on_export_csv_click
        self.on_export_json_click = on_export_json_click
        self.on_search_change = on_search_change

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. Page Header Bar
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="📜 Operation History",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        # Action Buttons (Export CSV, Export JSON, Clear)
        self.btn_export_csv = ctk.CTkButton(
            self.header_frame,
            text="📄 Export CSV",
            width=110,
            fg_color=("gray80", "gray30"),
            text_color=("gray10", "gray90"),
            command=self.on_export_csv_click,
        )
        self.btn_export_csv.grid(row=0, column=1, padx=(0, 8))

        self.btn_export_json = ctk.CTkButton(
            self.header_frame,
            text="📋 Export JSON",
            width=110,
            fg_color=("gray80", "gray30"),
            text_color=("gray10", "gray90"),
            command=self.on_export_json_click,
        )
        self.btn_export_json.grid(row=0, column=2, padx=(0, 8))

        self.btn_clear = ctk.CTkButton(
            self.header_frame,
            text="🗑️ Clear",
            width=85,
            height=36,
            corner_radius=10,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.on_clear_click,
        )
        self.btn_clear.grid(row=0, column=3)

        # 2. Search Box Row
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="🔍 Search history by filename or operation...",
            height=38,
            font=ctk.CTkFont(size=13),
        )
        self.search_entry.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.search_entry.bind("<KeyRelease>", self._on_search)

        # 3. Data Table Widget Container
        self.data_table = DataTableWidget(self)
        self.data_table.grid(row=2, column=0, sticky="nsew")

    def _on_search(self, event=None) -> None:
        """Triggers search query change callback."""
        if self.on_search_change:
            query = self.search_entry.get()
            self.on_search_change(query)
