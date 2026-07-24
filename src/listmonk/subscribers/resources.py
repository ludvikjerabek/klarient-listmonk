from __future__ import annotations

from typing import Any

from klarient import (
    PagedResponse,
    PagedResponseModel,
    ResourcePath,
    SyncResource,
)
from klarient.http.client import _SyncClientImpl
from listmonk.common import BooleanResponse, ListmonkPagePagination
from listmonk.subscribers.models import Subscriber
from listmonk.subscribers.requests import (
    QueryListMembershipUpdate,
    SubscriberCreate,
    SubscriberDeleteQuery,
    SubscriberIds,
    SubscriberListMembershipUpdate,
    SubscriberQuery,
    SubscriberQueryBlocklist,
    SubscriberQueryDelete,
    SubscriberSQLQuery,
    SubscriberUpdate,
)
from listmonk.subscribers.responses import (
    SubscriberBounces,
    SubscriberExport,
    SubscriberResponse,
)


class SubscriberExportResource(SyncResource[_SyncClientImpl]):
    """Export endpoint for one subscriber."""

    def retrieve(self) -> SubscriberExport:
        """Retrieve export data for this subscriber."""
        return self._executor.get(SubscriberExport)


class SubscriberBouncesResource(SyncResource[_SyncClientImpl]):
    """Bounces endpoint for one subscriber."""

    def retrieve(self) -> SubscriberBounces:
        """Retrieve bounces for this subscriber."""
        return self._executor.get(SubscriberBounces)

    def delete(self) -> BooleanResponse:
        """Delete bounces for this subscriber."""
        return self._executor.delete(BooleanResponse)


class SubscriberOptinResource(SyncResource[_SyncClientImpl]):
    """Opt-in endpoint for one subscriber."""

    def send(self) -> BooleanResponse:
        """Send an opt-in confirmation message."""
        return self._executor.post(BooleanResponse)


class SubscriberBlocklistResource(SyncResource[_SyncClientImpl]):
    """Blocklist endpoint for one subscriber."""

    def blocklist(self) -> BooleanResponse:
        """Blocklist this subscriber."""
        return self._executor.put(BooleanResponse)


