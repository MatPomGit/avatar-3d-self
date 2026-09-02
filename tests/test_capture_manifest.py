from pathlib import Path

from PIL import Image

from avatar_studio.capture import build_capture_manifest


def _write_image(path: Path, size: tuple[int, int] = (3200, 2400), value: int = 127) -> None:
    image = Image.new("L", size, color=value)
    image.save(path)


def test_capture_manifest_passes_complete_unique_set(tmp_path: Path) -> None:
    photos = tmp_path / "photos"
    photos.mkdir()
    for index in range(3):
        _write_image(photos / f"photo_{index:02d}.png", value=100 + index)

    progress: list[int] = []
    report = build_capture_manifest(
        photos,
        min_photos=3,
        min_long_edge_px=3000,
        progress_callback=lambda value, _message: progress.append(value),
    )

    assert report["summary"]["quality_gate"] == "passed"
    assert report["summary"]["photo_count"] == 3
    assert report["summary"]["duplicate_groups"] == 0
    assert progress[-1] == 100


def test_capture_manifest_fails_duplicate_and_too_small_set(tmp_path: Path) -> None:
    photos = tmp_path / "photos"
    photos.mkdir()
    first = photos / "a.png"
    second = photos / "b.png"
    _write_image(first, size=(1024, 768))
    second.write_bytes(first.read_bytes())

    report = build_capture_manifest(photos, min_photos=3, min_long_edge_px=3000)

    assert report["summary"]["quality_gate"] == "failed"
    assert report["summary"]["duplicate_groups"] == 1
    assert report["summary"]["low_resolution_images"] == 2
    checks = {issue["check"] for issue in report["issues"]}
    assert {"photo_count", "duplicate_files", "image_resolution"}.issubset(checks)
