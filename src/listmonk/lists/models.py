from __future__ import annotations

from typing import Any

from listmonk.common import ListOptin, ListStatus, ListType


class List(dict[str, Any]):
    """List record returned by listmonk."""

    @property
    def id(self) -> int:
        """List numeric identifier."""
        return int(self["id"])

    @property
    def uuid(self) -> str:
        """List UUID."""
        return str(self["uuid"])

    @property
    def name(self) -> str:
        """List display name."""
        return str(self["name"])

    @property
    def type(self) -> ListType:
        """List visibility type."""
        return ListType(str(self["type"]))

    @property
    def optin(self) -> ListOptin:
        """List opt-in mode."""
        return ListOptin(str(self["optin"]))

    @property
    def status(self) -> ListStatus:
        """List status."""
        return ListStatus(str(self["status"]))

    @property
    def tags(self) -> list[str]:
        """Tags assigned to the list."""
        tags = self.get("tags", [])
        if not isinstance(tags, list):
            return []
        return [str(tag) for tag in tags]

    @property
    def subscriber_count(self) -> int:
        """Number of subscribers in the list."""
        return int(self.get("subscriber_count", 0))

    @property
    def description(self) -> str:
        """List description."""
        return str(self.get("description", ""))


class PublicList(dict[str, Any]):
    """Public subscription list record."""

    @property
    def uuid(self) -> str:
        """Public list UUID."""
        return str(self["uuid"])

    @property
    def name(self) -> str:
        """Public list name."""
        return str(self["name"])
