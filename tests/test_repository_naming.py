from pathlib import Path


ROOT = Path(__file__).parents[1]
LEGACY_REPOSITORY_NAME = "avatar" + "-3d-self"
TEXT_EXTENSIONS = {".md", ".yml", ".yaml", ".py", ".toml", ".json", ".txt"}
SCAN_ROOTS = (
    ROOT / "README.md",
    ROOT / "mkdocs.yml",
    ROOT / "pyproject.toml",
    ROOT / "docs",
    ROOT / "apps",
    ROOT / "scripts",
    ROOT / ".github",
)


def iter_text_files():
    for root in SCAN_ROOTS:
        if root.is_file():
            yield root
            continue
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
                yield path


def test_legacy_repository_name_is_not_reintroduced():
    offenders = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if LEGACY_REPOSITORY_NAME in text:
            offenders.append(str(path.relative_to(ROOT)))

    assert not offenders, (
        "Legacy repository identifier found in active project files: "
        + ", ".join(sorted(offenders))
    )
