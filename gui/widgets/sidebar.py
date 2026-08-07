"""
Windows 11 Commercial Sidebar Navigation Widget (240px Width).

Features brand logo header, application title, version badge, navigation items with animated active blue pill,
and bottom shortcut buttons (Settings, About, GitHub repository link).
"""

import webbrowser
from typing import Callable, Dict

import customtkinter as ctk

import config


class SidebarWidget(ctk.CTkFrame):
    """
    Commercial 240px Sidebar Navigation Component.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_nav_click: Callable[[str], None],
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            width=240,
            corner_radius=20,
            fg_color=("gray90", "#1E293B"),
            border_width=1,
            border_color=("gray80", "#334155"),
            **kwargs,
        )
        self.on_nav_click = on_nav_click
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}

        self.grid_rowconfigure(7, weight=1)  # Push bottom shortcuts to bottom

        # 1. Brand Logo Header Section
        self.brand_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.brand_frame.grid(row=0, column=0, padx=16, pady=(20, 15), sticky="ew")
        self.brand_frame.grid_columnconfigure(1, weight=1)

        self.brand_icon = ctk.CTkLabel(
            self.brand_frame, text="🛡️", font=ctk.CTkFont(size=28)
        )
        self.brand_icon.grid(row=0, column=0, padx=(0, 10))

        self.brand_title = ctk.CTkLabel(
            self.brand_frame,
            text="FEDT Security",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        )
        self.brand_title.grid(row=0, column=1, sticky="w")

        self.brand_sub = ctk.CTkLabel(
            self.brand_frame,
            text=f"v{config.APP_VERSION} Pro",
            font=ctk.CTkFont(size=11),
            text_color="#2563EB",
            anchor="w",
        )
        self.brand_sub.grid(row=1, column=1, sticky="w")

        # Divider
        self.divider = ctk.CTkFrame(self, height=1, fg_color=("gray80", "#334155"))
        self.divider.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 15))

        # 2. Main Navigation Menu Items
        pages = [
            ("home", "🏠  Dashboard", "Ctrl+O"),
            ("encrypt", "🔒  Encrypt File", "Ctrl+E"),
            ("decrypt", "🔓  Decrypt File", "Ctrl+D"),
            ("history", "📜  Audit History", "Ctrl+H"),
        ]

        for idx, (page_key, label, shortcut) in enumerate(pages, start=2):
            btn = ctk.CTkButton(
                self,
                text=label,
                anchor="w",
                font=ctk.CTkFont(size=13),
                height=42,
                corner_radius=12,
                fg_color="transparent",
                text_color=("gray10", "#F8FAFC"),
                hover_color=("gray80", "#334155"),
                command=lambda k=page_key: self.on_nav_click(k),
            )
            btn.grid(row=idx, column=0, padx=12, pady=4, sticky="ew")
            self.nav_buttons[page_key] = btn

        # 3. Bottom Shortcuts (Settings, About, GitHub, Version Badge)
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.grid(row=8, column=0, padx=12, pady=(0, 15), sticky="ew")

        btn_settings = ctk.CTkButton(
            self.bottom_frame,
            text="⚙️  Settings",
            anchor="w",
            font=ctk.CTkFont(size=13),
            height=38,
            corner_radius=10,
            fg_color="transparent",
            text_color=("gray10", "#F8FAFC"),
            hover_color=("gray80", "#334155"),
            command=lambda: self.on_nav_click("settings"),
        )
        btn_settings.grid(row=0, column=0, sticky="ew", pady=2)
        self.nav_buttons["settings"] = btn_settings

        btn_about = ctk.CTkButton(
            self.bottom_frame,
            text="ℹ️  About Engine",
            anchor="w",
            font=ctk.CTkFont(size=13),
            height=38,
            corner_radius=10,
            fg_color="transparent",
            text_color=("gray10", "#F8FAFC"),
            hover_color=("gray80", "#334155"),
            command=lambda: self.on_nav_click("about"),
        )
        btn_about.grid(row=1, column=0, sticky="ew", pady=2)
        self.nav_buttons["about"] = btn_about

        btn_github = ctk.CTkButton(
            self.bottom_frame,
            text="🌐  GitHub Repo",
            anchor="w",
            font=ctk.CTkFont(size=13),
            height=38,
            corner_radius=10,
            fg_color="transparent",
            text_color="#2563EB",
            hover_color=("gray80", "#334155"),
            command=self._open_github,
        )
        btn_github.grid(row=2, column=0, sticky="ew", pady=2)

    def set_active_page(self, page_key: str) -> None:
        """Highlights active sidebar navigation button with active blue pill styling (#2563EB)."""
        for key, btn in self.nav_buttons.items():
            if key == page_key:
                btn.configure(
                    fg_color="#2563EB",
                    text_color="#FFFFFF",
                    font=ctk.CTkFont(size=13, weight="bold"),
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=("gray10", "#F8FAFC"),
                    font=ctk.CTkFont(size=13, weight="normal"),
                )

    @staticmethod
    def _open_github() -> None:
        """Opens project GitHub repository in browser."""
        webbrowser.open(
            "https://github.com/TheByteCrafter-cmd/File-Encryption-Decryption-Tool"
        )
