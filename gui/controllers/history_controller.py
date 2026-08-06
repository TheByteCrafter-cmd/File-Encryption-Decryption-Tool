"""
History View Business Logic Controller.

Manages history data rendering, real-time search filtering, record clearing,
and exporting history logs to CSV and JSON formats.
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List

from customtkinter import filedialog

from gui.models.history_model import HistoryModel
from gui.views.history_view import HistoryView
from gui.widgets.dialogs import ModernDialog


class HistoryController:
    """
    Controller managing operation history search, filtering, and export.
    """

    def __init__(self, view: HistoryView, history_model: HistoryModel) -> None:
        self.view = view
        self.history_model = history_model

        # Wire Up View Callbacks
        self.view.on_clear_click = self.clear_history
        self.view.on_export_csv_click = self.export_csv
        self.view.on_export_json_click = self.export_json
        self.view.on_search_change = self.filter_history

        # Initial Load
        self.refresh()

    def refresh(self) -> None:
        """Reloads records from HistoryModel into view data table."""
        records = self.history_model.records
        self.view.data_table.set_records(records)

    def filter_history(self, query: str) -> None:
        """Filters displayed records by search query."""
        if not query.strip():
            self.refresh()
            return

        q = query.lower().strip()
        filtered = [
            r
            for r in self.history_model.records
            if q in r.get("filename", "").lower()
            or q in r.get("operation", "").lower()
            or q in r.get("status", "").lower()
            or q in r.get("timestamp", "").lower()
        ]
        self.view.data_table.set_records(filtered)

    def clear_history(self) -> None:
        """Clears all history records after user confirmation."""
        if not self.history_model.records:
            return

        self.history_model.clear_history()
        self.refresh()
        ModernDialog(
            master=self.view.winfo_toplevel(),
            title="History Cleared",
            message="All operation history records have been cleared.",
            dialog_type="info",
        )

    def export_csv(self) -> None:
        """Exports history records to a CSV file."""
        records = self.history_model.records
        if not records:
            ModernDialog(
                master=self.view.winfo_toplevel(),
                title="No History",
                message="There are no operation records to export.",
                dialog_type="warning",
            )
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            initialfile="fedt_operation_history.csv",
        )
        if not save_path:
            return

        try:
            fieldnames = [
                "id",
                "timestamp",
                "filename",
                "operation",
                "file_size",
                "status",
                "output_path",
            ]
            with open(save_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in records:
                    writer.writerow(r)

            ModernDialog(
                master=self.view.winfo_toplevel(),
                title="Export Successful",
                message=f"History exported successfully to CSV!\nLocation:\n{save_path}",
                dialog_type="success",
            )
        except Exception as err:
            ModernDialog(
                master=self.view.winfo_toplevel(),
                title="Export Failed",
                message=f"Failed to export CSV: {err}",
                dialog_type="error",
            )

    def export_json(self) -> None:
        """Exports history records to a JSON file."""
        records = self.history_model.records
        if not records:
            ModernDialog(
                master=self.view.winfo_toplevel(),
                title="No History",
                message="There are no operation records to export.",
                dialog_type="warning",
            )
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            initialfile="fedt_operation_history.json",
        )
        if not save_path:
            return

        try:
            Path(save_path).write_text(json.dumps(records, indent=2), encoding="utf-8")
            ModernDialog(
                master=self.view.winfo_toplevel(),
                title="Export Successful",
                message=f"History exported successfully to JSON!\nLocation:\n{save_path}",
                dialog_type="success",
            )
        except Exception as err:
            ModernDialog(
                master=self.view.winfo_toplevel(),
                title="Export Failed",
                message=f"Failed to export JSON: {err}",
                dialog_type="error",
            )
