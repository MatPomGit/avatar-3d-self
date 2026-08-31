#!/usr/bin/env python3
"""
Process scan textures → high-quality PBR maps.
Photogrammetry scan → Diffuse, Normal, Roughness, Metallic, AO
"""
import json
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PBRTextureProcessor:
    def __init__(self, scan_textures_dir: str, output_dir: str):
        self.input_dir = Path(scan_textures_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_texture(self, path: str, max_size: int = 2048) -> np.ndarray:
        """Load & normalize texture"""
        img = Image.open(path)
        
        # Downscale if needed
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        return np.array(img, dtype=np.float32) / 255.0
    
    def generate_normal_map(self, diffuse_path: str, output_path: str, 
                           strength: float = 1.0) -> None:
        """
        Generate normal map from diffuse texture using Sobel edge detection.
        Simulates surface microdetails (pores, skin texture).
        """
        logger.info(f"Generating normal map: {output_path}")
        
        # Load diffuse
        diffuse = Image.open(diffuse_path).convert('L')
        diffuse_array = np.array(diffuse, dtype=np.float32) / 255.0
        
        # Sobel edge detection (simplified normal gen)
        from scipy import ndimage
        
        gx = ndimage.sobel(diffuse_array, axis=0) * strength
        gy = ndimage.sobel(diffuse_array, axis=1) * strength
        gz = np.ones_like(gx)  # Blue channel (Z-up)
        
        # Normalize
        normal = np.stack([gx, gy, gz], axis=2)
        norm = np.linalg.norm(normal, axis=2, keepdims=True)
        normal = normal / (norm + 1e-6)
        
        # Convert to RGB (0-255: -1 to +1 range)
        normal_rgb = ((normal + 1.0) / 2.0 * 255).astype(np.uint8)
        
        result = Image.fromarray(normal_rgb)
        result.save(output_path)
        logger.info(f"✓ Normal map: {output_path}")
    
    def generate_roughness_map(self, diffuse_path: str, output_path: str) -> None:
        """
        Generate roughness map from luminance variation.
        Skin: Medium roughness (0.4-0.6 = matte but not flat)
        """
        logger.info(f"Generating roughness map: {output_path}")
        
        diffuse = Image.open(diffuse_path)
        gray = diffuse.convert('L')
        enhancer = ImageEnhance.Contrast(gray)
        roughness = enhancer.enhance(1.5)
        roughness = roughness.filter(ImageFilter.GaussianBlur(radius=2))
        arr = np.array(roughness, dtype=np.float32) / 255.0
        arr = 0.4 + (arr * 0.2)
        result = Image.fromarray((arr * 255).astype(np.uint8))
        result.save(output_path)
        logger.info(f"✓ Roughness map: {output_path}")
    
    def generate_metallic_map(self, output_path: str, default_value: float = 0.0) -> None:
        """Create metallic map (skin is non-metallic, so mostly black)."""
        logger.info(f"Generating metallic map: {output_path}")
        size = (2048, 2048)
        metallic_array = np.full(size + (3,), int(default_value * 255), dtype=np.uint8)
        result = Image.fromarray(metallic_array)
        result.save(output_path)
        logger.info(f"✓ Metallic map: {output_path}")
    
    def generate_ao_map(self, diffuse_path: str, normal_path: str, 
                       output_path: str, occlusion_strength: float = 0.8) -> None:
        """Generate an approximate ambient-occlusion map from the diffuse texture."""
        logger.info(f"Generating AO map: {output_path}")
        Image.open(normal_path).verify()
        diffuse_pil = Image.open(diffuse_path).convert('L')
        blurred = diffuse_pil.filter(ImageFilter.GaussianBlur(radius=5))
        diffuse_arr = np.array(diffuse_pil, dtype=np.float32)
        blurred_arr = np.array(blurred, dtype=np.float32)
        high_pass = (diffuse_arr - blurred_arr) / 255.0
        ao = 1.0 - (np.abs(high_pass) * occlusion_strength)
        ao = np.clip(ao, 0, 1)
        result = Image.fromarray((ao * 255).astype(np.uint8))
        result.save(output_path)
        logger.info(f"✓ AO map: {output_path}")
    
    def process_scan_to_pbr(self, diffuse_input: str) -> dict:
        """Complete pipeline: Scan texture → Full PBR set."""
        logger.info("Starting PBR texture processing...")
        diffuse_out = self.output_dir / "diffuse.png"
        normal_out = self.output_dir / "normal.png"
        roughness_out = self.output_dir / "roughness.png"
        metallic_out = self.output_dir / "metallic.png"
        ao_out = self.output_dir / "ao.png"
        Image.open(diffuse_input).save(diffuse_out)
        logger.info(f"✓ Diffuse: {diffuse_out}")
        self.generate_normal_map(str(diffuse_input), str(normal_out), strength=0.8)
        self.generate_roughness_map(str(diffuse_input), str(roughness_out))
        self.generate_metallic_map(str(metallic_out), default_value=0.0)
        self.generate_ao_map(str(diffuse_input), str(normal_out), str(ao_out))
        logger.info("✓✓✓ PBR texture set complete")
        return {
            "diffuse": str(diffuse_out),
            "normal": str(normal_out),
            "roughness": str(roughness_out),
            "metallic": str(metallic_out),
            "ao": str(ao_out)
        }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PBR texture processing")
    parser.add_argument("--diffuse", required=True, help="Input diffuse texture")
    parser.add_argument("--output", default="assets/textures/pbr", help="Output directory")
    args = parser.parse_args()
    processor = PBRTextureProcessor(".", args.output)
    pbr_set = processor.process_scan_to_pbr(args.diffuse)
    print(json.dumps(pbr_set, indent=2))
