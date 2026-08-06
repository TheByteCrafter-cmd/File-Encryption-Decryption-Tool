"""
Job Model and Batch Queue Abstraction.

Defines job state data structure and queue manager ready for single-file and multi-file batch execution.
"""

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
    status: str = "PENDING"  # "PENDING", "PROCESSING", "SUCCESS", "FAILED"
    total_bytes: int = 0
    processed_bytes: int = 0
    error_message: Optional[str] = None


class JobQueue:
    """
    Queue manager maintaining active and completed jobs.
    """

    def __init__(self) -> None:
        self.queue: List[Job] = []

    def add_job(self, job: Job) -> None:
        """Appends job to queue."""
        self.queue.append(job)

    def get_pending_jobs(self) -> List[Job]:
        """Returns pending jobs."""
        return [j for j in self.queue if j.status == "PENDING"]

    def clear(self) -> None:
        """Clears queue."""
        self.queue.clear()
