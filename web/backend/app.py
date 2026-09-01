#!/usr/bin/env python3
"""
Flask REST API for avatar viewer & management
- Model statistics endpoint
- Animation list endpoint
- Lip sync generation
- Performance reports
"""
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pathlib import Path
import json
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from fbx_validator import FBXValidator
from performance_analyzer import PerformanceAnalyzer

app = Flask(__name__)
CORS(app)

# Configuration
EXPORTS_DIR = Path(__file__).parent.parent.parent / "exports"
AVATARS_DIR = Path(__file__).parent.parent.parent / "source/metahuman"

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "ok", "message": "Avatar API running"})

@app.route('/api/avatar/info', methods=['GET'])
def avatar_info():
    """Get avatar metadata"""
    
    fbx_path = EXPORTS_DIR / "avatar_final.fbx"
    
    if not fbx_path.exists():
        return jsonify({"error": "Avatar not found"}), 404
    
    try:
        validator = FBXValidator(str(fbx_path))
        report = validator.run_full_validation()
        
        return jsonify({
            "filename": report.filename,
            "file_size_mb": report.file_size_mb,
            "is_valid": report.is_valid,
            "geometry": {
                "vertices": report.vertex_count,
                "triangles": report.triangle_count
            },
            "rigging": {
                "bones": report.bone_count,
                "blendshapes": report.blendshape_count
            },
            "materials": report.material_count,
            "engine_compatibility": report.engine_compatibility
        })
    
    except Exception as e:
        logger.error(f"Error reading FBX: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/performance', methods=['GET'])
def performance_metrics():
    """Get performance metrics"""
    
    platform = request.args.get('platform', 'pc_vr_high')
    
    try:
        analyzer = PerformanceAnalyzer()
        
        # Default metrics (would come from FBX analysis)
        metrics = analyzer.analyze(
            triangles=80000,
            vertices=40000,
            bones=60,
            blendshapes=48,
            materials=3,
            platform=platform
        )
        
        return jsonify({
            "platform": metrics.platform,
            "geometry": {
                "triangles": metrics.triangles,
                "vertices": metrics.vertices
            },
            "performance": {
                "estimated_fps": metrics.estimated_fps_target,
                "vram_mb": metrics.estimated_vram_mb,
                "score": metrics.performance_score
            },
            "bottleneck": metrics.bottleneck,
            "recommendations": metrics.recommendations
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/animations', methods=['GET'])
def animations_list():
    """List available animations"""
    
    animations_dir = EXPORTS_DIR / "animations" if (EXPORTS_DIR / "animations").exists() else None
    
    if not animations_dir or not animations_dir.exists():
        return jsonify({
            "animations": [
                {"name": "idle", "duration_s": 2.5, "category": "locomotion"},
                {"name": "walk", "duration_s": 1.2, "category": "locomotion"},
                {"name": "gesture_wave", "duration_s": 1.8, "category": "gesture"}
            ]
        })
    
    animations = []
    for fbx in animations_dir.glob("*.fbx"):
        animations.append({
            "name": fbx.stem,
            "file": fbx.name,
            "size_mb": fbx.stat().st_size / (1024**2)
        })
    
    return jsonify({"animations": animations})

@app.route('/api/textures', methods=['GET'])
def textures_info():
    """Get texture information"""
    
    textures_dir = Path(__file__).parent.parent.parent / "assets/textures/pbr"
    
    textures = {}
    
    if textures_dir.exists():
        for tex_type in ["diffuse", "normal", "roughness", "metallic", "ao"]:
            tex_path = textures_dir / f"{tex_type}.png"
            if tex_path.exists():
                textures[tex_type] = {
                    "filename": tex_path.name,
                    "size_mb": tex_path.stat().st_size / (1024**2),
                    "format": "PNG"
                }
    
    return jsonify({"textures": textures})

@app.route('/api/validation/fbx', methods=['POST'])
def validate_fbx():
    """Validate FBX file"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if not file.filename.endswith('.fbx'):
        return jsonify({"error": "Only FBX files supported"}), 400
    
    # Save temporary
    temp_path = Path("/tmp") / file.filename
    file.save(temp_path)
    
    try:
        validator = FBXValidator(str(temp_path))
        report = validator.run_full_validation()
        
        return jsonify({
            "is_valid": report.is_valid,
            "warnings": report.warnings,
            "errors": report.errors,
            "geometry": {
                "triangles": report.triangle_count,
                "vertices": report.vertex_count
            }
        })
    
    finally:
        temp_path.unlink()

@app.route('/api/export/fbx', methods=['GET'])
def download_fbx():
    """Download avatar FBX"""
    
    fbx_path = EXPORTS_DIR / "avatar_final.fbx"
    
    if not fbx_path.exists():
        return jsonify({"error": "FBX not found"}), 404
    
    return send_file(fbx_path, as_attachment=True)

@app.route('/api/export/<engine>', methods=['GET'])
def engine_export(engine):
    """Download engine-specific export"""
    
    engine_dir = EXPORTS_DIR / engine
    fbx_path = engine_dir / f"avatar_{engine}.fbx"
    
    if not fbx_path.exists():
        return jsonify({"error": f"Export for {engine} not available"}), 404
    
    return send_file(fbx_path, as_attachment=True)

if __name__ == "__main__":
    logger.info("Starting Avatar API server...")
    app.run(debug=True, host="0.0.0.0", port=5000)