from __future__ import annotations

from typing import Any

from klarient import (
    Page,
    PageNumberState,
    PageableResource,
    ResourcePath,
    SyncResource,
)
from klarient.http.client import _SyncClientImpl
from listmonk.campaigns.models import Campaign
from listmonk.campaigns.requests import (
    CampaignAnalyticsQuery,
    CampaignAnalyticsType,
    CampaignArchiveUpdate,
    CampaignCreate,
    CampaignDeleteQuery,
    CampaignQuery,
    CampaignRetrieveQuery,
    CampaignRunningStatsQuery,
    CampaignStatusUpdate,
    CampaignTest,
    CampaignUpdate,
)
from listmonk.campaigns.responses import (
    CampaignAnalyticsResponse,
    CampaignPreview,
    CampaignResponse,
    CampaignRunningStatsResponse,
)
from listmonk.common import BooleanResponse, ListmonkPagePagination


class CampaignPreviewResource(SyncResource[_SyncClientImpl]):
    """Preview endpoint for one campaign."""

    def retrieve(self) -> CampaignPreview:
        """Retrieve the rendered campaign preview."""
        return self._executor.get(CampaignPreview)


class CampaignStatusResource(SyncResource[_SyncClientImpl]):
    """Status endpoint for one campaign."""

    def update(self, options: CampaignStatusUpdate) -> CampaignResponse:
        """Update this campaign's status."""
        return self._executor.put(CampaignResponse, options)


class CampaignArchiveResource(SyncResource[_SyncClientImpl]):
    """Archive settings endpoint for one campaign."""

    def update(self, options: CampaignArchiveUpdate) -> CampaignResponse:
        """Update this campaign's archive settings."""
        return self._executor.put(CampaignResponse, options)


class CampaignTestResource(SyncResource[_SyncClientImpl]):
    """Test send endpoint for one campaign."""

    def send(self, options: CampaignTest) -> BooleanResponse:
        """Send a test message for this campaign."""
        return self._executor.post(BooleanResponse, options)


class CampaignResource(SyncResource[_SyncClientImpl]):
    """Resource for one campaign."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__preview = CampaignPreviewResource(self, segment="preview")
        self.__status = CampaignStatusResource(self, segment="status")
        self.__archive = CampaignArchiveResource(self, segment="archive")
        self.__test = CampaignTestResource(self, segment="test")

    @property
    def preview(self) -> CampaignPreviewResource:
        """Preview resource below this campaign."""
        return self.__preview

    @property
    def status(self) -> CampaignStatusResource:
        """Status resource below this campaign."""
        return self.__status

    @property
    def archive(self) -> CampaignArchiveResource:
        """Archive resource below this campaign."""
        return self.__archive

    @property
    def test(self) -> CampaignTestResource:
        """Test send resource below this campaign."""
        return self.__test

    def retrieve(
            self,
            options: CampaignRetrieveQuery | None = None,
    ) -> CampaignResponse:
        """Retrieve this campaign."""
        return self._executor.get(CampaignResponse, options)

    def update(self, options: CampaignUpdate) -> CampaignResponse:
        """Update this campaign."""
        return self._executor.put(CampaignResponse, options)

    def delete(self) -> BooleanResponse:
        """Delete this campaign."""
        return self._executor.delete(BooleanResponse)


class CampaignRunningStatsResource(SyncResource[_SyncClientImpl]):
    """Running campaign stats endpoint."""

    def retrieve(
            self,
            options: CampaignRunningStatsQuery,
    ) -> CampaignRunningStatsResponse:
        """Retrieve running campaign stats."""
        return self._executor.get(CampaignRunningStatsResponse, options)


class CampaignRunningResource(SyncResource[_SyncClientImpl]):
    """Running campaigns API grouping."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__stats = CampaignRunningStatsResource(self, segment="stats")

    @property
    def stats(self) -> CampaignRunningStatsResource:
        """Running campaign stats resource."""
        return self.__stats


class CampaignAnalyticsTypeResource(SyncResource[_SyncClientImpl]):
    """Analytics endpoint for one analytics type."""

    def retrieve(
            self,
            options: CampaignAnalyticsQuery,
    ) -> CampaignAnalyticsResponse:
        """Retrieve analytics points for this analytics type."""
        return self._executor.get(CampaignAnalyticsResponse, options)


class CampaignAnalyticsResource(SyncResource[_SyncClientImpl]):
    """Campaign analytics API grouping."""

    def __getitem__(
            self,
            analytics_type: CampaignAnalyticsType | str,
    ) -> CampaignAnalyticsTypeResource:
        return CampaignAnalyticsTypeResource(
            self,
            segment=ResourcePath.segment(analytics_type),
        )


class CampaignsResource(PageableResource[_SyncClientImpl, Campaign, PageNumberState]):
    """Paged campaigns collection resource."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=Campaign,
            pagination=ListmonkPagePagination(),
            **kwargs,
        )
        self.__running = CampaignRunningResource(self, segment="running")
        self.__analytics = CampaignAnalyticsResource(self, segment="analytics")

    def __getitem__(self, campaign_id: int | str) -> CampaignResource:
        return CampaignResource(self, segment=ResourcePath.segment(campaign_id))

    @property
    def running(self) -> CampaignRunningResource:
        """Running campaigns resource."""
        return self.__running

    @property
    def analytics(self) -> CampaignAnalyticsResource:
        """Campaign analytics resource."""
        return self.__analytics

    def retrieve(
            self,
            options: CampaignQuery | None = None,
    ) -> Page[Campaign]:
        """Retrieve campaigns with optional query parameters."""
        return self._retrieve_page(options=options)

    def create(self, options: CampaignCreate) -> CampaignResponse:
        """Create a campaign."""
        return self._executor.post(CampaignResponse, options)

    def delete(
            self,
            options: CampaignDeleteQuery,
    ) -> BooleanResponse:
        """Delete campaigns in bulk."""
        return self._executor.delete(BooleanResponse, options)
