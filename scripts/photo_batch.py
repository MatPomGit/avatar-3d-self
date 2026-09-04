#!/usr/bin/env python3
"""Analyze and preprocess photogrammetry capture batches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from avatar_studio.photo_quality import analyze_photo_batch, preprocess_photo_batch


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Evaluate blur, exposure, contrast and sequential overlap")
    analyze.add_argument("photos", type=Path, help="Directory containing the capture batch")
    analyze.add_argument("--report", type=Path, default=Path("photo_quality_report.json"))

    preprocess = subparsers.add_parser("preprocess", help="Create non-destructive derived photographs")
    preprocess.add_argument("photos", type=Path, help="Directory containing source photographs")
    preprocess.add_argument("output", type=Path, help="Directory for derived photographs")
    preprocess.add_argument("--normalize-lighting", action="store_true")
    preprocess.add_argument("--improve-contrast", action="store_true")
    preprocess.add_argument("--background", type=Path, help="Empty-scene background photograph")
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.command == "analyze":
        report = analyze_photo_batch(args.photos)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Report: {args.report.resolve()}")
        print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
        if report["recapture_suggestions"]:
            print("Review / recapture suggestions:")
            for path in report["recapture_suggestions"]:
                print(f"  - {path}")
        return 0

    report = preprocess_photo_batch(
        args.photos,
        args.output,
        normalize_lighting=args.normalize_lighting,
        improve_contrast=args.improve_contrast,
        background_image=args.background,
    )
    print(f"Derived set: {report['output_directory']}")
    print(f"Report: {report['report_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
