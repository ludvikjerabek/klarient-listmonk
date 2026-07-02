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
from listmonk.common import BooleanResponse
from listmonk.common import ListmonkPagePagination
from listmonk.lists.models import List
from listmonk.lists.requests import (
    ListCreate,
    ListDeleteQuery,
    ListQuery,
    ListUpdate,
)
from listmonk.lists.responses import ListResponse


class ListResource(SyncResource[_SyncClientImpl]):
    """Resource for one list."""

    def retrieve(self) -> ListResponse:
        """Retrieve this list."""
        return self._executor.get(ListResponse)

    def update(self, options: ListUpdate) -> ListResponse:
        """Update this list."""
        return self._executor.put(ListResponse, options)

    def delete(self) -> BooleanResponse:
        """Delete this list."""
        return self._executor.delete(BooleanResponse)


class ListsResource(PageableResource[_SyncClientImpl, List, PageNumberState]):
    """Paged list collection resource."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=List,
            pagination=ListmonkPagePagination(),
            **kwargs,
        )

    def __getitem__(self, list_id: int | str) -> ListResource:
        return ListResource(self, segment=ResourcePath.segment(list_id))

    def retrieve(self, options: ListQuery | None = None) -> Page[List]:
        """Retrieve lists with optional query parameters."""
        return self._retrieve_page(options=options)

    def create(self, options: ListCreate) -> ListResponse:
        """Create a list."""
        return self._executor.post(ListResponse, options)

    def delete(self, options: ListDeleteQuery) -> BooleanResponse:
        """Delete lists in bulk."""
        return self._executor.delete(BooleanResponse, options)
