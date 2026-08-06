"""
Operation History Persistence Model.

Loads, saves, and manages operation records in output/history.json.
Provides metrics calculation (total encrypted, decrypted, bytes processed)
and search/filter capabilities.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

import config


class HistoryModel:
    """
    Manages persistent operation history JSON storage.
    """

    HISTORY_FILE: Path = config.OUTPUT_DIR / "history.json"

    def __init__(self) -> None:
        self.records: List[Dict[str, Any]] = []
        self.load()

    def load(self) -> None:
        """Loads operation history records from JSON file."""
        if self.HISTORY_FILE.exists():
            try:
                data = json.loads(self.HISTORY_FILE.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self.records = data
            except Exception:
                self.records = []

    def save(self) -> None:
        """Saves operation records to JSON file."""
        try:
            config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            self.HISTORY_FILE.write_text(
                json.dumps(self.records, indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    def add_record(
        self,
        filename: str,
        operation: str,
        file_size: int,
        status: str,
        output_path: str,
        timestamp: str,
    ) -> Dict[str, Any]:
        """Appends a new operation record and saves."""
        record = {
            "id": len(self.records) + 1,
            "timestamp": timestamp,
            "filename": filename,
            "operation": operation,  # "Encrypt" or "Decrypt"
            "file_size": file_size,
            "status": status,  # "SUCCESS" or "FAILED"
            "output_path": output_path,
        }
        self.records.insert(0, record)  # Newest first
        self.save()
        return record

    def clear_history(self) -> None:
        """Clears all history records."""
        self.records.clear()
        self.save()

    def get_stats(self) -> Dict[str, Any]:
        """Calculates dashboard summary metrics."""
        encrypted_count = sum(
            1
            for r in self.records
            if r.get("operation") == "Encrypt" and r.get("status") == "SUCCESS"
        )
        decrypted_count = sum(
            1
            for r in self.records
            if r.get("operation") == "Decrypt" and r.get("status") == "SUCCESS"
        )
        total_bytes = sum(
            r.get("file_size", 0) for r in self.records if r.get("status") == "SUCCESS"
        )

        return {
            "encrypted_count": encrypted_count,
            "decrypted_count": decrypted_count,
            "total_bytes": total_bytes,
        }
