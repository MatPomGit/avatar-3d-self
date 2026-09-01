#!/usr/bin/env python3
"""Verify that every publishable Markdown document is present in MkDocs navigation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"


def _nav_paths(node: Any) -> set[str]:
    paths: set[str] = set()
    if isinstance(node, str):
        if node.endswith(".md"):
            paths.add(node.replace("\\", "/"))
        return paths
    if isinstance(node, list):
        for item in node:
            paths.update(_nav_paths(item))
        return paths
    if isinstance(node, dict):
        for value in node.values():
            paths.update(_nav_paths(value))
    return paths


def markdown_files() -> set[str]:
    return {
        path.relative_to(DOCS).as_posix()
        for path in DOCS.rglob("*.md")
        if "assets" not in path.relative_to(DOCS).parts
    }


def nav_files() -> set[str]:
    config = yaml.safe_load(MKDOCS.read_text(encoding="utf-8"))
    return _nav_paths(config.get("nav", []))


def validate() -> tuple[set[str], set[str]]:
    docs = markdown_files()
    nav = nav_files()
    missing_from_nav = docs - nav
    nonexistent_in_nav = nav - docs
    return missing_from_nav, nonexistent_in_nav


def main() -> int:
    missing, nonexistent = validate()
    if missing:
        print("Markdown files missing from mkdocs.yml nav:")
        for path in sorted(missing):
            print(f"  - {path}")
    if nonexistent:
        print("mkdocs.yml nav entries pointing to missing files:")
        for path in sorted(nonexistent):
            print(f"  - {path}")
    if missing or nonexistent:
        return 1
    print(f"MkDocs navigation covers all {len(markdown_files())} Markdown documents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
