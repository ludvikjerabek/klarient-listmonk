from __future__ import annotations

import time

from common import ListMonkClient, load_settings, run_optional, setting, show_resource, skip
from listmonk.public import PublicSubscription, PublicSubscriptionForm


def main() -> None:
    settings = load_settings()
    client = ListMonkClient(
        base_url=settings["base_url"],
        username=settings.get("username"),
        access_token=settings.get("access_token") or settings.get("password"),
    )

    # Public endpoints are modeled under client.public, matching /api/public.
    # The leaves under that object are the actual callable API resources.
    show_resource("Public lists resource", client.public.lists)
    show_resource("Public subscription resource", client.public.subscription)

    lists = run_optional("retrieve public lists", lambda: client.public.lists.retrieve())
    if lists is not None:
        print(f"public_lists={len(lists)}")

    public_list_uuid = setting(settings, "public_list_uuid")
    if public_list_uuid is None:
        skip("set public_list_uuid to create public subscriptions")
        return

    suffix = int(time.time())
    json_subscription = run_optional(
        "create public JSON subscription",
        lambda: client.public.subscription.create(
            PublicSubscription()
            .with_email(f"klarient-example-{suffix}-json@example.com")
            .with_name("Klarient Public JSON")
            .add_list_uuid(str(public_list_uuid))
        ),
    )
    if json_subscription is not None:
        print(f"json_subscription={json_subscription.data}")

    form_subscription = run_optional(
        "create public form subscription",
        lambda: client.public.subscription.create_form(
            PublicSubscriptionForm()
            .with_email(f"klarient-example-{suffix}-form@example.com")
            .with_name("Klarient Public Form")
            .add_list_uuid(str(public_list_uuid))
        ),
    )
    if form_subscription is not None:
        print(f"form_subscription={form_subscription.data}")


if __name__ == "__main__":
    main()
