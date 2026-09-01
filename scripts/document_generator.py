#!/usr/bin/env python3
"""
Generate project documentation:
- Asset inventory documentation
- Technical specifications
- Integration guides
- Quality assurance reports
- Troubleshooting guides
"""
import json
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentGenerator:
    """Generate project documentation"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.docs_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_asset_inventory(self, metadata: dict,
                                output_file: str = "ASSET_INVENTORY.txt") -> None:
        """Generate asset inventory document"""
        
        output_path = self.docs_dir / output_file
        
        content = []
        content.append("=" * 80)
        content.append("ASSET INVENTORY REPORT")
        content.append("=" * 80)
        content.append("")
        
        content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")
        
        content.append("GEOMETRY")
        content.append("-" * 40)
        if "summary" in metadata:
            content.append(f"Total Nodes: {metadata['summary'].get('node_count', 'N/A')}")
            content.append(f"Total Triangles: {metadata.get('triangles', 'N/A')}")
            content.append(f"Total Vertices: {metadata.get('vertices', 'N/A')}")
        content.append("")
        
        content.append("RIGGING")
        content.append("-" * 40)
        if "summary" in metadata:
            content.append(f"Blendshape Count: {metadata['summary'].get('blendshape_count', 'N/A')}")
        if "blendshapes" in metadata:
            content.append(f"Blendshapes ({len(metadata['blendshapes'])}):")
            for i, bs in enumerate(metadata["blendshapes"][:30], 1):
                content.append(f"  {i:2d}. {bs}")
            if len(metadata["blendshapes"]) > 30:
                content.append(f"  ... and {len(metadata['blendshapes']) - 30} more")
        content.append("")
        
        content.append("MATERIALS")
        content.append("-" * 40)
        if "summary" in metadata:
            content.append(f"Material Count: {metadata['summary'].get('material_count', 'N/A')}")
        if "materials" in metadata:
            content.append(f"Materials ({len(metadata['materials'])}):")
            for material in metadata["materials"]:
                content.append(f"  - {material}")
        content.append("")
        
        content.append("TEXTURES")
        content.append("-" * 40)
        if "summary" in metadata:
            content.append(f"Texture Count: {metadata['summary'].get('texture_count', 'N/A')}")
        if "texture_references" in metadata:
            content.append("Texture References:")
            for texture in metadata["texture_references"][:20]:
                content.append(f"  - {texture}")
            if len(metadata.get("texture_references", [])) > 20:
                remaining = len(metadata["texture_references"]) - 20
                content.append(f"  ... and {remaining} more")
        content.append("")
        
        content.append("ANIMATIONS")
        content.append("-" * 40)
        if "summary" in metadata:
            content.append(f"Animation Count: {metadata['summary'].get('animation_count', 'N/A')}")
        if "animations" in metadata:
            content.append("Animations:")
            for anim_name in metadata["animations"].keys():
                content.append(f"  - {anim_name}")
        content.append("")
        
        content.append("=" * 80)
        
        doc_text = "\n".join(content)
        output_path.write_text(doc_text)
        logger.info(f"Asset inventory: {output_path}")
    
    def generate_technical_specs(self, metrics: dict,
                                output_file: str = "TECHNICAL_SPECS.txt") -> None:
        """Generate technical specifications"""
        
        output_path = self.docs_dir / output_file
        
        content = []
        content.append("=" * 80)
        content.append("TECHNICAL SPECIFICATIONS")
        content.append("=" * 80)
        content.append("")
        
        content.append("GEOMETRY")
        content.append("-" * 40)
        content.append(f"Polygon Count: {metrics.get('triangles', 'N/A'):,}")
        content.append(f"Vertex Count: {metrics.get('vertices', 'N/A'):,}")
        content.append(f"File Size: {metrics.get('file_size_mb', 'N/A'):.1f} MB")
        content.append("")
        
        content.append("SKELETAL DATA")
        content.append("-" * 40)
        content.append(f"Bone Count: {metrics.get('bones', 'N/A')}")
        content.append(f"Blendshape Count: {metrics.get('blendshapes', 'N/A')}")
        content.append(f"Material Count: {metrics.get('materials', 'N/A')}")
        content.append("")
        
        content.append("PERFORMANCE TARGETS")
        content.append("-" * 40)
        content.append("PC/VR (High-End):")
        content.append("  Target FPS: 90")
        content.append("  Polygon Budget: 150,000")
        content.append("  VRAM Budget: 512 MB")
        content.append("")
        content.append("Console (Next-Gen):")
        content.append("  Target FPS: 60")
        content.append("  Polygon Budget: 150,000")
        content.append("  VRAM Budget: 256 MB")
        content.append("")
        content.append("Mobile/VR:")
        content.append("  Target FPS: 72")
        content.append("  Polygon Budget: 50,000")
        content.append("  VRAM Budget: 128 MB")
        content.append("")
        content.append("Web (Real-time):")
        content.append("  Target FPS: 30-60")
        content.append("  Polygon Budget: 20,000")
        content.append("  VRAM Budget: 64 MB")
        content.append("")
        
        content.append("TEXTURE SPECIFICATIONS")
        content.append("-" * 40)
        content.append("Primary Resolution: 2048x2048")
        content.append("Color Depth: 32-bit RGBA")
        content.append("PBR Maps:")
        content.append("  - Diffuse (sRGB)")
        content.append("  - Normal (Linear)")
        content.append("  - Roughness (Linear)")
        content.append("  - Metallic (Linear)")
        content.append("  - Ambient Occlusion (Linear)")
        content.append("")
        
        content.append("ANIMATION SPECIFICATIONS")
        content.append("-" * 40)
        content.append("Frame Rate: 30 FPS (locomotion), 60 FPS (facial)")
        content.append("Keyframe Reduction: Enabled")
        content.append("Loop Detection: Enabled")
        content.append("Blendshape Animation: 48+ targets")
        content.append("")
        
        content.append("=" * 80)
        
        doc_text = "\n".join(content)
        output_path.write_text(doc_text)
        logger.info(f"Technical specs: {output_path}")
    
    def generate_troubleshooting_guide(self,
                                      output_file: str = "TROUBLESHOOTING.txt") -> None:
        """Generate troubleshooting guide"""
        
        output_path = self.docs_dir / output_file
        
        content = []
        content.append("=" * 80)
        content.append("TROUBLESHOOTING GUIDE")
        content.append("=" * 80)
        content.append("")
        
        issues = [
            {
                "title": "Textures not displaying in Unreal Engine",
                "causes": [
                    "Texture paths incorrect in material",
                    "Textures not imported to project",
                    "Material instance not applied to mesh"
                ],
                "solutions": [
                    "1. Verify texture files exist in Content/Characters/Textures/",
                    "2. Reimport FBX with 'Import Materials' enabled",
                    "3. Create Material Instance from M_Avatar_Master",
                    "4. Manually assign texture references in Material Instance"
                ]
            },
            {
                "title": "Blendshapes not working in game engine",
                "causes": [
                    "Blendshapes not exported from Blender",
                    "Morph target naming mismatch",
                    "Import settings not configured correctly"
                ],
                "solutions": [
                    "1. Check FBX contains blendshapes (fbx_validator.py)",
                    "2. Verify blendshape names in engine match FBX exactly",
                    "3. Ensure morph targets imported:",
                    "   - Unreal: FBX Import > Skeletal Mesh > Import Morph Targets",
                    "   - Unity: Model Settings > Animation > Rig Type: Humanoid"
                ]
            },
            {
                "title": "Animation clipping through mesh",
                "causes": [
                    "Bone weights incorrect",
                    "Skeleton T-pose incorrect",
                    "High polygon areas over-deformed"
                ],
                "solutions": [
                    "1. Check skeleton rest pose is T-pose aligned",
                    "2. Verify bone weights using heat map in Blender",
                    "3. Check for weight painting errors on high-poly areas",
                    "4. Test with mesh optimization (reduce poly near joints)"
                ]
            },
            {
                "title": "Model performance issues",
                "causes": [
                    "Polygon count too high for platform",
                    "Too many draw calls",
                    "Textures resolution too high",
                    "Inefficient material setup"
                ],
                "solutions": [
                    "1. Run performance_analyzer.py for target platform",
                    "2. Generate LOD levels (LOD0/1/2/3)",
                    "3. Reduce texture resolution (2048 > 1024)",
                    "4. Use texture atlasing for multiple materials",
                    "5. Profile in target engine"
                ]
            },
            {
                "title": "Lip sync out of sync with audio",
                "causes": [
                    "Frame rate mismatch",
                    "Phoneme timing incorrect",
                    "Animation curves not smooth"
                ],
                "solutions": [
                    "1. Ensure animation frame rate matches audio",
                    "2. Regenerate lip sync: piper_lipsync_generator.py",
                    "3. Check phoneme-to-blendshape mapping",
                    "4. Apply animation smoothing in engine"
                ]
            }
        ]
        
        for issue in issues:
            content.append(issue["title"].upper())
            content.append("-" * 40)
            content.append("")
            
            content.append("Possible Causes:")
            for cause in issue["causes"]:
                content.append(f"  - {cause}")
            content.append("")
            
            content.append("Solutions:")
            for solution in issue["solutions"]:
                content.append(f"  {solution}")
            content.append("")
            content.append("")
        
        content.append("=" * 80)
        content.append("COMMON COMMANDS")
        content.append("=" * 80)
        content.append("")
        content.append("Validation:")
        content.append("  python scripts/fbx_validator.py exports/avatar_final.fbx")
        content.append("")
        content.append("Performance Analysis:")
        content.append("  python scripts/performance_analyzer.py --platform pc_vr_high")
        content.append("")
        content.append("Mesh Optimization:")
        content.append("  python scripts/mesh_optimizer.py --triangles 80000")
        content.append("")
        content.append("Animation Quality:")
        content.append("  python scripts/animation_quality_checker.py --output report.json")
        content.append("")
        
        doc_text = "\n".join(content)
        output_path.write_text(doc_text)
        logger.info(f"Troubleshooting guide: {output_path}")
    
    def generate_quick_start(self,
                            output_file: str = "QUICK_START.txt") -> None:
        """Generate quick start guide"""
        
        output_path = self.docs_dir / output_file
        
        content = []
        content.append("=" * 80)
        content.append("QUICK START GUIDE")
        content.append("=" * 80)
        content.append("")
        
        content.append("1. ENVIRONMENT SETUP")
        content.append("-" * 40)
        content.append("python -m venv .venv")
        content.append("source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows")
        content.append("pip install -e '.[dev]'")
        content.append("")
        
        content.append("2. VALIDATE AVATAR")
        content.append("-" * 40)
        content.append("python scripts/fbx_validator.py exports/avatar_final.fbx --html artifacts/report.html")
        content.append("Open artifacts/report.html in browser to review")
        content.append("")
        
        content.append("3. CHECK PERFORMANCE")
        content.append("-" * 40)
        content.append("python scripts/performance_analyzer.py --triangles 80000 --platform pc_vr_high")
        content.append("")
        
        content.append("4. EXTRACT METADATA")
        content.append("-" * 40)
        content.append("python scripts/metadata_extractor.py exports/avatar_final.fbx")
        content.append("")
        
        content.append("5. GENERATE PBR TEXTURES")
        content.append("-" * 40)
        content.append("python scripts/pbr_texture_processor.py --diffuse references/photos/scan.png")
        content.append("")
        
        content.append("6. CREATE LIP SYNC")
        content.append("-" * 40)
        content.append("python scripts/piper_lipsync_generator.py --text 'Hello world'")
        content.append("")
        
        content.append("7. BUILD WEB VIEWER")
        content.append("-" * 40)
        content.append("cd web/viewer && npm install && npm run dev")
        content.append("Open http://localhost:5173 in browser")
        content.append("")
        
        content.append("8. START BACKEND API")
        content.append("-" * 40)
        content.append("cd web/backend && pip install flask flask-cors")
        content.append("python app.py")
        content.append("API available at http://localhost:5000")
        content.append("")
        
        content.append("NEXT STEPS")
        content.append("-" * 40)
        content.append("1. Import FBX to target game engine (Unreal/Unity/Twinmotion)")
        content.append("2. Apply PBR materials")
        content.append("3. Test blendshapes and animations")
        content.append("4. Verify lip sync")
        content.append("5. Profile performance and optimize if needed")
        content.append("")
        
        doc_text = "\n".join(content)
        output_path.write_text(doc_text)
        logger.info(f"Quick start guide: {output_path}")
    
    def generate_all_documentation(self, metadata: dict = None,
                                  metrics: dict = None) -> None:
        """Generate all documentation"""
        
        logger.info("Generating project documentation...")
        
        if metadata:
            self.generate_asset_inventory(metadata)
        
        if metrics:
            self.generate_technical_specs(metrics)
        
        self.generate_troubleshooting_guide()
        self.generate_quick_start()
        
        logger.info("Documentation generation complete")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate documentation")
    parser.add_argument("--metadata", help="Metadata JSON file")
    parser.add_argument("--metrics", help="Metrics JSON file")
    parser.add_argument("--output-dir", default="docs")
    
    args = parser.parse_args()
    
    generator = DocumentGenerator(args.output_dir)
    
    metadata = None
    metrics = None
    
    if args.metadata:
        with open(args.metadata) as f:
            metadata = json.load(f)
    
    if args.metrics:
        with open(args.metrics) as f:
            metrics = json.load(f)
    
    generator.generate_all_documentation(metadata, metrics)