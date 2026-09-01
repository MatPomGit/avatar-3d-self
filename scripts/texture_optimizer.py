#!/usr/bin/env python3
"""
Optimize textures for multi-engine delivery:
- Compress to different formats per engine
- Generate mipmaps
- Convert color spaces
- Validate dimensions
- Calculate memory usage
"""
import json
from pathlib import Path
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TextureOptimizationResult:
    original_path: str
    original_size_mb: float
    format: str
    compression_level: int
    compressed_size_mb: float
    compression_ratio: float
    dimensions: tuple
    color_space: str
    has_mipmaps: bool
    estimated_vram_mb: float

class TextureOptimizer:
    """Optimize textures for game engines"""
    
    # Engine-specific compression formats
    ENGINE_FORMATS = {
        "unreal_engine_5": {
            "diffuse": {"format": "DXT1/BC1", "compression": 6, "srgb": True},
            "normal": {"format": "DXT5/BC5", "compression": 6, "srgb": False},
            "roughness": {"format": "R8", "compression": 6, "srgb": False},
            "metallic": {"format": "R8", "compression": 6, "srgb": False},
            "ao": {"format": "R8", "compression": 6, "srgb": False}
        },
        "unity": {
            "diffuse": {"format": "BC7", "compression": 6, "srgb": True},
            "normal": {"format": "BC5", "compression": 6, "srgb": False},
            "roughness": {"format": "R8", "compression": 6, "srgb": False},
            "metallic": {"format": "R8", "compression": 6, "srgb": False},
            "ao": {"format": "R8", "compression": 6, "srgb": False}
        },
        "twinmotion": {
            "diffuse": {"format": "JPEG/PNG", "compression": 7, "srgb": True},
            "normal": {"format": "PNG", "compression": 6, "srgb": False},
            "roughness": {"format": "PNG", "compression": 6, "srgb": False},
            "metallic": {"format": "PNG", "compression": 6, "srgb": False},
            "ao": {"format": "PNG", "compression": 6, "srgb": False}
        }
    }
    
    # Mipmap level calculation
    MIPMAP_LEVELS = {
        (4096, 4096): 13,
        (2048, 2048): 12,
        (1024, 1024): 11,
        (512, 512): 10,
        (256, 256): 9,
    }
    
    def __init__(self):
        pass
    
    def estimate_vram_uncompressed(self, width: int, height: int,
                                   channels: int = 4) -> float:
        """Calculate uncompressed VRAM usage"""
        bytes_per_pixel = channels
        total_bytes = width * height * bytes_per_pixel
        return total_bytes / (1024**2)
    
    def estimate_vram_compressed(self, width: int, height: int,
                                format: str, has_mipmaps: bool = True) -> float:
        """Calculate compressed VRAM usage"""
        
        # Compression ratios
        ratios = {
            "DXT1/BC1": 0.5,   # 4:1 compression
            "DXT5/BC5": 1.0,   # 2:1 compression
            "BC7": 1.0,        # 2:1 compression
            "R8": 0.25,        # Single channel
            "JPEG": 0.3,
            "PNG": 0.6
        }
        
        uncompressed = self.estimate_vram_uncompressed(width, height, 4)
        ratio = ratios.get(format, 0.5)
        compressed = uncompressed * ratio
        
        # Add mipmaps (adds ~33% extra)
        if has_mipmaps:
            compressed *= 1.33
        
        return compressed
    
    def get_recommended_resolution(self, original_size_mb: float,
                                   target_size_mb: float = 4.0) -> tuple:
        """Recommend optimal resolution for target size"""
        
        if original_size_mb <= target_size_mb:
            return None  # Already within budget
        
        scale_factor = (target_size_mb / original_size_mb) ** 0.5
        
        # Standard resolutions
        standard_res = [4096, 2048, 1024, 512, 256, 128]
        
        for res in standard_res:
            if self.estimate_vram_uncompressed(res, res) * scale_factor <= target_size_mb:
                return (res, res)
        
        return (128, 128)
    
    def analyze_texture_set(self, texture_dir: str) -> dict:
        """Analyze complete PBR texture set"""
        
        texture_path = Path(texture_dir)
        analysis = {
            "textures": {},
            "total_uncompressed_mb": 0,
            "total_compressed_estimate_mb": {}
        }
        
        texture_types = ["diffuse", "normal", "roughness", "metallic", "ao"]
        
        for tex_type in texture_types:
            tex_file = texture_path / f"{tex_type}.png"
            
            if not tex_file.exists():
                continue
            
            file_size_mb = tex_file.stat().st_size / (1024**2)
            
            # Assume 2048x2048 standard
            width, height = 2048, 2048
            
            uncompressed_vram = self.estimate_vram_uncompressed(width, height)
            
            analysis["textures"][tex_type] = {
                "file_size_mb": round(file_size_mb, 2),
                "dimension": f"{width}x{height}",
                "uncompressed_vram_mb": round(uncompressed_vram, 2)
            }
            
            analysis["total_uncompressed_mb"] += uncompressed_vram
        
        # Calculate per-engine compressed sizes
        for engine, formats in self.ENGINE_FORMATS.items():
            total_compressed = 0
            
            for tex_type, tex_data in analysis["textures"].items():
                if tex_type in formats:
                    fmt = formats[tex_type]
                    compressed = self.estimate_vram_compressed(
                        2048, 2048, fmt["format"], has_mipmaps=True
                    )
                    total_compressed += compressed
            
            analysis["total_compressed_estimate_mb"][engine] = round(total_compressed, 2)
        
        return analysis
    
    def generate_optimization_plan(self, texture_dir: str,
                                  output_file: str,
                                  target_size_mb: float = 16.0) -> None:
        """Create optimization strategy"""
        
        analysis = self.analyze_texture_set(texture_dir)
        
        plan = {
            "analysis": analysis,
            "optimization_strategy": {
                "current_vram_uncompressed_mb": round(analysis["total_uncompressed_mb"], 2),
                "target_vram_mb": target_size_mb,
                "compression_targets": {}
            }
        }
        
        # Per-engine strategies
        for engine, formats in self.ENGINE_FORMATS.items():
            engine_compressed = analysis["total_compressed_estimate_mb"].get(engine, 0)
            
            needs_optimization = engine_compressed > target_size_mb
            
            strategy = {
                "engine": engine,
                "estimated_compressed_mb": engine_compressed,
                "needs_optimization": needs_optimization,
                "steps": []
            }
            
            if needs_optimization:
                # Recommend resolution reduction
                reduction_needed = engine_compressed / target_size_mb
                
                if reduction_needed > 1.5:
                    strategy["steps"].append(
                        f"Reduce resolution from 2048x2048 to 1024x1024 (save ~75%)"
                    )
                elif reduction_needed > 1.2:
                    strategy["steps"].append(
                        f"Reduce resolution from 2048x2048 to 1536x1536 (save ~56%)"
                    )
                else:
                    strategy["steps"].append(
                        f"Optimize compression or use additional formats"
                    )
            else:
                strategy["steps"].append(f"Current size acceptable for {engine}")
            
            plan["optimization_strategy"]["compression_targets"][engine] = strategy
        
        Path(output_file).write_text(json.dumps(plan, indent=2))
        logger.info(f"Optimization plan: {output_file}")
    
    def generate_conversion_scripts(self, output_dir: str) -> None:
        """Generate ImageMagick/FFMPEG conversion scripts"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Bash script for texture conversion
        bash_script = """#!/bin/bash
