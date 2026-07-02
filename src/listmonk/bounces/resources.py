from __future__ import annotations

from typing import Any

from klarient import (
    Page,
    PageNumberState,
    PageableResource,
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


class BouncesResource(PageableResource[_SyncClientImpl, Bounce, PageNumberState]):
    """Paged bounces collection resource."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=Bounce,
            pagination=ListmonkPagePagination(),
            **kwargs,
        )

    def __getitem__(self, bounce_id: int | str) -> BounceResource:
        return BounceResource(self, segment=ResourcePath.segment(bounce_id))

    def retrieve(
            self,
            options: BounceQuery | None = None,
    ) -> Page[Bounce]:
        """Retrieve bounces with optional query parameters."""
        return self._retrieve_page(options=options)

    def delete(self, options: BounceDeleteQuery) -> BooleanResponse:
        """Delete bounces in bulk."""
        return self._executor.delete(BooleanResponse, options)
