#!/usr/bin/env python3
"""
Manage exports for multiple game engines:
- Prepare FBX variants per engine
- Verify material compatibility
- Generate engine-specific configs
- Create export manifests
"""
import json
from pathlib import Path
from typing import Dict, List
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExportManager:
    """Manage cross-engine exports"""
    
    EXPORT_PROFILES = {
        "unreal_engine_5": {
            "fbx_settings": {
                "use_skeletal_mesh": True,
                "import_morph_targets": True,
                "import_materials": True,
                "create_physics_asset": False,
                "skeletal_mesh_import_data": {
                    "normal_import_method": 0,
                    "material_search_location": ""
                }
            },
            "material_format": "ue5_json",
            "texture_requirements": {
                "diffuse": "sRGB",
                "normal": "Linear",
                "roughness": "Linear",
                "metallic": "Linear",
                "ao": "Linear"
            },
            "animation_settings": {
                "convert_animations": True,
                "remove_redundant_keys": True,
                "rate_scale": 1.0
            }
        },
        "unity": {
            "fbx_settings": {
                "model": {
                    "meshes": True,
                    "animations": True,
                    "materials": False  # Import materials separately
                },
                "rig": {
                    "animate_physics": True,
                    "optimization": "General"
                },
                "deformation": {
                    "skin_weights": "Standard",
                    "max_bones_per_vertex": 4
                }
            },
            "material_format": "unity_json",
            "shader": "Standard (Specular setup)",
            "render_pipeline": "HDRP",  # or URP
            "texture_requirements": {
                "diffuse": "sRGB",
                "normal": "Normal (DXT5, BC5)",
                "roughness": "Linear",
                "metallic": "Linear"
            }
        },
        "twinmotion": {
            "fbx_settings": {
                "import_materials": True,
                "import_textures": True,
                "scale_factor": 1.0
            },
            "material_format": "twinmotion_json",
            "material_type": "PBRMaterial",
            "quality_preset": "HighQuality",
            "export_format": "glTF 2.0"  # Also supports FBX
        },
        "babylon_js": {
            "format": "glTF 2.0",
            "material_format": "babylon_pbr",
            "extensions": ["KHR_materials_transmission"],
            "optimization": {
                "draco_compression": True,
                "texture_compression": "KTX2"
            }
        }
    }
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.exports_dir = self.project_root / "exports"
        self.exports_dir.mkdir(exist_ok=True)
    
    def create_export_variant(self, engine: str, base_fbx: str,
                            output_dir: str = None) -> Dict:
        """Prepare export for specific engine"""
        
        if engine not in self.EXPORT_PROFILES:
            raise ValueError(f"Unknown engine: {engine}")
        
        profile = self.EXPORT_PROFILES[engine]
        output_path = Path(output_dir) if output_dir else self.exports_dir / engine
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create engine-specific config
        config = {
            "engine": engine,
            "source_fbx": base_fbx,
            "export_profile": profile,
            "generated_at": datetime.now().isoformat(),
            "files": {
                "fbx": str(output_path / f"avatar_{engine}.fbx"),
                "materials": str(output_path / "materials.json"),
                "config": str(output_path / "export_config.json")
            }
        }
        
        # Save config
        config_file = output_path / "export_config.json"
        config_file.write_text(json.dumps(config, indent=2))
        
        logger.info(f"✓ Created export config for {engine}: {config_file}")
        
        return config
    
    def generate_material_manifest(self, engine: str, output_file: str) -> None:
        """Generate material import guide per engine"""
        
        profile = self.EXPORT_PROFILES.get(engine)
        if not profile:
            raise ValueError(f"Unknown engine: {engine}")
        
        if engine == "unreal_engine_5":
            manifest = {
                "engine": "unreal_engine_5",
                "import_workflow": [
                    "1. Copy FBX to Content/Characters/",
                    "2. Configure FBX import settings (see export_config.json)",
                    "3. Create Material Instance from M_Avatar_Master",
                    "4. Assign textures (diffuse, normal, roughness, metallic, AO)",
                    "5. Enable Subsurface Scattering for skin"
                ],
                "material_instances": {
                    "Skin_Face": {
                        "parent_material": "M_Avatar_Master",
                        "parameters": {
                            "Base_Color": "diffuse.png",
                            "Normal": "normal.png",
                            "Roughness": 0.45,
                            "Subsurface_Radius": 1.5
                        }
                    }
                }
            }
        
        elif engine == "unity":
            manifest = {
                "engine": "unity",
                "import_workflow": [
                    "1. Import FBX to Assets/Characters/",
                    "2. Drag-drop materials folder",
                    "3. Create Material using Standard/HDRP shader",
                    "4. Assign textures via Material Inspector",
                    "5. Add AvatarAnimator.cs script for blendshape control"
                ],
                "shader": profile.get("shader"),
                "render_pipeline": profile.get("render_pipeline")
            }
        
        elif engine == "twinmotion":
            manifest = {
                "engine": "twinmotion",
                "import_workflow": [
                    "1. Drag FBX into Twinmotion scene",
                    "2. Material Library → Create Material from JSON",
                    "3. Assign from materials.json",
                    "4. Adjust lighting for photorealism"
                ],
                "quality_preset": profile.get("quality_preset")
            }
        
        else:
            manifest = {"engine": engine, "profile": profile}
        
        Path(output_file).write_text(json.dumps(manifest, indent=2))
        logger.info(f"✓ Material manifest: {output_file}")
    
    def create_export_checklist(self, engines: List[str], output_file: str) -> None:
        """Generate pre-export checklist"""
        
        checklist = {
            "pre_export_validation": [
                "☐ FBX passes fbx_validator.py (no errors)",
                "☐ Blendshape count ≥ 48",
                "☐ Polygon count optimized for target platform",
                "☐ UV mapping complete (no missing UVs)",
                "☐ All bones properly weighted",
                "☐ Materials assigned correctly",
                "☐ Textures exist and accessible",
                "☐ Performance metrics acceptable (see performance_report.json)"
            ],
            "per_engine_export": {}
        }
        
        for engine in engines:
            if engine not in self.EXPORT_PROFILES:
                continue
            
            checklist["per_engine_export"][engine] = [
                f"☐ Create export variant via export_manager.py --engine {engine}",
                f"☐ Review material manifest ({engine}/materials.json)",
                f"☐ Test in {engine} (import, check materials, play animations)",
                f"☐ Verify blendshapes functional",
                f"☐ Check performance (target FPS)",
                f"☐ Screenshot proof of success"
            ]
        
        Path(output_file).write_text(json.dumps(checklist, indent=2))
        logger.info(f"✓ Export checklist: {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage multi-engine exports")
    parser.add_argument("--base-fbx", required=True, help="Base FBX file")
    parser.add_argument("--engine", choices=list(ExportManager.EXPORT_PROFILES.keys()),
                       help="Export for specific engine")
    parser.add_argument("--all", action="store_true", help="Export for all engines")
    parser.add_argument("--output-dir", default="exports")
    
    args = parser.parse_args()
    
    manager = ExportManager()
    
    if args.all:
        engines = list(ExportManager.EXPORT_PROFILES.keys())
    elif args.engine:
        engines = [args.engine]
    else:
        engines = []
    
    for eng in engines:
        config = manager.create_export_variant(eng, args.base_fbx, args.output_dir)
        manager.generate_material_manifest(eng, Path(args.output_dir) / eng / "materials.json")
    
    if engines:
        manager.create_export_checklist(engines, Path(args.output_dir) / "EXPORT_CHECKLIST.json")
        logger.info(f"✓✓✓ Export configs created for {len(engines)} engines")