from __future__ import annotations

import time

from common import enabled, load_settings, run_optional, setting, skip
from listmonk import ListMonkClient
from listmonk.campaigns import (
    CampaignAnalyticsQuery,
    CampaignAnalyticsType,
    CampaignArchiveUpdate,
    CampaignContentType,
    CampaignCreate,
    CampaignDeleteQuery,
    CampaignQuery,
    CampaignRunningStatsQuery,
    CampaignStatus,
    CampaignStatusUpdate,
    CampaignTest,
    CampaignType,
    CampaignUpdate,
)
from listmonk.common import PerPage, SortOrder


def main() -> None:
    settings = load_settings()
    client = ListMonkClient(
        base_url=settings["base_url"],
        username=settings.get("username"),
        access_token=settings.get("access_token") or settings.get("password"),
    )

    # The resource tree mirrors the Listmonk URI tree. Printing the resource
    # path and URL makes that one-to-one mapping visible while reading.
    print("Campaign collection resource:")
    print(f"  path: {client.campaigns.path}")
    print(f"  url:  {client.campaigns.url}")

    campaigns = client.campaigns.retrieve(
        CampaignQuery()
        .add_status(CampaignStatus.RUNNING)
        .with_order(SortOrder.DESC)
        .with_per_page(PerPage.ALL)
        .without_body()
    )
    print(f"campaigns={campaigns.page.record_count}")

    for page in campaigns:
        print(f"first_page={page.current_page_number} size={page.page_size}")
        break

    campaign_id = setting(settings, "campaign_id")
    if campaign_id is None:
        skip("set campaign_id to retrieve campaign details")
        return

    campaign_resource = client.campaigns[campaign_id]
    # Indexing the campaign collection creates /api/campaigns/{campaign_id}.
    # The preview resource hangs off that specific campaign.
    print("Single campaign resource:")
    print(f"  path: {campaign_resource.path}")
    print(f"  url:  {campaign_resource.url}")
    print("Campaign preview resource:")
    print(f"  path: {campaign_resource.preview.path}")
    print(f"  url:  {campaign_resource.preview.url}")
    print("Campaign status resource:")
    print(f"  path: {campaign_resource.status.path}")
    print(f"  url:  {campaign_resource.status.url}")
    print("Campaign archive resource:")
    print(f"  path: {campaign_resource.archive.path}")
    print(f"  url:  {campaign_resource.archive.url}")
    print("Campaign test-send resource:")
    print(f"  path: {campaign_resource.test.path}")
    print(f"  url:  {campaign_resource.test.url}")

    campaign = run_optional(
        "retrieve campaign details",
        lambda: campaign_resource.retrieve(),
    )
    if campaign is not None:
        print(f"campaign={campaign.data.id} name={campaign.data.name}")

    preview = run_optional(
        "retrieve campaign preview",
        lambda: campaign_resource.preview.retrieve(),
    )
    if preview is not None:
        print(f"preview_chars={len(preview.data)}")

    # Some endpoints are not children of one campaign. They are modeled where
    # the URI places them: /api/campaigns/running/stats.
    print("Running campaign stats resource:")
    print(f"  path: {client.campaigns.running.stats.path}")
    print(f"  url:  {client.campaigns.running.stats.url}")
    stats = client.campaigns.running.stats.retrieve(
        CampaignRunningStatsQuery().add_campaign(int(campaign_id))
    )
    print(f"running_stats={len(stats.data)}")

    analytics_resource = client.campaigns.analytics[CampaignAnalyticsType.VIEWS]
    # Typed path segments can be modeled too. Here the analytics type becomes
    # part of the resource path.
    print("Campaign analytics resource:")
    print(f"  path: {analytics_resource.path}")
    print(f"  url:  {analytics_resource.url}")
    analytics = run_optional(
        "retrieve campaign analytics",
        lambda: analytics_resource.retrieve(
            CampaignAnalyticsQuery().add_campaign(int(campaign_id))
        ),
    )
    if analytics is not None:
        print(f"view_points={len(analytics.data)}")

    show_campaign_request_shapes(int(campaign_id))
    show_campaign_mutations(client, settings)


