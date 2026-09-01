#!/usr/bin/env python3
"""Small deterministic helpers shared by local checks and CI."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


def run(command: list[str], cwd: Path) -> dict[str, object]:
    """Run one command and return a compact serializable result."""

    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout[-4000:],
        "stderr": completed.stderr[-4000:],
    }


def build_report(project_root: str | Path = ".") -> dict[str, object]:
    """Run checks that are valid in a clean repository clone."""

    root = Path(project_root).resolve()
    checks = {
        "tests": run(["python", "-m", "pytest", "-q"], root),
        "ruff": run(["ruff", "check", "scripts", "apps", "tests"], root),
        "docs": run(["mkdocs", "build", "--strict"], root),
    }
    success = all(item["returncode"] == 0 for item in checks.values())
    return {"success": success, "checks": checks}


def main() -> int:
    """Write the CI report to `artifacts/build_report.json`."""

    report = build_report()
    output = Path("artifacts/build_report.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
