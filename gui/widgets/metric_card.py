"""
Dashboard Metric Card Widget.

Displays an accent-styled card containing an icon, metric value, and description label.
"""

import customtkinter as ctk


class MetricCardWidget(ctk.CTkFrame):
    """
    Modern dashboard statistic card container.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        icon: str,
        title: str,
        value: str,
        accent_color: str = "#0078D4",
        **kwargs,
    ) -> None:
        super().__init__(
            master, corner_radius=12, fg_color=("gray90", "gray20"), **kwargs
        )

        self.grid_columnconfigure(1, weight=1)

        # 1. Accent Left Strip / Icon
        self.icon_badge = ctk.CTkLabel(
            self,
            text=icon,
            font=ctk.CTkFont(size=28),
            width=50,
            height=50,
            corner_radius=8,
            fg_color=accent_color,
            text_color="white",
        )
        self.icon_badge.grid(row=0, column=0, rowspan=2, padx=15, pady=15)

        # 2. Metric Value
        self.val_label = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold"),
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

    def update_value(self, new_value: str) -> None:
        """Updates metric value text dynamically."""
        self.val_label.configure(text=new_value)
