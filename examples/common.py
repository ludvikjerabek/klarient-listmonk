from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

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


def run_optional(label: str, action: Callable[[], T]) -> T | None:
    try:
        return action()
    except Exception as exc:
        skip(f"{label}: {type(exc).__name__}: {exc}")
        return None
