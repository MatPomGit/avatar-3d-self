#!/usr/bin/env python3
"""
COLMAP pipeline: Photos → 3D mesh (fully automated)
Triggered by GitHub Actions on new photo uploads.
"""
import subprocess
import json
from pathlib import Path

PHOTOS_DIR = Path("references/photos/raw")
OUTPUT_DIR = Path("source/scans/colmap_output")

def run_colmap():
    """Execute COLMAP feature extraction → matching → SfM."""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Feature extraction
    subprocess.run([
        "colmap", "feature_extractor",
        "--database_path", str(OUTPUT_DIR / "database.db"),
        "--image_path", str(PHOTOS_DIR),
        "--ImageReader.camera_model", "SIMPLE_RADIAL"
    ], check=True)
    
    # Feature matching
    subprocess.run([
        "colmap", "exhaustive_matcher",
        "--database_path", str(OUTPUT_DIR / "database.db")
    ], check=True)
    
    # Sparse reconstruction
    subprocess.run([
        "colmap", "mapper",
        "--database_path", str(OUTPUT_DIR / "database.db"),
        "--image_path", str(PHOTOS_DIR),
        "--output_path", str(OUTPUT_DIR / "sparse")
    ], check=True)
    
    # Dense reconstruction
    subprocess.run([
        "colmap", "image_undistorter",
        "--image_path", str(PHOTOS_DIR),
        "--input_path", str(OUTPUT_DIR / "sparse/0"),
        "--output_path", str(OUTPUT_DIR / "dense")
    ], check=True)
    
    subprocess.run([
        "colmap", "stereo",
        "--workspace_path", str(OUTPUT_DIR / "dense")
    ], check=True)
    
    # Mesh fusion
    subprocess.run([
        "colmap", "poisson_mesher",
        "--input_path", str(OUTPUT_DIR / "dense/fused.ply"),
        "--output_path", str(OUTPUT_DIR / "mesh.ply")
    ], check=True)
    
    print("✓ Mesh generated: source/scans/colmap_output/mesh.ply")
    return OUTPUT_DIR / "mesh.ply"

if __name__ == "__main__":
    run_colmap()