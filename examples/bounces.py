from __future__ import annotations

from common import enabled, load_settings, setting, skip
from listmonk import ListMonkClient
from listmonk.bounces import (
    BounceDeleteQuery,
    BounceOrderBy,
    BounceQuery,
    BounceSortOrder,
)
from listmonk.common import PerPage


def main() -> None:
    settings = load_settings()
    client = ListMonkClient(
        base_url=settings["base_url"],
        username=settings.get("username"),
        access_token=settings.get("access_token") or settings.get("password"),
    )

    # This collection resource models /api/bounces directly. The examples print
    # paths so it is clear which URI each object represents.
    print("Bounce collection resource:")
    print(f"  path: {client.bounces.path}")
    print(f"  url:  {client.bounces.url}")

    query = (
        BounceQuery()
        .with_per_page(PerPage.ALL)
        .with_order_by(BounceOrderBy.CREATED_AT)
        .with_order(BounceSortOrder.DESC)
    )
    campaign_id = setting(settings, "campaign_id")
    if campaign_id is not None:
        query.with_campaign(int(campaign_id))

    bounces = client.bounces.retrieve(query)
    print(f"bounces={bounces.page.record_count}")

    for page in bounces:
        print(f"first_page={page.current_page_number} size={page.page_size}")
        break

    bounce_id = setting(settings, "bounce_id")
    if bounce_id is None:
        skip("set bounce_id to delete a single bounce")
        return

    if not enabled(settings, "delete_bounces"):
        skip("set delete_bounces=true to delete bounce records")
        return

    bounce_resource = client.bounces[bounce_id]
    # Collection indexing follows the same pattern across the wrapper:
    # client.bounces[123] -> /api/bounces/123.
    print("Single bounce resource:")
    print(f"  path: {bounce_resource.path}")
    print(f"  url:  {bounce_resource.url}")

    deleted_one = bounce_resource.delete()
    print(f"deleted_one={deleted_one.data}")

    extra_ids = setting(settings, "bounce_ids", [])
    if extra_ids:
        delete_query = BounceDeleteQuery()
        for item in extra_ids:
            delete_query.add_id(int(item))
        deleted_many = client.bounces.delete(delete_query)
        print(f"deleted_many={deleted_many.data}")


if __name__ == "__main__":
    main()
