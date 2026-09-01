#!/usr/bin/env python3
"""Validate forbidden terminology and repository naming in active text files."""

from __future__ import annotations

from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "terminology.yaml"


def load_config() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def iter_files(config: dict):
    scan = config["scan"]
    extensions = set(scan["extensions"])
    excluded_prefixes = tuple(scan.get("exclude_prefixes", []))
    excluded_files = set(scan.get("exclude_files", []))
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative in excluded_files or relative.startswith(excluded_prefixes):
            continue
        yield relative, path


def forbidden_terms(config: dict) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for rule in config["rules"]:
        preferred = rule["preferred"]
        for term in rule.get("forbidden", []):
            result.append((term, preferred))
    return result


def lint() -> list[str]:
    config = load_config()
    prohibited = forbidden_terms(config)
    errors: list[str] = []
    for relative, path in iter_files(config):
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            lower = line.casefold()
            for forbidden, preferred in prohibited:
                if forbidden.casefold() in lower:
                    errors.append(
                        f"{relative}:{line_number}: użyj '{preferred}' zamiast '{forbidden}'"
                    )
    return errors


def main() -> int:
    errors = lint()
    if errors:
        print("Terminology validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Terminology validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
