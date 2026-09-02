"""Reproducible project reporting for Avatar Studio."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from avatar_studio.pipeline import STAGES
from avatar_studio.store import ProjectStore


def build_project_report(store: ProjectStore) -> dict[str, Any]:
    """Build a JSON-safe snapshot of project state, provenance and quality gates."""

    statuses = store.stage_statuses()
    passed, total, percentage = store.progress()
    stages: list[dict[str, Any]] = []
    for stage in STAGES:
        artifacts = store.artifacts_for_stage(stage.stage_id)
        validations = store.validation_results(stage.stage_id)
        waivers = store.waivers(stage.stage_id)
        stages.append(
            {
                "id": stage.stage_id,
                "order": stage.order,
                "title": stage.title,
                "status": statuses.get(stage.stage_id, "pending"),
                "dependencies": list(stage.dependencies),
                "expected_outputs": list(stage.expected_outputs),
                "artifacts": [
                    {
                        "id": item["id"],
                        "path": item["path"],
                        "kind": item["kind"],
                        "sha256": item["sha256"],
                        "size_bytes": item["size_bytes"],
                        "created_at": item["created_at"],
                        "metadata": item["metadata"],
                    }
                    for item in artifacts
                ],
                "validations": validations,
                "waivers": waivers,
            }
        )

    runs = store.tool_runs()
    failed_runs = sum(run["exit_code"] not in (None, 0) for run in runs)
    validation_failures = sum(
        check["status"] == "failed"
        for stage in stages
        for check in stage["validations"]
    )
    waiver_count = sum(len(stage["waivers"]) for stage in stages)

    return {
        "schema": "avatar-studio-project-report-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(store.workspace),
        "project_created_at": store.meta("created_at"),
        "summary": {
            "passed_stages": passed,
            "total_stages": total,
            "completion_percentage": round(percentage, 2),
            "tool_runs": len(runs),
            "failed_tool_runs": failed_runs,
            "validation_failures": validation_failures,
            "waivers": waiver_count,
        },
        "tool_configuration": {
            name: store.tool_path(name)
            for name in ("blender", "colmap", "ffmpeg", "piper")
        },
        "stages": stages,
        "tool_runs": runs,
    }


def _markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Avatar Studio project report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Workspace: `{report['workspace']}`",
        "",
        "## Summary",
        "",
        f"- Pipeline completion: **{summary['passed_stages']}/{summary['total_stages']} ({summary['completion_percentage']:.1f}%)**",
        f"- Tool runs: **{summary['tool_runs']}**, failed: **{summary['failed_tool_runs']}**",
        f"- Recorded validation failures: **{summary['validation_failures']}**",
        f"- Controlled waivers: **{summary['waivers']}**",
        "",
        "## Pipeline status",
        "",
        "| Stage | Status | Artefacts | Validation failures | Waivers |",
        "|---|---|---:|---:|---:|",
    ]
    for stage in report["stages"]:
        failures = sum(item["status"] == "failed" for item in stage["validations"])
        lines.append(
            f"| {stage['order']:02d}. {stage['title']} | {stage['status']} | "
            f"{len(stage['artifacts'])} | {failures} | {len(stage['waivers'])} |"
        )

    lines.extend(["", "## Artefacts and provenance", ""])
    for stage in report["stages"]:
        if not stage["artifacts"] and not stage["validations"] and not stage["waivers"]:
            continue
        lines.extend([f"### {stage['order']:02d}. {stage['title']}", ""])
        for artifact in stage["artifacts"]:
            lines.append(
                f"- `{artifact['path']}`  "
                f"type: `{artifact['kind']}`, SHA-256: `{artifact['sha256']}`"
            )
        for validation in stage["validations"]:
            message = validation.get("message") or ""
            lines.append(
                f"- Validation `{validation['check_id']}`: **{validation['status']}**. {message}"
            )
        for waiver in stage["waivers"]:
            lines.append(f"- Waiver: {waiver['reason']}")
        lines.append("")

    lines.extend(["## Tool runs", ""])
    if not report["tool_runs"]:
        lines.append("No external tool runs were recorded.")
    else:
        lines.extend(
            [
                "| ID | Stage | Executable | Exit code | Started | Finished |",
                "|---:|---|---|---:|---|---|",
            ]
        )
        for run in report["tool_runs"]:
            lines.append(
                f"| {run['id']} | {run.get('stage_id') or ''} | `{run['executable']}` | "
                f"{'' if run['exit_code'] is None else run['exit_code']} | "
                f"{run['started_at']} | {run.get('finished_at') or ''} |"
            )

    lines.extend(
        [
            "",
            "## Reproducibility note",
            "",
            "The JSON companion file is the canonical machine-readable snapshot. "
            "Artefact hashes and recorded external-tool invocations allow later integrity and provenance checks.",
            "",
        ]
    )
    return "\n".join(lines)


def write_project_report(store: ProjectStore, directory: str | Path | None = None) -> tuple[Path, Path]:
    """Write Markdown and JSON reports and return their paths."""

    output_dir = Path(directory).expanduser().resolve() if directory else store.reports_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_project_report(store)
    stem = "project-report"
    json_path = output_dir / f"{stem}.json"
    markdown_path = output_dir / f"{stem}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(_markdown(report), encoding="utf-8")
    return markdown_path, json_path
