from __future__ import annotations

from enum import StrEnum
from typing import Any, Self

from klarient import (
    PageNumberState,
    RequestField,
    JSONBodyRequest,
    QueryFieldSpec,
    QueryRequest,
    QuerySerialization,
    list_of,
)
from listmonk.common import (
    CreateSubscriberStatus,
    PerPage,
    SortOrder,
    SubscriberStatus,
    SubscriptionStatus,
)
from listmonk.common.paging import _listmonk_page_state


class ListMembershipAction(StrEnum):
    """Actions for subscriber list membership updates."""

    ADD = "add"
    REMOVE = "remove"
    UNSUBSCRIBE = "unsubscribe"


class SubscriberOrderBy(StrEnum):
    """Fields accepted by subscriber ordering."""

    NAME = "name"
    STATUS = "status"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class SubscriberQuery(QueryRequest):
    """Query parameters for listing subscribers."""

    def __init__(
            self,
            *,
            query: str | None = None,
            list_id: list[int] | None = None,
            subscription_status: SubscriptionStatus | None = None,
            order_by: SubscriberOrderBy | None = None,
            order: SortOrder | None = None,
            page: int | None = None,
            per_page: int | PerPage | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            query=query,
            list_id=list_id,
            subscription_status=subscription_status,
            order_by=order_by,
            order=order,
            page=page,
            per_page=per_page,
        )

    query = RequestField[str](value_type=str)
    list_id = RequestField[list[int]](
        query=QueryFieldSpec(serialization=QuerySerialization.REPEAT),
        value_type=list,
        validator=list_of(int),
    )
    subscription_status = RequestField[SubscriptionStatus](value_type=SubscriptionStatus)
    order_by = RequestField[SubscriberOrderBy](value_type=SubscriberOrderBy)
    order = RequestField[SortOrder](value_type=SortOrder)
    page = RequestField[int](value_type=int)
    per_page = RequestField[int | PerPage](value_type=(int, PerPage))

    def with_query(self, query: str) -> Self:
        """Set the subscriber search query."""
        self.query = query
        return self

    def add_list(self, list_id: int) -> Self:
        """Add a list identifier filter."""
        self.list_id = [*(self.list_id or []), list_id]
        return self

    def with_subscription_status(self, status: SubscriptionStatus) -> Self:
        """Filter by subscription status."""
        self.subscription_status = status
        return self

    def with_order_by(self, field: SubscriberOrderBy) -> Self:
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


class SubscriberSQLQuery(SubscriberQuery):
    """Query parameters for SQL based subscriber filtering."""

    def __init__(
            self,
            *,
            query: str | None = None,
            list_id: list[int] | None = None,
            subscription_status: SubscriptionStatus | None = None,
            order_by: SubscriberOrderBy | None = None,
            order: SortOrder | None = None,
            page: int | None = None,
            per_page: int | PerPage | None = None,
    ) -> None:
        super().__init__(
            query=query,
            list_id=list_id,
            subscription_status=subscription_status,
            order_by=order_by,
            order=order,
            page=page,
            per_page=per_page,
        )

    def with_sql(self, expression: str) -> Self:
        """Set the SQL query expression."""
        self.query = expression
        return self


class SubscriberCreate(JSONBodyRequest):
    """JSON body for creating a subscriber."""

    def __init__(
            self,
            *,
            email: str | None = None,
            name: str | None = None,
            status: CreateSubscriberStatus | None = None,
            lists: list[int] | None = None,
            attribs: dict[str, Any] | None = None,
            preconfirm_subscriptions: bool | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            email=email,
            name=name,
            status=status,
            lists=lists,
            attribs=attribs,
            preconfirm_subscriptions=preconfirm_subscriptions,
        )

    email = RequestField[str](value_type=str)
    name = RequestField[str](value_type=str)
    status = RequestField[CreateSubscriberStatus](value_type=CreateSubscriberStatus)
    lists = RequestField[list[int]](value_type=list, validator=list_of(int))
    attribs = RequestField[dict[str, Any]](value_type=dict)
    preconfirm_subscriptions = RequestField[bool](value_type=bool)

    def with_email(self, email: str) -> Self:
        """Set the subscriber email address."""
        self.email = email
        return self

    def with_name(self, name: str) -> Self:
        """Set the subscriber display name."""
        self.name = name
        return self

    def with_status(self, status: CreateSubscriberStatus) -> Self:
        """Set the subscriber status."""
        self.status = status
        return self

    def add_list(self, list_id: int) -> Self:
        """Add a list identifier."""
        self.lists = [*(self.lists or []), list_id]
        return self

    def with_attrib(self, name: str, value: Any) -> Self:
        """Set a subscriber attribute value."""
        self.attribs = {**(self.attribs or {}), name: value}
        return self

    def with_preconfirm_subscriptions(self, enabled: bool = True) -> Self:
        """Set whether subscriptions are preconfirmed."""
        self.preconfirm_subscriptions = enabled
        return self


