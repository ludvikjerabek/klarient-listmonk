from __future__ import annotations

from klarient.http.client import _SyncClientImpl

from klarient import ResourcePath, SyncResource
from listmonk.common import BooleanResponse
from listmonk.media.requests import MediaUpload
from listmonk.media.responses import MediaCollectionResponse, MediaResponse


class MediaResource(SyncResource[_SyncClientImpl]):
    """Resource for one media item."""

    def retrieve(self) -> MediaResponse:
        """Retrieve this media item."""
        return self._executor.get(MediaResponse)

    def delete(self) -> BooleanResponse:
        """Delete this media item."""
        return self._executor.delete(BooleanResponse)


class MediaRootResource(SyncResource[_SyncClientImpl]):
    """Media API root."""

    def __getitem__(self, media_id: int | str) -> MediaResource:
        return MediaResource(self, segment=ResourcePath.segment(media_id))

    def retrieve(self) -> MediaCollectionResponse:
        """Retrieve uploaded media items."""
        return self._executor.get(MediaCollectionResponse)

    def upload(self, options: MediaUpload) -> MediaResponse:
        """Upload a media file."""
        return self._executor.post(MediaResponse, options)
