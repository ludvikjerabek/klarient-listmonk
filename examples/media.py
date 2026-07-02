from __future__ import annotations

from common import ListMonkClient, enabled, load_settings, setting, show_resource, skip
from listmonk.media import MediaUpload


def main() -> None:
    settings = load_settings()
    client = ListMonkClient(
        base_url=settings["base_url"],
        username=settings.get("username"),
        access_token=settings.get("access_token") or settings.get("password"),
    )

    # client.media models /api/media. Indexing it models /api/media/{media_id}.
    # This is the same collection-item shape used by lists, subscribers, and
    # bounces.
    show_resource("Media collection resource", client.media)

    media = client.media.retrieve()
    print(f"media_items={len(media.data)}")

    media_id = setting(settings, "media_id")
    if media_id is not None:
        media_resource = client.media[media_id]
        show_resource("Single media resource", media_resource)
        item = media_resource.retrieve()
        print(f"media={item.data.id} filename={item.data.filename}")

    media_file = setting(settings, "media_file")
    if media_file is None:
        skip("set media_file to upload media")
        return

    uploaded = client.media.upload(MediaUpload.from_file(str(media_file)))
    print(f"uploaded={uploaded.data.id} filename={uploaded.data.filename}")

    if enabled(settings, "delete_uploaded_media"):
        uploaded_resource = client.media[uploaded.data.id]
        show_resource("Uploaded media resource", uploaded_resource)
        deleted = uploaded_resource.delete()
        print(f"deleted_uploaded={deleted.data}")


if __name__ == "__main__":
    main()
