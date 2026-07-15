from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any, Self

from klarient import (
    HTTPRequestOptions,
    JSONBody,
    MultipartBuilder,
    MultipartValue,
    RequestField,
    RequestFields,
    RequestOptionsProvider,
    list_of,
)


class TransactionalContentType(StrEnum):
    """Transactional message content type values."""

    HTML = "html"
    MARKDOWN = "markdown"
    PLAIN = "plain"


class TransactionalSubscriberMode(StrEnum):
    """Subscriber lookup modes for transactional messages."""

    DEFAULT = "default"
    FALLBACK = "fallback"
    EXTERNAL = "external"


class TransactionalMessage(RequestFields, RequestOptionsProvider):
    """Request object for sending transactional messages."""

    _payload_fields = (
        "subscriber_email",
        "subscriber_id",
        "subscriber_emails",
        "subscriber_ids",
        "subscriber_mode",
        "template_id",
        "from_email",
        "subject",
        "data",
        "headers",
        "messenger",
        "content_type",
        "altbody",
    )

    def __init__(
            self,
            *,
            subscriber_email: str | None = None,
            subscriber_id: int | None = None,
            subscriber_emails: list[str] | None = None,
            subscriber_ids: list[int] | None = None,
            subscriber_mode: TransactionalSubscriberMode | None = None,
            template_id: int | None = None,
            from_email: str | None = None,
            subject: str | None = None,
            data: dict[str, Any] | None = None,
            headers: list[dict[str, str]] | dict[str, str] | None = None,
            messenger: str | None = None,
            content_type: TransactionalContentType | None = None,
            altbody: str | None = None,
            attachments: list[MultipartValue] | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            subscriber_email=subscriber_email,
            subscriber_id=subscriber_id,
            subscriber_emails=subscriber_emails,
            subscriber_ids=subscriber_ids,
            subscriber_mode=subscriber_mode,
            template_id=template_id,
            from_email=from_email,
            subject=subject,
            data=data,
            headers=headers,
            messenger=messenger,
            content_type=content_type,
            altbody=altbody,
            attachments=attachments,
        )

    subscriber_email = RequestField[str](value_type=str)
    subscriber_id = RequestField[int](value_type=int)
    subscriber_emails = RequestField[list[str]](value_type=list, validator=list_of(str))
    subscriber_ids = RequestField[list[int]](value_type=list, validator=list_of(int))
    subscriber_mode = RequestField[TransactionalSubscriberMode](value_type=TransactionalSubscriberMode)
    template_id = RequestField[int](value_type=int)
    from_email = RequestField[str](value_type=str)
    subject = RequestField[str](value_type=str)
    data = RequestField[dict[str, Any]](value_type=dict)
    headers = RequestField[list[dict[str, str]] | dict[str, str]](value_type=(list, dict))
    messenger = RequestField[str](value_type=str)
    content_type = RequestField[TransactionalContentType](value_type=TransactionalContentType)
    altbody = RequestField[str](value_type=str)
    attachments = RequestField[list[MultipartValue]](
        value_type=list,
        validator=list_of(MultipartValue),
    )

    def to_subscriber_email(self, email: str) -> Self:
        """Send to one subscriber email address."""
        self.subscriber_email = email
        return self

    def to_subscriber_id(self, subscriber_id: int) -> Self:
        """Send to one subscriber identifier."""
        self.subscriber_id = subscriber_id
        return self

    def add_subscriber_email(self, email: str) -> Self:
        """Add a subscriber email address recipient."""
        self.subscriber_emails = [*(self.subscriber_emails or []), email]
        return self

    def add_subscriber_id(self, subscriber_id: int) -> Self:
        """Add a subscriber identifier recipient."""
        self.subscriber_ids = [*(self.subscriber_ids or []), subscriber_id]
        return self

    def with_subscriber_mode(self, mode: TransactionalSubscriberMode) -> Self:
        """Set the subscriber lookup mode."""
        self.subscriber_mode = mode
        return self

    def with_template(self, template_id: int) -> Self:
        """Set the template identifier."""
        self.template_id = template_id
        return self

    def with_from_email(self, from_email: str) -> Self:
        """Set the sender email address."""
        self.from_email = from_email
        return self

    def with_subject(self, subject: str) -> Self:
        """Set the message subject."""
        self.subject = subject
        return self

    def with_data(self, name: str, value: Any) -> Self:
        """Add template data by name."""
        self.data = {**(self.data or {}), name: value}
        return self

    def with_headers(self, headers: list[dict[str, str]] | dict[str, str]) -> Self:
        """Set custom message headers."""
        self.headers = headers
        return self

    def with_messenger(self, messenger: str) -> Self:
        """Set the messenger name."""
        self.messenger = messenger
        return self

    def with_content_type(self, content_type: TransactionalContentType) -> Self:
        """Set the message content type."""
        self.content_type = content_type
        return self

    def with_alt_body(self, body: str) -> Self:
        """Set the alternate body text."""
        self.altbody = body
        return self

    def add_attachment(
            self,
            data: bytes,
            *,
            filename: str,
            content_type: str | None = None,
    ) -> Self:
        """Add an attachment from bytes."""
        attachment = MultipartValue(
            data,
            filename=filename,
            content_type=content_type,
        )
        self.attachments = [*(self.attachments or []), attachment]
        return self

    def add_attachment_file(
            self,
            path: str | Path,
            *,
            content_type: str | None = None,
    ) -> Self:
        """Add an attachment from a local file."""
        file_path = Path(path)
        return self.add_attachment(
            file_path.read_bytes(),
            filename=file_path.name,
            content_type=content_type,
        )

    def _to_request_options(self) -> HTTPRequestOptions:
        payload = self.to_mapping(fields=self._payload_fields)
        attachments = self.attachments or []
        if not attachments:
            return HTTPRequestOptions(body=JSONBody(payload))
        body = MultipartBuilder().json("data", payload)
        for attachment in attachments:
            body.file("file", attachment)
        return HTTPRequestOptions(body=body.to_body())
