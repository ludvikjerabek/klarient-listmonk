from __future__ import annotations

import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from listmonk import ListMonkClient
from listmonk.campaigns import (
    CampaignArchiveUpdate,
    CampaignContentType,
    CampaignCreate,
    CampaignType,
    CampaignUpdate,
)
from listmonk.common import (
    CreateSubscriberStatus,
    ListOptin,
    ListStatus,
    ListType,
    SubscriberStatus,
)
from listmonk.lists import ListCreate, ListUpdate
from listmonk.media import MediaUpload
from listmonk.subscribers import SubscriberCreate, SubscriberUpdate
from listmonk.templates import TemplateCreate, TemplateType, TemplateUpdate

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


def enabled(settings: dict[str, Any], name: str) -> bool:
    return bool(settings.get(name, False))


def create_client(settings: dict[str, Any]) -> ListMonkClient:
    return ListMonkClient(
        base_url=str(settings["base_url"]),
        username=settings.get("username"),
        access_token=settings.get("access_token") or settings.get("password"),
    )


def record(records: list[dict[str, str]], kind: str, name: str, identifier: object) -> None:
    records.append(
        {
            "kind": kind,
            "name": name,
            "id": "" if identifier is None else str(identifier),
        }
    )
    print(f"CREATED {kind}: name={name} id={identifier}")


def cleanup(client: ListMonkClient, records: list[dict[str, str]]) -> bool:
    ok = True
    for item in reversed(records):
        kind = item["kind"]
        name = item["name"]
        identifier = item["id"]
        try:
            if kind == "campaign":
                # DELETE https://{listmonk-host}/api/campaigns/{campaignId}
                result = client.campaigns[identifier].delete()
            elif kind == "template":
                # DELETE https://{listmonk-host}/api/templates/{templateId}
                result = client.templates[identifier].delete()
            elif kind == "subscriber":
                # DELETE https://{listmonk-host}/api/subscribers/{subscriberId}
                result = client.subscribers[identifier].delete()
            elif kind == "media":
                # DELETE https://{listmonk-host}/api/media/{mediaId}
                result = client.media[identifier].delete()
            elif kind == "list":
                # DELETE https://{listmonk-host}/api/lists/{listId}
                result = client.lists[identifier].delete()
            else:
                print(f"SKIP cleanup unknown kind={kind} name={name} id={identifier}")
                continue
        except Exception as exc:
            ok = False
            print(f"CLEANUP FAIL {kind}: name={name} id={identifier}: {type(exc).__name__}: {exc}")
        else:
            print(f"CLEANUP {kind}: name={name} id={identifier} result={getattr(result, 'data', '')}")
    return ok


