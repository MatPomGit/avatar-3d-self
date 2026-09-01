#!/usr/bin/env python3
"""Export a rigged character from an Unreal Engine project to FBX.

The Unreal project filename is deliberately independent from the GitHub repository
name. Pass either a `.uproject` file or a directory containing exactly one project.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess


def resolve_uproject(project: str | Path) -> Path:
    """Resolve an Unreal project without assuming that it matches the repository name."""

    candidate = Path(project).expanduser().resolve()
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


def export_from_unreal(
    project: str,
    output_fbx: str,
    editor_exe: str,
) -> bool:
    """Run the Unreal command-line export and verify that the expected FBX exists."""

    uproject = resolve_uproject(project)
    output_path = Path(output_fbx).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        editor_exe,
        str(uproject),
        "-run=ResavePackages",
        f"-FbxExportDir={output_path}",
        "-unattended",
        "-silent",
    ]
    subprocess.run(command, check=True)

    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024**2)
        print(f"Exported: {output_path} ({size_mb:.1f} MB)")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Unreal Engine FBX export")
    parser.add_argument(
        "--project",
        default=".",
        help="Path to a .uproject file or a directory containing exactly one .uproject file.",
    )
    parser.add_argument(
        "--editor",
        required=True,
        help="Path to UnrealEditor/UnrealEditor-Cmd (or the equivalent executable for the selected engine version).",
    )
    parser.add_argument("--output", default="exports/avatar_final.fbx")
    args = parser.parse_args()
    return 0 if export_from_unreal(args.project, args.output, args.editor) else 1


if __name__ == "__main__":
    raise SystemExit(main())
