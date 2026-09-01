"""FFmpeg workstation adapter."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re

from avatar_studio.adapters.base import CommandResult, ToolAdapter


class FFmpegAdapter(ToolAdapter):
    name = "FFmpeg"
    executable_names = ("ffmpeg", "ffmpeg.exe")
    version_args = ("-version",)

    def analyze_audio(self, audio_file: str | Path) -> dict:
        """Inspect an audio stream without modifying the source file."""

        path = Path(audio_file).resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        result = self.run(("-hide_banner", "-i", str(path), "-t", "0.01", "-f", "null", "-"))
        # ffmpeg may return zero or non-zero for probe-like invocations depending on build/input;
        # metadata is emitted to stderr, so require an Audio stream rather than returncode alone.
        text = result.stderr + "\n" + result.stdout
        report = self.parse_audio_metadata(text)
        if report["sample_rate_hz"] is None:
            raise RuntimeError(f"FFmpeg did not identify an audio stream: {text.strip()}")
        report.update(
            {
                "tool": "FFmpeg",
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "sha256": self._sha256(path),
                "command": list(result.command),
                "returncode": result.returncode,
            }
        )
        return report

    def normalize_wav(
        self,
        input_file: str | Path,
        output_file: str | Path,
        *,
        sample_rate_hz: int = 22050,
        channels: int = 1,
        integrated_lufs: float = -16.0,
        true_peak_db: float = -1.5,
        loudness_range_lu: float = 11.0,
        overwrite: bool = False,
        timeout_s: float = 600.0,
    ) -> dict:
        """Create normalized PCM 16-bit WAV suitable for speech pipeline processing."""

        source = Path(input_file).resolve()
        destination = Path(output_file).resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        if sample_rate_hz < 8000:
            raise ValueError("sample_rate_hz must be at least 8000")
        if channels not in {1, 2}:
            raise ValueError("channels must be 1 or 2")
        if destination.exists() and not overwrite:
            raise FileExistsError(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        loudnorm = (
            f"loudnorm=I={integrated_lufs}:TP={true_peak_db}:LRA={loudness_range_lu}:"
            "print_format=summary"
        )
        args = [
            "-hide_banner",
            "-nostdin",
            "-y" if overwrite else "-n",
            "-i",
            str(source),
            "-vn",
            "-af",
            loudnorm,
            "-ar",
            str(sample_rate_hz),
            "-ac",
            str(channels),
            "-c:a",
            "pcm_s16le",
            str(destination),
        ]
        result = self.run(args, timeout_s=timeout_s)
        self._require_success(result, "FFmpeg audio normalization")
        if not destination.is_file():
            raise RuntimeError("FFmpeg completed without creating the expected WAV file")
        return {
            "tool": "FFmpeg",
            "input": str(source),
            "output": str(destination),
            "sample_rate_hz": sample_rate_hz,
            "channels": channels,
            "codec": "pcm_s16le",
            "integrated_lufs_target": integrated_lufs,
            "true_peak_db_target": true_peak_db,
            "loudness_range_lu_target": loudness_range_lu,
            "input_sha256": self._sha256(source),
            "output_sha256": self._sha256(destination),
            "command": list(result.command),
        }

    @staticmethod
    def parse_audio_metadata(text: str) -> dict:
        duration = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", text)
        audio_line = re.search(r"(?im)^\s*Stream .*Audio:\s*(.+)$", text)
        sample_rate = re.search(r"(\d+)\s*Hz", audio_line.group(1)) if audio_line else None
        bit_rate = re.search(r"(\d+)\s*kb/s", audio_line.group(1)) if audio_line else None
        channels = None
        if audio_line:
            descriptor = audio_line.group(1).lower()
            if "mono" in descriptor:
                channels = 1
            elif "stereo" in descriptor:
                channels = 2
            else:
                match = re.search(r"(\d+)\s*channels?", descriptor)
                if match:
                    channels = int(match.group(1))
        duration_s = None
        if duration:
            duration_s = int(duration.group(1)) * 3600 + int(duration.group(2)) * 60 + float(duration.group(3))
        codec = audio_line.group(1).split(",", 1)[0].strip() if audio_line else None
        return {
            "duration_s": duration_s,
            "codec": codec,
            "sample_rate_hz": int(sample_rate.group(1)) if sample_rate else None,
            "channels": channels,
            "bit_rate_kbps": int(bit_rate.group(1)) if bit_rate else None,
        }

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()

    @staticmethod
    def _require_success(result: CommandResult, operation: str) -> None:
        if not result.ok:
            raise RuntimeError(
                f"{operation} failed with exit code {result.returncode}: {result.stderr.strip()}"
            )
