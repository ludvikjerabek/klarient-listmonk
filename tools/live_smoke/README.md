# Listmonk Live Smoke Tests

These scripts are maintainer release checks, not user examples. They require live Listmonk credentials and are meant to
validate that the modeled resource tree still matches a real Listmonk instance.

## Settings

Copy `examples/settings.example.json` to `settings.json` at the project root, or place `settings.json` in this
directory.

Required settings:

- `base_url`
- `username`
- `access_token` or `password`

Optional settings used by the smoke tests:

- `subscriber_sql_query`
- `mutation_from_email` or `campaign_from_email`
- `campaign_messenger`
- `run_mutation_smoke`

## Read-Only Smoke Test

```bash
PYTHONPATH=src python3 tools/live_smoke/read_only.py
```

The read-only smoke test calls safe collection and detail endpoints across lists, subscribers, campaigns, bounces,
imports, media, templates, and public lists. It prints status, page metadata for paged resources, and pagination links
where available.

The script deliberately skips endpoints that create public subscriptions or send transactional messages.

## Mutation Smoke Test

```bash
PYTHONPATH=src python3 tools/live_smoke/mutation.py
```

`mutation.py` requires `run_mutation_smoke=true` in `settings.json`. It creates temporary records with a
`klarient-smoke-*` prefix and removes only the records it created.

The mutation test exercises list, subscriber, template, media, and campaign mutation paths when the required settings
are present. Campaign creation is skipped unless `mutation_from_email` or `campaign_from_email` is configured.

Email-sending paths remain skipped by default.
