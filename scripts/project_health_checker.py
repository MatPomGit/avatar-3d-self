#!/usr/bin/env python3
"""Check repository-level health without pretending to validate private workstation assets."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(slots=True)
class HealthCheckResult:
    """Serializable repository health result."""

    checks_passed: int = 0
    checks_failed: int = 0
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def health_score(self) -> float:
        total = self.checks_passed + self.checks_failed
        return round(100 * self.checks_passed / total, 1) if total else 0.0


REQUIRED_DIRECTORIES = (
    "apps/avatar_studio",
    "docs/project",
    "docs/pipeline",
    "docs/capture",
    "docs/rigging",
    "docs/animation",
    "docs/speech",
    "docs/runtime",
    "docs/validation",
    "scripts",
    "tests",
    ".github/workflows",
)

REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "pyproject.toml",
    "mkdocs.yml",
    "docs/index.md",
    "docs/project/architecture.md",
    "docs/pipeline/overview.md",
    "docs/validation/acceptance-criteria.md",
    "docs/desktop/architecture.md",
)


def run_health_check(project_root: str | Path = ".") -> HealthCheckResult:
    """Validate repository structure and detect accidentally committed private workspace state."""

    root = Path(project_root)
    result = HealthCheckResult()
    for relative in REQUIRED_DIRECTORIES:
        if (root / relative).is_dir():
            result.checks_passed += 1
        else:
            result.checks_failed += 1
            result.issues.append(f"Missing directory: {relative}")
    for relative in REQUIRED_FILES:
        if (root / relative).is_file():
            result.checks_passed += 1
        else:
            result.checks_failed += 1
            result.issues.append(f"Missing file: {relative}")

    private_state = list(root.rglob(".avatar-studio/project.sqlite3"))
    if private_state:
        result.checks_failed += 1
        result.issues.append("Avatar Studio workspace database detected inside repository")
    else:
        result.checks_passed += 1

    if (root / "web").exists():
        result.warnings.append("Legacy web directory still exists; GitHub Pages should be MkDocs-only")
    return result


def main() -> int:
    """Write `project_health.json` and return non-zero for structural failures."""

    result = run_health_check()
    payload = asdict(result) | {"health_score": result.health_score}
    Path("project_health.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 1 if result.checks_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
