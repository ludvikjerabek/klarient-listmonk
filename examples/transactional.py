from __future__ import annotations

from common import load_settings, setting, skip
from listmonk import ListMonkClient
from listmonk.transactional import (
    TransactionalContentType,
    TransactionalMessage,
    TransactionalSubscriberMode,
)


def main() -> None:
    settings = load_settings()
    client = ListMonkClient(
        base_url=settings["base_url"],
        username=settings.get("username"),
        access_token=settings.get("access_token") or settings.get("password"),
    )

    # The tx resource models the actual Listmonk path: /api/tx.
    print("Transactional message resource:")
    print(f"  path: {client.tx.path}")
    print(f"  url:  {client.tx.url}")

    template_id = setting(settings, "transactional_template_id", setting(settings, "template_id"))
    if template_id is None:
        skip("set transactional_template_id or template_id")
        return

    subscriber_email = setting(settings, "transactional_email")
    if subscriber_email is None:
        skip("set transactional_email to send an example message")
        return

    message = (
        TransactionalMessage()
        .with_subscriber_mode(TransactionalSubscriberMode.EXTERNAL)
        .add_subscriber_email(str(subscriber_email))
        .with_template(int(template_id))
        .with_content_type(TransactionalContentType.HTML)
        .with_data("name", "Klarient")
    )

    attachment_file = setting(settings, "transactional_attachment_file")
    if attachment_file is not None:
        message.add_attachment_file(str(attachment_file))

    sent = client.tx.send(message)
    print(f"sent={sent.data}")


if __name__ == "__main__":
    main()
