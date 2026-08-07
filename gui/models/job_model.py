"""
Job Model and Batch Queue Abstraction.

Defines job state data structure and queue manager for multi-file batch execution,
supporting thread pause, resume, cancel signals, and status tracking.
"""

import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class Job:
    """
    Data model representing a file encryption or decryption job task.
    """

    id: str
    input_path: Path
    mode: str  # "Encrypt" or "Decrypt"
    password: str
    output_path: Optional[Path] = None
    status: str = (
        "PENDING"  # "PENDING", "PROCESSING", "PAUSED", "SUCCESS", "CANCELLED", "FAILED"
    )
    total_bytes: int = 0
    processed_bytes: int = 0
    error_message: Optional[str] = None
    cancel_event: threading.Event = field(default_factory=threading.Event)
    pause_event: threading.Event = field(default_factory=threading.Event)

    def is_cancelled(self) -> bool:
        """Checks if cancel signal was set."""
        return self.cancel_event.is_set()

    def is_paused(self) -> bool:
        """Checks if pause signal was set."""
        return self.pause_event.is_set()


class JobQueue:
    """
    Queue manager maintaining batch jobs and controlling pause/resume/cancel states.
    """

    def __init__(self) -> None:
        self.jobs: List[Job] = []

    def add_job(self, job: Job) -> None:
        """Appends a new job to the batch queue."""
        self.jobs.append(job)

    def get_pending_jobs(self) -> List[Job]:
        """Returns list of pending jobs."""
        return [j for j in self.jobs if j.status == "PENDING"]

    def pause_all(self) -> None:
        """Sets pause event signal on active/pending jobs."""
        for j in self.jobs:
            if j.status in ("PENDING", "PROCESSING"):
                j.pause_event.set()
                j.status = "PAUSED"

    def resume_all(self) -> None:
        """Clears pause event signal on paused jobs."""
        for j in self.jobs:
            if j.status == "PAUSED":
                j.pause_event.clear()
                j.status = "PROCESSING"

    def cancel_all(self) -> None:
        """Sets cancel event signal on all incomplete jobs."""
        for j in self.jobs:
            if j.status in ("PENDING", "PROCESSING", "PAUSED"):
                j.cancel_event.set()
                j.status = "CANCELLED"

    def clear(self) -> None:
        """Clears all jobs from queue."""
        self.jobs.clear()
