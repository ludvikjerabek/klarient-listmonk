from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from listmonk.common import BounceType


class BounceCampaign(dict[str, Any]):
    """Campaign summary attached to a bounce."""

    @property
    def id(self) -> int:
        """Campaign identifier."""
        return int(self["id"])

    @property
    def name(self) -> str:
        """Campaign name."""
        return str(self.get("name", ""))


class Bounce(dict[str, Any]):
    """Bounce record returned by listmonk."""

    @property
    def id(self) -> int:
        """Bounce identifier."""
        return int(self["id"])

    @property
    def type(self) -> BounceType:
        """Bounce type."""
        return BounceType(str(self["type"]))

    @property
    def source(self) -> str:
        """Bounce source."""
        return str(self.get("source", ""))

    @property
    def meta(self) -> dict[str, Any]:
        """Open bounce metadata."""
        meta = self.get("meta")
        return dict(meta) if isinstance(meta, Mapping) else {}

    @property
    def created_at(self) -> str:
        """Creation timestamp."""
        return str(self.get("created_at", ""))

    @property
    def email(self) -> str:
        """Bounced email address."""
        return str(self.get("email", ""))

    @property
    def subscriber_uuid(self) -> str:
        """Subscriber UUID."""
        return str(self.get("subscriber_uuid", ""))

    @property
    def subscriber_id(self) -> int:
        """Subscriber identifier."""
        return int(self.get("subscriber_id", 0) or 0)

    @property
    def campaign(self) -> BounceCampaign | None:
        """Campaign associated with the bounce when present."""
        campaign = self.get("campaign")
        if not isinstance(campaign, Mapping):
            return None
        return BounceCampaign(campaign)
