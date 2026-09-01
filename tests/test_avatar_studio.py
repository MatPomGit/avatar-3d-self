"""Tests for Avatar Studio domain state without loading the GUI."""

from pathlib import Path

from avatar_studio.pipeline import STAGES, get_stage
from avatar_studio.store import ProjectStore


def test_pipeline_has_unique_ordered_stage_ids() -> None:
    ids = [stage.stage_id for stage in STAGES]
    orders = [stage.order for stage in STAGES]
    assert len(ids) == 21
    assert len(ids) == len(set(ids))
    assert orders == sorted(orders)
    assert get_stage("21-runtime-validation").dependencies == ("20-export",)


def test_store_unlocks_dependent_stage(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    statuses = store.stage_statuses()
    assert statuses["01-reference-acquisition"] == "ready"
    assert statuses["02-photogrammetry"] == "pending"

    store.set_stage_status("01-reference-acquisition", "passed")
    statuses = store.stage_statuses()
    assert statuses["02-photogrammetry"] == "ready"


def test_store_registers_artifact_with_hash(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    artifact = tmp_path / "capture_manifest.json"
    artifact.write_text('{"schema_version": 1}', encoding="utf-8")
    artifact_id = store.register_artifact("01-reference-acquisition", artifact)
    records = store.artifacts_for_stage("01-reference-acquisition")
    assert artifact_id > 0
    assert records[0]["path"] == str(artifact.resolve())
    assert len(records[0]["sha256"]) == 64
