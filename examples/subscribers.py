from __future__ import annotations

import time

from common import enabled, load_settings, run_optional, setting, skip
from listmonk import ListMonkClient
from listmonk.common import (
    CreateSubscriberStatus,
    PerPage,
    SortOrder,
    SubscriberStatus,
    SubscriptionStatus,
)
from listmonk.subscribers import (
    ListMembershipAction,
    QueryListMembershipUpdate,
    SubscriberCreate,
    SubscriberDeleteQuery,
    SubscriberIds,
    SubscriberListMembershipUpdate,
    SubscriberOrderBy,
    SubscriberQuery,
    SubscriberQueryBlocklist,
    SubscriberQueryDelete,
    SubscriberSQLQuery,
    SubscriberUpdate,
)


def main() -> None:
    settings = load_settings()
    client = ListMonkClient(
        base_url=settings["base_url"],
        username=settings.get("username"),
        access_token=settings.get("access_token") or settings.get("password"),
    )

    # The Python object tree mirrors the REST API tree. This root collection is
    # /api/subscribers, and the printed path/url make that mapping explicit.
    print("Subscriber collection resource:")
    print(f"  path: {client.subscribers.path}")
    print(f"  url:  {client.subscribers.url}")

    query = (
        SubscriberQuery()
        .with_page(1)
        .with_per_page(PerPage.ALL)
        .with_order_by(SubscriberOrderBy.NAME)
        .with_order(SortOrder.ASC)
    )
    subscribers = client.subscribers.retrieve(query)
    print(f"subscribers={subscribers.record_count}")

    sql_query = setting(settings, "subscriber_sql_query")
    if sql_query is not None:
        # Listmonk gates SQL expressions with the subscribers:sql_query
        # permission. That permission is powerful: Listmonk documents it as a
        # read-only SQL capability that can bypass individual list/subscriber
        # permission boundaries, so grant it only to trusted API users.
        #
        # The HTTP route is still /api/subscribers. This semantic resource makes
        # the capability visible without inventing a URI segment that Listmonk
        # does not have.
        print("Subscriber SQL query resource:")
        print(f"  path: {client.subscribers.sql_query.path}")
        print(f"  url:  {client.subscribers.sql_query.url}")
        sql_results = client.subscribers.sql_query.retrieve(
            SubscriberSQLQuery()
            .with_sql(str(sql_query))
            .with_per_page(PerPage.ALL)
        )
        print(f"sql_query_subscribers={sql_results.record_count}")

    subscriber_id = setting(settings, "subscriber_id")
    if subscriber_id is not None:
        subscriber_resource = client.subscribers[subscriber_id]
        # Child resources hang off the parent resource. The same subscriber can
        # expose /export and /bounces without forcing those actions onto the
        # collection object.
        print("Single subscriber resource:")
        print(f"  path: {subscriber_resource.path}")
        print(f"  url:  {subscriber_resource.url}")
        print("Subscriber export resource:")
        print(f"  path: {subscriber_resource.export.path}")
        print(f"  url:  {subscriber_resource.export.url}")
        print("Subscriber bounces resource:")
        print(f"  path: {subscriber_resource.bounces.path}")
        print(f"  url:  {subscriber_resource.bounces.url}")

        subscriber = run_optional(
            "retrieve subscriber",
            lambda: subscriber_resource.retrieve(),
        )
        if subscriber is not None:
            print(f"subscriber={subscriber.data.id} email={subscriber.data.email}")
        exported = run_optional(
            "retrieve subscriber export",
            lambda: subscriber_resource.export.retrieve(),
        )
        if exported is not None:
            print(f"export_profile_records={len(exported.profile)}")
        bounces = run_optional(
            "retrieve subscriber bounces",
            lambda: subscriber_resource.bounces.retrieve(),
        )
        if bounces is not None:
            print(f"subscriber_bounces={len(bounces.data)}")

        if enabled(settings, "delete_subscriber_bounces"):
            deleted_bounces = run_optional(
                "delete subscriber bounces",
                lambda: subscriber_resource.bounces.delete(),
            )
            if deleted_bounces is not None:
                print(f"deleted_subscriber_bounces={deleted_bounces.data}")
        else:
            skip("set delete_subscriber_bounces=true to delete bounces for subscriber_id")

    if not enabled(settings, "create_test_data"):
        skip("set create_test_data=true to create and mutate subscribers")
        return

    suffix = int(time.time())
    created = client.subscribers.create(
        SubscriberCreate(
            email=f"klarient-example-{suffix}@example.com",
            name="Klarient Example",
            status=CreateSubscriberStatus.ENABLED,
            lists=[],
            attribs={"source": "klarient-example"},
            preconfirm_subscriptions=True,
        )
    )
    print(f"created={created.data.id}")

    created_resource = client.subscribers[created.data.id]
    # Once the create call returns a typed response, use the response data to
    # address the newly created resource directly.
    print("Created subscriber resource:")
    print(f"  path: {created_resource.path}")
    print(f"  url:  {created_resource.url}")

    updated = created_resource.update(
        SubscriberUpdate(
            email=created.data.email,
            name="Klarient Example Updated",
            status=SubscriberStatus.ENABLED,
            lists=[],
            attribs={"updated": True},
            preconfirm_subscriptions=True,
        )
    )
    print(f"updated={updated.data.name}")

    patched = created_resource.update_partial(
        SubscriberUpdate().with_name("Klarient Example Patched")
    )
    print(f"patched={patched.data.name}")

    # Nested action resources make URI-specific operations easy to find.
    print("Subscriber opt-in resource:")
    print(f"  path: {created_resource.optin.path}")
    print(f"  url:  {created_resource.optin.url}")
    optin = created_resource.optin.send()
    print(f"optin_sent={optin.data}")

    blocklisted = run_optional(
        "blocklist subscriber",
        lambda: created_resource.blocklist.blocklist(),
    )
    if blocklisted is not None:
        print(f"blocklisted={blocklisted.data}")

    bulk = run_optional(
        "bulk blocklist subscriber",
        lambda: client.subscribers.blocklist.blocklist(
            SubscriberIds().add_id(created.data.id)
        ),
    )
    if bulk is not None:
        print(f"bulk_blocklisted={bulk.data}")

    list_id = setting(settings, "list_id")
    if list_id is not None:
        print("Bulk subscriber list membership resource:")
        print(f"  path: {client.subscribers.lists.path}")
        print(f"  url:  {client.subscribers.lists.url}")
        membership = run_optional(
            "update subscriber list membership",
            lambda: client.subscribers.lists.update(
                SubscriberListMembershipUpdate()
                .add_id(created.data.id)
                .with_action(ListMembershipAction.ADD)
                .add_target_list(int(list_id))
                .with_status(SubscriptionStatus.CONFIRMED)
            ),
        )
        if membership is not None:
            print(f"membership={membership.data}")

        print("Query subscriber list membership resource:")
        print(f"  path: {client.subscribers.query.lists.path}")
        print(f"  url:  {client.subscribers.query.lists.url}")
        query_membership = run_optional(
            "query update subscriber list membership",
            lambda: client.subscribers.query.lists.update(
                QueryListMembershipUpdate()
                .with_query(f"subscribers.email = '{created.data.email}'")
                .with_action(ListMembershipAction.REMOVE)
                .add_target_list(int(list_id))
            ),
        )
        if query_membership is not None:
            print(f"query_membership={query_membership.data}")

    print("Query subscriber blocklist resource:")
    print(f"  path: {client.subscribers.query.blocklist.path}")
    print(f"  url:  {client.subscribers.query.blocklist.url}")
    query_blocklist = run_optional(
        "query blocklist subscribers",
        lambda: client.subscribers.query.blocklist.blocklist(
            SubscriberQueryBlocklist().with_query(
                f"subscribers.email = '{created.data.email}'"
            )
        ),
    )
    if query_blocklist is not None:
        print(f"query_blocklist={query_blocklist.data}")

    print("Query subscriber delete resource:")
    print(f"  path: {client.subscribers.query.delete.path}")
    print(f"  url:  {client.subscribers.query.delete.url}")
    query_delete = run_optional(
        "query delete subscribers",
        lambda: client.subscribers.query.delete.delete(
            SubscriberQueryDelete().with_query(
                f"subscribers.email = '{created.data.email}'"
            )
        ),
    )
    if query_delete is None:
        deleted = client.subscribers.delete(
            SubscriberDeleteQuery().add_id(created.data.id)
        )
        print(f"deleted={deleted.data}")
    else:
        print(f"query_deleted={query_delete.data}")


if __name__ == "__main__":
    main()
