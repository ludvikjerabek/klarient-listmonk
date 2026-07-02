from __future__ import annotations

from klarient.http.client import _SyncClientImpl

from klarient import SyncResource
from listmonk.common import BooleanResponse
from listmonk.transactional.requests import TransactionalMessage


class TransactionalResource(SyncResource[_SyncClientImpl]):
    """Transactional message endpoint."""

    def send(self, options: TransactionalMessage) -> BooleanResponse:
        """Send a transactional message."""
        return self._executor.post(BooleanResponse, options)
