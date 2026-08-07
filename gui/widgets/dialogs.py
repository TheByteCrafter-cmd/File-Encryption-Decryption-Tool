"""
Custom Modal Dialogs Subsystem.

Provides modern popups for alert notifications (Success, Warning, Error with Copy Error button, Info)
and interactive Password Generator dialogs.
"""

import random
import string
from typing import Callable, Optional

import customtkinter as ctk


class ModernDialog(ctk.CTkToplevel):
    """
    Modern custom modal alert dialog.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        title: str,
        message: str,
        dialog_type: str = "info",
        details: Optional[str] = None,
    ) -> None:
        super().__init__(master)
        self.title(title)
        self.geometry("450x260")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        icons = {
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "info": "ℹ️",
        }
        colors = {
            "success": "#107C41",
            "warning": "#FF8C00",
            "error": "#D13438",
            "info": "#0078D4",
        }

        icon_str = icons.get(dialog_type, "ℹ️")
        color = colors.get(dialog_type, "#0078D4")

        # Header Row
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        icon_lbl = ctk.CTkLabel(header_frame, text=icon_str, font=ctk.CTkFont(size=32))
        icon_lbl.grid(row=0, column=0, padx=(0, 10))

        title_lbl = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=color,
        )
        title_lbl.grid(row=0, column=1, sticky="w")

        # Message Text
        msg_lbl = ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=13),
            wraplength=400,
            justify="left",
        )
        msg_lbl.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        # Button Bar
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="e", padx=20, pady=20)

        if details:
            copy_btn = ctk.CTkButton(
                btn_frame,
                text="Copy Error Details",
                fg_color=("gray80", "gray30"),
                text_color=("gray10", "gray90"),
                command=lambda: self._copy_details(details),
            )
            copy_btn.grid(row=0, column=0, padx=(0, 10))

        ok_btn = ctk.CTkButton(
            btn_frame,
            text="OK",
            width=90,
            command=self.destroy,
        )
        ok_btn.grid(row=0, column=1)

    def _copy_details(self, details: str) -> None:
        self.clipboard_clear()
        self.clipboard_append(details)


class PasswordGenDialog(ctk.CTkToplevel):
    """
    Strong Password Generator Modal Dialog.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_password_selected: Optional[Callable[[str], None]] = None,
    ) -> None:
        super().__init__(master)
        self.title("Strong Password Generator")
        self.geometry("450x320")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.on_password_selected = on_password_selected
        self.grid_columnconfigure(0, weight=1)

        title_lbl = ctk.CTkLabel(
            self, text="🎲 Password Generator", font=ctk.CTkFont(size=16, weight="bold")
        )
        title_lbl.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Generated Output Entry
        self.output_entry = ctk.CTkEntry(
            self, font=ctk.CTkFont(size=14, weight="bold"), height=40
        )
        self.output_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Controls (Length slider)
        ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctrl_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        ctrl_frame.grid_columnconfigure(1, weight=1)

        len_title = ctk.CTkLabel(
            ctrl_frame, text="Length: 16", font=ctk.CTkFont(size=12)
        )
        self.len_title = len_title
        len_title.grid(row=0, column=0, padx=(0, 10))

        self.len_slider = ctk.CTkSlider(
            ctrl_frame, from_=8, to=64, number_of_steps=56, command=self._on_slider
        )
        self.len_slider.set(16)
        self.len_slider.grid(row=0, column=1, sticky="ew")

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=20, pady=20, sticky="e")

        regen_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Regenerate",
            command=self._generate,
            fg_color=("gray80", "gray30"),
            text_color=("gray10", "gray90"),
        )
        regen_btn.grid(row=0, column=0, padx=(0, 10))

        apply_btn = ctk.CTkButton(btn_frame, text="Use Password", command=self._apply)
        apply_btn.grid(row=0, column=1)

        self._generate()

    def _on_slider(self, val: float) -> None:
        length = int(val)
        self.len_title.configure(text=f"Length: {length}")
        self._generate()

    def _generate(self) -> None:
        length = int(self.len_slider.get())
        charset = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        pwd = "".join(random.choice(charset) for _ in range(length))
        self.output_entry.delete(0, "end")
        self.output_entry.insert(0, pwd)

    def _apply(self) -> None:
        pwd = self.output_entry.get()
        if self.on_password_selected:
            self.on_password_selected(pwd)
        self.destroy()
