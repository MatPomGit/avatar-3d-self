"""Photogrammetry photo-set quality analysis and non-destructive preprocessing."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


ProgressCallback = Callable[[int, str], None]
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}


@dataclass(frozen=True)
class PhotoQualityThresholds:
    """Configurable thresholds used by the pre-photogrammetry quality gate."""

    min_sharpness: float = 80.0
    min_mean_luma: float = 45.0
    max_mean_luma: float = 210.0
    min_contrast: float = 28.0
    max_clipped_fraction: float = 0.08
    min_overlap_score: float = 0.18
    min_overlap_matches: int = 30


def _load_cv2_numpy():
    try:
        import cv2  # type: ignore
        import numpy as np  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "Photo quality analysis requires the 'vision' optional dependencies. "
            "Install with: pip install -e '.[desktop,vision]'"
        ) from exc
    return cv2, np


def _image_paths(directory: str | Path) -> list[Path]:
    root = Path(directory).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(root)
    images = sorted(
        path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )
    if not images:
        raise ValueError("No supported image files were found in the selected directory")
    return images


def _resize_for_analysis(image, cv2, *, max_edge: int = 1600):
    height, width = image.shape[:2]
    edge = max(height, width)
    if edge <= max_edge:
        return image
    scale = max_edge / edge
    return cv2.resize(image, (round(width * scale), round(height * scale)), interpolation=cv2.INTER_AREA)


def _quality_metrics(image, cv2, np) -> dict[str, float]:
    analysis = _resize_for_analysis(image, cv2)
    gray = cv2.cvtColor(analysis, cv2.COLOR_BGR2GRAY)
    luma = float(np.mean(gray))
    contrast = float(np.std(gray))
    sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    shadow_clip = float(np.mean(gray <= 5))
    highlight_clip = float(np.mean(gray >= 250))
    return {
        "sharpness_laplacian_variance": round(sharpness, 3),
        "mean_luma": round(luma, 3),
        "contrast_stddev": round(contrast, 3),
        "shadow_clipped_fraction": round(shadow_clip, 5),
        "highlight_clipped_fraction": round(highlight_clip, 5),
    }


def _evaluate_metrics(metrics: dict[str, float], thresholds: PhotoQualityThresholds) -> list[str]:
    reasons: list[str] = []
    if metrics["sharpness_laplacian_variance"] < thresholds.min_sharpness:
        reasons.append("blur_or_defocus")
    if metrics["mean_luma"] < thresholds.min_mean_luma:
        reasons.append("underexposed")
    if metrics["mean_luma"] > thresholds.max_mean_luma:
        reasons.append("overexposed")
    if metrics["contrast_stddev"] < thresholds.min_contrast:
        reasons.append("low_contrast")
    if metrics["shadow_clipped_fraction"] > thresholds.max_clipped_fraction:
        reasons.append("shadow_clipping")
    if metrics["highlight_clipped_fraction"] > thresholds.max_clipped_fraction:
        reasons.append("highlight_clipping")
    return reasons


def _overlap_metrics(previous, current, cv2, np) -> dict[str, float | int | None]:
    previous = _resize_for_analysis(previous, cv2, max_edge=1200)
    current = _resize_for_analysis(current, cv2, max_edge=1200)
    prev_gray = cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)

    detector = cv2.ORB_create(nfeatures=2500, fastThreshold=12)
    kp1, des1 = detector.detectAndCompute(prev_gray, None)
    kp2, des2 = detector.detectAndCompute(curr_gray, None)
    if des1 is None or des2 is None or len(kp1) < 8 or len(kp2) < 8:
        return {"matches": 0, "inliers": 0, "inlier_ratio": 0.0, "overlap_score": 0.0}

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    pairs = matcher.knnMatch(des1, des2, k=2)
    good = [first for first, second in pairs if first.distance < 0.75 * second.distance]
    if len(good) < 8:
        return {
            "matches": len(good),
            "inliers": 0,
            "inlier_ratio": 0.0,
            "overlap_score": 0.0,
        }

    src = np.float32([kp1[item.queryIdx].pt for item in good]).reshape(-1, 1, 2)
    dst = np.float32([kp2[item.trainIdx].pt for item in good]).reshape(-1, 1, 2)
    _, mask = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
    inliers = int(mask.sum()) if mask is not None else 0
    inlier_ratio = inliers / len(good) if good else 0.0
    feature_support = min(1.0, inliers / 120.0)
    overlap_score = inlier_ratio * feature_support
    return {
        "matches": len(good),
        "inliers": inliers,
        "inlier_ratio": round(float(inlier_ratio), 4),
        "overlap_score": round(float(overlap_score), 4),
    }


def analyze_photo_batch(
    photo_directory: str | Path,
    *,
    thresholds: PhotoQualityThresholds | None = None,
    progress_callback: ProgressCallback | None = None,
) -> dict:
    """Analyze per-image quality and sequential overlap for a capture batch."""

    cv2, np = _load_cv2_numpy()
    root = Path(photo_directory).expanduser().resolve()
    paths = _image_paths(root)
    thresholds = thresholds or PhotoQualityThresholds()
    records: list[dict] = []
    recapture: list[str] = []
    low_overlap_pairs: list[dict] = []
    previous_image = None
    previous_relative: str | None = None

    for index, path in enumerate(paths, start=1):
        image = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if image is None:
            relative = str(path.relative_to(root))
            records.append({"path": relative, "status": "failed", "reasons": ["decode_failed"]})
            recapture.append(relative)
            continue

        relative = str(path.relative_to(root))
        metrics = _quality_metrics(image, cv2, np)
        reasons = _evaluate_metrics(metrics, thresholds)
        overlap = None
        if previous_image is not None and previous_relative is not None:
            overlap = _overlap_metrics(previous_image, image, cv2, np)
            if (
                int(overlap["matches"] or 0) < thresholds.min_overlap_matches
                or float(overlap["overlap_score"] or 0.0) < thresholds.min_overlap_score
            ):
                reasons.append("insufficient_overlap_with_previous")
                low_overlap_pairs.append(
                    {"previous": previous_relative, "current": relative, **overlap}
                )
        if reasons:
            recapture.append(relative)
        records.append(
            {
                "path": relative,
                "status": "review" if reasons else "passed",
                "reasons": reasons,
                "metrics": metrics,
                "overlap_with_previous": overlap,
            }
        )
        previous_image = image
        previous_relative = relative
        if progress_callback:
            progress_callback(round(index / len(paths) * 100), f"Analyzing photo quality ({index}/{len(paths)})")

    return {
        "schema": "avatar-studio-photo-quality-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "photo_directory": str(root),
        "thresholds": asdict(thresholds),
        "summary": {
            "photo_count": len(paths),
            "passed": sum(item["status"] == "passed" for item in records),
            "review": sum(item["status"] != "passed" for item in records),
            "recapture_suggested": len(set(recapture)),
            "low_overlap_pairs": len(low_overlap_pairs),
        },
        "recapture_suggestions": sorted(set(recapture)),
        "low_overlap_pairs": low_overlap_pairs,
        "photos": records,
    }


def _match_luminance(image, target_luma: float, cv2, np):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    current = float(np.median(l_channel))
    if current <= 1.0:
        return image
    scale = target_luma / current
    adjusted = np.clip(l_channel.astype(np.float32) * scale, 0, 255).astype(np.uint8)
    return cv2.cvtColor(cv2.merge((adjusted, a_channel, b_channel)), cv2.COLOR_LAB2BGR)


def _remove_static_background(image, background, cv2, np, *, threshold: int = 24):
    if background.shape[:2] != image.shape[:2]:
        background = cv2.resize(background, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_LINEAR)
    delta = cv2.absdiff(image, background)
    distance = np.max(delta, axis=2).astype(np.uint8)
    mask = cv2.threshold(distance, threshold, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    return cv2.cvtColor(cv2.merge((image[:, :, 0], image[:, :, 1], image[:, :, 2], mask)), cv2.COLOR_BGRA2RGBA)


def preprocess_photo_batch(
    photo_directory: str | Path,
    output_directory: str | Path,
    *,
    normalize_lighting: bool = False,
    improve_contrast: bool = False,
    background_image: str | Path | None = None,
    progress_callback: ProgressCallback | None = None,
) -> dict:
    """Create derived image copies for controlled photogrammetry preprocessing."""

    cv2, np = _load_cv2_numpy()
    root = Path(photo_directory).expanduser().resolve()
    output = Path(output_directory).expanduser().resolve()
    if output == root:
        raise ValueError("Output directory must differ from the source directory")
    paths = _image_paths(root)
    output.mkdir(parents=True, exist_ok=True)

    background = None
    if background_image is not None:
        background = cv2.imread(str(Path(background_image).expanduser().resolve()), cv2.IMREAD_COLOR)
        if background is None:
            raise ValueError(f"Cannot decode background image: {background_image}")

    target_luma = None
    if normalize_lighting:
        medians: list[float] = []
        for path in paths:
            image = cv2.imread(str(path), cv2.IMREAD_COLOR)
            if image is None:
                continue
            lab = cv2.cvtColor(_resize_for_analysis(image, cv2), cv2.COLOR_BGR2LAB)
            medians.append(float(np.median(lab[:, :, 0])))
        if medians:
            target_luma = float(np.median(medians))

    written: list[str] = []
    for index, path in enumerate(paths, start=1):
        image = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if image is None:
            continue
        processed = image
        if target_luma is not None:
            processed = _match_luminance(processed, target_luma, cv2, np)
        if improve_contrast:
            lab = cv2.cvtColor(processed, cv2.COLOR_BGR2LAB)
            l_channel, a_channel, b_channel = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8))
            processed = cv2.cvtColor(
                cv2.merge((clahe.apply(l_channel), a_channel, b_channel)), cv2.COLOR_LAB2BGR
            )

        relative = path.relative_to(root)
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if background is not None:
            destination = destination.with_suffix(".png")
            rgba = _remove_static_background(processed, background, cv2, np)
            cv2.imwrite(str(destination), cv2.cvtColor(rgba, cv2.COLOR_RGBA2BGRA))
        else:
            cv2.imwrite(str(destination), processed)
        written.append(str(destination.relative_to(output)))
        if progress_callback:
            progress_callback(round(index / len(paths) * 100), f"Preprocessing photographs ({index}/{len(paths)})")

    report = {
        "schema": "avatar-studio-photo-preprocess-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_directory": str(root),
        "output_directory": str(output),
        "operations": {
            "normalize_lighting": normalize_lighting,
            "target_luma": round(target_luma, 3) if target_luma is not None else None,
            "improve_contrast": improve_contrast,
            "background_image": str(Path(background_image).expanduser().resolve()) if background_image else None,
        },
        "written_images": written,
    }
    report_path = output / "preprocessing_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report["report_path"] = str(report_path)
    return report
