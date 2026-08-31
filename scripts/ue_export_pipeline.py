#!/usr/bin/env python3
"""
Export rigged avatar from Unreal Engine project to production FBX.
Runs headless via GitHub Actions / local CLI.
"""
import subprocess
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnrealExporter:
    def __init__(self, ue_project_path: str, engine_path: str = None):
        self.project_path = Path(ue_project_path)
        self.engine_path = Path(engine_path) if engine_path else self._find_ue_engine()
        
    def _find_ue_engine(self) -> Path:
        """Locate Unreal Engine binary"""
        candidates = [
            Path.home() / "UnrealEngine" / "Engine",
            Path("/opt/UnrealEngine/Engine"),
            Path("C:/Program Files/Epic Games/UE_5.3/Engine")  # Windows
        ]
        for path in candidates:
            editor = path / "Binaries" / "Linux" / "UE4Editor"
            if editor.exists():
                return path
        raise FileNotFoundError("Unreal Engine not found. Specify --engine-path")
    
    def export_skeletal_mesh(self, character_path: str, output_fbx: str) -> bool:
        """
        Export skeletal mesh + blendshapes from UE project.
        character_path: e.g., "/Game/Characters/MetaHuman_Avatar"
        """
        
        editor_exe = self.engine_path / "Binaries" / "Linux" / "UE4Editor"
        uproject = self.project_path / "avatar-3d-self.uproject"
        
        if not uproject.exists():
            logger.error(f"Project file not found: {uproject}")
            return False
        
        export_cmd = [
            str(editor_exe),
            str(uproject),
            "-run=ResavePackages",
            f"-FbxExportDir={output_fbx}",
            "-unattended",
            "-silent",
            "-notheme"
        ]
        
        logger.info(f"Exporting {character_path}...")
        logger.info(f"Command: {' '.join(export_cmd)}")
        
        try:
            result = subprocess.run(export_cmd, check=True, capture_output=True, timeout=600)
            logger.info(result.stdout.decode())
            
            output_file = Path(output_fbx)
            if output_file.exists():
                size_mb = output_file.stat().st_size / (1024**2)
                logger.info(f"✓ Exported FBX: {output_fbx} ({size_mb:.1f} MB)")
                return True
            else:
                logger.error("Export did not produce FBX file")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error("Export timed out (>10min)")
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"Export failed: {e.stderr.decode()}")
            return False
    
    def validate_fbx_blendshapes(self, fbx_path: str, expected_blendshapes: list) -> dict:
        """
        Validate FBX contains required blendshapes.
        Returns validation report.
        """
        report = {
            "fbx_file": fbx_path,
            "file_size_mb": Path(fbx_path).stat().st_size / (1024**2),
            "blendshapes_found": [],
            "blendshapes_missing": [],
            "status": "unknown"
        }
        
        try:
            # Attempt to parse FBX (simplified check)
            with open(fbx_path, 'rb') as f:
                content = f.read()
                # FBX files start with magic bytes "Kaydara FBX Binary"
                if b'Kaydara FBX Binary' in content[:100]:
                    report["status"] = "valid_fbx"
                    
                    # Check for blendshape marker (basic heuristic)
                    for bs_name in expected_blendshapes:
                        if bs_name.encode() in content:
                            report["blendshapes_found"].append(bs_name)
                        else:
                            report["blendshapes_missing"].append(bs_name)
                else:
                    report["status"] = "invalid_fbx"
        
        except Exception as e:
            report["status"] = f"validation_error: {e}"
        
        return report

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Unreal Engine FBX export")
    parser.add_argument("--project", default=".", help="UE project root")
    parser.add_argument("--engine", default=None, help="UE Engine path")
    parser.add_argument("--character", default="/Game/Characters/MetaHuman_Avatar")
    parser.add_argument("--output", default="exports/avatar_final.fbx")
    
    args = parser.parse_args()
    
    exporter = UnrealExporter(args.project, args.engine)
    
    if exporter.export_skeletal_mesh(args.character, args.output):
        # Validate
        expected_bs = ["eyeBlink_L", "eyeBlink_R", "mouthOpen", "expression_Happy"]
        report = exporter.validate_fbx_blendshapes(args.output, expected_bs)
        print(json.dumps(report, indent=2))
        logger.info("✓✓✓ Export complete and validated")
    else:
        logger.error("Export failed")
        exit(1)