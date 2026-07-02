from __future__ import annotations

from klarient import ResponseMap
from listmonk.imports.models import ImportStatus


class ImportStatusResponse(ResponseMap):
    """Response wrapper for subscriber import status."""

    @property
    def data(self) -> ImportStatus:
        """Import status returned by the endpoint."""
        data = self.get("data", {})
        return ImportStatus(data if isinstance(data, dict) else {})


class ImportLogsResponse(ResponseMap):
    """Response wrapper for subscriber import logs."""

    @property
    def data(self) -> str:
        """Import log text."""
        return str(self.get("data", ""))


class ImportUploadResponse(ResponseMap):
    """Response wrapper for subscriber import upload settings."""

    @property
    def mode(self) -> str:
        """Import mode echoed by listmonk."""
        return str(self.get("mode", ""))

    @property
    def delim(self) -> str:
        """Delimiter echoed by listmonk."""
        return str(self.get("delim", ""))

    @property
    def lists(self) -> list[int]:
        """Target list identifiers echoed by listmonk."""
        lists = self.get("lists", [])
        if not isinstance(lists, list):
            return []
        return [int(item) for item in lists if isinstance(item, int)]

    @property
    def overwrite(self) -> bool:
        """Whether overwrite was enabled."""
        return bool(self.get("overwrite", False))
