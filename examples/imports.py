from __future__ import annotations

from common import ListMonkClient, enabled, load_settings, setting, show_resource, skip
from listmonk.common import SubscriptionStatus
from listmonk.imports import (
    ImportMode,
    SubscriberImport,
    SubscriberImportParams,
)


def main() -> None:
    settings = load_settings()
    client = ListMonkClient(
        base_url=settings["base_url"],
        username=settings.get("username"),
        access_token=settings.get("access_token") or settings.get("password"),
    )

    # Nested attributes model nested URI paths. The import status endpoint and
    # its logs endpoint are separate resources under /api/import/subscribers.
    show_resource("Subscriber import resource", client.imports.subscribers)
    show_resource("Subscriber import logs resource", client.imports.subscribers.logs)

    status = client.imports.subscribers.retrieve()
    print(f"status={status.data.status} imported={status.data.imported}/{status.data.total}")

    logs = client.imports.subscribers.logs.retrieve()
    print(f"log_chars={len(logs.data)}")

    import_file = setting(settings, "import_file")
    if import_file is None:
        skip("set import_file to upload a subscriber CSV")
    else:
        params = (
            SubscriberImportParams()
            .with_mode(ImportMode.SUBSCRIBE)
            .with_delimiter(",")
            .with_overwrite(False)
            .with_subscription_status(SubscriptionStatus.CONFIRMED)
        )
        list_id = setting(settings, "list_id")
        if list_id is not None:
            params.add_list(int(list_id))
        uploaded = client.imports.subscribers.upload(
            SubscriberImport.from_file(str(import_file), params=params)
        )
        print(f"uploaded mode={uploaded.mode} lists={uploaded.lists}")

    if not enabled(settings, "delete_import"):
        skip("set delete_import=true to stop/delete the current import")
        return

    deleted = client.imports.subscribers.delete()
    print(f"deleted_status={deleted.data.status}")


if __name__ == "__main__":
    main()