class SubscriberResource(SyncResource[_SyncClientImpl]):
    """Resource for one subscriber."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__export = SubscriberExportResource(self, segment="export")
        self.__bounces = SubscriberBouncesResource(self, segment="bounces")
        self.__optin = SubscriberOptinResource(self, segment="optin")
        self.__blocklist = SubscriberBlocklistResource(self, segment="blocklist")

    @property
    def export(self) -> SubscriberExportResource:
        """Export resource below this subscriber."""
        return self.__export

    @property
    def bounces(self) -> SubscriberBouncesResource:
        """Bounces resource below this subscriber."""
        return self.__bounces

    @property
    def optin(self) -> SubscriberOptinResource:
        """Opt-in resource below this subscriber."""
        return self.__optin

    @property
    def blocklist(self) -> SubscriberBlocklistResource:
        """Blocklist resource below this subscriber."""
        return self.__blocklist

    def retrieve(self) -> SubscriberResponse:
        """Retrieve this subscriber."""
        return self._executor.get(SubscriberResponse)

    def update(self, options: SubscriberUpdate) -> SubscriberResponse:
        """Replace this subscriber."""
        return self._executor.put(SubscriberResponse, options)

    def update_partial(self, options: SubscriberUpdate) -> SubscriberResponse:
        """Patch this subscriber."""
        return self._executor.patch(SubscriberResponse, options)

    def delete(self) -> BooleanResponse:
        """Delete this subscriber."""
        return self._executor.delete(BooleanResponse)


class SubscriberListsResource(SyncResource[_SyncClientImpl]):
    """Bulk subscriber list membership endpoint."""

    def update(
            self,
            options: SubscriberListMembershipUpdate,
    ) -> BooleanResponse:
        """Update list membership for subscriber IDs."""
        return self._executor.put(BooleanResponse, options)


class SubscribersBlocklistResource(SyncResource[_SyncClientImpl]):
    """Bulk subscriber blocklist endpoint."""

    def blocklist(self, options: SubscriberIds) -> BooleanResponse:
        """Blocklist subscribers by ID."""
        return self._executor.put(BooleanResponse, options)


class SubscriberQueryListsResource(SyncResource[_SyncClientImpl]):
    """Query based subscriber list membership endpoint."""

    def update(
            self,
            options: QueryListMembershipUpdate,
    ) -> BooleanResponse:
        """Update list membership for subscribers matching a query."""
        return self._executor.put(BooleanResponse, options)


class SubscriberQueryBlocklistResource(SyncResource[_SyncClientImpl]):
    """Query based subscriber blocklist endpoint."""

    def blocklist(
            self,
            options: SubscriberQueryBlocklist,
    ) -> BooleanResponse:
        """Blocklist subscribers matching a query."""
        return self._executor.put(BooleanResponse, options)


class SubscriberQueryDeleteResource(SyncResource[_SyncClientImpl]):
    """Query based subscriber delete endpoint."""

    def delete(self, options: SubscriberQueryDelete) -> BooleanResponse:
        """Delete subscribers matching a query."""
        return self._executor.post(BooleanResponse, options)


class SubscriberQueryResource(SyncResource[_SyncClientImpl]):
    """Query based subscriber action resource."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__lists = SubscriberQueryListsResource(self, segment="lists")
        self.__blocklist = SubscriberQueryBlocklistResource(self, segment="blocklist")
        self.__delete = SubscriberQueryDeleteResource(self, segment="delete")

    @property
    def lists(self) -> SubscriberQueryListsResource:
        """List membership resource below subscriber query actions."""
        return self.__lists

    @property
    def blocklist(self) -> SubscriberQueryBlocklistResource:
        """Blocklist resource below subscriber query actions."""
        return self.__blocklist

    @property
    def delete(self) -> SubscriberQueryDeleteResource:
        """Delete resource below subscriber query actions."""
        return self.__delete


class SubscriberSQLQueryResource(SyncResource[_SyncClientImpl]):
    """SQL query resource for subscribers."""

    def retrieve(
            self,
            options: SubscriberSQLQuery,
    ) -> PagedResponse[Subscriber]:
        """Retrieve subscribers using a SQL query filter."""
        return self._executor.get(
            PagedResponseModel(Subscriber, ListmonkPagePagination()),
            options,
        )


class SubscribersResource(SyncResource[_SyncClientImpl]):
    """Paged subscribers collection resource."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__lists = SubscriberListsResource(self, segment="lists")
        self.__blocklist = SubscribersBlocklistResource(self, segment="blocklist")
        self.__query = SubscriberQueryResource(self, segment="query")
        self.__sql_query = SubscriberSQLQueryResource(self)

    def __getitem__(self, subscriber_id: int | str) -> SubscriberResource:
        return SubscriberResource(self, segment=ResourcePath.segment(subscriber_id))

    @property
    def lists(self) -> SubscriberListsResource:
        """Bulk list membership resource."""
        return self.__lists

    @property
    def blocklist(self) -> SubscribersBlocklistResource:
        """Bulk blocklist resource."""
        return self.__blocklist

    @property
    def query(self) -> SubscriberQueryResource:
        """Query based subscriber action resource."""
        return self.__query

    @property
    def sql_query(self) -> SubscriberSQLQueryResource:
        """SQL query resource."""
        return self.__sql_query

    def retrieve(
            self,
            options: SubscriberQuery | None = None,
    ) -> PagedResponse[Subscriber]:
        """Retrieve subscribers with optional query parameters."""
        return self._executor.get(
            PagedResponseModel(Subscriber, ListmonkPagePagination()),
            options,
        )

    def create(self, options: SubscriberCreate) -> SubscriberResponse:
        """Create a subscriber."""
        return self._executor.post(SubscriberResponse, options)

    def delete(self, options: SubscriberDeleteQuery) -> BooleanResponse:
        """Delete subscribers by ID."""
        return self._executor.delete(BooleanResponse, options)
