from __future__ import annotations

from enum import StrEnum
from typing import Any, Self

from klarient import (
    JSONBodyRequest,
    PageNumberState,
    QueryFieldSpec,
    QueryRequest,
    QuerySerialization,
    RequestField,
    list_of,
)
from listmonk.common import PerPage, SortOrder
from listmonk.common.paging import _listmonk_page_state


class CampaignAnalyticsType(StrEnum):
    """Campaign analytics data types."""

    VIEWS = "views"
    LINKS = "links"
    CLICKS = "clicks"
    BOUNCES = "bounces"


class CampaignContentType(StrEnum):
    """Campaign content type values."""

    RICHTEXT = "richtext"
    HTML = "html"
    MARKDOWN = "markdown"
    PLAIN = "plain"
    VISUAL = "visual"


class CampaignOrderBy(StrEnum):
    """Fields accepted by campaign ordering."""

    NAME = "name"
    STATUS = "status"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class CampaignStatus(StrEnum):
    """Campaign status values."""

    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    FINISHED = "finished"


class CampaignType(StrEnum):
    """Campaign type values."""

    REGULAR = "regular"
    OPTIN = "optin"


class CampaignQuery(QueryRequest):
    """Query parameters for listing campaigns."""

    def __init__(
            self,
            *,
            order: SortOrder | None = None,
            order_by: CampaignOrderBy | None = None,
            query: str | None = None,
            status: list[CampaignStatus] | None = None,
            tags: list[str] | None = None,
            page: int | None = None,
            per_page: int | PerPage | None = None,
            no_body: bool | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            order=order,
            order_by=order_by,
            query=query,
            status=status,
            tags=tags,
            page=page,
            per_page=per_page,
            no_body=no_body,
        )

    order = RequestField[SortOrder](value_type=SortOrder)
    order_by = RequestField[CampaignOrderBy](value_type=CampaignOrderBy)
    query = RequestField[str](value_type=str)
    status = RequestField[list[CampaignStatus]](
        query=QueryFieldSpec(serialization=QuerySerialization.REPEAT),
        value_type=list,
        validator=list_of(CampaignStatus),
    )
    tags = RequestField[list[str]](
        name="tag",
        query=QueryFieldSpec(serialization=QuerySerialization.REPEAT),
        value_type=list,
        validator=list_of(str),
    )
    page = RequestField[int](value_type=int)
    per_page = RequestField[int | PerPage](value_type=(int, PerPage))
    no_body = RequestField[bool](value_type=bool)

    def with_order(self, order: SortOrder) -> Self:
        """Set the sort order."""
        self.order = order
        return self

    def with_order_by(self, field: CampaignOrderBy) -> Self:
        """Set the ordering field."""
        self.order_by = field
        return self

    def with_query(self, query: str) -> Self:
        """Set the campaign search query."""
        self.query = query
        return self

    def add_status(self, status: CampaignStatus) -> Self:
        """Add a campaign status filter."""
        self.status = [*(self.status or []), status]
        return self

    def add_tag(self, tag: str) -> Self:
        """Add a repeated tag filter."""
        self.tags = [*(self.tags or []), tag]
        return self

    def with_page(self, page: int) -> Self:
        """Set the requested page number."""
        self.page = page
        return self

    def with_per_page(self, per_page: int | PerPage) -> Self:
        """Set the requested page size."""
        self.per_page = per_page
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return _listmonk_page_state(self.page, self.per_page, default)

    def without_body(self, enabled: bool = True) -> Self:
        """Request campaign data without body fields."""
        self.no_body = enabled
        return self


class CampaignRetrieveQuery(QueryRequest):
    """Query parameters for retrieving one campaign."""

    def __init__(self, *, no_body: bool | None = None) -> None:
        super().__init__()
        self._set_defined_fields(no_body=no_body)

    no_body = RequestField[bool](value_type=bool)

    def without_body(self, enabled: bool = True) -> Self:
        """Request campaign data without body fields."""
        self.no_body = enabled
        return self


