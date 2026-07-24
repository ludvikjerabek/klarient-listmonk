from __future__ import annotations

import json
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from klarient import PagedResponse
from listmonk import ListMonkClient
from listmonk.bounces import BounceQuery
from listmonk.campaigns import (
    CampaignAnalyticsQuery,
    CampaignAnalyticsType,
    CampaignQuery,
    CampaignRetrieveQuery,
    CampaignRunningStatsQuery,
)
from listmonk.common import PerPage
from listmonk.lists import ListQuery
from listmonk.subscribers import SubscriberQuery, SubscriberSQLQuery
from listmonk.templates import TemplatePreviewRender, TemplateType

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CAMPAIGN_TEMPLATE_BODY = """
<!doctype html>
<html>
<body>
    <main>
        {{ template "content" . }}
    </main>
</body>
</html>
""".strip()


def load_settings() -> dict[str, Any]:
    for path in (
            PROJECT_ROOT / "settings.json",
            PROJECT_ROOT / "examples" / "settings.json",
            Path(__file__).resolve().parent / "settings.json",
    ):
        if path.exists():
            return json.loads(path.read_text())
    raise FileNotFoundError("settings.json was not found")


def setting(settings: dict[str, Any], name: str, default: Any = None) -> Any:
    value = settings.get(name, default)
    if isinstance(value, str) and value.startswith("optional/"):
        return default
    if isinstance(value, str) and value.startswith("optional-"):
        return default
    return value


def create_client(settings: dict[str, Any]) -> ListMonkClient:
    return ListMonkClient(
        base_url=str(settings["base_url"]),
        username=settings.get("username"),
        access_token=settings.get("access_token") or settings.get("password"),
    )


def check(name: str, call: Callable[[], object]) -> object | None:
    try:
        result = call()
    except Exception as exc:
        print(f"FAIL {name}: {type(exc).__name__}: {exc}")
        return None

    status = getattr(result, "status", "ok")
    data = getattr(result, "data", None)
    count = len(data) if hasattr(data, "__len__") else ""
    print(f"PASS {name}: status={status} count={count}")
    return result


def check_page(name: str, call: Callable[[], PagedResponse[Any]]) -> PagedResponse[Any] | None:
    try:
        result = call()
        page = result.page
    except Exception as exc:
        print(f"FAIL {name}: {type(exc).__name__}: {exc}")
        return None

    print(
        f"PASS {name}: "
        f"status={page.status} "
        f"page={page.current_page_number} "
        f"size={page.page_size} "
        f"items={len(page.data)} "
        f"total={page.record_count}"
    )
    print(f"  self={page.self_link}")
    print(f"  next={page.next_link}")
    return result


def first_item(value: object) -> Any | None:
    data = getattr(value, "data", value)
    if isinstance(value, PagedResponse):
        data = value.data
    if not data:
        return None
    return data[0]


