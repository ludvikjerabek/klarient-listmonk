from enum import StrEnum


class BounceType(StrEnum):
    """Bounce type values used by listmonk."""

    HARD = "hard"
    SOFT = "soft"


class SubscriberStatus(StrEnum):
    """Subscriber status values."""

    ENABLED = "enabled"
    DISABLED = "disabled"
    BLOCKLISTED = "blocklisted"


class CreateSubscriberStatus(StrEnum):
    """Subscriber status values accepted during subscriber creation."""

    ENABLED = "enabled"
    BLOCKLISTED = "blocklisted"


class SubscriptionStatus(StrEnum):
    """List subscription status values."""

    CONFIRMED = "confirmed"
    UNCONFIRMED = "unconfirmed"
    UNSUBSCRIBED = "unsubscribed"


class ListType(StrEnum):
    """List visibility type values."""

    PUBLIC = "public"
    PRIVATE = "private"


class ListOptin(StrEnum):
    """List opt-in mode values."""

    SINGLE = "single"
    DOUBLE = "double"


class ListStatus(StrEnum):
    """List status values."""

    ACTIVE = "active"
    ARCHIVED = "archived"


class SortOrder(StrEnum):
    """Sort order values accepted by listmonk."""

    ASC = "ASC"
    DESC = "DESC"


class PerPage(StrEnum):
    """Special per_page values accepted by listmonk."""

    ALL = "all"
