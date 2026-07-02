from __future__ import annotations

from typing import Any

from klarient.http.client import _SyncClientImpl

from klarient import (
    SyncResource,
)
from listmonk.imports.requests import SubscriberImport
from listmonk.imports.responses import (
    ImportLogsResponse,
    ImportStatusResponse,
    ImportUploadResponse,
)


class ImportSubscriberLogsResource(SyncResource[_SyncClientImpl]):
    """Subscriber import logs endpoint."""

    def retrieve(self) -> ImportLogsResponse:
        """Retrieve subscriber import logs."""
        return self._executor.get(ImportLogsResponse)


class ImportSubscribersResource(SyncResource[_SyncClientImpl]):
    """Subscriber import endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__logs = ImportSubscriberLogsResource(self, segment="logs")

    @property
    def logs(self) -> ImportSubscriberLogsResource:
        """Logs resource below subscriber imports."""
        return self.__logs

    def retrieve(self) -> ImportStatusResponse:
        """Retrieve subscriber import status."""
        return self._executor.get(ImportStatusResponse)

    def upload(self, options: SubscriberImport) -> ImportUploadResponse:
        """Upload subscribers for import."""
        return self._executor.post(ImportUploadResponse, options)

    def delete(self) -> ImportStatusResponse:
        """Stop and clear the current subscriber import."""
        return self._executor.delete(ImportStatusResponse)


class ImportResource(SyncResource[_SyncClientImpl]):
    """Import API root."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__subscribers = ImportSubscribersResource(self, segment="subscribers")

    @property
    def subscribers(self) -> ImportSubscribersResource:
        """Subscriber import resource."""
        return self.__subscribers