def main() -> int:
    settings = load_settings()
    client = create_client(settings)
    ok = True

    try:
        print("Listmonk API live smoke test")
        print(f"lists_url={client.lists.url}")
        print(f"subscribers_url={client.subscribers.url}")
        print(f"campaigns_url={client.campaigns.url}")
        end = date.today()
        start = end - timedelta(days=30)

        # GET https://{listmonk-host}/api/lists
        lists = check_page(
            "lists.retrieve",
            lambda: client.lists.retrieve(
                ListQuery().with_page(1).with_per_page(PerPage.ALL)
            ),
        )
        ok &= lists is not None
        list_item = first_item(lists) if lists is not None else None

        if list_item is not None:
            # GET https://{listmonk-host}/api/lists/{listId}
            ok &= check("lists.item.retrieve", lambda: client.lists[list_item.id].retrieve()) is not None
        else:
            print("SKIP lists.item.retrieve: no lists returned")

        # GET https://{listmonk-host}/api/subscribers
        subscribers = check_page(
            "subscribers.retrieve",
            lambda: client.subscribers.retrieve(
                SubscriberQuery().with_page(1).with_per_page(PerPage.ALL)
            ),
        )
        ok &= subscribers is not None
        subscriber = first_item(subscribers) if subscribers is not None else None

        if subscriber is not None:
            # GET https://{listmonk-host}/api/subscribers/{subscriberId}
            ok &= check(
                "subscribers.item.retrieve",
                lambda: client.subscribers[subscriber.id].retrieve(),
            ) is not None

            # GET https://{listmonk-host}/api/subscribers/{subscriberId}/export
            ok &= check(
                "subscribers.item.export",
                lambda: client.subscribers[subscriber.id].export.retrieve(),
            ) is not None

            # GET https://{listmonk-host}/api/subscribers/{subscriberId}/bounces
            ok &= check(
                "subscribers.item.bounces",
                lambda: client.subscribers[subscriber.id].bounces.retrieve(),
            ) is not None
        else:
            print("SKIP subscribers.item: no subscribers returned")

        sql_query = setting(settings, "subscriber_sql_query")
        if sql_query is not None:
            # GET https://{listmonk-host}/api/subscribers
            ok &= check_page(
                "subscribers.sql_query.retrieve",
                lambda: client.subscribers.sql_query.retrieve(
                    SubscriberSQLQuery()
                    .with_sql(str(sql_query))
                    .with_page(1)
                    .with_per_page(PerPage.ALL)
                ),
            ) is not None
        else:
            print("SKIP subscribers.sql_query.retrieve: set subscriber_sql_query")

        # GET https://{listmonk-host}/api/campaigns
        campaigns = check_page(
            "campaigns.retrieve",
            lambda: client.campaigns.retrieve(
                CampaignQuery()
                .with_page(1)
                .with_per_page(PerPage.ALL)
                .without_body()
            ),
        )
        ok &= campaigns is not None
        campaign = first_item(campaigns) if campaigns is not None else None

        if campaign is not None:
            # GET https://{listmonk-host}/api/campaigns/{campaignId}
            ok &= check(
                "campaigns.item.retrieve",
                lambda: client.campaigns[campaign.id].retrieve(
                    CampaignRetrieveQuery().without_body()
                ),
            ) is not None

            # GET https://{listmonk-host}/api/campaigns/{campaignId}/preview
            ok &= check(
                "campaigns.item.preview",
                lambda: client.campaigns[campaign.id].preview.retrieve(),
            ) is not None

            # GET https://{listmonk-host}/api/campaigns/running/stats
            ok &= check(
                "campaigns.running.stats",
                lambda: client.campaigns.running.stats.retrieve(
                    CampaignRunningStatsQuery().add_campaign(int(campaign.id))
                ),
            ) is not None

            # GET https://{listmonk-host}/api/campaigns/analytics/{type}
            ok &= check(
                "campaigns.analytics.views",
                lambda: client.campaigns.analytics[CampaignAnalyticsType.VIEWS].retrieve(
                    CampaignAnalyticsQuery()
                    .add_campaign(int(campaign.id))
                    .from_date(start.isoformat())
                    .to_date(end.isoformat())
                ),
            ) is not None
        else:
            print("SKIP campaigns.item: no campaigns returned")

        # GET https://{listmonk-host}/api/bounces
        ok &= check_page(
            "bounces.retrieve",
            lambda: client.bounces.retrieve(
                BounceQuery().with_page(1).with_per_page(PerPage.ALL)
            ),
        ) is not None

        # GET https://{listmonk-host}/api/import/subscribers
        ok &= check("imports.subscribers.retrieve", lambda: client.imports.subscribers.retrieve()) is not None

        # GET https://{listmonk-host}/api/import/subscribers/logs
        ok &= check(
            "imports.subscribers.logs.retrieve",
            lambda: client.imports.subscribers.logs.retrieve(),
        ) is not None

        # GET https://{listmonk-host}/api/media
        media = check("media.retrieve", lambda: client.media.retrieve())
        ok &= media is not None
        media_item = first_item(media) if media is not None else None

        if media_item is not None:
            # GET https://{listmonk-host}/api/media/{mediaId}
            ok &= check("media.item.retrieve", lambda: client.media[media_item.id].retrieve()) is not None
        else:
            print("SKIP media.item.retrieve: no media returned")

        # GET https://{listmonk-host}/api/templates
        templates = check("templates.retrieve", lambda: client.templates.retrieve())
        ok &= templates is not None
        template = first_item(templates) if templates is not None else None

        if template is not None:
            # GET https://{listmonk-host}/api/templates/{templateId}
            ok &= check(
                "templates.item.retrieve",
                lambda: client.templates[template.id].retrieve(),
            ) is not None

            # GET https://{listmonk-host}/api/templates/{templateId}/preview
            ok &= check(
                "templates.item.preview",
                lambda: client.templates[template.id].preview.retrieve(),
            ) is not None
        else:
            print("SKIP templates.item: no templates returned")

        # POST https://{listmonk-host}/api/templates/preview
        ok &= check(
            "templates.preview.render",
            lambda: client.templates.preview.render(
                TemplatePreviewRender(
                    type=TemplateType.CAMPAIGN,
                    body=CAMPAIGN_TEMPLATE_BODY,
                )
            ),
        ) is not None

        # GET https://{listmonk-host}/api/public/lists
        ok &= check("public.lists.retrieve", lambda: client.public.lists.retrieve()) is not None

        print("SKIP public.subscription.create: mutates subscriber data")
        print("SKIP tx.send: sends an email")
    finally:
        client.close()

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
