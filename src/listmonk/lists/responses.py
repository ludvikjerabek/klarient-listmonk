from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from klarient import HTTPResponse, ResponseMap, ResponseList
from listmonk.lists.models import List, PublicList


class ListResponse(ResponseMap):
    """Response wrapper for one list."""

    @property
    def data(self) -> List:
        """List returned by the endpoint."""
        data = self.get("data", {})
        return List(data if isinstance(data, Mapping) else {})


class PublicListsResponse(ResponseList[PublicList]):
    """Response wrapper for public lists."""

    def __init__(
            self,
            data: list[Any] | None = None,
            *,
            response: HTTPResponse[Any] | None = None,
    ) -> None:
        items = [
            PublicList(item)
            for item in data or []
            if isinstance(item, Mapping)
        ]
        super().__init__(items, response=response)
