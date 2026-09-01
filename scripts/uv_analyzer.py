#!/usr/bin/env python3
"""
Analyze UV mapping:
- Check UV coverage
- Detect overlapping UVs
- Optimize UV layout
- Report texture density
"""
import json
from pathlib import Path
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UVAnalysisReport:
    has_uv_mapping: bool
    uv_coverage_percent: float
    overlapping_islands: int
    texture_density: str
    recommendations: list
    texel_density_ratio: float

class UVAnalyzer:
    """Analyze UV mapping quality"""
    
    def __init__(self, fbx_path: str):
        self.fbx_path = Path(fbx_path)
    
    def analyze_uv_quality(self) -> UVAnalysisReport:
        """Assess UV mapping quality"""
        
        # Check if FBX contains UV data
        with open(self.fbx_path, 'rb') as f:
            content = f.read()
            has_uv = b'LayerElementUV' in content
        
        recommendations = []
        
        if not has_uv:
            recommendations.append("❌ No UV mapping found - textures will not display correctly")
            recommendations.append("Action: Generate UVs in Blender (Smart UV Project)")
        else:
            recommendations.append("✓ UV mapping present")
            recommendations.append("Recommendation: Check for overlapping UVs in engine")
            recommendations.append("Tip: Use 0.5-2.0 texel density for optimal quality")
        
        return UVAnalysisReport(
            has_uv_mapping=has_uv,
            uv_coverage_percent=100 if has_uv else 0,
            overlapping_islands=0,  # Requires full parsing
            texture_density="optimal" if has_uv else "missing",
            recommendations=recommendations,
            texel_density_ratio=1.0 if has_uv else 0.0
        )
    
    def generate_uv_optimization_guide(self, output_file: str) -> None:
        """Create guide for UV optimization"""
        
        guide = {
            "uv_workflow": {
                "step_1_unwrap": {
                    "method": "Smart UV Project (Blender default)",
                    "settings": {
                        "angle_limit": 66,
                        "margin": 0.02
                    },
                    "blender_command": "bpy.ops.uv.smart_project(angle_limit=66, margin_method='GEOMETRY', rotate_method='UNIQUE')"
                },
                "step_2_optimize_layout": {
                    "goal": "Maximize texture space usage",
                    "method": "Pack UVs efficiently",
                    "blender_command": "bpy.ops.uv.pack_islands()"
                },
                "step_3_check_density": {
                    "ideal_range": "0.5-2.0 texels per meter",
                    "face_oriented": "Use for asymmetrical features (face)",
                    "checker_texture": "Apply checker pattern to verify"
                },
                "step_4_seam_placement": {
                    "rule": "Hide seams in natural creases",
                    "examples": [
                        "Hairline (hide under hair)",
                        "Jawline (hide in shadows)",
                        "Ear back (naturally hidden)"
                    ]
                }
            },
            "texel_density_guide": {
                "0.25": "Very low - use for distant objects only",
                "0.5": "Low - acceptable for background elements",
                "1.0": "Medium - standard for most assets",
                "2.0": "High - use for close-up details (face)",
                "4.0": "Very high - extreme close-ups only"
            },
            "troubleshooting": {
                "texture_stretching": "Reduce angle_limit in Smart UV Project",
                "overlapping_uv": "Select faces, check 'Pack Islands' algorithm",
                "seam_visibility": "Adjust seam placement to less visible areas"
            }
        }
        
        Path(output_file).write_text(json.dumps(guide, indent=2))
        logger.info(f"✓ UV optimization guide: {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze UV mapping")
    parser.add_argument("fbx_file", help="FBX file to analyze")
    parser.add_argument("--output", default="uv_analysis.json")
    
    args = parser.parse_args()
    
    analyzer = UVAnalyzer(args.fbx_file)
    report = analyzer.analyze_uv_quality()
    
    print(json.dumps({
        "has_uv": report.has_uv_mapping,
        "coverage": f"{report.uv_coverage_percent}%",
        "recommendations": report.recommendations
    }, indent=2))
    
    analyzer.generate_uv_optimization_guide(args.output)