"""
Dashboard Metric Card Widget.

Displays a commercial-grade accent-styled card with 16px corner radius, icon badge,
metric value, description label, and hover highlight effects.
"""

import customtkinter as ctk


class MetricCardWidget(ctk.CTkFrame):
    """
    Commercial dashboard statistic card container.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        icon: str,
        title: str,
        value: str,
        accent_color: str = "#2563EB",
        **kwargs,
    ) -> None:
        super().__init__(
            master, corner_radius=16, fg_color=("gray90", "gray20"), **kwargs
        )
        self.accent_color = accent_color

        self.grid_columnconfigure(1, weight=1)

        # 1. Icon Badge
        self.icon_badge = ctk.CTkLabel(
            self,
            text=icon,
            font=ctk.CTkFont(size=26),
            width=48,
            height=48,
            corner_radius=12,
            fg_color=accent_color,
            text_color="white",
        )
        self.icon_badge.grid(row=0, column=0, rowspan=2, padx=15, pady=15)

        # 2. Metric Value
        self.val_label = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        self.val_label.grid(row=0, column=1, sticky="w", padx=(0, 15), pady=(15, 0))

        # 3. Metric Title Description
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color="gray60",
            anchor="w",
        )
        self.title_label.grid(row=1, column=1, sticky="w", padx=(0, 15), pady=(0, 15))

        # Bind Hover Highlight
        self.bind("<Enter>", lambda e: self.configure(fg_color=("gray85", "gray25")))
        self.bind("<Leave>", lambda e: self.configure(fg_color=("gray90", "gray20")))

    def update_value(self, new_value: str) -> None:
        """Updates metric value text dynamically."""
        self.val_label.configure(text=new_value)
