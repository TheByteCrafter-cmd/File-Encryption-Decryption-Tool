"""
Password Entry and Real-Time Strength Meter Widget.

Combines a CTk password input field, Eye toggle (Show/Hide), real-time entropy gauge bar,
estimated crack time indicator, and Strong Password Generator trigger button.
"""

from typing import Callable, Optional

import customtkinter as ctk

from gui.utils.password_entropy import PasswordEntropy


class PasswordMeterWidget(ctk.CTkFrame):
    """
    Password entry widget with strength meter and eye toggle.
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

        # 1. Entry Row (Input Field + Eye Toggle + Generate Button)
        self.entry_row = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_row.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        self.entry_row.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(
            self.entry_row,
            placeholder_text=placeholder_text,
            show="•",
            height=38,
            font=ctk.CTkFont(size=13),
        )
        self.password_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.password_entry.bind("<KeyRelease>", self._on_password_change)

        self.eye_btn = ctk.CTkButton(
            self.entry_row,
            text="👁️",
            width=40,
            height=38,
            fg_color=("gray85", "gray25"),
            hover_color=("gray75", "gray35"),
            text_color=("gray10", "gray90"),
            command=self._toggle_eye,
        )
        self.eye_btn.grid(row=0, column=1, padx=(0, 8))

        if self.on_generate_click:
            self.gen_btn = ctk.CTkButton(
                self.entry_row,
                text="🎲 Generate",
                width=100,
                height=38,
                command=self.on_generate_click,
            )
            self.gen_btn.grid(row=0, column=2)

        # 2. Strength Gauge Progress Bar
        self.strength_bar = ctk.CTkProgressBar(self, height=8, corner_radius=4)
        self.strength_bar.grid(row=1, column=0, sticky="ew", pady=3)
        self.strength_bar.set(0.0)

        # 3. Strength Label & Crack Time Row
        self.info_row = ctk.CTkFrame(self, fg_color="transparent")
        self.info_row.grid(row=2, column=0, sticky="ew")
        self.info_row.grid_columnconfigure(1, weight=1)

        self.rating_label = ctk.CTkLabel(
            self.info_row,
            text="Strength: Empty",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray60",
        )
        self.rating_label.grid(row=0, column=0, sticky="w")

        self.crack_time_label = ctk.CTkLabel(
            self.info_row,
            text="Est. Crack Time: Instant",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
        )
        self.crack_time_label.grid(row=0, column=1, sticky="e")

    def get_password(self) -> str:
        """Returns current entered password string."""
        return self.password_entry.get()

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

        self.strength_bar.set(ratio)
        self.strength_bar.configure(progress_color=color)

        self.rating_label.configure(text=f"Strength: {rating}", text_color=color)
        self.crack_time_label.configure(text=f"Est. Crack Time: {crack_time}")
