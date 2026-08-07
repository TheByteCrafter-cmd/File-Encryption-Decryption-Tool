"""
Home Dashboard View Frame.

Displays hero header, quick action navigation cards, dashboard metric cards,
security status badges, and recent activity history.
"""

from typing import Callable, Optional

import customtkinter as ctk

import config
from gui.widgets.metric_card import MetricCardWidget


class HomeView(ctk.CTkFrame):
    """
    Home Dashboard page view.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_encrypt_click: Optional[Callable[[], None]] = None,
        on_decrypt_click: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, corner_radius=16, fg_color="transparent", **kwargs)
        self.on_encrypt_click = on_encrypt_click
        self.on_decrypt_click = on_decrypt_click

        self.grid_columnconfigure(0, weight=1)

        # 1. Hero Branding Banner Card
        self.hero_card = ctk.CTkFrame(
            self, corner_radius=16, fg_color=("gray90", "gray20")
        )
        self.hero_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.hero_card.grid_columnconfigure(1, weight=1)

        self.hero_icon = ctk.CTkLabel(
            self.hero_card, text="🛡️", font=ctk.CTkFont(size=44)
        )
        self.hero_icon.grid(row=0, column=0, rowspan=2, padx=25, pady=25)

        self.hero_title = ctk.CTkLabel(
            self.hero_card,
            text=f"{config.APP_NAME}",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        self.hero_title.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=(25, 0))

        self.hero_subtitle = ctk.CTkLabel(
            self.hero_card,
            text=(
                "Enterprise AES-256-GCM authenticated file protection engine featuring "
                "PBKDF2 key derivation (600,000 iterations) and non-blocking streaming."
            ),
            font=ctk.CTkFont(size=13),
            text_color="gray60",
            wraplength=620,
            justify="left",
            anchor="w",
        )
        self.hero_subtitle.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=(5, 25))

        # 2. Quick Action Cards Row
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.actions_frame.grid_columnconfigure((0, 1), weight=1)

        # Encrypt Card
        self.enc_card = ctk.CTkFrame(
            self.actions_frame, corner_radius=16, fg_color=("gray90", "gray20")
        )
        self.enc_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.enc_card.grid_columnconfigure(0, weight=1)

        self.enc_title = ctk.CTkLabel(
            self.enc_card,
            text="🔒  Encrypt File",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.enc_title.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.enc_desc = ctk.CTkLabel(
            self.enc_card,
            text="Securely encrypt any text or binary file with authenticated AES-256-GCM.",
            font=ctk.CTkFont(size=12),
            text_color="gray60",
            wraplength=300,
            justify="left",
        )
        self.enc_desc.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        self.enc_btn = ctk.CTkButton(
            self.enc_card,
            text="Go to Encrypt",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.on_encrypt_click,
            height=38,
            corner_radius=10,
        )
        self.enc_btn.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Decrypt Card
        self.dec_card = ctk.CTkFrame(
            self.actions_frame, corner_radius=16, fg_color=("gray90", "gray20")
        )
        self.dec_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.dec_card.grid_columnconfigure(0, weight=1)

        self.dec_title = ctk.CTkLabel(
            self.dec_card,
            text="🔓  Decrypt File",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.dec_title.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.dec_desc = ctk.CTkLabel(
            self.dec_card,
            text="Decrypt .enc files and automatically restore original metadata.",
            font=ctk.CTkFont(size=12),
            text_color="gray60",
            wraplength=300,
            justify="left",
        )
        self.dec_desc.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        self.dec_btn = ctk.CTkButton(
            self.dec_card,
            text="Go to Decrypt",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.on_decrypt_click,
            height=38,
            corner_radius=10,
        )
        self.dec_btn.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        # 3. Statistics Metrics Grid
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        self.stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.card_enc = MetricCardWidget(
            self.stats_frame,
            icon="🔒",
            title="Files Encrypted",
            value="0",
            accent_color="#2563EB",
        )
        self.card_enc.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.card_dec = MetricCardWidget(
            self.stats_frame,
            icon="🔓",
            title="Files Decrypted",
            value="0",
            accent_color="#16A34A",
        )
        self.card_dec.grid(row=0, column=1, sticky="ew", padx=5)

        self.card_data = MetricCardWidget(
            self.stats_frame,
            icon="📊",
            title="Data Processed",
            value="0.0 MB",
            accent_color="#8B5CF6",
        )
        self.card_data.grid(row=0, column=2, sticky="ew", padx=(10, 0))

        # 4. Recent Activity List Card
        self.recent_card = ctk.CTkFrame(
            self, corner_radius=16, fg_color=("gray90", "gray20")
        )
        self.recent_card.grid(row=3, column=0, sticky="ew")
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
                fg_color=("gray95", "gray25"),
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
            status_color = "#16A34A" if status == "SUCCESS" else "#DC2626"
            lbl_status = ctk.CTkLabel(
                row,
                text=status,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=status_color,
                anchor="e",
            )
            lbl_status.grid(row=0, column=2, padx=12, pady=8, sticky="e")
