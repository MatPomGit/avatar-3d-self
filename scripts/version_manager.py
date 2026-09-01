#!/usr/bin/env python3
"""
Manage asset versioning and snapshots:
- Create versioned snapshots
- Track changes between versions
- Store version metadata
- Generate changelog
- Manage version storage
"""
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import logging
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VersionManager:
    """Manage asset versions"""
    
    def __init__(self, versions_dir: str = "asset_versions"):
        self.versions_dir = Path(versions_dir)
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_file = self.versions_dir / "manifest.json"
    
    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()[:16]  # Short hash
    
    def load_manifest(self) -> Dict:
        """Load version manifest"""
        
        if self.manifest_file.exists():
            with open(self.manifest_file) as f:
                return json.load(f)
        
        return {
            "versions": [],
            "current_version": None,
            "total_versions": 0
        }
    
    def save_manifest(self, manifest: Dict) -> None:
        """Save version manifest"""
        
        self.manifest_file.write_text(json.dumps(manifest, indent=2))
    
    def create_version(self, fbx_file: str, description: str = "",
                      tags: List[str] = None) -> str:
        """Create new version snapshot"""
        
        if not Path(fbx_file).exists():
            raise FileNotFoundError(f"File not found: {fbx_file}")
        
        # Generate version ID
        timestamp = datetime.now()
        version_id = timestamp.strftime("%Y%m%d_%H%M%S")
        
        # Create version directory
        version_dir = self.versions_dir / version_id
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy asset
        fbx_path = Path(fbx_file)
        dest_fbx = version_dir / fbx_path.name
        shutil.copy2(fbx_file, dest_fbx)
        
        # Calculate hash
        file_hash = self.calculate_file_hash(fbx_file)
        file_size_mb = fbx_path.stat().st_size / (1024**2)
        
        # Create version metadata
        version_meta = {
            "version_id": version_id,
            "timestamp": timestamp.isoformat(),
            "file_name": fbx_path.name,
            "file_hash": file_hash,
            "file_size_mb": round(file_size_mb, 2),
            "description": description,
            "tags": tags or [],
            "path": str(dest_fbx)
        }
        
        # Update manifest
        manifest = self.load_manifest()
        manifest["versions"].append(version_meta)
        manifest["current_version"] = version_id
        manifest["total_versions"] = len(manifest["versions"])
        self.save_manifest(manifest)
        
        # Save version metadata
        meta_file = version_dir / "version_info.json"
        meta_file.write_text(json.dumps(version_meta, indent=2))
        
        logger.info(f"Created version: {version_id}")
        
        return version_id
    
    def get_version(self, version_id: str) -> Path:
        """Get path to specific version"""
        
        version_dir = self.versions_dir / version_id
        
        if not version_dir.exists():
            raise FileNotFoundError(f"Version not found: {version_id}")
        
        # Find FBX file
        fbx_files = list(version_dir.glob("*.fbx"))
        
        if not fbx_files:
            raise FileNotFoundError(f"No FBX in version {version_id}")
        
        return fbx_files[0]
    
    def compare_versions(self, version_id1: str,
                        version_id2: str) -> Dict:
        """Compare two versions"""
        
        manifest = self.load_manifest()
        
        v1 = next((v for v in manifest["versions"] if v["version_id"] == version_id1), None)
        v2 = next((v for v in manifest["versions"] if v["version_id"] == version_id2), None)
        
        if not v1 or not v2:
            raise ValueError("One or both versions not found")
        
        comparison = {
            "version_1": version_id1,
            "version_2": version_id2,
            "timestamp_1": v1["timestamp"],
            "timestamp_2": v2["timestamp"],
            "size_difference_mb": round(v2["file_size_mb"] - v1["file_size_mb"], 2),
            "hash_same": v1["file_hash"] == v2["file_hash"],
            "description_1": v1["description"],
            "description_2": v2["description"]
        }
        
        return comparison
    
    def generate_changelog(self, output_file: str) -> None:
        """Generate changelog from versions"""
        
        manifest = self.load_manifest()
        
        changelog = {
            "title": "Asset Version Changelog",
            "total_versions": manifest["total_versions"],
            "entries": []
        }
        
        # Sort versions by timestamp
        sorted_versions = sorted(
            manifest["versions"],
            key=lambda v: v["timestamp"],
            reverse=True
        )
        
        for i, version in enumerate(sorted_versions):
            entry = {
                "version": version["version_id"],
                "date": version["timestamp"],
                "description": version["description"],
                "file_size_mb": version["file_size_mb"],
                "tags": version["tags"],
                "file_hash": version["file_hash"]
            }
            
            # Add delta info
            if i < len(sorted_versions) - 1:
                prev_version = sorted_versions[i + 1]
                size_diff = version["file_size_mb"] - prev_version["file_size_mb"]
                entry["size_delta_mb"] = round(size_diff, 2)
            
            changelog["entries"].append(entry)
        
        Path(output_file).write_text(json.dumps(changelog, indent=2))
        logger.info(f"Changelog saved: {output_file}")
    
    def cleanup_old_versions(self, keep_count: int = 5) -> None:
        """Remove old version snapshots"""
        
        manifest = self.load_manifest()
        
        if len(manifest["versions"]) <= keep_count:
            logger.info(f"Only {len(manifest['versions'])} versions, no cleanup needed")
            return
        
        # Sort by timestamp
        sorted_versions = sorted(
            manifest["versions"],
            key=lambda v: v["timestamp"]
        )
        
        # Remove old versions
        to_remove = sorted_versions[:-keep_count]
        
        for version in to_remove:
            version_dir = self.versions_dir / version["version_id"]
            if version_dir.exists():
                shutil.rmtree(version_dir)
                logger.info(f"Removed version: {version['version_id']}")
        
        # Update manifest
        manifest["versions"] = sorted_versions[-keep_count:]
        self.save_manifest(manifest)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage asset versions")
    parser.add_argument("--action", choices=["create", "list", "compare", "changelog"],
                       default="list")
    parser.add_argument("--file", help="FBX file to version")
    parser.add_argument("--description", default="", help="Version description")
    parser.add_argument("--version1", help="First version to compare")
    parser.add_argument("--version2", help="Second version to compare")
    parser.add_argument("--output", default="changelog.json")
    parser.add_argument("--versions-dir", default="asset_versions")
    
    args = parser.parse_args()
    
    manager = VersionManager(args.versions_dir)
    
    if args.action == "create":
        if not args.file:
            parser.error("--file required for create action")
        version_id = manager.create_version(args.file, args.description)
        print(f"Created version: {version_id}")
    
    elif args.action == "list":
        manifest = manager.load_manifest()
        print(f"Total versions: {manifest['total_versions']}")
        for v in manifest["versions"][-5:]:
            print(f"  {v['version_id']}: {v['description']}")
    
    elif args.action == "compare":
        if not args.version1 or not args.version2:
            parser.error("--version1 and --version2 required")
        comparison = manager.compare_versions(args.version1, args.version2)
        print(json.dumps(comparison, indent=2))
    
    elif args.action == "changelog":
        manager.generate_changelog(args.output)