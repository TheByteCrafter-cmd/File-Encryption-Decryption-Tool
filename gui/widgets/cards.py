"""
Reusable Commercial Card Components (Windows 11 Fluent Design).

Provides Base Card, Gradient Hero Card, Action Card, and Security Tip Card.
"""

from typing import Callable, Optional

import customtkinter as ctk


class CardWidget(ctk.CTkFrame):
    """
    Base card container with 16px corner radius, soft border, and hover elevation.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        corner_radius: int = 16,
        fg_color: Optional[tuple] = None,
        hover: bool = True,
        **kwargs,
    ) -> None:
        colors = fg_color or ("gray90", "#1E293B")
        super().__init__(
            master,
            corner_radius=corner_radius,
            fg_color=colors,
            border_width=1,
            border_color=("gray80", "#334155"),
            **kwargs,
        )

        if hover:
            self.bind(
                "<Enter>", lambda e: self.configure(fg_color=("gray85", "#334155"))
            )
            self.bind("<Leave>", lambda e: self.configure(fg_color=colors))


class GradientHeroCard(CardWidget):
    """
    Gradient Hero Header Card section for Dashboard and Home views.
    """

    def __init__(self, master: ctk.CTkBaseClass, **kwargs) -> None:
        super().__init__(
            master,
            corner_radius=20,
            fg_color=("#1E40AF", "#1E293B"),
            hover=False,
            **kwargs,
        )
        self.grid_columnconfigure(1, weight=1)

        self.hero_icon = ctk.CTkLabel(self, text="🛡️", font=ctk.CTkFont(size=48))
        self.hero_icon.grid(row=0, column=0, rowspan=2, padx=25, pady=25)

        self.hero_title = ctk.CTkLabel(
            self,
            text="Secure File Protection Engine",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFFFFF",
            anchor="w",
        )
        self.hero_title.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=(25, 0))

        self.hero_subtitle = ctk.CTkLabel(
            self,
            text=(
                "Authenticated AES-256-GCM encryption with PBKDF2 key derivation (600,000 iterations). "
                "Zero-trust in-memory key wiping and non-blocking streaming execution."
            ),
            font=ctk.CTkFont(size=13),
            text_color="#E2E8F0",
            wraplength=640,
            justify="left",
            anchor="w",
        )
        self.hero_subtitle.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=(5, 25))


class ActionCard(CardWidget):
    """
    Interactive Quick Action Card.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        icon: str,
        title: str,
        description: str,
        button_text: str,
        button_color: str,
        button_hover: str,
        command: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, corner_radius=16, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.title_lbl = ctk.CTkLabel(
            self,
            text=f"{icon}  {title}",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        )
        self.title_lbl.grid(row=0, column=0, padx=20, pady=(20, 6), sticky="w")

        self.desc_lbl = ctk.CTkLabel(
            self,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color="gray60",
            wraplength=280,
            justify="left",
            anchor="w",
        )
        self.desc_lbl.grid(row=1, column=0, padx=20, pady=(0, 16), sticky="w")

        self.action_btn = ctk.CTkButton(
            self,
            text=button_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            corner_radius=10,
            fg_color=button_color,
            hover_color=button_hover,
            command=command,
        )
        self.action_btn.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
