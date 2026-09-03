"""Static contracts for GitHub Actions workflows."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
PYTHON_SCRIPT_RE = re.compile(r"(?:python(?:3)?(?:\s+-m)?\s+)(scripts/[A-Za-z0-9_./-]+\.py)")


def test_workflows_are_valid_yaml_mappings() -> None:
    for workflow in sorted(WORKFLOWS.glob("*.yml")):
        parsed = yaml.safe_load(workflow.read_text(encoding="utf-8"))
        assert isinstance(parsed, dict), f"{workflow} must contain a YAML mapping"
        assert "jobs" in parsed, f"{workflow} must define jobs"


def test_workflow_python_script_references_exist() -> None:
    missing: list[str] = []
    for workflow in sorted(WORKFLOWS.glob("*.yml")):
        text = workflow.read_text(encoding="utf-8")
        for relative in PYTHON_SCRIPT_RE.findall(text):
            if not (ROOT / relative).is_file():
                missing.append(f"{workflow.relative_to(ROOT)} -> {relative}")
    assert not missing, "Workflow references missing Python scripts:\n" + "\n".join(missing)


def test_workflows_do_not_reference_old_repository_name() -> None:
    offenders: list[str] = []
    for workflow in sorted(WORKFLOWS.glob("*.yml")):
        text = workflow.read_text(encoding="utf-8")
        if "MatPomGit/avatar-3d-self" in text:
            offenders.append(str(workflow.relative_to(ROOT)))
    assert not offenders, "Workflows still reference the retired repository name: " + ", ".join(offenders)
