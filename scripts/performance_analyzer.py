#!/usr/bin/env python3
"""
Analyze avatar performance metrics:
- Polygon budget vs platform
- VRAM usage estimation
- FPS predictions
- Draw calls estimation
- Optimization score
"""
import json
from pathlib import Path
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    platform: str
    triangles: int
    vertices: int
    bones: int
    blendshapes: int
    materials: int
    estimated_vram_mb: float
    estimated_fps_optimal: int
    estimated_fps_target: int
    performance_score: float  # 0-100
    bottleneck: str
    recommendations: list = field(default_factory=list)

class PerformanceAnalyzer:
    """Analyze avatar performance for different platforms"""
    
    PLATFORM_BUDGETS = {
        "pc_vr_high": {
            "max_triangles": 200000,
            "max_vram_mb": 512,
            "target_fps": 90,
            "draw_calls_budget": 50
        },
        "console_next_gen": {
            "max_triangles": 150000,
            "max_vram_mb": 256,
            "target_fps": 60,
            "draw_calls_budget": 40
        },
        "highend_desktop": {
            "max_triangles": 150000,
            "max_vram_mb": 1024,
            "target_fps": 60,
            "draw_calls_budget": 100
        },
        "mobile_vr": {
            "max_triangles": 50000,
            "max_vram_mb": 128,
            "target_fps": 72,
            "draw_calls_budget": 15
        },
        "web_realtime": {
            "max_triangles": 20000,
            "max_vram_mb": 64,
            "target_fps": 30,
            "draw_calls_budget": 10
        }
    }
    
    def __init__(self):
        pass
    
    def calculate_vram(self, vertices: int, materials: int, 
                      textures_per_material: int = 5) -> float:
        """Estimate VRAM usage"""
        
        # Vertex attributes: ~32 bytes per vertex
        vertex_vram = (vertices * 32) / (1024**2)
        
        # Blendshape targets: ~32 bytes per vertex per target
        # Assume 48 blendshapes average
        blendshape_vram = (vertices * 32 * 48) / (1024**2)
        
        # Textures: assume 2048×2048, RGBA8
        # ~16 MB per texture
        texture_vram = materials * textures_per_material * 16
        
        return vertex_vram + blendshape_vram + texture_vram
    
    def estimate_fps(self, triangles: int, platform: str) -> tuple:
        """Estimate FPS on target platform"""
        
        budget = self.PLATFORM_BUDGETS.get(platform)
        if not budget:
            return (30, 0)
        
        max_triangles = budget["max_triangles"]
        
        # Simple FPS model: 
        # FPS = target_fps * (1 - (triangles/max)^2)
        if triangles > max_triangles:
            excess_ratio = triangles / max_triangles
            fps_optimal = budget["target_fps"] * 0.5  # 50% on target
            fps_target = max(10, int(budget["target_fps"] / (excess_ratio ** 1.5)))
        else:
            fps_optimal = budget["target_fps"]
            fps_target = budget["target_fps"]
        
        return (int(fps_optimal), int(fps_target))
    
    def analyze(self, triangles: int, vertices: int, bones: int,
               blendshapes: int, materials: int,
               platform: str = "pc_vr_high") -> PerformanceMetrics:
        """Full performance analysis"""
        
        budget = self.PLATFORM_BUDGETS.get(platform)
        if not budget:
            raise ValueError(f"Unknown platform: {platform}")
        
        # Calculate metrics
        vram = self.calculate_vram(vertices, materials)
        fps_optimal, fps_target = self.estimate_fps(triangles, platform)
        
        # Calculate performance score (0-100)
        tri_ratio = triangles / budget["max_triangles"]
        vram_ratio = vram / budget["max_vram_mb"]
        
        tri_score = max(0, 100 * (1 - tri_ratio))
        vram_score = max(0, 100 * (1 - vram_ratio))
        
        performance_score = (tri_score + vram_score) / 2
        
        # Identify bottleneck
        if tri_ratio > vram_ratio:
            bottleneck = "Polygon count"
        elif vram_ratio > tri_ratio:
            bottleneck = "VRAM usage"
        else:
            bottleneck = "Balanced"
        
        # Recommendations
        recommendations = []
        
        if tri_ratio > 1.2:
            recommendations.append(f"❌ Polygon count {triangles:,} exceeds budget {budget['max_triangles']:,}")
            recommendations.append("Action: Use mesh optimization (target 20-30% reduction)")
        elif tri_ratio > 0.8:
            recommendations.append(f"⚠ High polygon density ({tri_ratio*100:.0f}% of budget)")
            recommendations.append("Action: Generate LOD levels for distant views")
        else:
            recommendations.append(f"✓ Polygon count optimal ({tri_ratio*100:.0f}% of budget)")
        
        if vram_ratio > 1.0:
            recommendations.append("❌ VRAM exceeds budget - reduce texture resolution")
        elif vram_ratio > 0.7:
            recommendations.append("⚠ VRAM usage high - consider texture atlasing")
        else:
            recommendations.append("✓ VRAM usage acceptable")
        
        if blendshapes < 20:
            recommendations.append("⚠ Few blendshapes (<20) - facial animation limited")
        elif blendshapes >= 48:
            recommendations.append("✓ Excellent blendshape coverage for realistic animation")
        
        if bones < 30:
            recommendations.append("⚠ Few bones - may limit deformation quality")
        
        return PerformanceMetrics(
            platform=platform,
            triangles=triangles,
            vertices=vertices,
            bones=bones,
            blendshapes=blendshapes,
            materials=materials,
            estimated_vram_mb=vram,
            estimated_fps_optimal=fps_optimal,
            estimated_fps_target=fps_target,
            performance_score=performance_score,
            bottleneck=bottleneck,
            recommendations=recommendations
        )
    
    def generate_report_json(self, metrics: PerformanceMetrics,
                            output_file: str) -> None:
        """Export performance report as JSON"""
        
        report = {
            "platform": metrics.platform,
            "geometry": {
                "triangles": metrics.triangles,
                "vertices": metrics.vertices
            },
            "rigging": {
                "bones": metrics.bones,
                "blendshapes": metrics.blendshapes
            },
            "materials": metrics.materials,
            "vram": {
                "estimated_mb": round(metrics.estimated_vram_mb, 2),
                "budget_mb": self.PLATFORM_BUDGETS[metrics.platform]["max_vram_mb"],
                "usage_percent": round(100 * metrics.estimated_vram_mb / 
                                     self.PLATFORM_BUDGETS[metrics.platform]["max_vram_mb"], 1)
            },
            "performance": {
                "estimated_fps_optimal": metrics.estimated_fps_optimal,
                "estimated_fps_target": metrics.estimated_fps_target,
                "target_fps": self.PLATFORM_BUDGETS[metrics.platform]["target_fps"],
                "score": round(metrics.performance_score, 1)
            },
            "bottleneck": metrics.bottleneck,
            "recommendations": metrics.recommendations
        }
        
        Path(output_file).write_text(json.dumps(report, indent=2))
        logger.info(f"✓ Performance report: {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze avatar performance")
    parser.add_argument("--triangles", type=int, default=80000)
    parser.add_argument("--vertices", type=int, default=40000)
    parser.add_argument("--bones", type=int, default=60)
    parser.add_argument("--blendshapes", type=int, default=48)
    parser.add_argument("--materials", type=int, default=3)
    parser.add_argument("--platform", default="pc_vr_high",
                       choices=list(PerformanceAnalyzer.PLATFORM_BUDGETS.keys()))
    parser.add_argument("--output", default="performance_report.json")
    
    args = parser.parse_args()
    
    analyzer = PerformanceAnalyzer()
    metrics = analyzer.analyze(
        args.triangles, args.vertices, args.bones,
        args.blendshapes, args.materials, args.platform
    )
    
    print(f"Performance Score: {metrics.performance_score:.1f}/100")
    print(f"Bottleneck: {metrics.bottleneck}")
    print(f"Estimated FPS: {metrics.estimated_fps_target} ({metrics.platform})")
    
    analyzer.generate_report_json(metrics, args.output)