class CampaignCreate(JSONBodyRequest):
    """JSON body for creating a campaign."""

    def __init__(
            self,
            *,
            name: str | None = None,
            subject: str | None = None,
            lists: list[int] | None = None,
            from_email: str | None = None,
            type: CampaignType | None = None,
            content_type: CampaignContentType | None = None,
            body: str | None = None,
            body_source: str | None = None,
            altbody: str | None = None,
            send_at: str | None = None,
            messenger: str | None = None,
            template_id: int | None = None,
            tags: list[str] | None = None,
            headers: list[dict[str, str]] | dict[str, str] | None = None,
            attribs: dict[str, Any] | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            name=name,
            subject=subject,
            lists=lists,
            from_email=from_email,
            type=type,
            content_type=content_type,
            body=body,
            body_source=body_source,
            altbody=altbody,
            send_at=send_at,
            messenger=messenger,
            template_id=template_id,
            tags=tags,
            headers=headers,
            attribs=attribs,
        )

    name = RequestField[str](value_type=str)
    subject = RequestField[str](value_type=str)
    lists = RequestField[list[int]](value_type=list, validator=list_of(int))
    from_email = RequestField[str](value_type=str)
    type = RequestField[CampaignType](value_type=CampaignType)
    content_type = RequestField[CampaignContentType](value_type=CampaignContentType)
    body = RequestField[str](value_type=str)
    body_source = RequestField[str](value_type=str)
    altbody = RequestField[str](value_type=str)
    send_at = RequestField[str](value_type=str)
    messenger = RequestField[str](value_type=str)
    template_id = RequestField[int](value_type=int)
    tags = RequestField[list[str]](value_type=list, validator=list_of(str))
    headers = RequestField[list[dict[str, str]] | dict[str, str]](value_type=(list, dict))
    attribs = RequestField[dict[str, Any]](value_type=dict)

    def with_name(self, name: str) -> Self:
        """Set the campaign name."""
        self.name = name
        return self

    def with_subject(self, subject: str) -> Self:
        """Set the campaign subject."""
        self.subject = subject
        return self

    def add_list(self, list_id: int) -> Self:
        """Add a target list identifier."""
        self.lists = [*(self.lists or []), list_id]
        return self

    def with_from_email(self, from_email: str) -> Self:
        """Set the sender email address."""
        self.from_email = from_email
        return self

    def with_type(self, type: CampaignType) -> Self:
        """Set the campaign type."""
        self.type = type
        return self

    def with_content_type(self, content_type: CampaignContentType) -> Self:
        """Set the campaign content type."""
        self.content_type = content_type
        return self

    def with_body(self, body: str, *, source: str | None = None) -> Self:
        """Set the campaign body and optional source body."""
        self.body = body
        if source is not None:
            self.body_source = source
        return self

    def with_alt_body(self, body: str) -> Self:
        """Set the alternate body."""
        self.altbody = body
        return self

    def with_send_at(self, send_at: str) -> Self:
        """Set the scheduled send timestamp."""
        self.send_at = send_at
        return self

    def with_messenger(self, messenger: str) -> Self:
        """Set the messenger name."""
        self.messenger = messenger
        return self

    def with_template(self, template_id: int) -> Self:
        """Set the template identifier."""
        self.template_id = template_id
        return self

    def add_tag(self, tag: str) -> Self:
        """Add a campaign tag."""
        self.tags = [*(self.tags or []), tag]
        return self

    def with_headers(self, headers: list[dict[str, str]] | dict[str, str]) -> Self:
        """Set custom campaign headers."""
        self.headers = headers
        return self

    def with_attrib(self, name: str, value: Any) -> Self:
        """Set a campaign attribute value."""
        self.attribs = {**(self.attribs or {}), name: value}
        return self


class CampaignUpdate(CampaignCreate):
    """JSON body for updating a campaign."""

    pass


class CampaignTest(CampaignCreate):
    """JSON body for sending a campaign test message."""

    def __init__(
            self,
            *,
            subscribers: list[str] | None = None,
            **fields: Any,
    ) -> None:
        super().__init__(**fields)
        self._set_defined_fields(subscribers=subscribers)

    subscribers = RequestField[list[str]](value_type=list, validator=list_of(str))

    def add_subscriber(self, email: str) -> Self:
        """Add a test subscriber email address."""
        self.subscribers = [*(self.subscribers or []), email]
        return self


