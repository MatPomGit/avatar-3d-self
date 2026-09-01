#!/usr/bin/env python3
"""
Check overall project health:
- Verify all required files exist
- Validate directory structure
- Check file dependencies
- Generate health score
- Suggest improvements
"""
import json
from pathlib import Path
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class HealthCheckResult:
    project_root: str
    checks_passed: int
    checks_failed: int
    health_score: float
    issues: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)

class ProjectHealthChecker:
    """Check project structure and completeness"""
    
    REQUIRED_STRUCTURE = {
        "directories": [
            "scripts",
            "source/metahuman",
            "exports",
            "animations",
            "references/photos",
            "assets/textures",
            "docs",
            ".github/workflows",
            "tests",
            "web/viewer",
            "web/backend",
            "notebooks"
        ],
        "files": [
            "pyproject.toml",
            "README.md",
            ".gitignore",
            ".gitattributes",
            "LICENSE"
        ],
        "scripts": [
            "fbx_validator.py",
            "mesh_optimizer.py",
            "uv_analyzer.py",
            "performance_analyzer.py",
            "export_manager.py",
            "pbr_texture_processor.py",
            "material_converter.py",
            "piper_lipsync_generator.py",
            "animation_quality_checker.py",
            "skeleton_validator.py",
            "metadata_extractor.py",
            "batch_processor.py",
            "version_manager.py",
            "document_generator.py"
        ],
        "workflows": [
            "avatar_production_export.yml",
            "avatar_complete_pipeline.yml",
            "complete_avatar_build.yml"
        ]
    }
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.checks = []
    
    def check_directory_exists(self, dir_name: str) -> tuple:
        """Check if directory exists"""
        path = self.project_root / dir_name
        exists = path.is_dir()
        
        return exists, path
    
    def check_file_exists(self, file_name: str) -> tuple:
        """Check if file exists"""
        path = self.project_root / file_name
        exists = path.is_file()
        
        return exists, path
    
    def check_python_dependencies(self) -> dict:
        """Verify Python environment"""
        
        required_packages = [
            "pillow",
            "numpy",
            "trimesh",
            "flask",
            "flask-cors",
            "anthropic"
        ]
        
        missing = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        return {
            "required": required_packages,
            "missing": missing,
            "complete": len(missing) == 0
        }
    
    def check_file_integrity(self) -> list:
        """Check file integrity and sizes"""
        
        issues = []
        
        # Check FBX file
        fbx_path = self.project_root / "exports" / "avatar_final.fbx"
        if fbx_path.exists():
            size_mb = fbx_path.stat().st_size / (1024**2)
            
            if size_mb < 0.1:
                issues.append(f"FBX file suspiciously small: {size_mb:.2f} MB")
            elif size_mb > 500:
                issues.append(f"FBX file very large: {size_mb:.2f} MB (consider LOD)")
        
        # Check texture directory
        texture_dir = self.project_root / "assets" / "textures" / "pbr"
        if texture_dir.exists():
            texture_files = list(texture_dir.glob("*.png"))
            
            if len(texture_files) == 0:
                issues.append("No PBR textures found in assets/textures/pbr")
            elif len(texture_files) < 5:
                issues.append(f"Only {len(texture_files)}/5 PBR textures present")
        
        return issues
    
    def check_git_configuration(self) -> tuple:
        """Verify Git is properly configured"""
        
        gitignore_path = self.project_root / ".gitignore"
        gitattributes_path = self.project_root / ".gitattributes"
        
        gitignore_exists = gitignore_path.exists()
        gitattributes_exists = gitattributes_path.exists()
        
        if gitignore_exists:
            with open(gitignore_path) as f:
                content = f.read()
                has_lfs = "lfs" in content.lower()
        else:
            has_lfs = False
        
        return gitignore_exists, gitattributes_exists, has_lfs
    
    def run_health_check(self) -> HealthCheckResult:
        """Execute complete health check"""
        
        logger.info(f"Checking project health: {self.project_root}")
        
        passed = 0
        failed = 0
        issues = []
        warnings = []
        recommendations = []
        
        # Check directories
        for dir_name in self.REQUIRED_STRUCTURE["directories"]:
            exists, path = self.check_directory_exists(dir_name)
            
            if exists:
                passed += 1
            else:
                failed += 1
                issues.append(f"Missing directory: {dir_name}")
        
        # Check files
        for file_name in self.REQUIRED_STRUCTURE["files"]:
            exists, path = self.check_file_exists(file_name)
            
            if exists:
                passed += 1
            else:
                failed += 1
                issues.append(f"Missing file: {file_name}")
        
        # Check scripts
        scripts_dir = self.project_root / "scripts"
        if scripts_dir.exists():
            for script_name in self.REQUIRED_STRUCTURE["scripts"]:
                script_path = scripts_dir / script_name
                if script_path.exists():
                    passed += 1
                else:
                    failed += 1
                    warnings.append(f"Missing script: {script_name}")
        
        # Check workflows
        workflows_dir = self.project_root / ".github" / "workflows"
        if workflows_dir.exists():
            for workflow_name in self.REQUIRED_STRUCTURE["workflows"]:
                workflow_path = workflows_dir / workflow_name
                if workflow_path.exists():
                    passed += 1
                else:
                    failed += 1
                    warnings.append(f"Missing workflow: {workflow_name}")
        
        # Check Python dependencies
        dep_check = self.check_python_dependencies()
        if dep_check["complete"]:
            passed += 1
        else:
            failed += 1
            issues.append(f"Missing packages: {', '.join(dep_check['missing'])}")
            recommendations.append(f"Install: pip install {' '.join(dep_check['missing'])}")
        
        # Check file integrity
        integrity_issues = self.check_file_integrity()
        issues.extend(integrity_issues)
        failed += len(integrity_issues)
        
        # Check Git configuration
        has_gitignore, has_gitattributes, has_lfs = self.check_git_configuration()
        
        if not has_gitignore:
            warnings.append("Missing .gitignore file")
        else:
            passed += 1
        
        if not has_gitattributes:
            warnings.append("Consider adding .gitattributes for Git LFS")
        
        if not has_lfs:
            recommendations.append("Configure Git LFS for large binary files")
        
        # Calculate health score
        total_checks = passed + failed
        health_score = (passed / total_checks * 100) if total_checks > 0 else 0
        
        if health_score < 50:
            recommendations.append("Critical issues detected - address immediately")
        elif health_score < 80:
            recommendations.append("Several issues need attention")
        elif health_score < 95:
            recommendations.append("Minor improvements recommended")
        else:
            recommendations.append("Project structure is healthy")
        
        return HealthCheckResult(
            project_root=str(self.project_root),
            checks_passed=passed,
            checks_failed=failed,
            health_score=round(health_score, 1),
            issues=issues,
            warnings=warnings,
            recommendations=recommendations
        )
    
    def generate_health_report(self, output_file: str = "project_health.json") -> None:
        """Export health check results"""
        
        result = self.run_health_check()
        
        report = {
            "project": result.project_root,
            "timestamp": str(Path.cwd()),
            "health_score": result.health_score,
            "summary": {
                "checks_passed": result.checks_passed,
                "checks_failed": result.checks_failed,
                "total_checks": result.checks_passed + result.checks_failed
            },
            "issues": result.issues,
            "warnings": result.warnings,
            "recommendations": result.recommendations
        }
        
        Path(output_file).write_text(json.dumps(report, indent=2))
        
        logger.info(f"Health report: {output_file}")
        logger.info(f"Score: {result.health_score}/100")
        
        if result.issues:
            logger.error(f"Critical issues: {len(result.issues)}")
            for issue in result.issues:
                logger.error(f"  - {issue}")
        
        if result.warnings:
            logger.warning(f"Warnings: {len(result.warnings)}")
            for warning in result.warnings:
                logger.warning(f"  - {warning}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check project health")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output", default="project_health.json")
    
    args = parser.parse_args()
    
    checker = ProjectHealthChecker(args.project_root)
    checker.generate_health_report(args.output)