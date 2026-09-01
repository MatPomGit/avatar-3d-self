"""Load and query Avatar Studio machine-readable technical baselines."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


@lru_cache(maxsize=4)
def load_baselines(path: str | Path = "config/technical_baselines.yaml") -> dict[str, Any]:
    """Load a versioned technical-baseline document."""

    config_path = Path(path)
    if not config_path.is_absolute():
        config_path = Path.cwd() / config_path
    if not config_path.exists():
        raise FileNotFoundError(f"Technical baseline file not found: {config_path}")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Unsupported technical-baseline schema")
    return data


def get_baseline(dotted_path: str, *, path: str | Path = "config/technical_baselines.yaml") -> Any:
    """Return a nested value using a dotted path such as behaviour.blink.duration_s."""

    value: Any = load_baselines(path)
    for component in dotted_path.split("."):
        if not isinstance(value, dict) or component not in value:
            raise KeyError(dotted_path)
        value = value[component]
    return value
