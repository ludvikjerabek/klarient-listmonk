from __future__ import annotations

import time

from common import load_settings, run_optional, setting, skip
from listmonk import ListMonkClient
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
    print("Public lists resource:")
    print(f"  path: {client.public.lists.path}")
    print(f"  url:  {client.public.lists.url}")
    print("Public subscription resource:")
    print(f"  path: {client.public.subscription.path}")
    print(f"  url:  {client.public.subscription.url}")

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
