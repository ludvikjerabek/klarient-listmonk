from __future__ import annotations

from typing import Any

from listmonk.templates.requests import TemplateType


class Template(dict[str, Any]):
    """Template record returned by listmonk."""

    @property
    def id(self) -> int:
        """Template numeric identifier."""
        return int(self["id"])

    @property
    def created_at(self) -> str:
        """Creation timestamp."""
        return str(self.get("created_at", ""))

    @property
    def updated_at(self) -> str:
        """Last update timestamp."""
        return str(self.get("updated_at", ""))

    @property
    def name(self) -> str:
        """Template name."""
        return str(self.get("name", ""))

    @property
    def body(self) -> str:
        """Rendered template body."""
        return str(self.get("body", ""))

    @property
    def body_source(self) -> str:
        """Template source body."""
        value = self.get("body_source", "")
        return "" if value is None else str(value)

    @property
    def type(self) -> TemplateType:
        """Template type."""
        return TemplateType(str(self["type"]))

    @property
    def subject(self) -> str:
        """Template subject."""
        return str(self.get("subject", ""))

    @property
    def is_default(self) -> bool:
        """Whether this is the default template for its type."""
        return bool(self.get("is_default", False))
