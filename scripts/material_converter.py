#!/usr/bin/env python3
"""
Convert PBR materials between engine formats.
Unreal → Unity, Unity → Twinmotion, etc.
"""
import json
from pathlib import Path
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PBRMaterial:
    """Universal PBR material definition"""
    name: str
    diffuse_path: str  # Albedo texture
    normal_path: str
    roughness_path: str
    metallic_path: str
    ao_path: str  # Ambient occlusion
    
    # Material properties
    roughness_factor: float = 0.5
    metallic_factor: float = 0.0
    ao_factor: float = 1.0
    
    # Engine-specific overrides
    ue_properties: dict = None
    unity_properties: dict = None
    twinmotion_properties: dict = None

class MaterialConverter:
    """Convert PBR materials between engine specifications"""
    
    # Unreal Engine 5 material node setup
    UE5_TEMPLATE = {
        "base_color": {"type": "TextureSample", "texture": "albedo"},
        "normal": {"type": "TextureSample", "texture": "normal"},
        "roughness": {"type": "ScalarParameter", "value": 0.5},
        "metallic": {"type": "ScalarParameter", "value": 0.0},
        "ambient_occlusion": {"type": "TextureSample", "texture": "ao"}
    }
    
    # Unity material setup
    UNITY_TEMPLATE = {
        "_MainTex": "albedo",
        "_BumpMap": "normal",
        "_Glossiness": 0.5,
        "_Metallic": 0.0,
        "_OcclusionMap": "ao",
        "shader": "Standard (Specular setup)"
    }
    
    # Twinmotion material setup
    TWINMOTION_TEMPLATE = {
        "DiffuseTexture": "albedo",
        "NormalMap": "normal",
        "RoughnessMap": "roughness",
        "MetallicMap": "metallic",
        "AOMap": "ao",
        "MaterialType": "PBRMaterial"
    }
    
    def __init__(self, textures_dir: str = "assets/textures"):
        self.textures_dir = Path(textures_dir)
        self.textures_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_ue5_material_instance(self, material: PBRMaterial) -> dict:
        """Generate Unreal Engine 5 material instance JSON"""
        return {
            "version": "5.3",
            "material_name": material.name,
            "material_class": "/Engine/Materials/M_PBRMaster",
            "parameters": {
                "texture_base_color": material.diffuse_path,
                "texture_normal": material.normal_path,
                "scalar_roughness": material.roughness_factor,
                "scalar_metallic": material.metallic_factor,
                "texture_ao": material.ao_path,
                "scalar_ao_strength": material.ao_factor,
                # UE-specific tweaks
                **(material.ue_properties or {})
            },
            "subsurface_scattering": {
                "enabled": True,
                "strength": 0.3,  # Skin SSS
                "color": [1.0, 0.8, 0.6]
            }
        }
    
    def generate_unity_material(self, material: PBRMaterial) -> dict:
        """Generate Unity material setup (compatible with Standard/HDRP)"""
        return {
            "shader": "Standard",
            "material_name": material.name,
            "properties": {
                "_MainTex": {"type": "Texture", "value": material.diffuse_path},
                "_BumpMap": {"type": "Texture", "value": material.normal_path},
                "_MetallicGlossMap": {"type": "Texture", "value": material.metallic_path},
                "_OcclusionMap": {"type": "Texture", "value": material.ao_path},
                "_Glossiness": {"type": "Float", "value": 1.0 - material.roughness_factor},
                "_Metallic": {"type": "Float", "value": material.metallic_factor},
                # HDRP addition
                "_Smoothness": 1.0 - material.roughness_factor,
                **(material.unity_properties or {})
            },
            "renderQueue": 2000,
            "tags": {"RenderType": "Opaque"}
        }
    
    def generate_twinmotion_material(self, material: PBRMaterial) -> dict:
        """Generate Twinmotion-compatible material"""
        return {
            "material_name": material.name,
            "material_type": "PBRMaterial",
            "textures": {
                "diffuse": material.diffuse_path,
                "normal": material.normal_path,
                "roughness": material.roughness_path,
                "metallic": material.metallic_path,
                "ambient_occlusion": material.ao_path
            },
            "parameters": {
                "roughness": material.roughness_factor,
                "metallic": material.metallic_factor,
                "ao_strength": material.ao_factor,
                # Twinmotion-specific
                "bump_height": 1.0,
                "reflection_strength": 0.8
            },
            **(material.twinmotion_properties or {})
        }
    
    def export_multi_engine(self, material: PBRMaterial, output_dir: str) -> None:
        """Export material in all engine formats"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Unreal Engine
        ue_config = self.generate_ue5_material_instance(material)
        ue_file = output_path / f"{material.name}_UE5.json"
        ue_file.write_text(json.dumps(ue_config, indent=2))
        logger.info(f"✓ UE5 material: {ue_file}")
        
        # Unity
        unity_config = self.generate_unity_material(material)
        unity_file = output_path / f"{material.name}_Unity.json"
        unity_file.write_text(json.dumps(unity_config, indent=2))
        logger.info(f"✓ Unity material: {unity_file}")
        
        # Twinmotion
        tm_config = self.generate_twinmotion_material(material)
        tm_file = output_path / f"{material.name}_Twinmotion.json"
        tm_file.write_text(json.dumps(tm_config, indent=2))
        logger.info(f"✓ Twinmotion material: {tm_file}")

# Skin material (realistic)
SKIN_MATERIAL = PBRMaterial(
    name="Skin_Face",
    diffuse_path="assets/textures/skin_diffuse.png",
    normal_path="assets/textures/skin_normal.png",
    roughness_path="assets/textures/skin_roughness.png",
    metallic_path="assets/textures/skin_metallic.png",
    ao_path="assets/textures/skin_ao.png",
    roughness_factor=0.45,
    metallic_factor=0.0,
    ao_factor=1.0,
    ue_properties={
        "subsurface_radius": 1.5,
        "subsurface_color": [1.0, 0.75, 0.6]
    }
)

if __name__ == "__main__":
    converter = MaterialConverter()
    converter.export_multi_engine(SKIN_MATERIAL, "exports/materials")
    logger.info("✓✓✓ Material export complete")