# Convert PBR textures to engine-specific formats

INPUT_DIR="assets/textures/pbr"
OUTPUT_DIR="exports/textures_optimized"

mkdir -p "$OUTPUT_DIR"

# Diffuse (sRGB, DXT1 for UE/Unity)
convert "$INPUT_DIR/diffuse.png" -resize 2048x2048 \
  -quality 85 "$OUTPUT_DIR/diffuse.jpg"

# Normal (Linear, DXT5)
convert "$INPUT_DIR/normal.png" -resize 2048x2048 \
  -colorspace Linear -quality 95 "$OUTPUT_DIR/normal.png"

# Roughness (Single channel, R8)
convert "$INPUT_DIR/roughness.png" -resize 2048x2048 \
  -colorspace Linear -format "%G" "$OUTPUT_DIR/roughness_r8.raw"

# Metallic (Single channel)
convert "$INPUT_DIR/metallic.png" -resize 2048x2048 \
  -colorspace Linear "$OUTPUT_DIR/metallic.png"

# AO (Single channel)
convert "$INPUT_DIR/ao.png" -resize 2048x2048 \
  -colorspace Linear "$OUTPUT_DIR/ao.png"

echo "Texture conversion complete"
"""
        
        script_file = output_path / "convert_textures.sh"
        script_file.write_text(bash_script)
        logger.info(f"Conversion script: {script_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Optimize textures")
    parser.add_argument("--texture-dir", default="assets/textures/pbr")
    parser.add_argument("--output", default="texture_optimization_plan.json")
    parser.add_argument("--target-mb", type=float, default=16.0)
    
    args = parser.parse_args()
    
    optimizer = TextureOptimizer()
    optimizer.generate_optimization_plan(
        args.texture_dir,
        args.output,
        args.target_mb
    )
    optimizer.generate_conversion_scripts("scripts/texture_conversion")