class CampaignStatusUpdate(JSONBodyRequest):
    """JSON body for updating a campaign status."""

    def __init__(self, *, status: CampaignStatus | None = None) -> None:
        super().__init__()
        self._set_defined_fields(status=status)

    status = RequestField[CampaignStatus](value_type=CampaignStatus)

    def with_status(self, status: CampaignStatus) -> Self:
        """Set the campaign status."""
        self.status = status
        return self


class CampaignArchiveUpdate(JSONBodyRequest):
    """JSON body for updating campaign archive settings."""

    def __init__(
            self,
            *,
            archive: bool | None = None,
            archive_template_id: int | None = None,
            archive_meta: str | None = None,
            archive_slug: str | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            archive=archive,
            archive_template_id=archive_template_id,
            archive_meta=archive_meta,
            archive_slug=archive_slug,
        )

    archive = RequestField[bool](value_type=bool)
    archive_template_id = RequestField[int](value_type=int)
    archive_meta = RequestField[str](value_type=str)
    archive_slug = RequestField[str](value_type=str)

    def with_archive(self, enabled: bool = True) -> Self:
        """Set whether archive publishing is enabled."""
        self.archive = enabled
        return self

    def with_template(self, template_id: int) -> Self:
        """Set the archive template identifier."""
        self.archive_template_id = template_id
        return self

    def with_meta(self, meta: str) -> Self:
        """Set archive metadata."""
        self.archive_meta = meta
        return self

    def with_slug(self, slug: str) -> Self:
        """Set archive slug."""
        self.archive_slug = slug
        return self


class CampaignDeleteQuery(QueryRequest):
    """Query parameters for deleting campaigns in bulk."""

    def __init__(
            self,
            *,
            ids: list[int] | None = None,
            query: str | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(ids=ids, query=query)

    ids = RequestField[list[int]](
        name="id",
        query=QueryFieldSpec(serialization=QuerySerialization.REPEAT),
        value_type=list,
        validator=list_of(int),
    )
    query = RequestField[str](value_type=str)

    def add_id(self, campaign_id: int) -> Self:
        """Add a campaign identifier to delete."""
        self.ids = [*(self.ids or []), campaign_id]
        return self

    def with_query(self, query: str) -> Self:
        """Delete campaigns matching the search query."""
        self.query = query
        return self


class CampaignRunningStatsQuery(QueryRequest):
    """Query parameters for running campaign stats."""

    def __init__(self, *, campaign_ids: list[int] | None = None) -> None:
        super().__init__()
        self._set_defined_fields(campaign_ids=campaign_ids)

    campaign_ids = RequestField[list[int]](
        name="campaign_id",
        query=QueryFieldSpec(serialization=QuerySerialization.REPEAT),
        value_type=list,
        validator=list_of(int),
    )

    def add_campaign(self, campaign_id: int) -> Self:
        """Add a campaign identifier."""
        self.campaign_ids = [*(self.campaign_ids or []), campaign_id]
        return self


class CampaignAnalyticsQuery(QueryRequest):
    """Query parameters for campaign analytics."""

    def __init__(
            self,
            *,
            ids: list[int] | None = None,
            from_: str | None = None,
            to: str | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(ids=ids, from_=from_, to=to)

    ids = RequestField[list[int]](
        name="id",
        query=QueryFieldSpec(serialization=QuerySerialization.REPEAT),
        value_type=list,
        validator=list_of(int),
    )
    from_ = RequestField[str](name="from", value_type=str)
    to = RequestField[str](value_type=str)

    def add_campaign(self, campaign_id: int) -> Self:
        """Add a campaign identifier."""
        self.ids = [*(self.ids or []), campaign_id]
        return self

    def from_date(self, value: str) -> Self:
        """Set the analytics start date."""
        self.from_ = value
        return self

    def to_date(self, value: str) -> Self:
        """Set the analytics end date."""
        self.to = value
        return self
