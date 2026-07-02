from __future__ import annotations

from collections.abc import Mapping

from klarient import ResponseMap
from listmonk.media.models import Media


class MediaCollectionResponse(ResponseMap):
    """Response wrapper for media collections."""

    @property
    def data(self) -> list[Media]:
        """Media items returned by the endpoint."""
        return [Media(item) for item in self.get("data", []) if isinstance(item, Mapping)]


class MediaResponse(ResponseMap):
    """Response wrapper for one media item."""

    @property
    def data(self) -> Media:
        """Media item returned by the endpoint."""
        data = self.get("data", {})
        return Media(data if isinstance(data, Mapping) else {})
