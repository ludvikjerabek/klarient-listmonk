from __future__ import annotations

from typing import Self

from klarient import RequestField, FormBodyRequest, JSONBodyRequest, list_of


class PublicSubscription(JSONBodyRequest):
    """JSON body for public subscription requests."""

    def __init__(
            self,
            *,
            email: str | None = None,
            name: str | None = None,
            list_uuids: list[str] | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            email=email,
            name=name,
            list_uuids=list_uuids,
        )

    email = RequestField[str](value_type=str)
    name = RequestField[str](value_type=str)
    list_uuids = RequestField[list[str]](value_type=list, validator=list_of(str))

    def with_email(self, email: str) -> Self:
        """Set the subscriber email address."""
        self.email = email
        return self

    def with_name(self, name: str) -> Self:
        """Set the subscriber display name."""
        self.name = name
        return self

    def add_list_uuid(self, list_uuid: str) -> Self:
        """Add a public list UUID."""
        self.list_uuids = [*(self.list_uuids or []), list_uuid]
        return self


class PublicSubscriptionForm(FormBodyRequest):
    """Form body for public subscription requests."""

    def __init__(
            self,
            *,
            email: str | None = None,
            name: str | None = None,
            list_uuids: list[str] | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            email=email,
            name=name,
            list_uuids=list_uuids,
        )

    email = RequestField[str](value_type=str)
    name = RequestField[str](value_type=str)
    list_uuids = RequestField[list[str]](
        name="l",
        value_type=list,
        validator=list_of(str),
    )

    def with_email(self, email: str) -> Self:
        """Set the subscriber email address."""
        self.email = email
        return self

    def with_name(self, name: str) -> Self:
        """Set the subscriber display name."""
        self.name = name
        return self

    def add_list_uuid(self, list_uuid: str) -> Self:
        """Add a public list UUID."""
        self.list_uuids = [*(self.list_uuids or []), list_uuid]
        return self
