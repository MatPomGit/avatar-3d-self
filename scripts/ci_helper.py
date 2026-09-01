#!/usr/bin/env python3
"""
Helper functions for CI/CD pipeline:
- Pre-commit checks
- Test execution
- Artifact management
- Deployment verification
- Build status reporting
"""
import json
import subprocess
from pathlib import Path
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CIHelper:
    """Manage CI/CD operations"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.artifacts_dir = self.project_root / "artifacts"
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    def run_pre_commit_checks(self) -> Dict:
        """Execute pre-commit validation"""
        
        logger.info("Running pre-commit checks...")
        
        checks = {
            "python_syntax": self._check_python_syntax(),
            "linting": self._check_linting(),
            "file_size": self._check_file_sizes(),
            "git_status": self._check_git_status()
        }
        
        all_passed = all(checks.values())
        
        return {
            "all_passed": all_passed,
            "checks": checks,
            "timestamp": str(Path.cwd())
        }
    
    def _check_python_syntax(self) -> bool:
        """Validate Python syntax"""
        
        scripts_dir = self.project_root / "scripts"
        
        if not scripts_dir.exists():
            return True
        
        python_files = list(scripts_dir.glob("*.py"))
        
        all_valid = True
        
        for py_file in python_files:
            try:
                compile(py_file.read_text(), py_file, 'exec')
                logger.info(f"  OK: {py_file.name}")
            except SyntaxError as e:
                logger.error(f"  ERROR: {py_file.name} - {e}")
                all_valid = False
        
        return all_valid
    
    def _check_linting(self) -> bool:
        """Run basic linting"""
        
        scripts_dir = self.project_root / "scripts"
        
        if not scripts_dir.exists():
            return True
        
        python_files = list(scripts_dir.glob("*.py"))
        
        issues = []
        
        for py_file in python_files:
            content = py_file.read_text()
            
            # Check for common issues
            if "import *" in content:
                issues.append(f"{py_file.name}: wildcard import found")
            
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if len(line) > 120:
                    issues.append(f"{py_file.name}:{i}: line too long ({len(line)} chars)")
        
        if issues:
            logger.warning("Linting issues found:")
            for issue in issues[:10]:
                logger.warning(f"  - {issue}")
        
        return len(issues) == 0
    
    def _check_file_sizes(self) -> bool:
        """Validate file sizes"""
        
        max_size_mb = 100
        
        large_files = []
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                size_mb = file_path.stat().st_size / (1024**2)
                
                if size_mb > max_size_mb:
                    large_files.append({
                        "path": str(file_path.relative_to(self.project_root)),
                        "size_mb": round(size_mb, 2)
                    })
        
        if large_files:
            logger.warning(f"Found {len(large_files)} large files:")
            for f in large_files[:5]:
                logger.warning(f"  - {f['path']} ({f['size_mb']} MB)")
        
        return True
    
    def _check_git_status(self) -> bool:
        """Check Git repository status"""
        
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                status = result.stdout
                
                if status:
                    logger.warning("Uncommitted changes detected:")
                    for line in status.split('\n')[:5]:
                        if line:
                            logger.warning(f"  {line}")
                    return False
                
                return True
            
            return True
        
        except FileNotFoundError:
            logger.warning("Git not found - skipping status check")
            return True
    
    def run_tests(self, test_dir: str = "tests") -> Dict:
        """Execute project tests"""
        
        logger.info("Running tests...")
        
        test_path = self.project_root / test_dir
        
        if not test_path.exists():
            logger.warning(f"Test directory not found: {test_dir}")
            return {"status": "skipped", "message": "No test directory"}
        
        test_files = list(test_path.glob("test_*.py"))
        
        results = {
            "total": len(test_files),
            "passed": 0,
            "failed": 0,
            "tests": []
        }
        
        for test_file in test_files:
            try:
                result = subprocess.run(
                    ["python", "-m", "pytest", str(test_file), "-v"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    results["passed"] += 1
                    logger.info(f"  PASS: {test_file.name}")
                else:
                    results["failed"] += 1
                    logger.error(f"  FAIL: {test_file.name}")
            
            except Exception as e:
                results["failed"] += 1
                logger.error(f"  ERROR: {test_file.name} - {e}")
        
        return results
    
    def verify_artifacts(self) -> Dict:
        """Verify build artifacts"""
        
        logger.info("Verifying artifacts...")
        
        artifacts_expected = [
            "exports/avatar_final.fbx",
            "exports/materials",
            "web/viewer/dist",
            "project_health.json",
            "EXPORT_CHECKLIST.json"
        ]
        
        verification = {
            "present": [],
            "missing": [],
            "total": len(artifacts_expected)
        }
        
        for artifact in artifacts_expected:
            artifact_path = self.project_root / artifact
            
            if artifact_path.exists():
                verification["present"].append(artifact)
                logger.info(f"  OK: {artifact}")
            else:
                verification["missing"].append(artifact)
                logger.warning(f"  MISSING: {artifact}")
        
        return verification
    
    def generate_build_report(self, output_file: str = "build_report.json") -> None:
        """Generate complete build report"""
        
        logger.info("Generating build report...")
        
        pre_commit = self.run_pre_commit_checks()
        tests = self.run_tests()
        artifacts = self.verify_artifacts()
        
        report = {
            "timestamp": str(Path.cwd()),
            "pre_commit_checks": pre_commit,
            "tests": tests,
            "artifacts": artifacts,
            "status": "success" if pre_commit["all_passed"] and artifacts["missing"] == [] else "failure"
        }
        
        output_path = self.artifacts_dir / output_file
        output_path.write_text(json.dumps(report, indent=2))
        
        logger.info(f"Build report: {output_path}")
        logger.info(f"Overall status: {report['status'].upper()}")
        
        return report

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CI/CD helper")
    parser.add_argument("--check", action="store_true", help="Run pre-commit checks")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--verify", action="store_true", help="Verify artifacts")
    parser.add_argument("--report", action="store_true", help="Generate full report")
    parser.add_argument("--project-root", default=".")
    
    args = parser.parse_args()
    
    helper = CIHelper(args.project_root)
    
    if args.check or args.report:
        result = helper.run_pre_commit_checks()
        print(json.dumps(result, indent=2))
    
    if args.test or args.report:
        result = helper.run_tests()
        print(json.dumps(result, indent=2))
    
    if args.verify or args.report:
        result = helper.verify_artifacts()
        print(json.dumps(result, indent=2))
    
    if args.report:
        helper.generate_build_report()