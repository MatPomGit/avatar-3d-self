#!/usr/bin/env python3
"""
Export rigged character + blendshapes from Unreal Engine to FBX.
Runs headless via GitHub Actions.
"""
import subprocess
import json
from pathlib import Path

def export_from_unreal(project_path: str, character_path: str, output_fbx: str):
    """
    Trigger Unreal Engine export via command line.
    
    Usage:
        UnrealEngine/Engine/Build/Linux/Engine/Binaries/UE4Editor
        -run=ResavePackages
        -PROJECT="avatar-3d-self.uproject"
        -FBXExportDir="exports/"
    """
    
    cmd = [
        "/path/to/UnrealEngine/Engine/Binaries/Linux/UE4Editor",
        f"{project_path}/avatar-3d-self.uproject",
        "-run=ResavePackages",
        "-unattended",
        "-silent"
    ]
    
    subprocess.run(cmd, check=True)
    
    # Verify export
    export_path = Path(output_fbx)
    if export_path.exists():
        size_mb = export_path.stat().st_size / (1024**2)
        print(f"✓ Exported: {output_fbx} ({size_mb:.1f} MB)")
        return True
    return False

if __name__ == "__main__":
    export_from_unreal(
        ".",
        "/Game/Characters/MetaHuman_Rigged",
        "exports/avatar_final.fbx"
    )