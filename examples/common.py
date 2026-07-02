from __future__ import annotations

import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

# When these examples are run from a source checkout, make the local package
# importable without requiring an editable install first. Installed packages do
# not need this path entry.
SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from klarient import Resource  # noqa: E402
from listmonk import ListMonkClient  # noqa: E402

T = TypeVar("T")


def load_settings(path: str | Path = "settings.json") -> dict[str, Any]:
    settings_path = Path(path)
    if not settings_path.is_absolute():
        settings_path = Path(__file__).resolve().parent / settings_path
    if not settings_path.exists():
        settings_path = Path(__file__).resolve().parents[1] / "settings.json"
    return json.loads(settings_path.read_text())


def setting(settings: dict[str, Any], name: str, default: T | None = None) -> T | None:
    value = settings.get(name, default)
    if isinstance(value, str) and value.startswith("optional/"):
        return default
    if isinstance(value, str) and value.startswith("optional-"):
        return default
    return value


def enabled(settings: dict[str, Any], name: str) -> bool:
    return bool(settings.get(name, False))


def skip(message: str) -> None:
    print(f"SKIP: {message}")


def show_resource(label: str, resource: Resource) -> None:
    # Every Klarient resource knows the URI path it models and the final URL
    # that will be called. Printing both is useful when learning how the Python
    # object tree maps to the REST API tree.
    print(f"{label}:")
    print(f"  path: {resource.path}")
    print(f"  url:  {resource.url}")


def run_optional(label: str, action: Callable[[], T]) -> T | None:
    try:
        return action()
    except Exception as exc:
        skip(f"{label}: {type(exc).__name__}: {exc}")
        return None
