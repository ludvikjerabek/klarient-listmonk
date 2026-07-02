from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from klarient import ResponseMap
from listmonk.subscribers.models import (
    Subscriber,
    SubscriberBounce,
    SubscriberExportProfile,
    SubscriberExportSubscription,
)


class SubscriberResponse(ResponseMap):
    """Response wrapper for one subscriber."""

    @property
    def data(self) -> Subscriber:
        """Subscriber returned by the endpoint."""
        data = self.get("data", {})
        return Subscriber(data if isinstance(data, Mapping) else {})


class SubscriberExport(ResponseMap):
    """Response wrapper for subscriber export data."""

    @property
    def profile(self) -> list[SubscriberExportProfile]:
        """Exported subscriber profile rows."""
        return [
            SubscriberExportProfile(item)
            for item in self.get("profile", [])
            if isinstance(item, Mapping)
        ]

    @property
    def subscriptions(self) -> list[SubscriberExportSubscription]:
        """Exported subscriber subscription rows."""
        return [
            SubscriberExportSubscription(item)
            for item in self.get("subscriptions", [])
            if isinstance(item, Mapping)
        ]

    @property
    def campaign_views(self) -> list[Any]:
        """Raw campaign view export rows."""
        value = self.get("campaign_views", [])
        return value if isinstance(value, list) else []

    @property
    def link_clicks(self) -> list[Any]:
        """Raw link click export rows."""
        value = self.get("link_clicks", [])
        return value if isinstance(value, list) else []


class SubscriberBounces(ResponseMap):
    """Response wrapper for subscriber bounce data."""

    @property
    def data(self) -> list[SubscriberBounce]:
        """Bounce records returned for the subscriber."""
        return [
            SubscriberBounce(item)
            for item in self.get("data", [])
            if isinstance(item, Mapping)
        ]
