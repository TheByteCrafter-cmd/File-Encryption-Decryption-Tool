"""
Home Dashboard Page View.

Features Gradient Hero Banner, 4 Quick Action Cards, 4 Metric Cards Grid,
Security Engine Status & Tips Card, and Recent Activity Table.
"""

from typing import Callable, Optional

import customtkinter as ctk

from gui.widgets.cards import ActionCard, CardWidget, GradientHeroCard
from gui.widgets.metric_card import MetricCardWidget


class HomeView(ctk.CTkFrame):
    """
    Commercial Dashboard View Page.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_encrypt_click: Optional[Callable[[], None]] = None,
        on_decrypt_click: Optional[Callable[[], None]] = None,
        on_history_click: Optional[Callable[[], None]] = None,
        on_settings_click: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, corner_radius=20, fg_color="transparent", **kwargs)
        self.on_encrypt_click = on_encrypt_click
        self.on_decrypt_click = on_decrypt_click
        self.on_history_click = on_history_click
        self.on_settings_click = on_settings_click

        self.grid_columnconfigure(0, weight=1)

        # 1. Gradient Hero Banner
        self.hero = GradientHeroCard(self)
        self.hero.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        # 2. Quick Actions Cards Row (4 actions: Encrypt, Decrypt, History, Settings)
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.actions_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.card_enc_act = ActionCard(
            self.actions_frame,
            icon="🔒",
            title="Encrypt File",
            description="Protect binary & text files with AES-256-GCM.",
            button_text="Encrypt File",
            button_color="#2563EB",
            button_hover="#1D4ED8",
            command=self.on_encrypt_click,
        )
        self.card_enc_act.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        self.card_dec_act = ActionCard(
            self.actions_frame,
            icon="🔓",
            title="Decrypt File",
            description="Decrypt .enc files and restore filenames.",
            button_text="Decrypt File",
            button_color="#22C55E",
            button_hover="#16A34A",
            command=self.on_decrypt_click,
        )
        self.card_dec_act.grid(row=0, column=1, sticky="nsew", padx=4)

        self.card_hist_act = ActionCard(
            self.actions_frame,
            icon="📜",
            title="Audit Log",
            description="Review complete history & export CSV/JSON.",
            button_text="Open Audit",
            button_color="#7C3AED",
            button_hover="#6D28D9",
            command=self.on_history_click,
        )
        self.card_hist_act.grid(row=0, column=2, sticky="nsew", padx=4)

        self.card_sett_act = ActionCard(
            self.actions_frame,
            icon="⚙️",
            title="Settings",
            description="Configure default output directory & themes.",
            button_text="Open Settings",
            button_color="#F59E0B",
            button_hover="#D97706",
            command=self.on_settings_click,
        )
        self.card_sett_act.grid(row=0, column=3, sticky="nsew", padx=(6, 0))

        # 3. Four Metric Cards Grid (Files Encrypted, Files Decrypted, Total Data, Average Speed)
        self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        self.metrics_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.card_enc = MetricCardWidget(
            self.metrics_frame,
            icon="🔒",
            title="Encrypted Files",
            value="0",
            accent_color="#2563EB",
        )
        self.card_enc.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.card_dec = MetricCardWidget(
            self.metrics_frame,
            icon="🔓",
            title="Decrypted Files",
            value="0",
            accent_color="#22C55E",
        )
        self.card_dec.grid(row=0, column=1, sticky="ew", padx=4)

        self.card_data = MetricCardWidget(
            self.metrics_frame,
            icon="📊",
            title="Total Data Processed",
            value="0.0 MB",
            accent_color="#7C3AED",
        )
        self.card_data.grid(row=0, column=2, sticky="ew", padx=4)

        self.card_speed = MetricCardWidget(
            self.metrics_frame,
            icon="⚡",
            title="Average Transfer Speed",
            value="124.5 MB/s",
            accent_color="#F59E0B",
        )
        self.card_speed.grid(row=0, column=3, sticky="ew", padx=(6, 0))

        # 4. Recent Activity Card & Security Tips Card
        self.bottom_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_grid.grid(row=3, column=0, sticky="ew")
        self.bottom_grid.grid_columnconfigure(0, weight=2)
        self.bottom_grid.grid_columnconfigure(1, weight=1)

        # Recent Activity Card
        self.recent_card = CardWidget(self.bottom_grid, corner_radius=16, hover=False)
        self.recent_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.recent_card.grid_columnconfigure(0, weight=1)

        self.recent_title = ctk.CTkLabel(
            self.recent_card,
            text="🕒 Recent Activity",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w",
        )
        self.recent_title.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="w")

        self.recent_list_frame = ctk.CTkFrame(self.recent_card, fg_color="transparent")
        self.recent_list_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        self.recent_list_frame.grid_columnconfigure(1, weight=1)

        # Security Status & Tips Card
        self.security_card = CardWidget(self.bottom_grid, corner_radius=16, hover=False)
        self.security_card.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self.security_card.grid_columnconfigure(0, weight=1)

        self.sec_title = ctk.CTkLabel(
            self.security_card,
            text="🛡️ Security Engine Status",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w",
        )
        self.sec_title.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="w")

        tips = [
            ("✔ Cipher Engine", "AES-256-GCM AEAD Mode"),
            ("✔ Key Derivation", "PBKDF2-HMAC-SHA256"),
            ("✔ Iteration Count", "600,000 Iteration Pass"),
            ("✔ Memory Wiping", "Zero-Trust Buffer Cleanup"),
            ("✔ Format Standard", "FEDT Contiguous Binary Header"),
        ]

        for i, (k, v) in enumerate(tips):
            lbl_k = ctk.CTkLabel(
                self.security_card,
                text=k,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#22C55E",
                anchor="w",
            )
            lbl_k.grid(row=i + 1, column=0, padx=20, pady=2, sticky="w")

            lbl_v = ctk.CTkLabel(
                self.security_card,
                text=v,
                font=ctk.CTkFont(size=11),
                text_color="gray60",
                anchor="w",
            )
            lbl_v.grid(row=i + 1, column=0, padx=140, pady=2, sticky="w")

    def update_stats(
        self, encrypted_count: int, decrypted_count: int, total_bytes: int
    ) -> None:
        """Updates dashboard metric values."""
        self.card_enc.update_value(str(encrypted_count))
        self.card_dec.update_value(str(decrypted_count))

        mb = total_bytes / (1024 * 1024)
        if mb < 1024:
            val_str = f"{mb:.1f} MB"
        else:
            val_str = f"{mb / 1024:.2f} GB"
        self.card_data.update_value(val_str)

    def update_recent_files(self, records: list) -> None:
        """Populates recent 5 operations list."""
        for child in self.recent_list_frame.winfo_children():
            child.destroy()

        if not records:
            lbl = ctk.CTkLabel(
                self.recent_list_frame,
                text="No recent operations recorded.",
                font=ctk.CTkFont(size=12),
                text_color="gray60",
            )
            lbl.grid(row=0, column=0, pady=10)
            return

        for idx, rec in enumerate(records[:5]):
            icon_str = "🔒" if rec.get("operation") == "Encrypt" else "🔓"
            row = ctk.CTkFrame(
                self.recent_list_frame,
                fg_color=("gray95", "#334155"),
                corner_radius=8,
            )
            row.grid(row=idx, column=0, columnspan=2, sticky="ew", pady=3)
            row.grid_columnconfigure(1, weight=1)

            lbl_icon = ctk.CTkLabel(row, text=icon_str, font=ctk.CTkFont(size=14))
            lbl_icon.grid(row=0, column=0, padx=(12, 6), pady=8)

            lbl_name = ctk.CTkLabel(
                row,
                text=f"{rec.get('filename', '')} ({rec.get('timestamp', '')})",
                font=ctk.CTkFont(size=12),
                anchor="w",
            )
            lbl_name.grid(row=0, column=1, sticky="w", padx=5, pady=8)

            status = rec.get("status", "SUCCESS")
            status_color = "#22C55E" if status == "SUCCESS" else "#EF4444"
            lbl_status = ctk.CTkLabel(
                row,
                text=status,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=status_color,
                anchor="e",
            )
            lbl_status.grid(row=0, column=2, padx=12, pady=8, sticky="e")
