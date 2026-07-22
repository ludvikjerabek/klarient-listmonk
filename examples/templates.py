from __future__ import annotations

from common import enabled, load_settings, run_optional, setting, skip
from listmonk import ListMonkClient
from listmonk.templates import (
    TemplateCreate,
    TemplatePreviewRender,
    TemplateType,
    TemplateUpdate,
)

CAMPAIGN_TEMPLATE_BODY = """
<!doctype html>
<html>
<body>
    <main>
        {{ template "content" . }}
    </main>
</body>
</html>
""".strip()


def main() -> None:
    settings = load_settings()
    client = ListMonkClient(
        base_url=settings["base_url"],
        username=settings.get("username"),
        access_token=settings.get("access_token") or settings.get("password"),
    )

    # The Python object tree mirrors the REST API tree. The template collection
    # is /api/templates, and child resources model the item and preview paths.
    print("Template collection resource:")
    print(f"  path: {client.templates.path}")
    print(f"  url:  {client.templates.url}")

    templates = client.templates.retrieve()
    print(f"templates={len(templates.data)}")

    template_id = setting(settings, "template_id")
    if template_id is not None:
        template_resource = client.templates[template_id]
        # /api/templates/{template_id} and
        # /api/templates/{template_id}/preview are distinct resources.
        print("Single template resource:")
        print(f"  path: {template_resource.path}")
        print(f"  url:  {template_resource.url}")
        print("Template preview resource:")
        print(f"  path: {template_resource.preview.path}")
        print(f"  url:  {template_resource.preview.url}")
        print("Template default resource:")
        print(f"  path: {template_resource.default.path}")
        print(f"  url:  {template_resource.default.url}")

        template = template_resource.retrieve()
        print(f"template={template.data.id} name={template.data.name}")

        preview = run_optional(
            "retrieve template preview",
            lambda: template_resource.preview.retrieve(),
        )
        if preview is not None:
            print(f"preview_chars={len(preview.data)}")

        if enabled(settings, "set_default_template"):
            defaulted = template_resource.default.update()
            print(f"default_template={defaulted.data.id}")
        else:
            skip("set set_default_template=true to make template_id the default template")

    # The render-preview endpoint lives on the collection, so it is modeled as
    # client.templates.preview instead of template_resource.preview.
    print("Render preview resource:")
    print(f"  path: {client.templates.preview.path}")
    print(f"  url:  {client.templates.preview.url}")
    # Campaign HTML templates must include the content placeholder exactly once.
    # Listmonk uses this slot later when rendering campaign-specific content.
    rendered = client.templates.preview.render(
        TemplatePreviewRender(
            type=TemplateType.CAMPAIGN,
            body=CAMPAIGN_TEMPLATE_BODY,
        )
    )
    print(f"rendered_chars={len(rendered.data)}")

    if not enabled(settings, "create_test_data"):
        skip("set create_test_data=true to create, update, and delete a template")
        return

    created = client.templates.create(
        TemplateCreate(
            name="Klarient Example",
            type=TemplateType.CAMPAIGN,
            body=CAMPAIGN_TEMPLATE_BODY,
        )
    )
    print(f"created={created.data.id}")

    created_resource = client.templates[created.data.id]
    print("Created template resource:")
    print(f"  path: {created_resource.path}")
    print(f"  url:  {created_resource.url}")

    updated = created_resource.update(
        TemplateUpdate(
            name="Klarient Example Updated",
            type=TemplateType.CAMPAIGN,
            body=CAMPAIGN_TEMPLATE_BODY,
        )
    )
    print(f"updated={updated.data.name}")

    deleted = created_resource.delete()
    print(f"deleted={deleted.data}")


if __name__ == "__main__":
    main()
