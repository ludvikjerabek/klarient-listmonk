from __future__ import annotations

from enum import StrEnum
from typing import Self

from klarient import FormBodyRequest, JSONBodyRequest, RequestField


class TemplateType(StrEnum):
    """Template type values."""

    CAMPAIGN = "campaign"
    CAMPAIGN_VISUAL = "campaign_visual"
    TRANSACTIONAL = "tx"


class TemplateCreate(JSONBodyRequest):
    """JSON body for creating a template."""

    def __init__(
            self,
            *,
            name: str | None = None,
            type: TemplateType | None = None,
            subject: str | None = None,
            body_source: str | None = None,
            body: str | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            name=name,
            type=type,
            subject=subject,
            body_source=body_source,
            body=body,
        )

    name = RequestField[str](value_type=str)
    type = RequestField[TemplateType](value_type=TemplateType)
    subject = RequestField[str](value_type=str)
    body_source = RequestField[str](value_type=str)
    body = RequestField[str](value_type=str)

    def with_name(self, name: str) -> Self:
        """Set the template name."""
        self.name = name
        return self

    def with_type(self, type: TemplateType) -> Self:
        """Set the template type."""
        self.type = type
        return self

    def with_subject(self, subject: str) -> Self:
        """Set the template subject."""
        self.subject = subject
        return self

    def with_body_source(self, body_source: str) -> Self:
        """Set the template source body."""
        self.body_source = body_source
        return self

    def with_body(self, body: str) -> Self:
        """Set the rendered template body."""
        self.body = body
        return self


class TemplateUpdate(TemplateCreate):
    """JSON body for updating a template."""

    pass


class TemplatePreviewRender(FormBodyRequest):
    """Form body for rendering a template preview."""

    def __init__(
            self,
            *,
            type: TemplateType | None = None,
            body: str | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(type=type, body=body)

    type = RequestField[TemplateType](name="template_type", value_type=TemplateType)
    body = RequestField[str](value_type=str)

    def with_type(self, type: TemplateType) -> Self:
        """Set the template type used for preview rendering."""
        self.type = type
        return self

    def with_body(self, body: str) -> Self:
        """Set the template body used for preview rendering."""
        self.body = body
        return self
