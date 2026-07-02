from __future__ import annotations

from enum import StrEnum
from typing import Self

from klarient import (
    PageNumberState,
    QueryFieldSpec,
    QueryRequest,
    QuerySerialization,
    RequestField,
    list_of,
)
from listmonk.common import PerPage
from listmonk.common.paging import _listmonk_page_state


class BounceOrderBy(StrEnum):
    """Fields accepted by bounce ordering."""

    EMAIL = "email"
    CAMPAIGN_NAME = "campaign_name"
    SOURCE = "source"
    CREATED_AT = "created_at"


class BounceSortOrder(StrEnum):
    """Sort order values for bounces."""

    ASC = "asc"
    DESC = "desc"


class BounceQuery(QueryRequest):
    """Query parameters for listing bounces."""

    def __init__(
            self,
            *,
            campaign_id: int | None = None,
            page: int | None = None,
            per_page: int | PerPage | None = None,
            source: str | None = None,
            order_by: BounceOrderBy | None = None,
            order: BounceSortOrder | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            campaign_id=campaign_id,
            page=page,
            per_page=per_page,
            source=source,
            order_by=order_by,
            order=order,
        )

    campaign_id = RequestField[int](value_type=int)
    page = RequestField[int](value_type=int)
    per_page = RequestField[int | PerPage](value_type=(int, PerPage))
    source = RequestField[str](value_type=str)
    order_by = RequestField[BounceOrderBy](value_type=BounceOrderBy)
    order = RequestField[BounceSortOrder](value_type=BounceSortOrder)

    def with_campaign(self, campaign_id: int) -> Self:
        """Filter by campaign identifier."""
        self.campaign_id = campaign_id
        return self

    def with_page(self, page: int) -> Self:
        """Set the requested page number."""
        self.page = page
        return self

    def with_per_page(self, per_page: int | PerPage) -> Self:
        """Set the requested page size."""
        self.per_page = per_page
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return _listmonk_page_state(self.page, self.per_page, default)

    def with_source(self, source: str) -> Self:
        """Filter by bounce source."""
        self.source = source
        return self

    def with_order_by(self, field: BounceOrderBy) -> Self:
        """Set the ordering field."""
        self.order_by = field
        return self

    def with_order(self, order: BounceSortOrder) -> Self:
        """Set the sort order."""
        self.order = order
        return self


class BounceDeleteQuery(QueryRequest):
    """Query parameters for deleting bounces."""

    def __init__(
            self,
            *,
            all: bool | None = None,
            ids: list[int] | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(all=all, ids=ids)

    all = RequestField[bool](value_type=bool)
    ids = RequestField[list[int]](
        name="id",
        query=QueryFieldSpec(serialization=QuerySerialization.REPEAT),
        value_type=list,
        validator=list_of(int),
    )

    def delete_all(self, enabled: bool = True) -> Self:
        """Delete all bounces when enabled."""
        self.all = enabled
        return self

    def add_id(self, bounce_id: int) -> Self:
        """Add a bounce identifier to delete."""
        self.ids = [*(self.ids or []), bounce_id]
        return self
