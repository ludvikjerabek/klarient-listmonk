from __future__ import annotations

from collections.abc import Mapping
from typing import ClassVar

from klarient import (
    ResponseBase,
    ResponseDecoder,
    ResponseMap,
    TextDecoder,
)
from listmonk.templates.models import Template


class TemplatesResponse(ResponseMap):
    """Response wrapper for template collections."""

    @property
    def data(self) -> list[Template]:
        """Templates returned by the endpoint."""
        return [Template(item) for item in self.get("data", []) if isinstance(item, Mapping)]


class TemplateResponse(ResponseMap):
    """Response wrapper for one template."""

    @property
    def data(self) -> Template:
        """Template returned by the endpoint."""
        data = self["data"]
        if isinstance(data, list):
            data = data[0] if data else {}
        if not isinstance(data, Mapping):
            data = {}
        return Template(data)


class TemplatePreview(ResponseBase):
    """Text response wrapper for template preview HTML."""

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
