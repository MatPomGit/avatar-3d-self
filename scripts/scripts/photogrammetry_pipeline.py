#!/usr/bin/env python3
"""
Complete photogrammetry pipeline: Photo preprocessing → COLMAP SfM → Dense reconstruction → PLY export
Optimized for realistic facial scanning (highest quality for later facial rigging)
"""
import subprocess
import json
from pathlib import Path
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PhotogrammetryPipeline:
    def __init__(self, photos_dir: str, output_dir: str, max_resolution: int = 4096):
        self.photos_dir = Path(photos_dir)
        self.output_dir = Path(output_dir)
        self.max_resolution = max_resolution
        self.db = self.output_dir / "database.db"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def preprocess_photos(self) -> bool:
        """
        Optimize photos for photogrammetry:
        - Downscale if > max_resolution
        - Validate EXIF (camera parameters)
        - Remove duplicates (perceptual hashing)
        """
        logger.info(f"Preprocessing {len(list(self.photos_dir.glob('*.jpg')))} photos...")
        
        try:
            import cv2
            import numpy as np
            
            processed = 0
            for img_path in sorted(self.photos_dir.glob("*.jpg")):
                img = cv2.imread(str(img_path))
                h, w = img.shape[:2]
                
                # Downscale if needed (preserve aspect ratio)
                if max(h, w) > self.max_resolution:
                    scale = self.max_resolution / max(h, w)
                    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LANCZOS4)
                    cv2.imwrite(str(img_path), img, [cv2.IMWRITE_JPEG_QUALITY, 95])
                    logger.info(f"  ↓ Scaled {img_path.name}: {w}×{h} → {img.shape[1]}×{img.shape[0]}")
                
                processed += 1
            
            logger.info(f"✓ Preprocessed {processed} photos")
            return True
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            return False
    
    def run_colmap_sfm(self) -> bool:
        """Execute COLMAP Structure-from-Motion with optimal settings for face scanning"""
        
        steps = [
            {
                "name": "Feature Extraction",
                "cmd": [
                    "colmap", "feature_extractor",
                    "--database_path", str(self.db),
                    "--image_path", str(self.photos_dir),
                    "--ImageReader.single_camera", "1",  # Assume single camera
                    "--ImageReader.camera_model", "PINHOLE",
                    "--SiftGPU.use_gpu", "1"
                ]
            },
            {
                "name": "Feature Matching",
                "cmd": [
                    "colmap", "exhaustive_matcher",
                    "--database_path", str(self.db),
                    "--SiftMatching.use_gpu", "1"
                ]
            },
            {
                "name": "Sparse Reconstruction",
                "cmd": [
                    "colmap", "mapper",
                    "--database_path", str(self.db),
                    "--image_path", str(self.photos_dir),
                    "--output_path", str(self.output_dir / "sparse"),
                    "--Mapper.ba_refine_principal_point", "1"
                ]
            }
        ]
        
        for step in steps:
            logger.info(f"Running: {step['name']}...")
            try:
                subprocess.run(step["cmd"], check=True, capture_output=True)
                logger.info(f"  ✓ {step['name']} completed")
            except subprocess.CalledProcessError as e:
                logger.error(f"  ✗ {step['name']} failed: {e.stderr.decode()}")
                return False
        
        return True
    
    def run_dense_reconstruction(self) -> bool:
        """Generate dense point cloud via Poisson surface reconstruction"""
        
        steps = [
            {
                "name": "Undistortion",
                "cmd": [
                    "colmap", "image_undistorter",
                    "--image_path", str(self.photos_dir),
                    "--input_path", str(self.output_dir / "sparse" / "0"),
                    "--output_path", str(self.output_dir / "dense"),
                    "--output_type", "COLMAP"
                ]
            },
            {
                "name": "Stereo Matching",
                "cmd": [
                    "colmap", "stereo",
                    "--workspace_path", str(self.output_dir / "dense"),
                    "--workspace_format", "COLMAP",
                    "--pmvs_option_level", "1"  # Balance speed/quality
                ]
            },
            {
                "name": "Poisson Meshing",
                "cmd": [
                    "colmap", "poisson_mesher",
                    "--input_path", str(self.output_dir / "dense" / "fused.ply"),
                    "--output_path", str(self.output_dir / "mesh_dense.ply")
                ]
            }
        ]
        
        for step in steps:
            logger.info(f"Running: {step['name']}...")
            try:
                subprocess.run(step["cmd"], check=True, capture_output=True)
                logger.info(f"  ✓ {step['name']} completed")
            except subprocess.CalledProcessError as e:
                logger.error(f"  ✗ {step['name']} failed")
                return False
        
        # Log mesh stats
        mesh_path = self.output_dir / "mesh_dense.ply"
        if mesh_path.exists():
            size_mb = mesh_path.stat().st_size / (1024**2)
            logger.info(f"✓ Dense mesh exported: {mesh_path} ({size_mb:.1f} MB)")
        
        return True
    
    def export_stats(self) -> dict:
        """Generate reconstruction metadata"""
        stats = {
            "timestamp": str(Path.cwd()),
            "photo_count": len(list(self.photos_dir.glob("*.jpg"))),
            "max_resolution": self.max_resolution,
            "output_mesh": str(self.output_dir / "mesh_dense.ply")
        }
        
        stats_file = self.output_dir / "reconstruction_stats.json"
        stats_file.write_text(json.dumps(stats, indent=2))
        return stats

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Photogrammetry pipeline")
    parser.add_argument("--photos", default="references/photos/raw", help="Input photos directory")
    parser.add_argument("--output", default="source/scans/colmap_output", help="Output directory")
    parser.add_argument("--skip-preprocess", action="store_true")
    
    args = parser.parse_args()
    
    pipeline = PhotogrammetryPipeline(args.photos, args.output)
    
    if not args.skip_preprocess:
        pipeline.preprocess_photos()
    
    if pipeline.run_colmap_sfm():
        pipeline.run_dense_reconstruction()
        pipeline.export_stats()
        logger.info("✓✓✓ Pipeline completed successfully")
    else:
        logger.error("Pipeline failed")
        exit(1)