class SubscriberUpdate(JSONBodyRequest):
    """JSON body for updating a subscriber."""

    def __init__(
            self,
            *,
            email: str | None = None,
            name: str | None = None,
            status: SubscriberStatus | None = None,
            lists: list[int] | None = None,
            attribs: dict[str, Any] | None = None,
            preconfirm_subscriptions: bool | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            email=email,
            name=name,
            status=status,
            lists=lists,
            attribs=attribs,
            preconfirm_subscriptions=preconfirm_subscriptions,
        )

    email = RequestField[str](value_type=str)
    name = RequestField[str](value_type=str)
    status = RequestField[SubscriberStatus](value_type=SubscriberStatus)
    lists = RequestField[list[int]](value_type=list, validator=list_of(int))
    attribs = RequestField[dict[str, Any]](value_type=dict)
    preconfirm_subscriptions = RequestField[bool](value_type=bool)

    def with_email(self, email: str) -> Self:
        """Set the subscriber email address."""
        self.email = email
        return self

    def with_name(self, name: str) -> Self:
        """Set the subscriber display name."""
        self.name = name
        return self

    def with_status(self, status: SubscriberStatus) -> Self:
        """Set the subscriber status."""
        self.status = status
        return self

    def add_list(self, list_id: int) -> Self:
        """Add a list identifier."""
        self.lists = [*(self.lists or []), list_id]
        return self

    def with_attrib(self, name: str, value: Any) -> Self:
        """Set a subscriber attribute value."""
        self.attribs = {**(self.attribs or {}), name: value}
        return self

    def with_preconfirm_subscriptions(self, enabled: bool = True) -> Self:
        """Set whether subscriptions are preconfirmed."""
        self.preconfirm_subscriptions = enabled
        return self


class SubscriberListMembershipUpdate(JSONBodyRequest):
    """JSON body for updating list membership by subscriber IDs."""

    def __init__(
            self,
            *,
            ids: list[int] | None = None,
            action: ListMembershipAction | None = None,
            target_list_ids: list[int] | None = None,
            status: SubscriptionStatus | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            ids=ids,
            action=action,
            target_list_ids=target_list_ids,
            status=status,
        )

    ids = RequestField[list[int]](value_type=list, validator=list_of(int))
    action = RequestField[ListMembershipAction](value_type=ListMembershipAction)
    target_list_ids = RequestField[list[int]](value_type=list, validator=list_of(int))
    status = RequestField[SubscriptionStatus](value_type=SubscriptionStatus)

    def add_id(self, subscriber_id: int) -> Self:
        """Add a subscriber identifier."""
        self.ids = [*(self.ids or []), subscriber_id]
        return self

    def with_action(self, action: ListMembershipAction) -> Self:
        """Set the membership action."""
        self.action = action
        return self

    def add_target_list(self, list_id: int) -> Self:
        """Add a target list identifier."""
        self.target_list_ids = [*(self.target_list_ids or []), list_id]
        return self

    def with_status(self, status: SubscriptionStatus) -> Self:
        """Set the resulting subscription status."""
        self.status = status
        return self


