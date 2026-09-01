#!/usr/bin/env python3
"""Export a rigged avatar from an Unreal Engine project to production FBX.

The exporter does not assume that the Unreal `.uproject` filename matches the
GitHub repository name. This keeps the integration stable across repository
renames and allows an external Unreal validation project to be used.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import subprocess
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnrealExporter:
    def __init__(self, ue_project_path: str, engine_path: str | None = None):
        self.uproject = self._resolve_uproject(Path(ue_project_path))
        self.editor_exe = self._resolve_editor(Path(engine_path) if engine_path else None)

    @staticmethod
    def _resolve_uproject(project: Path) -> Path:
        candidate = project.expanduser().resolve()
        if candidate.is_file() and candidate.suffix.lower() == ".uproject":
            return candidate
        if not candidate.is_dir():
            raise FileNotFoundError(f"Unreal project path does not exist: {candidate}")

        projects = sorted(candidate.glob("*.uproject"))
        if len(projects) == 1:
            return projects[0]
        if not projects:
            raise FileNotFoundError(f"No .uproject file found in {candidate}")
        names = ", ".join(path.name for path in projects)
        raise RuntimeError(
            f"Multiple .uproject files found in {candidate}: {names}. Pass the required file explicitly."
        )

    @staticmethod
    def _editor_candidates(engine_root: Path) -> list[Path]:
        return [
            engine_root / "Binaries" / "Win64" / "UnrealEditor-Cmd.exe",
            engine_root / "Binaries" / "Win64" / "UnrealEditor.exe",
            engine_root / "Binaries" / "Linux" / "UnrealEditor-Cmd",
            engine_root / "Binaries" / "Linux" / "UnrealEditor",
            engine_root / "Binaries" / "Linux" / "UE4Editor",
        ]

    def _resolve_editor(self, explicit: Path | None) -> Path:
        if explicit:
            explicit = explicit.expanduser().resolve()
            if explicit.is_file():
                return explicit
            for editor in self._editor_candidates(explicit):
                if editor.exists():
                    return editor
            raise FileNotFoundError(f"Unreal editor executable not found under: {explicit}")

        engine_roots = [
            Path.home() / "UnrealEngine" / "Engine",
            Path("/opt/UnrealEngine/Engine"),
            Path("C:/Program Files/Epic Games/UE_5.6/Engine"),
            Path("C:/Program Files/Epic Games/UE_5.5/Engine"),
            Path("C:/Program Files/Epic Games/UE_5.4/Engine"),
            Path("C:/Program Files/Epic Games/UE_5.3/Engine"),
        ]
        for root in engine_roots:
            for editor in self._editor_candidates(root):
                if editor.exists():
                    return editor
        raise FileNotFoundError("Unreal Engine not found. Specify --engine.")

    def export_skeletal_mesh(self, character_path: str, output_fbx: str) -> bool:
        """Export the selected character and verify that an FBX file was produced."""

        output_file = Path(output_fbx).expanduser().resolve()
        output_file.parent.mkdir(parents=True, exist_ok=True)
        export_cmd = [
            str(self.editor_exe),
            str(self.uproject),
            "-run=ResavePackages",
            f"-FbxExportDir={output_file}",
            "-unattended",
            "-silent",
            "-notheme",
        ]

        logger.info("Exporting %s from %s", character_path, self.uproject)
        logger.info("Command: %s", " ".join(export_cmd))

        try:
            result = subprocess.run(
                export_cmd,
                check=True,
                capture_output=True,
                text=True,
                timeout=600,
            )
            if result.stdout:
                logger.info(result.stdout)
        except subprocess.TimeoutExpired:
            logger.error("Export timed out (>10 min)")
            return False
        except subprocess.CalledProcessError as exc:
            logger.error("Export failed: %s", exc.stderr or exc)
            return False

        if not output_file.exists():
            logger.error("Export did not produce FBX file: %s", output_file)
            return False

        size_mb = output_file.stat().st_size / (1024**2)
        logger.info("Exported FBX: %s (%.1f MB)", output_file, size_mb)
        return True

    def validate_fbx_blendshapes(self, fbx_path: str, expected_blendshapes: list[str]) -> dict:
        """Perform a lightweight binary FBX check for expected morph-target names."""

        path = Path(fbx_path)
        report = {
            "fbx_file": str(path),
            "file_size_mb": path.stat().st_size / (1024**2),
            "blendshapes_found": [],
            "blendshapes_missing": [],
            "status": "unknown",
        }

        try:
            content = path.read_bytes()
            if b"Kaydara FBX Binary" not in content[:100]:
                report["status"] = "invalid_or_ascii_fbx"
                return report
            report["status"] = "valid_binary_fbx"
            for name in expected_blendshapes:
                target = report["blendshapes_found"] if name.encode() in content else report["blendshapes_missing"]
                target.append(name)
        except OSError as exc:
            report["status"] = f"validation_error: {exc}"
        return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Unreal Engine FBX export")
    parser.add_argument(
        "--project",
        default=".",
        help="Path to a .uproject file or a directory containing exactly one .uproject file.",
    )
    parser.add_argument(
        "--engine",
        default=None,
        help="Path to the Unreal Engine root or directly to UnrealEditor/UnrealEditor-Cmd.",
    )
    parser.add_argument("--character", default="/Game/Characters/Avatar")
    parser.add_argument("--output", default="exports/avatar_final.fbx")
    parser.add_argument(
        "--expected-morph",
        action="append",
        default=[],
        help="Morph target name expected in the exported binary FBX. May be repeated.",
    )
    args = parser.parse_args()

    exporter = UnrealExporter(args.project, args.engine)
    if not exporter.export_skeletal_mesh(args.character, args.output):
        return 1

    if args.expected_morph:
        report = exporter.validate_fbx_blendshapes(args.output, args.expected_morph)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        if report["blendshapes_missing"]:
            logger.error("Missing expected morph targets")
            return 2

    logger.info("Export complete and validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
