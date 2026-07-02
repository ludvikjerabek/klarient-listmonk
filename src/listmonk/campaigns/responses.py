from __future__ import annotations

from collections.abc import Mapping
from typing import ClassVar

from klarient import (
    ResponseBase,
    ResponseDecoder,
    ResponseMap,
    TextDecoder,
)
from listmonk.campaigns.models import (
    Campaign,
    CampaignAnalyticsPoint,
    CampaignRunningStat,
)


class CampaignResponse(ResponseMap):
    """Response wrapper for one campaign."""

    @property
    def data(self) -> Campaign:
        """Campaign returned by the endpoint."""
        data = self.get("data", {})
        return Campaign(data if isinstance(data, Mapping) else {})


class CampaignPreview(ResponseBase):
    """Text response wrapper for campaign preview HTML."""

    _default_decoder: ClassVar[ResponseDecoder[str] | None] = TextDecoder()

    def __init__(self, data: str = "", *, response=None) -> None:
        super().__init__(data, response=response)
        self.__data = data

    @property
    def data(self) -> str:
        """Rendered preview text."""
        return self.__data

    def __str__(self) -> str:
        return self.__data


class CampaignRunningStatsResponse(ResponseMap):
    """Response wrapper for running campaign stats."""

    @property
    def data(self) -> list[CampaignRunningStat]:
        """Running campaign stats returned by the endpoint."""
        return [
            CampaignRunningStat(item)
            for item in self.get("data", [])
            if isinstance(item, Mapping)
        ]


class CampaignAnalyticsResponse(ResponseMap):
    """Response wrapper for campaign analytics data."""

    @property
    def data(self) -> list[CampaignAnalyticsPoint]:
        """Analytics points returned by the endpoint."""
        return [
            CampaignAnalyticsPoint(item)
            for item in self.get("data", [])
            if isinstance(item, Mapping)
        ]
