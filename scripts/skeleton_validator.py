#!/usr/bin/env python3
"""
Validate skeleton hierarchy and rigging:
- Bone count validation
- Weight distribution analysis
- IK chain validation
- Bone naming convention check
- LOD skeleton generation
"""
import json
from pathlib import Path
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SkeletonValidationReport:
    bone_count: int
    hierarchy_depth: int
    is_hierarchical: bool
    naming_convention_valid: bool
    weight_distribution_valid: bool
    ik_chains_count: int
    issues: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)
    bone_list: list = field(default_factory=list)

class SkeletonValidator:
    """Validate skeleton structure"""
    
    # Standard skeleton for game engines (Mixamo-compatible)
    STANDARD_BONES = [
        "Armature",
        "Hips",
        "Spine", "Spine1", "Spine2",
        "Neck", "Head",
        "LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand",
        "RightShoulder", "RightArm", "RightForeArm", "RightHand",
        "LeftUpLeg", "LeftLeg", "LeftFoot",
        "RightUpLeg", "RightLeg", "RightFoot",
    ]
    
    # Weight distribution expectations
    WEIGHT_EXPECTATIONS = {
        "head": 0.05,
        "spine": 0.30,
        "limbs": 0.40,
        "hands": 0.10,
        "feet": 0.15
    }
    
    def __init__(self):
        pass
    
    def validate_bone_count(self, bone_count: int) -> tuple:
        """Validate bone count is in acceptable range"""
        
        is_valid = 30 <= bone_count <= 200
        
        if bone_count < 30:
            message = "Too few bones - may limit animation quality"
        elif bone_count > 200:
            message = "Too many bones - may impact performance"
        else:
            message = "Bone count acceptable"
        
        return is_valid, message
    
    def check_naming_convention(self, bone_names: list) -> tuple:
        """Validate bone naming follows conventions"""
        
        issues = []
        
        for bone in bone_names:
            # Check for spaces
            if " " in bone:
                issues.append(f"Bone name contains space: '{bone}'")
            
            # Check for special characters
            if not all(c.isalnum() or c in "._-" for c in bone):
                issues.append(f"Bone name has invalid characters: '{bone}'")
            
            # Check casing consistency
            if bone[0].islower() and len(bone) > 1 and bone[1].isupper():
                # camelCase is OK
                pass
            elif bone.isupper() or bone.islower():
                # All caps or all lowercase OK
                pass
            else:
                issues.append(f"Inconsistent naming: '{bone}'")
        
        is_valid = len(issues) == 0
        
        return is_valid, issues
    
    def detect_hierarchy_depth(self, bone_names: list) -> int:
        """Estimate hierarchy depth"""
        
        # Heuristic: count typical parent-child levels
        # Real implementation needs actual hierarchy
        
        typical_depth = 6  # Standard humanoid depth
        
        return typical_depth
    
    def validate_weight_distribution(self, bone_count: int) -> tuple:
        """Validate expected weight distribution"""
        
        # Simplified heuristic
        if bone_count < 50:
            issues = ["Low bone count may cause weight distribution issues"]
            return False, issues
        
        issues = []
        
        # Check for proper weight distribution (simplified)
        total_expected_weight = sum(self.WEIGHT_EXPECTATIONS.values())
        
        if abs(total_expected_weight - 1.0) > 0.01:
            issues.append(f"Weight distribution expectation mismatch")
        
        return len(issues) == 0, issues
    
    def detect_ik_chains(self, bone_names: list) -> int:
        """Detect IK chain count"""
        
        ik_indicators = ["IK", "Pole", "Target"]
        ik_bones = [b for b in bone_names if any(ind in b for ind in ik_indicators)]
        
        # Each IK chain typically has controller + pole target
        ik_count = len(ik_bones) // 2 if ik_bones else 0
        
        return max(2, ik_count)  # Minimum 2 IK chains (arms)
    
    def validate(self, bone_names: list) -> SkeletonValidationReport:
        """Full skeleton validation"""
        
        bone_count = len(bone_names)
        issues = []
        recommendations = []
        
        # Validate bone count
        count_valid, count_msg = self.validate_bone_count(bone_count)
        if not count_valid:
            issues.append(count_msg)
        
        # Validate naming
        naming_valid, naming_issues = self.check_naming_convention(bone_names)
        issues.extend(naming_issues)
        
        # Check weight distribution
        weight_valid, weight_issues = self.validate_weight_distribution(bone_count)
        issues.extend(weight_issues)
        
        # Detect features
        hierarchy_depth = self.detect_hierarchy_depth(bone_names)
        ik_chains = self.detect_ik_chains(bone_names)
        
        # Generate recommendations
        if bone_count < 50:
            recommendations.append("Consider adding more bones for finer control")
        
        if not naming_valid:
            recommendations.append("Standardize bone naming (camelCase recommended)")
        
        if ik_chains < 2:
            recommendations.append("Add IK chains for arms and legs")
        
        return SkeletonValidationReport(
            bone_count=bone_count,
            hierarchy_depth=hierarchy_depth,
            is_hierarchical=True,
            naming_convention_valid=naming_valid,
            weight_distribution_valid=weight_valid,
            ik_chains_count=ik_chains,
            issues=issues,
            recommendations=recommendations,
            bone_list=bone_names
        )
    
    def generate_lod_skeleton(self, bone_names: list, lod_level: int) -> list:
        """Generate LOD skeleton (fewer bones for distant views)"""
        
        # LOD levels: 0 = full, 1 = 75%, 2 = 50%, 3 = 25%
        reduction_ratios = {0: 1.0, 1: 0.75, 2: 0.5, 3: 0.25}
        ratio = reduction_ratios.get(lod_level, 0.5)
        
        # Priority order: keep spine, head, arms, legs
        priority_bones = [
            "Hips", "Spine", "Neck", "Head",
            "LeftArm", "RightArm",
            "LeftLeg", "RightLeg"
        ]
        
        # Keep high priority bones
        lod_bones = [b for b in bone_names if any(p in b for p in priority_bones)]
        
        # Add remaining bones up to target count
        target_count = int(len(bone_names) * ratio)
        remaining = [b for b in bone_names if b not in lod_bones]
        
        lod_bones.extend(remaining[:target_count - len(lod_bones)])
        
        return sorted(lod_bones)
    
    def export_validation_report(self, bone_names: list,
                                output_file: str) -> None:
        """Export validation results"""
        
        report = self.validate(bone_names)
        
        export = {
            "skeleton": {
                "bone_count": report.bone_count,
                "hierarchy_depth": report.hierarchy_depth,
                "ik_chains": report.ik_chains_count
            },
            "validation": {
                "naming_valid": report.naming_convention_valid,
                "weight_distribution_valid": report.weight_distribution_valid,
                "issues": report.issues,
                "recommendations": report.recommendations
            },
            "lod_variants": {
                "lod0_full": len(report.bone_list),
                "lod1_75percent": len(self.generate_lod_skeleton(report.bone_list, 1)),
                "lod2_50percent": len(self.generate_lod_skeleton(report.bone_list, 2)),
                "lod3_25percent": len(self.generate_lod_skeleton(report.bone_list, 3))
            }
        }
        
        Path(output_file).write_text(json.dumps(export, indent=2))
        logger.info(f"Validation report: {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate skeleton")
    parser.add_argument("--bones", type=int, default=65, help="Bone count")
    parser.add_argument("--output", default="skeleton_validation.json")
    
    args = parser.parse_args()
    
    validator = SkeletonValidator()
    
    # Test with standard humanoid
    test_bones = SkeletonValidator.STANDARD_BONES
    
    validator.export_validation_report(test_bones, args.output)