"""
Batch Queue Manager Widget.

Displays scrollable queue of active and completed jobs, status indicators,
and control buttons (Pause, Resume, Cancel, Clear Queue).
"""

from typing import Callable, List, Optional

import customtkinter as ctk

from gui.models.job_model import Job


class QueuePanelWidget(ctk.CTkFrame):
    """
    Queue panel widget displaying batch job execution states.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_pause_click: Optional[Callable[[], None]] = None,
        on_resume_click: Optional[Callable[[], None]] = None,
        on_cancel_click: Optional[Callable[[], None]] = None,
        on_clear_click: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            master, corner_radius=10, fg_color=("gray90", "gray20"), **kwargs
        )
        self.on_pause_click = on_pause_click
        self.on_resume_click = on_resume_click
        self.on_cancel_click = on_cancel_click
        self.on_clear_click = on_clear_click

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Control Button Bar (Pause, Resume, Cancel, Clear)
        self.ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.ctrl_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.ctrl_frame.grid_columnconfigure(0, weight=1)

        self.title_lbl = ctk.CTkLabel(
            self.ctrl_frame,
            text="📋 Batch Execution Queue",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        self.title_lbl.grid(row=0, column=0, sticky="w")

        self.btn_pause = ctk.CTkButton(
            self.ctrl_frame,
            text="⏸️ Pause",
            width=70,
            height=28,
            fg_color="#FF8C00",
            hover_color="#CC7000",
            command=self.on_pause_click,
        )
        self.btn_pause.grid(row=0, column=1, padx=(0, 5))

        self.btn_resume = ctk.CTkButton(
            self.ctrl_frame,
            text="▶️ Resume",
            width=75,
            height=28,
            fg_color="#107C41",
            hover_color="#0E6B37",
            command=self.on_resume_click,
        )
        self.btn_resume.grid(row=0, column=2, padx=(0, 5))

        self.btn_cancel = ctk.CTkButton(
            self.ctrl_frame,
            text="⏹️ Cancel",
            width=70,
            height=28,
            fg_color="#D13438",
            hover_color="#A8282C",
            command=self.on_cancel_click,
        )
        self.btn_cancel.grid(row=0, column=3, padx=(0, 5))

        self.btn_clear = ctk.CTkButton(
            self.ctrl_frame,
            text="🗑️ Clear",
            width=65,
            height=28,
            fg_color=("gray80", "gray30"),
            text_color=("gray10", "gray90"),
            command=self.on_clear_click,
        )
        self.btn_clear.grid(row=0, column=4)

        # 2. Scrollable Jobs List Container
        self.jobs_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent", height=140
        )
        self.jobs_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.jobs_frame.grid_columnconfigure(0, weight=1)

    def update_jobs(self, jobs: List[Job]) -> None:
        """Renders list of jobs into scrollable container."""
        for child in self.jobs_frame.winfo_children():
            child.destroy()

        if not jobs:
            lbl = ctk.CTkLabel(
                self.jobs_frame,
                text="Queue is empty.",
                font=ctk.CTkFont(size=12),
                text_color="gray60",
            )
            lbl.grid(row=0, column=0, pady=20)
            return

        status_colors = {
            "PENDING": ("gray60", "gray50"),
            "PROCESSING": ("#0078D4", "#0078D4"),
            "PAUSED": ("#FF8C00", "#FF8C00"),
            "SUCCESS": ("#107C41", "#107C41"),
            "CANCELLED": ("#FF8C00", "#FF8C00"),
            "FAILED": ("#D13438", "#D13438"),
        }

        for idx, job in enumerate(jobs):
            card = ctk.CTkFrame(
                self.jobs_frame, fg_color=("gray95", "gray25"), corner_radius=6
            )
            card.grid(row=idx, column=0, sticky="ew", pady=3)
            card.grid_columnconfigure(1, weight=1)

            name_lbl = ctk.CTkLabel(
                card,
                text=job.input_path.name,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
            )
            name_lbl.grid(row=0, column=0, padx=10, pady=6, sticky="w")

            color = status_colors.get(job.status, ("gray60", "gray50"))
            status_lbl = ctk.CTkLabel(
                card,
                text=job.status,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=color[0],
                anchor="e",
            )
            status_lbl.grid(row=0, column=1, padx=10, pady=6, sticky="e")
