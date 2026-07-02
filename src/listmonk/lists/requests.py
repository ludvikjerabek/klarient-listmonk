from __future__ import annotations

from enum import StrEnum
from typing import Self

from klarient import (
    JSONBodyRequest,
    PageNumberState,
    QueryFieldSpec,
    QueryRequest,
    QuerySerialization,
    RequestField,
    list_of,
)
from listmonk.common import (
    ListOptin,
    ListStatus,
    ListType,
    PerPage,
    SortOrder,
)
from listmonk.common.paging import _listmonk_page_state


class ListOrderBy(StrEnum):
    """Fields accepted by list ordering."""

    NAME = "name"
    STATUS = "status"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class ListQuery(QueryRequest):
    """Query parameters for listing listmonk lists."""

    def __init__(
            self,
            *,
            query: str | None = None,
            status: ListStatus | None = None,
            minimal: bool | None = None,
            tags: list[str] | None = None,
            order_by: ListOrderBy | None = None,
            order: SortOrder | None = None,
            page: int | None = None,
            per_page: int | PerPage | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            query=query,
            status=status,
            minimal=minimal,
            tags=tags,
            order_by=order_by,
            order=order,
            page=page,
            per_page=per_page,
        )

    query = RequestField[str](value_type=str)
    status = RequestField[ListStatus](value_type=ListStatus)
    minimal = RequestField[bool](value_type=bool)
    tags = RequestField[list[str]](
        name="tag",
        query=QueryFieldSpec(serialization=QuerySerialization.REPEAT),
        value_type=list,
        validator=list_of(str),
    )
    order_by = RequestField[ListOrderBy](value_type=ListOrderBy)
    order = RequestField[SortOrder](value_type=SortOrder)
    page = RequestField[int](value_type=int)
    per_page = RequestField[int | PerPage](value_type=(int, PerPage))

    def with_query(self, query: str) -> Self:
        """Set the search query."""
        self.query = query
        return self

    def with_status(self, status: ListStatus) -> Self:
        """Filter by list status."""
        self.status = status
        return self

    def with_minimal(self, enabled: bool = True) -> Self:
        """Request minimal list data."""
        self.minimal = enabled
        return self

    def add_tag(self, tag: str) -> Self:
        """Add a repeated tag filter."""
        self.tags = [*(self.tags or []), tag]
        return self

    def with_order_by(self, field: ListOrderBy) -> Self:
        """Set the ordering field."""
        self.order_by = field
        return self

    def with_order(self, order: SortOrder) -> Self:
        """Set the sort order."""
        self.order = order
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


class ListCreate(JSONBodyRequest):
    """JSON body for creating a list."""

    def __init__(
            self,
            *,
            name: str | None = None,
            type: ListType | None = None,
            optin: ListOptin | None = None,
            status: ListStatus | None = None,
            tags: list[str] | None = None,
            description: str | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            name=name,
            type=type,
            optin=optin,
            status=status,
            tags=tags,
            description=description,
        )

    name = RequestField[str](value_type=str)
    type = RequestField[ListType](value_type=ListType)
    optin = RequestField[ListOptin](value_type=ListOptin)
    status = RequestField[ListStatus](value_type=ListStatus)
    tags = RequestField[list[str]](value_type=list, validator=list_of(str))
    description = RequestField[str](value_type=str)

    def with_name(self, name: str) -> Self:
        """Set the list name."""
        self.name = name
        return self

    def with_type(self, type: ListType) -> Self:
        """Set the list type."""
        self.type = type
        return self

    def with_optin(self, optin: ListOptin) -> Self:
        """Set the list opt-in mode."""
        self.optin = optin
        return self

    def with_status(self, status: ListStatus) -> Self:
        """Set the list status."""
        self.status = status
        return self

    def add_tag(self, tag: str) -> Self:
        """Add a tag to the list."""
        self.tags = [*(self.tags or []), tag]
        return self

    def with_description(self, description: str) -> Self:
        """Set the list description."""
        self.description = description
        return self


class ListUpdate(ListCreate):
    """Form body for updating a list."""

    pass


class ListDeleteQuery(QueryRequest):
    """Query parameters for deleting lists in bulk."""

    def __init__(
            self,
            *,
            ids: list[int] | None = None,
            query: str | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(ids=ids, query=query)

    ids = RequestField[list[int]](
        name="id",
        query=QueryFieldSpec(serialization=QuerySerialization.REPEAT),
        value_type=list,
        validator=list_of(int),
    )
    query = RequestField[str](value_type=str)

    def add_id(self, list_id: int) -> Self:
        """Add a list identifier to delete."""
        self.ids = [*(self.ids or []), list_id]
        return self

    def with_query(self, query: str) -> Self:
        """Delete lists matching the search query."""
        self.query = query
        return self
