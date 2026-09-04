"""Tests for the photogrammetry photo quality module."""

from __future__ import annotations

import pytest

from avatar_studio.photo_quality import PhotoQualityThresholds, _evaluate_metrics


def test_quality_thresholds_flag_blur_exposure_and_low_contrast() -> None:
    metrics = {
        "sharpness_laplacian_variance": 20.0,
        "mean_luma": 25.0,
        "contrast_stddev": 10.0,
        "shadow_clipped_fraction": 0.12,
        "highlight_clipped_fraction": 0.0,
    }

    reasons = _evaluate_metrics(metrics, PhotoQualityThresholds())

    assert "blur_or_defocus" in reasons
    assert "underexposed" in reasons
    assert "low_contrast" in reasons
    assert "shadow_clipping" in reasons


def test_analyze_photo_batch_reports_recapture_for_flat_images(tmp_path) -> None:
    cv2 = pytest.importorskip("cv2")
    np = pytest.importorskip("numpy")
    from avatar_studio.photo_quality import analyze_photo_batch

    photos = tmp_path / "photos"
    photos.mkdir()
    first = np.full((480, 640, 3), 120, dtype=np.uint8)
    second = np.full((480, 640, 3), 122, dtype=np.uint8)
    assert cv2.imwrite(str(photos / "001.png"), first)
    assert cv2.imwrite(str(photos / "002.png"), second)

    report = analyze_photo_batch(photos)

    assert report["summary"]["photo_count"] == 2
    assert report["summary"]["recapture_suggested"] == 2
    assert "001.png" in report["recapture_suggestions"]
    assert "002.png" in report["recapture_suggestions"]
