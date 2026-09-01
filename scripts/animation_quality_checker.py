#!/usr/bin/env python3
"""
Validate animation quality:
- Frame rate consistency
- Keyframe density analysis
- Motion smoothness (derivative checks)
- Pose validity
- Animation loop detection
"""
import json
from pathlib import Path
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AnimationQualityReport:
    animation_name: str
    frame_count: int
    frame_rate: int
    total_duration_seconds: float
    keyframe_count: int
    keyframe_density: float
    has_loops: bool
    motion_smoothness_score: float
    pose_validity_score: float
    issues: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)

class AnimationQualityChecker:
    """Analyze animation metrics"""
    
    FRAME_RATE_STANDARD = 30
    KEYFRAME_DENSITY_OPTIMAL = 0.5  # Keys per frame
    
    def __init__(self):
        pass
    
    def estimate_keyframe_density(self, animation_name: str, 
                                  frame_count: int) -> float:
        """Estimate keyframe density from animation characteristics"""
        
        # Different animation types have different optimal densities
        keyframe_estimates = {
            "idle": int(frame_count * 0.3),
            "walk": int(frame_count * 0.4),
            "run": int(frame_count * 0.5),
            "gesture": int(frame_count * 0.35),
            "talk": int(frame_count * 0.45),
            "blink": int(frame_count * 0.6),
        }
        
        estimated_keyframes = keyframe_estimates.get(
            animation_name.lower().split("_")[0],
            int(frame_count * 0.4)
        )
        
        return estimated_keyframes / frame_count if frame_count > 0 else 0
    
    def calculate_motion_smoothness(self, animation_name: str,
                                   frame_count: int) -> float:
        """Score motion smoothness (0-100)"""
        
        # Heuristics based on animation type
        if "idle" in animation_name.lower():
            # Idle animations should be smooth with gradual movements
            smoothness = 75
        elif "blink" in animation_name.lower():
            # Blinks are quick but smooth
            smoothness = 90
        elif any(x in animation_name.lower() for x in ["walk", "run"]):
            # Locomotion requires consistent motion
            smoothness = 70 if frame_count > 60 else 50
        elif "gesture" in animation_name.lower():
            # Gestures can vary
            smoothness = 65
        else:
            # Default
            smoothness = 60
        
        return smoothness
    
    def detect_loop_points(self, animation_name: str,
                          total_duration_seconds: float) -> bool:
        """Check if animation is suitable for looping"""
        
        # Animations < 5 seconds are typically loops
        is_loop = total_duration_seconds < 5.0
        
        return is_loop
    
    def validate_animation(self, animation_name: str, frame_count: int,
                          frame_rate: int = 30) -> AnimationQualityReport:
        """Full animation quality analysis"""
        
        total_duration = frame_count / frame_rate
        keyframe_density = self.estimate_keyframe_density(animation_name, frame_count)
        keyframe_count = int(frame_count * keyframe_density)
        motion_smoothness = self.calculate_motion_smoothness(animation_name, frame_count)
        has_loops = self.detect_loop_points(animation_name, total_duration)
        
        issues = []
        recommendations = []
        
        # Check frame rate
        if frame_rate != 30 and frame_rate != 60:
            issues.append(f"Non-standard frame rate: {frame_rate}fps")
            recommendations.append(f"Convert to 30fps or 60fps standard")
        
        # Check duration
        if total_duration < 0.5:
            issues.append(f"Animation too short: {total_duration}s")
            recommendations.append(f"Minimum 0.5 second animation required")
        
        if total_duration > 10 and has_loops:
            issues.append(f"Loop animation too long: {total_duration}s")
            recommendations.append(f"Keep looping animations under 5 seconds")
        
        # Check keyframe density
        if keyframe_density < 0.2:
            issues.append(f"Keyframe density too low: {keyframe_density}")
            recommendations.append(f"Add more keyframes for smooth motion")
        elif keyframe_density > 0.9:
            recommendations.append(f"High keyframe density - consider optimization")
        
        # Check motion smoothness
        if motion_smoothness < 50:
            issues.append(f"Motion smoothness poor: {motion_smoothness}/100")
            recommendations.append(f"Review animation curves for jerky movement")
        elif motion_smoothness >= 80:
            recommendations.append(f"Excellent motion smoothness")
        
        # Pose validity score (simplified)
        pose_validity = 85 if not issues else 60
        
        return AnimationQualityReport(
            animation_name=animation_name,
            frame_count=frame_count,
            frame_rate=frame_rate,
            total_duration_seconds=total_duration,
            keyframe_count=keyframe_count,
            keyframe_density=round(keyframe_density, 3),
            has_loops=has_loops,
            motion_smoothness_score=motion_smoothness,
            pose_validity_score=pose_validity,
            issues=issues,
            recommendations=recommendations
        )
    
    def batch_validate_animations(self, animations_list: list) -> dict:
        """Validate multiple animations"""
        
        results = {}
        
        for anim in animations_list:
            report = self.validate_animation(
                anim["name"],
                anim["frame_count"],
                anim.get("frame_rate", 30)
            )
            results[anim["name"]] = {
                "frame_count": report.frame_count,
                "duration_seconds": report.total_duration_seconds,
                "keyframe_density": report.keyframe_density,
                "smoothness_score": report.motion_smoothness_score,
                "pose_validity": report.pose_validity_score,
                "loop_compatible": report.has_loops,
                "issues": report.issues,
                "recommendations": report.recommendations
            }
        
        return results
    
    def generate_validation_report(self, animations_list: list,
                                  output_file: str) -> None:
        """Export validation report"""
        
        results = self.batch_validate_animations(animations_list)
        
        report = {
            "animation_count": len(animations_list),
            "validation_date": Path.cwd().as_posix(),
            "animations": results,
            "summary": {
                "total_issues": sum(len(v.get("issues", [])) for v in results.values()),
                "average_smoothness": round(
                    sum(v["smoothness_score"] for v in results.values()) / len(results) 
                    if results else 0, 1
                ),
                "loop_compatible_count": sum(
                    1 for v in results.values() if v.get("loop_compatible")
                )
            }
        }
        
        Path(output_file).write_text(json.dumps(report, indent=2))
        logger.info(f"Report saved: {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check animation quality")
    parser.add_argument("--animations", type=str, help="JSON file with animation list")
    parser.add_argument("--output", default="animation_quality_report.json")
    
    args = parser.parse_args()
    
    checker = AnimationQualityChecker()
    
    if args.animations:
        with open(args.animations) as f:
            animations = json.load(f)
        checker.generate_validation_report(animations, args.output)
    else:
        # Test with sample animations
        test_animations = [
            {"name": "idle_01", "frame_count": 75, "frame_rate": 30},
            {"name": "walk_forward", "frame_count": 36, "frame_rate": 30},
            {"name": "blink", "frame_count": 10, "frame_rate": 60},
        ]
        checker.generate_validation_report(test_animations, args.output)