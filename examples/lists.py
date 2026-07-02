from __future__ import annotations

import time

from common import ListMonkClient, enabled, load_settings, setting, show_resource, skip
from listmonk.common import ListOptin, ListStatus, ListType, PerPage, SortOrder
from listmonk.lists import (
    ListCreate,
    ListDeleteQuery,
    ListOrderBy,
    ListQuery,
    ListUpdate,
)


def main() -> None:
    settings = load_settings()
    client = ListMonkClient(
        base_url=settings["base_url"],
        username=settings.get("username"),
        access_token=settings.get("access_token") or settings.get("password"),
    )

    # Klarient resources are meant to read like the API documentation. This
    # collection resource maps to /api/lists, and resource.path/resource.url can
    # be printed whenever you want to confirm the modeled URI.
    show_resource("List collection resource", client.lists)

    query = (
        ListQuery()
        .with_status(ListStatus.ACTIVE)
        .with_order_by(ListOrderBy.NAME)
        .with_order(SortOrder.ASC)
        .with_per_page(PerPage.ALL)
    )
    lists = client.lists.retrieve(query)
    print(f"lists={lists.record_count}")

    for page in client.lists:
        print(f"first_page={page.current_page_number} size={page.page_size}")
        break

    list_id = setting(settings, "list_id")
    if list_id is not None:
        list_resource = client.lists[list_id]
        # Indexing a collection creates the child resource for one list:
        # client.lists[123] -> /api/lists/123.
        show_resource("Single list resource", list_resource)
        item = list_resource.retrieve()
        print(f"list_id={item.data.id} name={item.data.name}")

    if not enabled(settings, "create_test_data"):
        skip("set create_test_data=true to create, update, and delete a list")
        return

    suffix = int(time.time())
    created = client.lists.create(
        ListCreate(
            name=f"Klarient Example {suffix}",
            type=ListType.PRIVATE,
            optin=ListOptin.SINGLE,
            status=ListStatus.ACTIVE,
            tags=["klarient-example"],
        )
    )
    print(f"created={created.data.id}")

    created_resource = client.lists[created.data.id]
    show_resource("Created list resource", created_resource)

    updated = created_resource.update(
        ListUpdate(
            name=f"Klarient Example Updated {suffix}",
            type=ListType.PRIVATE,
            optin=ListOptin.SINGLE,
            status=ListStatus.ACTIVE,
            tags=["klarient-example", "updated"],
        )
    )
    print(f"updated={updated.data.name}")

    deleted = client.lists.delete(ListDeleteQuery().add_id(created.data.id))
    print(f"deleted={deleted.data}")


if __name__ == "__main__":
    main()
