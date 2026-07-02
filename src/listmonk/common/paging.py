from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Any
from urllib.parse import urlencode

from klarient import (
    DecodedResponsePaginationStrategy,
    PageInfo,
    PageParseContext,
    PageNumberRequest,
    PageNumberState,
    RequestOptionsProvider,
)
from listmonk.common.enums import PerPage


def _listmonk_page_state(
        page: int | None,
        per_page: int | PerPage | None,
        default: PageNumberState,
) -> PageNumberState:
    """Return a page-number state for listmonk query objects."""
    page_size = per_page if isinstance(per_page, int) else default.page_size
    return PageNumberState(
        page_number=page if page is not None else default.page_number,
        page_size=page_size,
    )


@dataclass(frozen=True, slots=True)
class ListmonkPagePagination(DecodedResponsePaginationStrategy[PageNumberState, Any]):
    """Pagination for listmonk responses shaped as data.results/page/per_page/total."""

    page_size: int = 20
    path: str = ""

    def bind(self, resource_path: str) -> ListmonkPagePagination:
        if self.path:
            return self
        return replace(self, path=resource_path)

    def initial_state(self, resource: object) -> PageNumberState:
        return PageNumberState(page_number=1, page_size=self.page_size)

    def request(self, state: PageNumberState) -> RequestOptionsProvider:
        return PageNumberRequest(state, "page", "per_page")

    def _extract_items(
            self,
            context: PageParseContext[PageNumberState, Any],
    ) -> tuple[Mapping[str, Any], ...]:
        data = context.reader.mapping("data")
        raw_items = data.get("results", [])
        return tuple(item for item in raw_items if isinstance(item, Mapping))

    def _build_page_info(
            self,
            context: PageParseContext[PageNumberState, Any],
            items: tuple[Any, ...],
    ) -> PageInfo:
        data = context.reader.mapping("data")
        page_number = context.reader.integer(data.get("page"), context.state.page_number)
        per_page = context.reader.integer(data.get("per_page"), context.state.page_size)
        total = context.reader.integer(data.get("total"))
        total_pages = max(1, (total + per_page - 1) // per_page) if per_page else None
        has_next = total_pages is not None and page_number < total_pages
        return PageInfo(
            number=page_number,
            size=len(items),
            total_pages=total_pages,
            total_items=total,
            self_link=self._link(page_number, per_page) or context.response.url,
            first_link=self._link(1, per_page),
            next_link=self._link(page_number + 1, per_page) if has_next else "",
            last_link="" if total_pages is None else self._link(total_pages, per_page),
        )

    def _next_state(
            self,
            context: PageParseContext[PageNumberState, Any],
            info: PageInfo,
    ) -> PageNumberState | None:
        if info.total_pages is None or info.number >= info.total_pages:
            return None
        data = context.reader.mapping("data")
        per_page = context.reader.integer(data.get("per_page"), context.state.page_size)
        return PageNumberState(info.number + 1, per_page)

    def _link(self, page_number: int, page_size: int) -> str:
        if not self.path or page_number <= 0 or page_size <= 0:
            return ""
        return f"{self.path}?{urlencode({'page': page_number, 'per_page': page_size})}"
