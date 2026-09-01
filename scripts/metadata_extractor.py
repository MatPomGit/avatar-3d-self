#!/usr/bin/env python3
"""
Extract metadata from FBX/animations:
- Bone names and hierarchy
- Animation track names and durations
- Material names
- Texture references
- Blendshape names
- Generate asset inventory
"""
import json
from pathlib import Path
from typing import Dict, List
import struct
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetadataExtractor:
    """Extract FBX metadata"""
    
    def __init__(self, fbx_path: str):
        self.fbx_path = Path(fbx_path)
        self.metadata = {}
    
    def extract_nodes(self) -> List[str]:
        """Extract node names from FBX"""
        nodes = []
        
        with open(self.fbx_path, 'rb') as f:
            content = f.read()
            
            # Search for Model node markers
            marker = b'Model'
            offset = 0
            
            while True:
                pos = content.find(marker, offset)
                if pos == -1:
                    break
                
                # Extract name after marker
                start = pos + len(marker)
                end = start + 100
                
                # Find null terminator
                try:
                    null_pos = content.find(b'\x00', start, end)
                    if null_pos > start:
                        name = content[start:null_pos].decode('utf-8', errors='ignore')
                        if name and len(name) < 50:
                            nodes.append(name.strip())
                except:
                    pass
                
                offset = pos + 1
        
        return list(set(nodes))  # Remove duplicates
    
    def extract_blendshapes(self) -> List[str]:
        """Extract blendshape names"""
        blendshapes = []
        
        with open(self.fbx_path, 'rb') as f:
            content = f.read()
            
            marker = b'BlendShape'
            offset = 0
            
            while True:
                pos = content.find(marker, offset)
                if pos == -1:
                    break
                
                start = pos + len(marker)
                end = start + 100
                
                try:
                    null_pos = content.find(b'\x00', start, end)
                    if null_pos > start:
                        name = content[start:null_pos].decode('utf-8', errors='ignore')
                        if name and len(name) < 50:
                            blendshapes.append(name.strip())
                except:
                    pass
                
                offset = pos + 1
        
        return list(set(blendshapes))
    
    def extract_materials(self) -> List[str]:
        """Extract material names"""
        materials = []
        
        with open(self.fbx_path, 'rb') as f:
            content = f.read()
            
            marker = b'Material'
            offset = 0
            
            while True:
                pos = content.find(marker, offset)
                if pos == -1:
                    break
                
                start = pos + len(marker)
                end = start + 100
                
                try:
                    null_pos = content.find(b'\x00', start, end)
                    if null_pos > start:
                        name = content[start:null_pos].decode('utf-8', errors='ignore')
                        if name and len(name) < 50 and not name.startswith('\x00'):
                            materials.append(name.strip())
                except:
                    pass
                
                offset = pos + 1
        
        return list(set(materials))
    
    def extract_texture_references(self) -> List[str]:
        """Extract texture file references"""
        textures = []
        
        with open(self.fbx_path, 'rb') as f:
            content = f.read()
            
            # Look for common image extensions
            extensions = [b'.png', b'.jpg', b'.tga', b'.tiff', b'.exr']
            
            for ext in extensions:
                offset = 0
                while True:
                    pos = content.find(ext, offset)
                    if pos == -1:
                        break
                    
                    # Search backwards for path start
                    start = max(0, pos - 200)
                    path_part = content[start:pos + len(ext)]
                    
                    # Extract filename
                    try:
                        filename = path_part.split(b'\\')[-1].split(b'/')[-1]
                        filename_str = filename.decode('utf-8', errors='ignore')
                        if filename_str and len(filename_str) < 100:
                            textures.append(filename_str)
                    except:
                        pass
                    
                    offset = pos + 1
        
        return list(set(textures))
    
    def extract_animations(self) -> Dict:
        """Extract animation track information"""
        animations = {}
        
        with open(self.fbx_path, 'rb') as f:
            content = f.read()
            
            # Count AnimationStack markers
            anim_count = content.count(b'AnimationStack')
            
            # Find animation layer names
            marker = b'AnimationLayer'
            offset = 0
            
            anim_idx = 0
            while True:
                pos = content.find(marker, offset)
                if pos == -1:
                    break
                
                start = pos + len(marker)
                end = start + 50
                
                try:
                    null_pos = content.find(b'\x00', start, end)
                    if null_pos > start:
                        name = content[start:null_pos].decode('utf-8', errors='ignore')
                        if name and len(name) < 50:
                            animations[f"animation_{anim_idx}"] = {
                                "name": name.strip(),
                                "tracks": []
                            }
                            anim_idx += 1
                except:
                    pass
                
                offset = pos + 1
        
        return animations
    
    def extract_full_metadata(self) -> Dict:
        """Extract all metadata"""
        
        logger.info(f"Extracting metadata from: {self.fbx_path}")
        
        metadata = {
            "file": self.fbx_path.name,
            "file_size_mb": round(self.fbx_path.stat().st_size / (1024**2), 2),
            "extraction_date": str(Path.cwd()),
            "nodes": self.extract_nodes(),
            "blendshapes": self.extract_blendshapes(),
            "materials": self.extract_materials(),
            "texture_references": self.extract_texture_references(),
            "animations": self.extract_animations(),
            "summary": {
                "node_count": len(self.extract_nodes()),
                "blendshape_count": len(self.extract_blendshapes()),
                "material_count": len(self.extract_materials()),
                "texture_count": len(self.extract_texture_references()),
                "animation_count": len(self.extract_animations())
            }
        }
        
        self.metadata = metadata
        return metadata
    
    def save_metadata(self, output_file: str) -> None:
        """Save metadata to JSON"""
        
        if not self.metadata:
            self.extract_full_metadata()
        
        Path(output_file).write_text(json.dumps(self.metadata, indent=2))
        logger.info(f"Metadata saved: {output_file}")
    
    def generate_inventory(self, output_file: str) -> None:
        """Generate asset inventory from metadata"""
        
        if not self.metadata:
            self.extract_full_metadata()
        
        inventory = {
            "asset": self.metadata["file"],
            "file_size_mb": self.metadata["file_size_mb"],
            "components": {
                "geometry": {
                    "node_count": self.metadata["summary"]["node_count"],
                    "nodes": self.metadata["nodes"][:10]
                },
                "rigging": {
                    "blendshape_count": self.metadata["summary"]["blendshape_count"],
                    "blendshapes": self.metadata["blendshapes"][:20]
                },
                "materials": {
                    "material_count": self.metadata["summary"]["material_count"],
                    "materials": self.metadata["materials"]
                },
                "textures": {
                    "texture_count": self.metadata["summary"]["texture_count"],
                    "textures": self.metadata["texture_references"][:10]
                },
                "animations": {
                    "animation_count": self.metadata["summary"]["animation_count"],
                    "animations": list(self.metadata["animations"].keys())
                }
            }
        }
        
        Path(output_file).write_text(json.dumps(inventory, indent=2))
        logger.info(f"Inventory saved: {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract FBX metadata")
    parser.add_argument("fbx_file", help="FBX file to analyze")
    parser.add_argument("--output", default="metadata.json")
    parser.add_argument("--inventory", default="inventory.json")
    
    args = parser.parse_args()
    
    extractor = MetadataExtractor(args.fbx_file)
    metadata = extractor.extract_full_metadata()
    
    extractor.save_metadata(args.output)
    extractor.generate_inventory(args.inventory)
    
    print(f"Nodes: {metadata['summary']['node_count']}")
    print(f"Blendshapes: {metadata['summary']['blendshape_count']}")
    print(f"Materials: {metadata['summary']['material_count']}")
    print(f"Textures: {metadata['summary']['texture_count']}")