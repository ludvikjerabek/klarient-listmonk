from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from listmonk.campaigns.requests import (
    CampaignContentType,
    CampaignStatus,
    CampaignType,
)


class CampaignList(dict[str, Any]):
    """List summary attached to a campaign."""

    @property
    def id(self) -> int:
        """List identifier."""
        return int(self["id"])

    @property
    def name(self) -> str:
        """List name."""
        return str(self["name"])


class Campaign(dict[str, Any]):
    """Campaign record returned by listmonk."""

    @property
    def id(self) -> int:
        """Campaign identifier."""
        return int(self["id"])

    @property
    def uuid(self) -> str:
        """Campaign UUID."""
        return str(self.get("uuid", ""))

    @property
    def name(self) -> str:
        """Campaign name."""
        return str(self.get("name", ""))

    @property
    def subject(self) -> str:
        """Campaign subject."""
        return str(self.get("subject", ""))

    @property
    def from_email(self) -> str:
        """Sender email address."""
        return str(self.get("from_email", ""))

    @property
    def body(self) -> str:
        """Rendered campaign body."""
        return str(self.get("body", ""))

    @property
    def body_source(self) -> str:
        """Campaign source body."""
        return str(self.get("body_source", ""))

    @property
    def altbody(self) -> str:
        """Alternate campaign body."""
        return str(self.get("altbody", ""))

    @property
    def send_at(self) -> str:
        """Scheduled send timestamp."""
        return str(self.get("send_at", ""))

    @property
    def status(self) -> CampaignStatus:
        """Campaign status."""
        return CampaignStatus(str(self["status"]))

    @property
    def type(self) -> CampaignType:
        """Campaign type."""
        return CampaignType(str(self["type"]))

    @property
    def content_type(self) -> CampaignContentType:
        """Campaign content type."""
        return CampaignContentType(str(self["content_type"]))

    @property
    def lists(self) -> list[CampaignList]:
        """Lists targeted by the campaign."""
        lists = self.get("lists", [])
        if not isinstance(lists, list):
            return []
        return [
            CampaignList(item)
            for item in lists
            if isinstance(item, Mapping)
        ]

    @property
    def tags(self) -> list[str]:
        """Tags assigned to the campaign."""
        tags = self.get("tags", [])
        if not isinstance(tags, list):
            return []
        return [str(tag) for tag in tags]

    @property
    def template_id(self) -> int:
        """Template identifier."""
        return int(self.get("template_id", 0) or 0)

    @property
    def messenger(self) -> str:
        """Messenger name."""
        return str(self.get("messenger", ""))

    @property
    def views(self) -> int:
        """Campaign view count."""
        return int(self.get("views", 0) or 0)

    @property
    def clicks(self) -> int:
        """Campaign click count."""
        return int(self.get("clicks", 0) or 0)

    @property
    def bounces(self) -> int:
        """Campaign bounce count."""
        return int(self.get("bounces", 0) or 0)

    @property
    def to_send(self) -> int:
        """Number of messages still queued to send."""
        return int(self.get("to_send", 0) or 0)

    @property
    def sent(self) -> int:
        """Number of sent messages."""
        return int(self.get("sent", 0) or 0)

    @property
    def headers(self) -> list[dict[str, Any]]:
        """Custom campaign headers."""
        headers = self.get("headers", [])
        if not isinstance(headers, list):
            return []
        return [dict(item) for item in headers if isinstance(item, Mapping)]

    @property
    def attribs(self) -> dict[str, Any]:
        """Open campaign attributes."""
        attribs = self.get("attribs")
        return dict(attribs) if isinstance(attribs, Mapping) else {}

    @property
    def archive(self) -> bool:
        """Whether archive publishing is enabled."""
        return bool(self.get("archive", False))

    @property
    def archive_slug(self) -> str:
        """Archive slug."""
        return str(self.get("archive_slug", ""))

    @property
    def archive_template_id(self) -> int:
        """Archive template identifier."""
        return int(self.get("archive_template_id", 0) or 0)

    @property
    def archive_meta(self) -> str:
        """Archive metadata."""
        return str(self.get("archive_meta", ""))


class CampaignRunningStat(dict[str, Any]):
    """Running campaign statistics."""

    @property
    def campaign_id(self) -> int:
        """Campaign identifier."""
        return int(self.get("campaign_id", 0) or 0)

    @property
    def status(self) -> str:
        """Campaign status."""
        return str(self.get("status", ""))

    @property
    def sent(self) -> int:
        """Number of sent messages."""
        return int(self.get("sent", 0) or 0)

    @property
    def to_send(self) -> int:
        """Number of messages still queued to send."""
        return int(self.get("to_send", 0) or 0)


class CampaignAnalyticsPoint(dict[str, Any]):
    """Campaign analytics point."""

    @property
    def campaign_id(self) -> int:
        """Campaign identifier."""
        return int(self.get("campaign_id", 0) or 0)

    @property
    def count(self) -> int:
        """Analytics count."""
        return int(self.get("count", 0) or 0)

    @property
    def timestamp(self) -> str:
        """Analytics timestamp."""
        return str(self.get("timestamp", ""))

    @property
    def url(self) -> str:
        """Analytics URL when present."""
        return str(self.get("url", ""))
