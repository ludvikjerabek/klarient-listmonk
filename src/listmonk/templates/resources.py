from __future__ import annotations

from typing import Any

from klarient.http.client import _SyncClientImpl

from klarient import ResourcePath, SyncResource
from listmonk.common import BooleanResponse
from listmonk.templates.requests import (
    TemplateCreate,
    TemplatePreviewRender,
    TemplateUpdate,
)
from listmonk.templates.responses import (
    TemplatePreview,
    TemplateResponse,
    TemplatesResponse,
)


class TemplatePreviewResource(SyncResource[_SyncClientImpl]):
    """Preview endpoint for one template."""

    def retrieve(self) -> TemplatePreview:
        """Retrieve the rendered preview for this template."""
        return self._executor.get(TemplatePreview)


class TemplateDefaultResource(SyncResource[_SyncClientImpl]):
    """Default endpoint for one template."""

    def update(self) -> TemplateResponse:
        """Set this template as the default for its type."""
        return self._executor.put(TemplateResponse)


class TemplateResource(SyncResource[_SyncClientImpl]):
    """Resource for one template."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__preview = TemplatePreviewResource(self, segment="preview")
        self.__default = TemplateDefaultResource(self, segment="default")

    @property
    def preview(self) -> TemplatePreviewResource:
        """Preview resource below this template."""
        return self.__preview

    @property
    def default(self) -> TemplateDefaultResource:
        """Default resource below this template."""
        return self.__default

    def retrieve(self) -> TemplateResponse:
        """Retrieve this template."""
        return self._executor.get(TemplateResponse)

    def update(self, options: TemplateUpdate) -> TemplateResponse:
        """Update this template."""
        return self._executor.put(TemplateResponse, options)

    def delete(self) -> BooleanResponse:
        """Delete this template."""
        return self._executor.delete(BooleanResponse)


class TemplateRenderPreviewResource(SyncResource[_SyncClientImpl]):
    """Standalone template preview rendering endpoint."""

    def render(self, options: TemplatePreviewRender) -> TemplatePreview:
        """Render a preview from request data."""
        return self._executor.post(TemplatePreview, options)


class TemplatesResource(SyncResource[_SyncClientImpl]):
    """Templates API root."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__preview = TemplateRenderPreviewResource(self, segment="preview")

    def __getitem__(self, template_id: int | str) -> TemplateResource:
        return TemplateResource(self, segment=ResourcePath.segment(template_id))

    @property
    def preview(self) -> TemplateRenderPreviewResource:
        """Standalone preview renderer resource."""
        return self.__preview

    def retrieve(self) -> TemplatesResponse:
        """Retrieve templates."""
        return self._executor.get(TemplatesResponse)

    def create(self, options: TemplateCreate) -> TemplateResponse:
        """Create a template."""
        return self._executor.post(TemplateResponse, options)
