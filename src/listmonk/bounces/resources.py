from __future__ import annotations

from klarient import (
    PagedResponse,
    PagedResponseModel,
    ResourcePath,
    SyncResource,
)
from klarient.http.client import _SyncClientImpl
from listmonk.bounces.models import Bounce
from listmonk.bounces.requests import BounceDeleteQuery, BounceQuery
from listmonk.common import BooleanResponse
from listmonk.common import ListmonkPagePagination


class BounceResource(SyncResource[_SyncClientImpl]):
    """Resource for one bounce."""

    def delete(self) -> BooleanResponse:
        """Delete this bounce."""
        return self._executor.delete(BooleanResponse)


class BouncesResource(SyncResource[_SyncClientImpl]):
    """Paged bounces collection resource."""

    def __getitem__(self, bounce_id: int | str) -> BounceResource:
        return BounceResource(self, segment=ResourcePath.segment(bounce_id))

    def retrieve(
            self,
            options: BounceQuery | None = None,
    ) -> PagedResponse[Bounce]:
        """Retrieve bounces with optional query parameters."""
        return self._executor.get(
            PagedResponseModel(Bounce, ListmonkPagePagination()),
            options,
        )

    def delete(self, options: BounceDeleteQuery) -> BooleanResponse:
        """Delete bounces in bulk."""
        return self._executor.delete(BooleanResponse, options)
