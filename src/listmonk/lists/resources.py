from __future__ import annotations

from klarient import (
    PagedResponse,
    PagedResponseModel,
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


class ListsResource(SyncResource[_SyncClientImpl]):
    """Paged list collection resource."""

    def __getitem__(self, list_id: int | str) -> ListResource:
        return ListResource(self, segment=ResourcePath.segment(list_id))

    def retrieve(self, options: ListQuery | None = None) -> PagedResponse[List]:
        """Retrieve lists with optional query parameters."""
        return self._executor.get(
            PagedResponseModel(List, ListmonkPagePagination()),
            options,
        )

    def create(self, options: ListCreate) -> ListResponse:
        """Create a list."""
        return self._executor.post(ListResponse, options)

    def delete(self, options: ListDeleteQuery) -> BooleanResponse:
        """Delete lists in bulk."""
        return self._executor.delete(BooleanResponse, options)
