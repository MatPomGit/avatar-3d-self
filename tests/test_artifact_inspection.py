"""Tests for Avatar Studio artefact inspection."""

from __future__ import annotations

import json
import wave
from pathlib import Path

from avatar_studio.inspectors import inspect_artifact
from avatar_studio.store import ProjectStore


def test_json_inspection(tmp_path: Path) -> None:
    path = tmp_path / "capture_manifest.json"
    path.write_text(json.dumps({"camera": "test", "images": 42}), encoding="utf-8")

    result = inspect_artifact(path)

    assert result.kind == "json"
    assert result.metadata["top_level_key_count"] == 2
    assert result.metadata["top_level_keys"] == ["camera", "images"]


def test_wave_inspection(tmp_path: Path) -> None:
    path = tmp_path / "speech.wav"
    with wave.open(str(path), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(16_000)
        audio.writeframes(b"\x00\x00" * 16_000)

    result = inspect_artifact(path)

    assert result.kind == "audio"
    assert result.metadata["sample_rate_hz"] == 16_000
    assert result.metadata["duration_seconds"] == 1.0


def test_store_registers_inspected_metadata(tmp_path: Path) -> None:
    artifact = tmp_path / "capture_manifest.json"
    artifact.write_text("{}", encoding="utf-8")
    store = ProjectStore(tmp_path / "workspace")

    artifact_id = store.register_artifact("01-reference-acquisition", artifact)
    stored = store.artifact(artifact_id)

    assert stored is not None
    assert stored["kind"] == "json"
    assert stored["metadata"]["root_type"] == "dict"
    assert len(stored["sha256"]) == 64
