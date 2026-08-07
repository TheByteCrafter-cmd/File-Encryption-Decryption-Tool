"""
About Page View Frame.

Displays application branding, version badges, developer credits, cryptographic specifications grid,
system environment information, and GitHub repository links.
"""

import platform
import sys
import webbrowser

import customtkinter as ctk

import config


class AboutView(ctk.CTkFrame):
    """
    About & Specifications page view frame.
    """

    def __init__(self, master: ctk.CTkBaseClass, **kwargs) -> None:
        super().__init__(master, corner_radius=16, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(0, weight=1)

        # Header Title
        self.title_label = ctk.CTkLabel(
            self,
            text="ℹ️ About Application",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Main Info Card Container
        self.card_frame = ctk.CTkFrame(
            self, corner_radius=16, fg_color=("gray90", "gray20")
        )
        self.card_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.card_frame.grid_columnconfigure(1, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.card_frame, text="🛡️", font=ctk.CTkFont(size=44)
        )
        self.logo_label.grid(row=0, column=0, rowspan=3, padx=25, pady=25)

        self.app_name_lbl = ctk.CTkLabel(
            self.card_frame,
            text=f"{config.APP_NAME}",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        self.app_name_lbl.grid(row=0, column=1, sticky="w", padx=(0, 25), pady=(25, 0))

        self.version_lbl = ctk.CTkLabel(
            self.card_frame,
            text=f"Version {config.APP_VERSION} | License: MIT",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#2563EB",
            anchor="w",
        )
        self.version_lbl.grid(row=1, column=1, sticky="w", padx=(0, 25), pady=2)

        self.dev_lbl = ctk.CTkLabel(
            self.card_frame,
            text="Developed by: TheByteCrafter-cmd",
            font=ctk.CTkFont(size=12),
            text_color="gray60",
            anchor="w",
        )
        self.dev_lbl.grid(row=2, column=1, sticky="w", padx=(0, 25), pady=(0, 25))

        # Specifications Frame
        self.specs_frame = ctk.CTkFrame(
            self, corner_radius=16, fg_color=("gray90", "gray20")
        )
        self.specs_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        self.specs_frame.grid_columnconfigure(1, weight=1)

        specs = [
            ("Encryption Standard", "AES-256-GCM (Authenticated Encryption)"),
            ("Key Derivation Function", "PBKDF2-HMAC-SHA256 (600,000 Iterations)"),
            ("Streaming Architecture", "Low-level Cipher API (64 KB Chunks)"),
            ("Binary Header Protocol", "Contiguous Format (Magic: FEDT)"),
            ("GUI Presentation Layer", "CustomTkinter / TkinterDnD2 / Pillow"),
            ("Host Python Environment", f"Python {sys.version.split()[0]}"),
            (
                "Operating System",
                f"{platform.system()} {platform.release()} ({platform.machine()})",
            ),
        ]

        for i, (k, v) in enumerate(specs):
            lbl_k = ctk.CTkLabel(
                self.specs_frame,
                text=k,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
            )
            lbl_k.grid(row=i, column=0, padx=20, pady=8, sticky="w")

            lbl_v = ctk.CTkLabel(
                self.specs_frame,
                text=v,
                font=ctk.CTkFont(size=13),
                text_color="gray60",
                anchor="w",
            )
            lbl_v.grid(row=i, column=1, padx=20, pady=8, sticky="w")

        # GitHub Repository Action Button
        self.github_btn = ctk.CTkButton(
            self,
            text="🌐 Open GitHub Repository",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=42,
            corner_radius=10,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self._open_github,
        )
        self.github_btn.grid(row=3, column=0, sticky="ew")

    @staticmethod
    def _open_github() -> None:
        """Opens project GitHub repository in default browser."""
        webbrowser.open(
            "https://github.com/TheByteCrafter-cmd/File-Encryption-Decryption-Tool"
        )