class QueryListMembershipUpdate(JSONBodyRequest):
    """JSON body for updating list membership by query."""

    def __init__(
            self,
            *,
            action: ListMembershipAction | None = None,
            target_list_ids: list[int] | None = None,
            query: str | None = None,
            search: str | None = None,
            list_ids: list[int] | None = None,
            status: SubscriptionStatus | None = None,
            subscription_status: SubscriptionStatus | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            action=action,
            target_list_ids=target_list_ids,
            query=query,
            search=search,
            list_ids=list_ids,
            status=status,
            subscription_status=subscription_status,
        )

    action = RequestField[ListMembershipAction](value_type=ListMembershipAction)
    target_list_ids = RequestField[list[int]](value_type=list, validator=list_of(int))
    query = RequestField[str](value_type=str)
    search = RequestField[str](value_type=str)
    list_ids = RequestField[list[int]](value_type=list, validator=list_of(int))
    status = RequestField[SubscriptionStatus](value_type=SubscriptionStatus)
    subscription_status = RequestField[SubscriptionStatus](value_type=SubscriptionStatus)

    def with_action(self, action: ListMembershipAction) -> Self:
        """Set the membership action."""
        self.action = action
        return self

    def add_target_list(self, list_id: int) -> Self:
        """Add a target list identifier."""
        self.target_list_ids = [*(self.target_list_ids or []), list_id]
        return self

    def with_query(self, query: str) -> Self:
        """Set the query expression."""
        self.query = query
        return self

    def with_search(self, search: str) -> Self:
        """Set the search expression."""
        self.search = search
        return self

    def add_list(self, list_id: int) -> Self:
        """Add a source list identifier."""
        self.list_ids = [*(self.list_ids or []), list_id]
        return self

    def with_status(self, status: SubscriptionStatus) -> Self:
        """Set the resulting subscription status."""
        self.status = status
        return self

    def with_subscription_status(self, status: SubscriptionStatus) -> Self:
        """Filter by current subscription status."""
        self.subscription_status = status
        return self


class SubscriberIds(JSONBodyRequest):
    """JSON body containing subscriber identifiers."""

    def __init__(self, *, ids: list[int] | None = None) -> None:
        super().__init__()
        self._set_optional_fields(ids=ids)

    ids = RequestField[list[int]](value_type=list, validator=list_of(int))

    def add_id(self, subscriber_id: int) -> Self:
        """Add a subscriber identifier."""
        self.ids = [*(self.ids or []), subscriber_id]
        return self


class SubscriberDeleteQuery(QueryRequest):
    """Query parameters for deleting subscribers by ID."""

    def __init__(self, *, ids: list[int] | None = None) -> None:
        super().__init__()
        self._set_optional_fields(ids=ids)

    ids = RequestField[list[int]](
        name="id",
        query=QueryFieldSpec(serialization=QuerySerialization.REPEAT),
        value_type=list,
        validator=list_of(int),
    )

    def add_id(self, subscriber_id: int) -> Self:
        """Add a subscriber identifier to delete."""
        self.ids = [*(self.ids or []), subscriber_id]
        return self


class SubscriberQueryBlocklist(JSONBodyRequest):
    """JSON body for blocklisting subscribers by query."""

    def __init__(
            self,
            *,
            query: str | None = None,
            list_ids: list[int] | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(query=query, list_ids=list_ids)

    query = RequestField[str](value_type=str)
    list_ids = RequestField[list[int]](value_type=list, validator=list_of(int))

    def with_query(self, query: str) -> Self:
        """Set the blocklist query expression."""
        self.query = query
        return self

    def add_list(self, list_id: int) -> Self:
        """Add a list identifier filter."""
        self.list_ids = [*(self.list_ids or []), list_id]
        return self


class SubscriberQueryDelete(JSONBodyRequest):
    """JSON body for deleting subscribers by query."""

    def __init__(
            self,
            *,
            query: str | None = None,
            list_ids: list[int] | None = None,
            all: bool | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(query=query, list_ids=list_ids, all=all)

    query = RequestField[str](value_type=str)
    list_ids = RequestField[list[int]](value_type=list, validator=list_of(int))
    all = RequestField[bool](value_type=bool)

    def with_query(self, query: str) -> Self:
        """Set the delete query expression."""
        self.query = query
        return self

    def add_list(self, list_id: int) -> Self:
        """Add a list identifier filter."""
        self.list_ids = [*(self.list_ids or []), list_id]
        return self

    def with_all(self, enabled: bool = True) -> Self:
        """Delete all matching subscribers when enabled."""
        self.all = enabled
        return self
