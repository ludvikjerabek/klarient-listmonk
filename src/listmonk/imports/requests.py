from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from klarient import (
    RequestField,
    RequestFields,
    HTTPRequestOptions,
    MultipartBuilder,
    MultipartValue,
    RequestOptionsProvider,
    list_of,
)
from listmonk.common import SubscriptionStatus


class ImportMode(StrEnum):
    """Subscriber import modes."""

    SUBSCRIBE = "subscribe"
    BLOCKLIST = "blocklist"


class SubscriberImportParams(RequestFields):
    """JSON params part for subscriber import uploads."""

    def __init__(
            self,
            *,
            mode: ImportMode | None = None,
            delim: str | None = None,
            lists: list[int] | None = None,
            overwrite: bool | None = None,
            subscription_status: SubscriptionStatus | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            mode=mode,
            delim=delim,
            lists=lists,
            overwrite=overwrite,
            subscription_status=subscription_status,
        )

    mode = RequestField[ImportMode](value_type=ImportMode)
    delim = RequestField[str](value_type=str)
    lists = RequestField[list[int]](value_type=list, validator=list_of(int))
    overwrite = RequestField[bool](value_type=bool)
    subscription_status = RequestField[SubscriptionStatus](value_type=SubscriptionStatus)

    def with_mode(self, mode: ImportMode) -> Self:
        """Set the import mode."""
        self.mode = mode
        return self

    def with_delimiter(self, delimiter: str) -> Self:
        """Set the CSV delimiter."""
        self.delim = delimiter
        return self

    def add_list(self, list_id: int) -> Self:
        """Add a target list identifier."""
        self.lists = [*(self.lists or []), list_id]
        return self

    def with_overwrite(self, enabled: bool = True) -> Self:
        """Set whether existing subscribers should be overwritten."""
        self.overwrite = enabled
        return self

    def with_subscription_status(self, status: SubscriptionStatus) -> Self:
        """Set the subscription status for imported subscribers."""
        self.subscription_status = status
        return self


class SubscriberImport(RequestFields, RequestOptionsProvider):
    """Multipart subscriber import request."""

    def __init__(
            self,
            *,
            params: SubscriberImportParams | None = None,
            file: bytes | MultipartValue | None = None,
            filename: str = "subscribers.csv",
            content_type: str = "text/csv",
    ) -> None:
        super().__init__()
        self._set_defined_fields(params=params)
        if file is not None:
            self.file = (
                MultipartValue(file, filename=filename, content_type=content_type)
                if isinstance(file, bytes)
                else file
            )

    params = RequestField[SubscriberImportParams](value_type=SubscriberImportParams)
    file = RequestField[MultipartValue](value_type=MultipartValue)

    @classmethod
    def from_file(
            cls,
            path: str | Path,
            *,
            params: SubscriberImportParams,
            content_type: str = "text/csv",
    ) -> SubscriberImport:
        file_path = Path(path)
        return cls(
            params=params,
            file=file_path.read_bytes(),
            filename=file_path.name,
            content_type=content_type,
        )

    def with_params(self, params: SubscriberImportParams) -> Self:
        """Set the import params part."""
        self.params = params
        return self

    def with_file(
            self,
            data: bytes,
            *,
            filename: str = "subscribers.csv",
            content_type: str = "text/csv",
    ) -> Self:
        """Set the CSV file part from bytes."""
        self.file = MultipartValue(
            data,
            filename=filename,
            content_type=content_type,
        )
        return self

    def _to_request_options(self) -> HTTPRequestOptions:
        if self.params is None:
            raise ValueError("params are required")
        if self.file is None:
            raise ValueError("file is required")
        body = (
            MultipartBuilder()
            .json("params", self.params.to_mapping())
            .file("file", self.file)
            .to_body()
        )
        return HTTPRequestOptions(body=body)
