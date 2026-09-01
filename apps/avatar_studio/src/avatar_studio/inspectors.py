"""Lightweight local artefact inspectors used by Avatar Studio."""

from __future__ import annotations

import json
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Any


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
MESH_SUFFIXES = {".obj", ".ply", ".stl", ".glb", ".gltf", ".fbx"}


@dataclass(frozen=True, slots=True)
class InspectionResult:
    """Normalized result returned by an artefact inspector."""

    kind: str
    metadata: dict[str, Any]
    warnings: tuple[str, ...] = ()


def inspect_artifact(path: str | Path) -> InspectionResult:
    """Inspect a local artefact without requiring a specific DCC application."""

    artifact = Path(path).expanduser().resolve()
    if not artifact.is_file():
        raise FileNotFoundError(artifact)

    suffix = artifact.suffix.lower()
    base = {
        "name": artifact.name,
        "suffix": suffix,
        "size_bytes": artifact.stat().st_size,
    }

    if suffix in IMAGE_SUFFIXES:
        return _inspect_image(artifact, base)
    if suffix == ".wav":
        return _inspect_wave(artifact, base)
    if suffix == ".json":
        return _inspect_json(artifact, base)
    if suffix in MESH_SUFFIXES:
        return _inspect_mesh(artifact, base)
    if suffix == ".blend":
        return InspectionResult("blender_scene", base, ("Deep .blend inspection requires Blender.",))
    return InspectionResult("file", base)


def _inspect_image(path: Path, base: dict[str, Any]) -> InspectionResult:
    try:
        from PIL import Image
    except ImportError:
        return InspectionResult("image", base, ("Install the vision extra for image dimensions.",))

    with Image.open(path) as image:
        metadata = {
            **base,
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "format": image.format,
            "megapixels": round((image.width * image.height) / 1_000_000, 3),
        }
    return InspectionResult("image", metadata)


def _inspect_wave(path: Path, base: dict[str, Any]) -> InspectionResult:
    with wave.open(str(path), "rb") as audio:
        frames = audio.getnframes()
        sample_rate = audio.getframerate()
        metadata = {
            **base,
            "channels": audio.getnchannels(),
            "sample_rate_hz": sample_rate,
            "sample_width_bytes": audio.getsampwidth(),
            "frames": frames,
            "duration_seconds": round(frames / sample_rate, 4) if sample_rate else 0.0,
        }
    return InspectionResult("audio", metadata)


def _inspect_json(path: Path, base: dict[str, Any]) -> InspectionResult:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return InspectionResult("json", base, (f"Invalid JSON: {exc}",))

    metadata = {**base, "root_type": type(payload).__name__}
    if isinstance(payload, dict):
        metadata["top_level_keys"] = sorted(str(key) for key in payload.keys())[:100]
        metadata["top_level_key_count"] = len(payload)
    elif isinstance(payload, list):
        metadata["item_count"] = len(payload)
    return InspectionResult("json", metadata)


def _inspect_mesh(path: Path, base: dict[str, Any]) -> InspectionResult:
    try:
        import trimesh
    except ImportError:
        return InspectionResult("model_3d", base, ("Install the geometry extra for mesh metrics.",))

    try:
        loaded = trimesh.load(path, force="scene")
        geometries = list(loaded.geometry.values())
        vertices = sum(len(mesh.vertices) for mesh in geometries)
        faces = sum(len(mesh.faces) for mesh in geometries if hasattr(mesh, "faces"))
        metadata = {
            **base,
            "geometry_count": len(geometries),
            "vertices": vertices,
            "faces": faces,
            "triangles": faces,
        }
        if geometries:
            bounds = loaded.bounds
            metadata["bounds_min"] = [round(float(value), 6) for value in bounds[0]]
            metadata["bounds_max"] = [round(float(value), 6) for value in bounds[1]]
            metadata["extents"] = [round(float(value), 6) for value in loaded.extents]
        return InspectionResult("model_3d", metadata)
    except Exception as exc:  # third-party parsers expose heterogeneous errors
        return InspectionResult("model_3d", base, (f"Mesh inspection failed: {exc}",))
