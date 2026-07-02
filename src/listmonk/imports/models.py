from __future__ import annotations

from typing import Any


class ImportStatus(dict[str, Any]):
    """Subscriber import status data."""

    @property
    def name(self) -> str:
        """Import job name."""
        return str(self.get("name", ""))

    @property
    def total(self) -> int:
        """Total records in the import."""
        return int(self.get("total", 0))

    @property
    def imported(self) -> int:
        """Number of imported records."""
        return int(self.get("imported", 0))

    @property
    def status(self) -> str:
        """Import status value."""
        return str(self.get("status", ""))
