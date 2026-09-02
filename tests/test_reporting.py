import json
from pathlib import Path

from avatar_studio.reporting import build_project_report, write_project_report
from avatar_studio.store import ProjectStore


def test_project_report_contains_stage_artifact_hash_and_quality_summary(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    artifact = tmp_path / "capture_manifest.json"
    artifact.write_text('{"capture": "ok"}\n', encoding="utf-8")
    artifact_id = store.register_artifact("01-reference-acquisition", artifact)
    stored = store.artifact(artifact_id)
    assert stored is not None

    store.add_validation_result(
        "01-reference-acquisition",
        "manifest_valid",
        "passed",
        message="Manifest parsed successfully.",
    )
    store.set_stage_status("01-reference-acquisition", "passed")

    report = build_project_report(store)
    assert report["schema"] == "avatar-studio-project-report-v1"
    assert report["summary"]["passed_stages"] == 1
    first = report["stages"][0]
    assert first["status"] == "passed"
    assert first["artifacts"][0]["sha256"] == stored["sha256"]
    assert first["validations"][0]["check_id"] == "manifest_valid"


def test_write_project_report_creates_markdown_and_json(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    markdown_path, json_path = write_project_report(store)

    assert markdown_path.is_file()
    assert json_path.is_file()
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["summary"]["total_stages"] == 21
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "# Avatar Studio project report" in markdown
    assert "Pipeline completion" in markdown
