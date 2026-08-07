"""
Password Entry and Real-Time Strength Meter Widget.

Combines a CTk password input field, Eye toggle (Show/Hide), real-time entropy gauge bar,
estimated crack time indicator, Password Requirements Checklist card, and Strong Password Generator trigger button.
"""

from typing import Callable, Optional

import customtkinter as ctk

from gui.utils.password_entropy import PasswordEntropy


class PasswordMeterWidget(ctk.CTkFrame):
    """
    Password entry widget with strength meter, requirement checklist, and eye toggle.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        placeholder_text: str = "Enter secret password...",
        on_generate_click: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_generate_click = on_generate_click
        self.show_password: bool = False

        self.grid_columnconfigure(0, weight=1)

        # Container Card Frame
        self.card = ctk.CTkFrame(self, corner_radius=16, fg_color=("gray90", "gray20"))
        self.card.grid(row=0, column=0, sticky="ew")
        self.card.grid_columnconfigure(0, weight=1)

        # Header Title Label
        self.card_header = ctk.CTkLabel(
            self.card,
            text="🔑 Password Protection",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        )
        self.card_header.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="w")

        # 1. Entry Row (Input Field + Eye Toggle + Generate Button)
        self.entry_row = ctk.CTkFrame(self.card, fg_color="transparent")
        self.entry_row.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.entry_row.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(
            self.entry_row,
            placeholder_text=placeholder_text,
            show="•",
            height=42,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
        )
        self.password_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.password_entry.bind("<KeyRelease>", self._on_password_change)

        self.eye_btn = ctk.CTkButton(
            self.entry_row,
            text="👁️",
            width=42,
            height=42,
            corner_radius=10,
            fg_color=("gray80", "gray30"),
            hover_color=("gray70", "gray40"),
            text_color=("gray10", "gray90"),
            command=self._toggle_eye,
        )
        self.eye_btn.grid(row=0, column=1, padx=(0, 8))

        if self.on_generate_click:
            self.gen_btn = ctk.CTkButton(
                self.entry_row,
                text="🎲 Generate",
                font=ctk.CTkFont(size=13, weight="bold"),
                width=110,
                height=42,
                corner_radius=10,
                fg_color="#2563EB",
                hover_color="#1D4ED8",
                command=self.on_generate_click,
            )
            self.gen_btn.grid(row=0, column=2)

        # 2. Strength Gauge Progress Bar
        self.strength_bar = ctk.CTkProgressBar(self.card, height=8, corner_radius=4)
        self.strength_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 6))
        self.strength_bar.set(0.0)

        # 3. Strength Rating & Crack Time Row
        self.info_row = ctk.CTkFrame(self.card, fg_color="transparent")
        self.info_row.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.info_row.grid_columnconfigure(1, weight=1)

        self.rating_label = ctk.CTkLabel(
            self.info_row,
            text="Strength: Empty (0.0 bits)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray60",
        )
        self.rating_label.grid(row=0, column=0, sticky="w")

        self.crack_time_label = ctk.CTkLabel(
            self.info_row,
            text="Est. Crack Time: Instant",
            font=ctk.CTkFont(size=12),
            text_color="gray60",
        )
        self.crack_time_label.grid(row=0, column=1, sticky="e")

        # 4. Security Requirements Checklist
        self.checklist_frame = ctk.CTkFrame(
            self.card, fg_color=("gray95", "gray25"), corner_radius=10
        )
        self.checklist_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 15))
        self.checklist_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.chk_length = ctk.CTkLabel(
            self.checklist_frame,
            text="✖ 12+ Chars",
            font=ctk.CTkFont(size=11),
            text_color="#DC2626",
        )
        self.chk_length.grid(row=0, column=0, pady=8)

        self.chk_upper = ctk.CTkLabel(
            self.checklist_frame,
            text="✖ Uppercase",
            font=ctk.CTkFont(size=11),
            text_color="#DC2626",
        )
        self.chk_upper.grid(row=0, column=1, pady=8)

        self.chk_symbol = ctk.CTkLabel(
            self.checklist_frame,
            text="✖ Symbol / Number",
            font=ctk.CTkFont(size=11),
            text_color="#DC2626",
        )
        self.chk_symbol.grid(row=0, column=2, pady=8)

    def get_password(self) -> str:
        """Returns current entered password string."""
        return str(self.password_entry.get())

    def set_password(self, password: str) -> None:
        """Sets password programmatically and updates strength gauge."""
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)
        self._update_meter(password)

    def _toggle_eye(self) -> None:
        """Toggles password visibility between bullet and plaintext."""
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.configure(show="")
            self.eye_btn.configure(text="🔒")
        else:
            self.password_entry.configure(show="•")
            self.eye_btn.configure(text="👁️")

    def _on_password_change(self, event=None) -> None:
        """Key release handler updating strength meter."""
        password = self.password_entry.get()
        self._update_meter(password)

    def _update_meter(self, password: str) -> None:
        """Recalculates entropy score and updates UI strength bar & labels."""
        ratio, rating, color, crack_time = PasswordEntropy.get_strength_rating(password)
        bits = PasswordEntropy.calculate_entropy(password)

        self.strength_bar.set(ratio)
        self.strength_bar.configure(progress_color=color)

        self.rating_label.configure(
            text=f"Strength: {rating} ({bits:.1f} bits)", text_color=color
        )
        self.crack_time_label.configure(text=f"Est. Crack Time: {crack_time}")

        # Update Checklist Labels
        if len(password) >= 12:
            self.chk_length.configure(text="✔ 12+ Chars", text_color="#16A34A")
        else:
            self.chk_length.configure(text="✖ 12+ Chars", text_color="#DC2626")

        if any(c.isupper() for c in password):
            self.chk_upper.configure(text="✔ Uppercase", text_color="#16A34A")
        else:
            self.chk_upper.configure(text="✖ Uppercase", text_color="#DC2626")

        if any(c.isdigit() or not c.isalnum() for c in password):
            self.chk_symbol.configure(text="✔ Symbol / Number", text_color="#16A34A")
        else:
            self.chk_symbol.configure(text="✖ Symbol / Number", text_color="#DC2626")