def show_campaign_request_shapes(campaign_id: int) -> None:
    """Show campaign mutation request bodies without touching live data."""
    campaign_create = (
        CampaignCreate(
            name="Klarient Example Campaign",
            subject="Klarient Example",
            from_email="sender@example.com",
            type=CampaignType.REGULAR,
            content_type=CampaignContentType.HTML,
            body="<p>Hello from Klarient.</p>",
        )
        .add_list(1)
        .add_tag("klarient-example")
    )
    campaign_update = CampaignUpdate(
        name="Klarient Example Campaign Updated",
        subject="Klarient Example Updated",
        from_email="sender@example.com",
        type=CampaignType.REGULAR,
        content_type=CampaignContentType.HTML,
        body="<p>Hello from Klarient.</p>",
    ).add_list(1)
    status_update = CampaignStatusUpdate().with_status(CampaignStatus.PAUSED)
    archive_update = CampaignArchiveUpdate().with_archive(True).with_slug("klarient-example")
    test_send = CampaignTest(subject="Klarient Test", from_email="sender@example.com").add_subscriber(
        "person@example.com"
    )
    delete_query = CampaignDeleteQuery().add_id(campaign_id)

    print(f"campaign_create={campaign_create.to_mapping()}")
    print(f"campaign_update={campaign_update.to_mapping()}")
    print(f"status_update={status_update.to_mapping()}")
    print(f"archive_update={archive_update.to_mapping()}")
    print(f"test_send={test_send.to_mapping()}")
    print(f"delete_query={delete_query.to_mapping()}")

    # created = client.campaigns.create(campaign_create)
    # updated = client.campaigns[created.data.id].update(campaign_update)
    # status = client.campaigns[created.data.id].status.update(status_update)
    # archive = client.campaigns[created.data.id].archive.update(archive_update)
    # test = client.campaigns[created.data.id].test.send(test_send)
    # deleted = client.campaigns[created.data.id].delete()


def show_campaign_mutations(client: ListMonkClient, settings: dict[str, object]) -> None:
    """Create, update, exercise actions, and delete a temporary campaign."""
    if not enabled(settings, "create_test_data"):
        skip("set create_test_data=true to create, update, and delete a campaign")
        return

    list_id = setting(settings, "list_id")
    if list_id is None:
        skip("set list_id to create a temporary campaign")
        return

    from_email = setting(settings, "campaign_from_email", setting(settings, "from_email", "sender@example.com"))
    template_id = setting(settings, "campaign_template_id", setting(settings, "template_id"))
    messenger = setting(settings, "campaign_messenger", "email")
    suffix = int(time.time())

    create_request = (
        CampaignCreate(
            name=f"Klarient Example Campaign {suffix}",
            subject="Klarient Example Campaign",
            from_email=str(from_email),
            type=CampaignType.REGULAR,
            content_type=CampaignContentType.HTML,
            body="<p>Hello from a temporary Klarient example campaign.</p>",
            messenger=str(messenger),
            tags=["klarient-example"],
        )
        .add_list(int(list_id))
        .with_attrib("source", "klarient-example")
    )
    if template_id is not None:
        create_request.with_template(int(template_id))

    created = client.campaigns.create(create_request)
    print(f"created_campaign={created.data.id}")

    created_resource = client.campaigns[created.data.id]
    print("Created campaign resource:")
    print(f"  path: {created_resource.path}")
    print(f"  url:  {created_resource.url}")
    print("Created campaign status resource:")
    print(f"  path: {created_resource.status.path}")
    print(f"  url:  {created_resource.status.url}")
    print("Created campaign archive resource:")
    print(f"  path: {created_resource.archive.path}")
    print(f"  url:  {created_resource.archive.url}")
    print("Created campaign test-send resource:")
    print(f"  path: {created_resource.test.path}")
    print(f"  url:  {created_resource.test.url}")

    try:
        update_request = (
            CampaignUpdate(
                name=f"Klarient Example Campaign Updated {suffix}",
                subject="Klarient Example Campaign Updated",
                from_email=str(from_email),
                type=CampaignType.REGULAR,
                content_type=CampaignContentType.HTML,
                body="<p>Hello from an updated temporary Klarient example campaign.</p>",
                messenger=str(messenger),
                tags=["klarient-example", "updated"],
            )
            .add_list(int(list_id))
            .with_attrib("updated", True)
        )
        if template_id is not None:
            update_request.with_template(int(template_id))

        updated = created_resource.update(update_request)
        print(f"updated_campaign={updated.data.name}")

        archived = run_optional(
            "update campaign archive settings",
            lambda: created_resource.archive.update(
                CampaignArchiveUpdate()
                .with_archive(True)
                .with_slug(f"klarient-example-{suffix}")
            ),
        )
        if archived is not None:
            print(f"archive_enabled={archived.data.archive}")

        paused = run_optional(
            "update campaign status",
            lambda: created_resource.status.update(
                CampaignStatusUpdate().with_status(CampaignStatus.PAUSED)
            ),
        )
        if paused is not None:
            print(f"campaign_status={paused.data.status}")

        test_email = setting(settings, "campaign_test_email")
        if enabled(settings, "send_campaign_test") and test_email is not None:
            test = created_resource.test.send(
                CampaignTest(
                    subject="Klarient Example Test",
                    from_email=str(from_email),
                    type=CampaignType.REGULAR,
                    content_type=CampaignContentType.HTML,
                    body="<p>Hello from a Klarient campaign test.</p>",
                    messenger=str(messenger),
                ).add_subscriber(str(test_email))
            )
            print(f"test_sent={test.data}")
        else:
            skip("set send_campaign_test=true and campaign_test_email to send a campaign test email")
    finally:
        deleted = created_resource.delete()
        print(f"deleted_campaign={deleted.data}")


if __name__ == "__main__":
    main()