def main() -> int:
    settings = load_settings()
    if not enabled(settings, "run_mutation_smoke"):
        print("SKIP: set run_mutation_smoke=true to create and clean up temporary Listmonk records")
        return 0

    client = create_client(settings)
    created: list[dict[str, str]] = []
    run_id = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    prefix = f"klarient-smoke-{run_id}"
    from_email = setting(settings, "mutation_from_email", setting(settings, "campaign_from_email"))

    try:
        print("Listmonk API mutation smoke test")
        print(f"prefix={prefix}")

        # POST https://{listmonk-host}/api/lists
        created_list = client.lists.create(
            ListCreate(
                name=f"{prefix}-list",
                type=ListType.PRIVATE,
                optin=ListOptin.SINGLE,
                status=ListStatus.ACTIVE,
                tags=["klarient-smoke"],
                description="Temporary list created by the Klarient mutation smoke test.",
            )
        )
        list_id = created_list.data.id
        record(created, "list", created_list.data.name, list_id)

        # PUT https://{listmonk-host}/api/lists/{listId}
        updated_list = client.lists[list_id].update(
            ListUpdate(
                name=f"{prefix}-list-updated",
                type=ListType.PRIVATE,
                optin=ListOptin.SINGLE,
                status=ListStatus.ACTIVE,
                tags=["klarient-smoke", "updated"],
                description="Updated by the Klarient mutation smoke test.",
            )
        )
        print(f"UPDATED list: id={updated_list.data.id} name={updated_list.data.name}")

        # POST https://{listmonk-host}/api/subscribers
        created_subscriber = client.subscribers.create(
            SubscriberCreate(
                email=f"{prefix}@example.com",
                name=f"{prefix}-subscriber",
                status=CreateSubscriberStatus.ENABLED,
                lists=[list_id],
                attribs={"source": "klarient-mutation-smoke"},
                preconfirm_subscriptions=True,
            )
        )
        subscriber_id = created_subscriber.data.id
        record(created, "subscriber", created_subscriber.data.email, subscriber_id)

        # PUT https://{listmonk-host}/api/subscribers/{subscriberId}
        updated_subscriber = client.subscribers[subscriber_id].update(
            SubscriberUpdate(
                email=created_subscriber.data.email,
                name=f"{prefix}-subscriber-updated",
                status=SubscriberStatus.ENABLED,
                lists=[list_id],
                attribs={"updated": True},
                preconfirm_subscriptions=True,
            )
        )
        print(f"UPDATED subscriber: id={updated_subscriber.data.id} name={updated_subscriber.data.name}")

        # PATCH https://{listmonk-host}/api/subscribers/{subscriberId}
        patched_subscriber = client.subscribers[subscriber_id].update_partial(
            SubscriberUpdate().with_name(f"{prefix}-subscriber-patched")
        )
        print(f"PATCHED subscriber: id={patched_subscriber.data.id} name={patched_subscriber.data.name}")

        # GET https://{listmonk-host}/api/subscribers/{subscriberId}/export
        exported = client.subscribers[subscriber_id].export.retrieve()
        print(f"EXPORT subscriber: profile_records={len(exported.profile)}")

        # POST https://{listmonk-host}/api/templates
        created_template = client.templates.create(
            TemplateCreate(
                name=f"{prefix}-template",
                type=TemplateType.CAMPAIGN,
                body=CAMPAIGN_TEMPLATE_BODY,
            )
        )
        template_id = created_template.data.id
        record(created, "template", created_template.data.name, template_id)

        # PUT https://{listmonk-host}/api/templates/{templateId}
        updated_template = client.templates[template_id].update(
            TemplateUpdate(
                name=f"{prefix}-template-updated",
                type=TemplateType.CAMPAIGN,
                body=CAMPAIGN_TEMPLATE_BODY,
            )
        )
        print(f"UPDATED template: id={updated_template.data.id} name={updated_template.data.name}")

        # POST https://{listmonk-host}/api/media
        with tempfile.NamedTemporaryFile("wb", prefix=f"{prefix}-media-", suffix=".txt", delete=False) as handle:
            handle.write(b"temporary media created by klarient-listmonk mutation smoke\n")
            media_path = Path(handle.name)
        try:
            uploaded_media = client.media.upload(
                MediaUpload.from_file(media_path, content_type="text/plain")
            )
        finally:
            media_path.unlink(missing_ok=True)
        media_id = uploaded_media.data.id
        record(created, "media", uploaded_media.data.filename, media_id)

        if from_email is None:
            print("SKIP campaign create/update/archive: set mutation_from_email or campaign_from_email")
        else:
            # POST https://{listmonk-host}/api/campaigns
            created_campaign = client.campaigns.create(
                CampaignCreate(
                    name=f"{prefix}-campaign",
                    subject="Klarient mutation smoke",
                    from_email=str(from_email),
                    type=CampaignType.REGULAR,
                    content_type=CampaignContentType.HTML,
                    body="<p>Hello from a temporary Klarient mutation smoke campaign.</p>",
                    messenger=str(setting(settings, "campaign_messenger", "email")),
                    template_id=template_id,
                    tags=["klarient-smoke"],
                )
                .add_list(list_id)
                .with_attrib("source", "klarient-mutation-smoke")
            )
            campaign_id = created_campaign.data.id
            record(created, "campaign", created_campaign.data.name, campaign_id)

            # PUT https://{listmonk-host}/api/campaigns/{campaignId}
            updated_campaign = client.campaigns[campaign_id].update(
                CampaignUpdate(
                    name=f"{prefix}-campaign-updated",
                    subject="Klarient mutation smoke updated",
                    from_email=str(from_email),
                    type=CampaignType.REGULAR,
                    content_type=CampaignContentType.HTML,
                    body="<p>Hello from an updated Klarient mutation smoke campaign.</p>",
                    messenger=str(setting(settings, "campaign_messenger", "email")),
                    template_id=template_id,
                    tags=["klarient-smoke", "updated"],
                )
                .add_list(list_id)
                .with_attrib("updated", True)
            )
            print(f"UPDATED campaign: id={updated_campaign.data.id} name={updated_campaign.data.name}")

            # PUT https://{listmonk-host}/api/campaigns/{campaignId}/archive
            archived_campaign = client.campaigns[campaign_id].archive.update(
                CampaignArchiveUpdate()
                .with_archive(True)
                .with_slug(prefix)
            )
            print(f"ARCHIVED campaign: id={archived_campaign.data.id} archive={archived_campaign.data.archive}")

        print("SKIP subscriber opt-in: sends email")
        print("SKIP campaign test-send: sends email")
        print("SKIP public subscription create: mutates public subscriber data")
        print("SKIP transactional send: sends email")
    finally:
        cleanup_ok = cleanup(client, created)
        client.close()

    return 0 if cleanup_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
