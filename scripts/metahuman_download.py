#!/usr/bin/env python3
"""
Download MetaHuman export from Epic Games.
Assumes manual creation in MetaHuman Creator; this script manages versioning.
"""
import json
from pathlib import Path
import shutil
from datetime import datetime

METAHUMAN_DIR = Path("source/metahuman")
VERSION_FILE = METAHUMAN_DIR / "version_history.json"

def register_metahuman_export(fbx_path: str, face_config: dict, notes: str = ""):
    """Log MetaHuman export version."""
    
    METAHUMAN_DIR.mkdir(parents=True, exist_ok=True)
    
    version = {
        "timestamp": datetime.now().isoformat(),
        "fbx_path": fbx_path,
        "face_config": face_config,
        "notes": notes
    }
    
    # Load history
    if VERSION_FILE.exists():
        history = json.loads(VERSION_FILE.read_text())
    else:
        history = []
    
    history.append(version)
    VERSION_FILE.write_text(json.dumps(history, indent=2))
    
    print(f"✓ Registered MetaHuman v{len(history)}")

if __name__ == "__main__":
    # Example: Register a new MH export
    register_metahuman_export(
        "source/metahuman/metahuman_base.fbx",
        {"hair": "style_001", "skin_tone": 0.75},
        "Initial MetaHuman creation"
    )