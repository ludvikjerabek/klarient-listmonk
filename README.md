# Listmonk API Package
[![PyPI Downloads](https://static.pepy.tech/badge/klarient-listmonk)](https://pepy.tech/projects/klarient-listmonk)  
Library implements the Listmonk REST API via Python.

### Requirements:

* Python 3.11+
* klarient
* requests

### Installing the Package

You can install the API library using pip.

```
pip install klarient-listmonk
```

For local development from this folder, use an editable install.

```
python3 -m pip install -e .
```

### Creating an API client object

```python
from listmonk import ListMonkClient

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
    )
```

### Endpoint Examples

Endpoint-focused examples are available under `examples/`.

```text
examples/
  bounces.py
  campaigns.py
  imports.py
  lists.py
  media.py
  public.py
  subscribers.py
  templates.py
  transactional.py
```

Copy `examples/settings.example.json` to `settings.json` at the project root and add your Listmonk URL and API
credentials to run them locally. The examples also accept `examples/settings.json` if you prefer to keep local example
settings beside the example files.

Most scripts are read-only by default. Actions that create, update, delete, upload, blocklist, change defaults, or send
messages are guarded by settings flags such as `create_test_data`, `delete_import`, `delete_uploaded_media`,
`delete_bounces`, `run_mutation_smoke`, `send_campaign_test`, `set_default_template`, and
`delete_subscriber_bounces`.

### Maintainer Smoke Tests

Release smoke tests live under `tools/live_smoke/`. They are separate from the user-facing examples and require live
Listmonk credentials.

See `tools/live_smoke/README.md`.

### Resource Paths

The API is modeled as a resource tree. Each resource exposes its path and URL, which can be useful when learning or
debugging the wrapper.

```python
from listmonk import ListMonkClient

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
    )

    print(client.lists.path)
    # /api/lists

    print(client.lists[1].path)
    # /api/lists/1

    print(client.templates[1].preview.path)
    # /api/templates/1/preview
```

### Querying Lists

```python
from listmonk import ListMonkClient
from listmonk.common import PerPage
from listmonk.lists import ListQuery

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
    )

    lists = client.lists.retrieve(ListQuery().with_per_page(PerPage.ALL))

    print("Total Lists: {}".format(lists.page.record_count))
    for item in lists.items():
        print(item.id)
        print(item.name)
```

### Pagination

Listmonk collection endpoints return `PagedResponse[T]`. The first page is available immediately through
`result.page`, and `result.data` is a shortcut for `result.page.data`. Iterating the result yields page objects, starting
with the first page and fetching continuation pages as needed. Calling `items()` flattens page boundaries and yields
typed rows.

```python
from listmonk import ListMonkClient
from listmonk.common import PerPage
from listmonk.subscribers import SubscriberQuery

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
    )

    result = client.subscribers.retrieve(
        SubscriberQuery()
        .with_page(1)
        .with_per_page(PerPage.ALL)
    )

    print("First Page: {}".format(result.page.current_page_number))
    print("Total Subscribers: {}".format(result.page.record_count))

    for subscriber in result.data:
        print(subscriber.email)

    for page in result:
        print("Page: {}".format(page.current_page_number))
        for subscriber in page:
            print(subscriber.email)
        break

    for subscriber in result.items():
        print(subscriber.email)
```

Paged Listmonk actions include:

```text
client.bounces.retrieve(...)
client.campaigns.retrieve(...)
client.lists.retrieve(...)
client.subscribers.retrieve(...)
client.subscribers.sql_query.retrieve(...)
```

### Querying Subscribers

```python
from listmonk import ListMonkClient
from listmonk.common import PerPage, SortOrder
from listmonk.subscribers import SubscriberOrderBy, SubscriberQuery

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
    )

    query = (
        SubscriberQuery()
        .with_page(1)
        .with_per_page(PerPage.ALL)
        .with_order_by(SubscriberOrderBy.NAME)
        .with_order(SortOrder.ASC)
    )

    subscribers = client.subscribers.retrieve(query)

    print("Total Subscribers: {}".format(subscribers.page.record_count))
    for subscriber in subscribers.items():
        print(subscriber.id)
        print(subscriber.email)
        print(subscriber.name)
```

### Subscriber SQL Query

Listmonk exposes SQL filtering on `GET /api/subscribers`. The wrapper models this as
`client.subscribers.sql_query`.

```python
from listmonk import ListMonkClient
from listmonk.common import PerPage
from listmonk.subscribers import SubscriberSQLQuery

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
    )

    response = client.subscribers.sql_query.retrieve(
        SubscriberSQLQuery()
        .with_sql("subscribers.id > 0")
        .with_per_page(PerPage.ALL)
    )

    print("SQL Results: {}".format(response.page.record_count))
```

This requires the `subscribers:sql_query` permission. Listmonk documents that permission as powerful because it can
bypass individual list and subscriber permission boundaries, even though the query is read-only.

### Previewing Templates

```python
from listmonk import ListMonkClient
from listmonk.templates import TemplatePreviewRender, TemplateType

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
    )

    existing = client.templates[1].preview.retrieve()
    print(existing.data)

    html = """
    <!doctype html>
    <html>
      <body>
        {{ template "content" . }}
        {{ TrackView }}
      </body>
    </html>
    """.strip()

    preview = client.templates.preview.render(
        TemplatePreviewRender(
            type=TemplateType.CAMPAIGN,
            body=html,
        )
    )
    print(preview.data)
```

Listmonk expects `POST /api/templates/preview` to be form encoded, even though template create and update use JSON. The
wrapper hides that detail behind `TemplatePreviewRender`.

### Uploading Media

```python
from listmonk import ListMonkClient
from listmonk.media import MediaUpload

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
    )

    uploaded = client.media.upload(MediaUpload.from_file("logo.png"))
    print(uploaded.data.id)
    print(uploaded.data.filename)
```

### Sending Transactional Messages

```python
from listmonk import ListMonkClient
from listmonk.transactional import (
    TransactionalContentType,
    TransactionalMessage,
    TransactionalSubscriberMode,
)

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
    )

    message = (
        TransactionalMessage()
        .with_template(1)
        .with_subscriber_mode(TransactionalSubscriberMode.EXTERNAL)
        .add_subscriber_email("user@example.com")
        .with_content_type(TransactionalContentType.HTML)
        .with_data("name", "Jane")
    )

    result = client.tx.send(message)
    print(result.status)
```

### Network Options

Network settings such as proxy, timeout, and SSL verification are configured with `RequestsOptions`.

```python
from klarient import RequestsOptions, RequestsTimeout
from listmonk import ListMonkClient

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
        options=RequestsOptions(
            timeout=RequestsTimeout(connect=10, read=120),
            proxy="http://proxy.example.com:8080",
            verify_ssl=True,
        ),
    )

    lists = client.lists.retrieve()
    print(lists.page.status)
```

### Proxy Support

A single proxy URL is used for both HTTP and HTTPS requests.

SOCKS5 proxy example:

```python
from klarient import RequestsOptions
from listmonk import ListMonkClient

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
        options=RequestsOptions(
            proxy="socks5h://proxyuser:proxypass@proxy.example.com:8128",
        ),
    )
```

HTTP proxy example:

```python
from klarient import RequestsOptions
from listmonk import ListMonkClient

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
        options=RequestsOptions(
            proxy="http://proxyuser:proxypass@proxy.example.com:8080",
        ),
    )
```

If your environment requires different proxies by scheme, pass a requests-style mapping:

```python
from klarient import RequestsOptions
from listmonk import ListMonkClient

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
        options=RequestsOptions(
            proxy={
                "http": "http://proxy.example.com:8080",
                "https": "http://secure-proxy.example.com:8080",
            },
        ),
    )
```

If your environment already uses standard proxy variables, those can also be used.

```bash
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
```

### HTTP Timeout Settings

```python
from klarient import RequestsOptions, RequestsTimeout
from listmonk import ListMonkClient

if __name__ == '__main__':
    client = ListMonkClient(
        base_url="https://listmonk.example.com",
        username="api-user",
        access_token="api-token",
        options=RequestsOptions(timeout=RequestsTimeout(connect=10, read=120)),
    )
```

### Endpoint Coverage

The wrapper models the documented Listmonk API areas:

* Bounces
* Campaigns
* Imports
* Lists
* Media
* Public list and subscription endpoints
* Subscribers
* Templates
* Transactional messages
