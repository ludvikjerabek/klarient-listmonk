from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from listmonk.common import (
    BounceType,
    ListType,
    SubscriberStatus,
    SubscriptionStatus,
)


class SubscriberList(dict[str, Any]):
    """List membership attached to a subscriber."""

    @property
    def id(self) -> int:
        """List identifier."""
        return int(self["id"])

    @property
    def uuid(self) -> str:
        """List UUID."""
        return str(self["uuid"])

    @property
    def name(self) -> str:
        """List name."""
        return str(self["name"])

    @property
    def type(self) -> ListType:
        """List type."""
        return ListType(str(self["type"]))

    @property
    def subscription_status(self) -> SubscriptionStatus:
        """Subscriber status for this list."""
        return SubscriptionStatus(str(self["subscription_status"]))


class Subscriber(dict[str, Any]):
    """Subscriber record returned by listmonk."""

    @property
    def id(self) -> int:
        """Subscriber identifier."""
        return int(self["id"])

    @property
    def uuid(self) -> str:
        """Subscriber UUID."""
        return str(self["uuid"])

    @property
    def email(self) -> str:
        """Subscriber email address."""
        return str(self["email"])

    @property
    def name(self) -> str:
        """Subscriber display name."""
        return str(self.get("name", ""))

    @property
    def attribs(self) -> dict[str, Any]:
        """Open subscriber attributes."""
        attribs = self.get("attribs")
        return dict(attribs) if isinstance(attribs, Mapping) else {}

    @property
    def status(self) -> SubscriberStatus:
        """Subscriber status."""
        return SubscriberStatus(str(self["status"]))

    @property
    def lists(self) -> list[SubscriberList]:
        """List memberships attached to the subscriber."""
        lists = self.get("lists", [])
        if not isinstance(lists, list):
            return []
        return [
            SubscriberList(item)
            for item in lists
            if isinstance(item, Mapping)
        ]

    @property
    def list_ids(self) -> list[int]:
        """List identifiers when list data is returned as IDs."""
        lists = self.get("lists", [])
        if not isinstance(lists, list):
            return []
        return [int(item) for item in lists if isinstance(item, int)]


class SubscriberExportProfile(dict[str, Any]):
    """Subscriber profile data from export."""

    @property
    def id(self) -> int:
        """Subscriber identifier."""
        return int(self["id"])

    @property
    def email(self) -> str:
        """Subscriber email address."""
        return str(self["email"])


class SubscriberExportSubscription(dict[str, Any]):
    """Subscription data from subscriber export."""

    @property
    def name(self) -> str:
        """List name."""
        return str(self["name"])

    @property
    def type(self) -> ListType:
        """List type."""
        return ListType(str(self["type"]))

    @property
    def subscription_status(self) -> SubscriptionStatus:
        """Subscription status."""
        return SubscriptionStatus(str(self["subscription_status"]))


class BounceCampaign(dict[str, Any]):
    """Campaign summary attached to a subscriber bounce."""

    @property
    def id(self) -> int:
        """Campaign identifier."""
        return int(self["id"])

    @property
    def name(self) -> str:
        """Campaign name."""
        return str(self["name"])


class SubscriberBounce(dict[str, Any]):
    """Bounce record for one subscriber."""

    @property
    def id(self) -> int:
        """Bounce identifier."""
        return int(self["id"])

    @property
    def type(self) -> BounceType:
        """Bounce type."""
        return BounceType(str(self["type"]))

    @property
    def email(self) -> str:
        """Bounced email address."""
        return str(self["email"])

    @property
    def subscriber_id(self) -> int:
        """Subscriber identifier."""
        return int(self["subscriber_id"])

    @property
    def campaign(self) -> BounceCampaign | None:
        """Campaign associated with the bounce when present."""
        campaign = self.get("campaign")
        if not isinstance(campaign, Mapping):
            return None
        return BounceCampaign(campaign)
