from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class Media(dict[str, Any]):
    """Media record returned by listmonk."""

    @property
    def id(self) -> int:
        """Media numeric identifier."""
        return int(self["id"])

    @property
    def uuid(self) -> str:
        """Media UUID."""
        return str(self.get("uuid", ""))

    @property
    def filename(self) -> str:
        """Stored media filename."""
        return str(self.get("filename", ""))

    @property
    def content_type(self) -> str:
        """Media content type."""
        return str(self.get("content_type", ""))

    @property
    def created_at(self) -> str:
        """Creation timestamp."""
        return str(self.get("created_at", ""))

    @property
    def thumb_url(self) -> str:
        """Thumbnail URL or URI."""
        value = self.get("thumb_url", self.get("thumb_uri", ""))
        return "" if value is None else str(value)

    @property
    def thumb_uri(self) -> str:
        """Alias for thumb_url."""
        return self.thumb_url

    @property
    def uri(self) -> str:
        """Media URI."""
        return str(self.get("uri", ""))

    @property
    def url(self) -> str:
        """Media URL when provided, otherwise the URI."""
        return str(self.get("url", self.uri))

    @property
    def provider(self) -> str:
        """Storage provider name."""
        return str(self.get("provider", ""))

    @property
    def meta(self) -> dict[str, Any]:
        """Open metadata returned for the media item."""
        meta = self.get("meta")
        return dict(meta) if isinstance(meta, Mapping) else {}
