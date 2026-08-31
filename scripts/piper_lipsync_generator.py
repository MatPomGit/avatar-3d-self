#!/usr/bin/env python3
"""
Lip sync animation from text using Piper TTS + phoneme detection.
Generates blendshape values timed to speech.
"""
import json
import subprocess
from pathlib import Path
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PiperLipSyncGenerator:
    """Generate lip sync data from text using Piper TTS"""
    
    # Phoneme → Blendshape mapping
    PHONEME_BLENDSHAPE_MAP = {
        # Vowels
        'a': {'mouthOpen': 0.8, 'mouthWide': 0.5},
        'e': {'mouthOpen': 0.6, 'mouthWide': 0.7},
        'i': {'mouthOpen': 0.4, 'mouthWide': 0.6},
        'o': {'mouthOpen': 0.9, 'mouthWide': 0.3},
        'u': {'mouthOpen': 0.7, 'mouthWide': 0.2},
        
        # Consonants (lips)
        'p': {'mouthPress_L': 1.0, 'mouthPress_R': 1.0},
        'b': {'mouthPress_L': 1.0, 'mouthPress_R': 1.0},
        'm': {'mouthPress_L': 1.0, 'mouthPress_R': 1.0},
        'f': {'mouthUpperUp_L': 0.7, 'mouthUpperUp_R': 0.7},
        'v': {'mouthUpperUp_L': 0.7, 'mouthUpperUp_R': 0.7},
        
        # Tongue/Jaw
        'th': {'jawOpen': 0.5, 'mouthOpen': 0.5},
        'n': {'jawOpen': 0.3},
        'l': {'jawOpen': 0.4},
        't': {'jawOpen': 0.5},
        'd': {'jawOpen': 0.5},
        's': {'mouthSmile_L': 0.3, 'mouthSmile_R': 0.3},
        'sh': {'mouthWide': 0.4},
        
        # Neutral/silence
        'sil': {'mouthOpen': 0.0, 'mouthWide': 0.0},
    }
    
    def __init__(self, piper_executable: str = "piper"):
        self.piper_exe = piper_executable
    
    def synthesize_with_phonemes(self, text: str, output_audio: str, 
                                output_phonemes: str) -> bool:
        """
        Use Piper TTS to synthesize speech + extract phoneme timing.
        
        Piper outputs: phoneme, start_time, end_time
        """
        logger.info(f"Synthesizing with Piper: '{text}'")
        
        cmd = [
            self.piper_exe,
            "--model", "en_US-libritts-high",
            "--output_file", output_audio,
            "--output_phonemes", output_phonemes,
            "--text", text
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"✓ Audio generated: {output_audio}")
            logger.info(f"✓ Phonemes saved: {output_phonemes}")
            return True
        except FileNotFoundError:
            logger.error("Piper not found. Install: pip install piper-tts")
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"Piper synthesis failed: {e.stderr.decode()}")
            return False
    
    def parse_phoneme_timeline(self, phoneme_file: str) -> List[Dict]:
        """
        Parse Piper phoneme output.
        Format: phoneme start_ms end_ms
        """
        timeline = []
        
        try:
            with open(phoneme_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        phoneme = parts[0]
                        start_time = int(parts[1])
                        end_time = int(parts[2])
                        
                        timeline.append({
                            "phoneme": phoneme,
                            "start_ms": start_time,
                            "end_ms": end_time,
                            "duration_ms": end_time - start_time
                        })
            
            logger.info(f"✓ Parsed {len(timeline)} phonemes")
            return timeline
        
        except Exception as e:
            logger.error(f"Failed to parse phonemes: {e}")
            return []
    
    def generate_blendshape_keyframes(self, phoneme_timeline: List[Dict], 
                                     fps: int = 30) -> Dict:
        """
        Convert phoneme timeline → blendshape keyframe animation.
        
        Output format for game engines:
        {
            "frame": blendshape_values
        }
        """
        frame_duration_ms = 1000 / fps
        total_time_ms = phoneme_timeline[-1]["end_ms"] if phoneme_timeline else 0
        total_frames = int(total_time_ms / frame_duration_ms) + 1
        
        # Initialize all frames with neutral
        animation_data = {}
        all_blendshapes = set()
        
        for phoneme_data in phoneme_timeline:
            for bs in self.PHONEME_BLENDSHAPE_MAP.get(phoneme_data["phoneme"], {}).keys():
                all_blendshapes.add(bs)
        
        # Neutral defaults
        neutral_state = {bs: 0.0 for bs in all_blendshapes}
        
        for frame in range(total_frames):
            frame_time_ms = frame * frame_duration_ms
            animation_data[frame] = neutral_state.copy()
        
        # Apply phoneme blendshapes across frames
        for phoneme_data in phoneme_timeline:
            phoneme = phoneme_data["phoneme"]
            start_frame = int(phoneme_data["start_ms"] / frame_duration_ms)
            end_frame = int(phoneme_data["end_ms"] / frame_duration_ms)
            
            blendshape_targets = self.PHONEME_BLENDSHAPE_MAP.get(phoneme, {})
            
            # Ease in/out blendshapes
            for frame in range(max(0, start_frame - 2), min(total_frames, end_frame + 2)):
                for bs_name, target_value in blendshape_targets.items():
                    # Smooth interpolation
                    relative_pos = (frame - start_frame) / (end_frame - start_frame) if end_frame > start_frame else 0
                    ease = max(0, 1 - abs(relative_pos * 2 - 1) ** 2)  # Ease in/out
                    
                    animation_data[frame][bs_name] = target_value * ease
        
        return {
            "fps": fps,
            "total_frames": total_frames,
            "total_duration_ms": int(total_time_ms),
            "keyframes": animation_data
        }
    
    def export_to_multiple_formats(self, blendshape_anim: Dict, 
                                  output_dir: str) -> None:
        """Export lip sync to different engine formats"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # JSON (universal)
        json_file = output_path / "lipsync_blendshapes.json"
        json_file.write_text(json.dumps(blendshape_anim, indent=2))
        logger.info(f"✓ JSON export: {json_file}")
        
        # FBX export format (for Unreal/Maya)
        fbx_config = {
            "animation_name": "SpeechAnimation",
            "fps": blendshape_anim["fps"],
            "total_frames": blendshape_anim["total_frames"],
            "blendshape_tracks": {}
        }
        
        # Extract per-blendshape tracks
        for bs_name in set().union(*[set(frame.keys()) for frame in blendshape_anim["keyframes"].values()]):
            fbx_config["blendshape_tracks"][bs_name] = [
                blendshape_anim["keyframes"].get(frame, {}).get(bs_name, 0.0)
                for frame in range(blendshape_anim["total_frames"])
            ]
        
        fbx_file = output_path / "lipsync_fbx_format.json"
        fbx_file.write_text(json.dumps(fbx_config, indent=2))
        logger.info(f"✓ FBX format: {fbx_file}")

def generate_speech_with_lipsync(text: str, output_dir: str = "exports/speech") -> None:
    """Complete pipeline: Text → Audio + Lip Sync Animation"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    audio_file = output_path / "speech.wav"
    phoneme_file = output_path / "phonemes.txt"
    lipsync_file = output_path / "lipsync.json"
    
    generator = PiperLipSyncGenerator()
    
    # Generate speech + phonemes
    if generator.synthesize_with_phonemes(text, str(audio_file), str(phoneme_file)):
        # Parse phoneme timeline
        timeline = generator.parse_phoneme_timeline(str(phoneme_file))
        
        # Generate blendshape keyframes
        anim_data = generator.generate_blendshape_keyframes(timeline, fps=30)
        
        # Export
        generator.export_to_multiple_formats(anim_data, str(output_path))
        
        logger.info("✓✓✓ Speech + Lip Sync complete")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate lip sync from text")
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--output", default="exports/speech")
    
    args = parser.parse_args()
    
    generate_speech_with_lipsync(args.text, args.output)