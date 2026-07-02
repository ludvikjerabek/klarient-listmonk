from __future__ import annotations

from typing import Any

from klarient.http.client import _SyncClientImpl

from klarient import SyncResource
from listmonk.common import BooleanResponse
from listmonk.lists.responses import PublicListsResponse
from listmonk.public.requests import PublicSubscription, PublicSubscriptionForm


class PublicSubscriptionResource(SyncResource[_SyncClientImpl]):
    """Public subscription endpoint."""

    def create(self, options: PublicSubscription) -> BooleanResponse:
        """Create a public subscription using JSON."""
        return self._executor.post(BooleanResponse, options)

    def create_form(
            self,
            options: PublicSubscriptionForm,
    ) -> BooleanResponse:
        """Create a public subscription using form data."""
        return self._executor.post(BooleanResponse, options)


class PublicResource(SyncResource[_SyncClientImpl]):
    """Public API root."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__lists = PublicListsResource(self, segment="lists")
        self.__subscription = PublicSubscriptionResource(self, segment="subscription")

    @property
    def lists(self) -> PublicListsResource:
        """Public lists resource."""
        return self.__lists

    @property
    def subscription(self) -> PublicSubscriptionResource:
        """Public subscription resource."""
        return self.__subscription


class PublicListsResource(SyncResource[_SyncClientImpl]):
    """Public lists endpoint."""

    def retrieve(self) -> PublicListsResponse:
        """Retrieve public subscription lists."""
        return self._executor.get(PublicListsResponse)
