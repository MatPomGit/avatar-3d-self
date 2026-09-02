"""Reference-photo manifest generation and pre-COLMAP quality checks."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from avatar_studio.inspectors import IMAGE_SUFFIXES, inspect_artifact


ProgressCallback = Callable[[int, str], None]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_capture_manifest(
    photo_directory: str | Path,
    *,
    min_photos: int = 60,
    min_long_edge_px: int = 3000,
    progress_callback: ProgressCallback | None = None,
) -> dict:
    """Inspect a capture set and return a reproducible manifest plus quality summary."""

    root = Path(photo_directory).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(root)
    if min_photos < 1:
        raise ValueError("min_photos must be positive")
    if min_long_edge_px < 1:
        raise ValueError("min_long_edge_px must be positive")

    photos = sorted(
        path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )
    if not photos:
        raise ValueError("No supported image files were found in the selected directory")

    records: list[dict] = []
    hashes: dict[str, list[str]] = {}
    low_resolution: list[str] = []
    inspection_warnings: list[str] = []
    total = len(photos)
    for index, path in enumerate(photos, start=1):
        inspection = inspect_artifact(path)
        digest = _sha256(path)
        relative = str(path.relative_to(root))
        width = inspection.metadata.get("width")
        height = inspection.metadata.get("height")
        long_edge = max(width, height) if isinstance(width, int) and isinstance(height, int) else None
        if long_edge is not None and long_edge < min_long_edge_px:
            low_resolution.append(relative)
        warnings = list(inspection.warnings)
        inspection_warnings.extend(f"{relative}: {warning}" for warning in warnings)
        hashes.setdefault(digest, []).append(relative)
        records.append(
            {
                "path": relative,
                "sha256": digest,
                "size_bytes": path.stat().st_size,
                "width": width,
                "height": height,
                "long_edge_px": long_edge,
                "inspection_warnings": warnings,
            }
        )
        if progress_callback:
            progress_callback(round(index / total * 90), f"Inspecting photographs ({index}/{total})")

    duplicate_groups = [paths for paths in hashes.values() if len(paths) > 1]
    issues: list[dict] = []
    if total < min_photos:
        issues.append(
            {
                "severity": "failed",
                "check": "photo_count",
                "message": f"Only {total} photographs found; at least {min_photos} are required by this profile.",
            }
        )
    if duplicate_groups:
        issues.append(
            {
                "severity": "failed",
                "check": "duplicate_files",
                "message": f"Found {len(duplicate_groups)} duplicate image group(s) by SHA-256.",
            }
        )
    if low_resolution:
        issues.append(
            {
                "severity": "warning",
                "check": "image_resolution",
                "message": f"{len(low_resolution)} image(s) have a long edge below {min_long_edge_px} px.",
            }
        )
    if inspection_warnings:
        issues.append(
            {
                "severity": "warning",
                "check": "image_inspection",
                "message": f"{len(inspection_warnings)} inspector warning(s) were recorded.",
            }
        )

    failed = any(issue["severity"] == "failed" for issue in issues)
    if progress_callback:
        progress_callback(100, "Capture manifest complete")
    return {
        "schema": "avatar-studio-capture-manifest-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "photo_directory": str(root),
        "profile": {"min_photos": min_photos, "min_long_edge_px": min_long_edge_px},
        "summary": {
            "photo_count": total,
            "duplicate_groups": len(duplicate_groups),
            "low_resolution_images": len(low_resolution),
            "inspection_warnings": len(inspection_warnings),
            "quality_gate": "failed" if failed else "passed",
        },
        "duplicate_groups": duplicate_groups,
        "low_resolution_images": low_resolution,
        "issues": issues,
        "photos": records,
    }


def write_capture_manifest(
    photo_directory: str | Path,
    output_path: str | Path,
    *,
    min_photos: int = 60,
    min_long_edge_px: int = 3000,
    progress_callback: ProgressCallback | None = None,
) -> tuple[dict, Path]:
    """Generate and persist a capture manifest."""

    report = build_capture_manifest(
        photo_directory,
        min_photos=min_photos,
        min_long_edge_px=min_long_edge_px,
        progress_callback=progress_callback,
    )
    destination = Path(output_path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report, destination
