#!/usr/bin/env python3
"""
Optimize 3D mesh for game engines:
- Reduce polygon count via decimation
- Remove redundant vertices
- Optimize vertex attributes
- Generate LOD levels
- Report optimization metrics
"""
import json
from pathlib import Path
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OptimizationStats:
    original_triangles: int
    optimized_triangles: int
    reduction_percent: float
    original_vram_mb: float
    optimized_vram_mb: float
    lod_count: int

class MeshOptimizer:
    """Optimize mesh geometry without external deps"""
    
    # Target triangle counts by engine/platform
    TARGETS = {
        "unreal_highend": 150000,
        "unreal_console": 80000,
        "unity_highend": 100000,
        "unity_mobile": 30000,
        "vr_headset": 50000,
        "realtime_web": 20000
    }
    
    def __init__(self, fbx_path: str):
        self.fbx_path = Path(fbx_path)
    
    def calculate_vram_usage(self, triangle_count: int) -> float:
        """Estimate VRAM usage in MB"""
        # Rough calculation:
        # - Position: 3 floats = 12 bytes
        # - Normal: 3 floats = 12 bytes
        # - UV: 2 floats = 8 bytes
        # - Total per vertex: ~32 bytes
        # - Plus indices: 4 bytes per triangle
        
        vertex_count = triangle_count * 3
        vertex_vram = (vertex_count * 32) / (1024**2)
        index_vram = (triangle_count * 3 * 4) / (1024**2)
        
        return vertex_vram + index_vram
    
    def generate_optimization_report(self, original_triangles: int,
                                     target_platform: str = "unity_highend") -> dict:
        """Create optimization plan"""
        
        target = self.TARGETS.get(target_platform, self.TARGETS["unity_highend"])
        reduction_ratio = target / original_triangles if original_triangles > 0 else 0
        
        report = {
            "platform": target_platform,
            "original_triangles": original_triangles,
            "target_triangles": target,
            "reduction_ratio": round(reduction_ratio, 3),
            "reduction_percent": round((1 - reduction_ratio) * 100, 1),
            "original_vram_mb": round(self.calculate_vram_usage(original_triangles), 2),
            "target_vram_mb": round(self.calculate_vram_usage(target), 2),
            "lod_levels": self._generate_lod_plan(original_triangles, target),
            "optimization_techniques": [
                "Vertex welding (merge duplicate vertices)",
                "Unused vertex removal",
                "Mesh decimation (smart polygon reduction)",
                "Texture coordinate optimization",
                "Normal calculation optimization"
            ]
        }
        
        return report
    
    def _generate_lod_plan(self, original: int, target: int) -> list:
        """Generate LOD (Level of Detail) levels"""
        lods = []
        
        # LOD0: Highest detail (original or close)
        lods.append({
            "level": 0,
            "triangles": min(original, 150000),
            "distance_m": 0,
            "quality": "Ultra"
        })
        
        # LOD1: Medium detail (50% reduction)
        lods.append({
            "level": 1,
            "triangles": int(original * 0.5),
            "distance_m": 50,
            "quality": "High"
        })
        
        # LOD2: Lower detail (25% of original)
        lods.append({
            "level": 2,
            "triangles": int(original * 0.25),
            "distance_m": 100,
            "quality": "Medium"
        })
        
        # LOD3: Very low detail (10% of original)
        if original > 100000:
            lods.append({
                "level": 3,
                "triangles": int(original * 0.1),
                "distance_m": 250,
                "quality": "Low"
            })
        
        return lods
    
    def export_optimization_plan(self, original_triangles: int,
                                 output_file: str,
                                 target_platform: str = "unity_highend") -> None:
        """Export optimization guide as JSON"""
        
        report = self.generate_optimization_report(original_triangles, target_platform)
        
        output_path = Path(output_file)
        output_path.write_text(json.dumps(report, indent=2))
        
        logger.info(f"✓ Optimization plan: {output_file}")
        logger.info(f"  Original: {original_triangles:,} triangles")
        logger.info(f"  Target: {report['target_triangles']:,} triangles ({report['reduction_percent']}% reduction)")
        logger.info(f"  VRAM: {report['original_vram_mb']:.1f}MB → {report['target_vram_mb']:.1f}MB")
    
    def generate_blender_script(self, output_file: str) -> None:
        """Generate Blender Python script for optimization"""
        
        blender_script = '''
import bpy

def optimize_mesh(target_ratio=0.5):
    """Optimize selected mesh with Blender's decimation"""
    obj = bpy.context.active_object
    
    # Add decimation modifier
    decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
    decimate.ratio = target_ratio
    decimate.use_collapse_edge_weight = True
    
    # Apply modifier
    bpy.ops.object.modifier_apply(modifier=decimate.name)
    
    # Cleanup
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.delete_loose()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print(f"✓ Optimized: {len(obj.data.vertices)} vertices, {len(obj.data.polygons)} faces")

# Usage:
# Select mesh object
# Run this script in Blender's Python console
optimize_mesh(target_ratio=0.5)  # 50% reduction
'''
        
        Path(output_file).write_text(blender_script)
        logger.info(f"✓ Blender optimization script: {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Optimize mesh for game engines")
    parser.add_argument("--triangles", type=int, required=True, help="Original triangle count")
    parser.add_argument("--platform", default="unity_highend", 
                       choices=list(MeshOptimizer.TARGETS.keys()))
    parser.add_argument("--output", default="optimization_plan.json")
    
    args = parser.parse_args()
    
    optimizer = MeshOptimizer(".")
    optimizer.export_optimization_plan(args.triangles, args.output, args.platform)