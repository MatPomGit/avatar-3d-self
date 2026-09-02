"""Local external-tool discovery for Avatar Studio."""

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from avatar_studio.adapters import BlenderAdapter, ColmapAdapter, FFmpegAdapter, PiperAdapter


@dataclass(frozen=True, slots=True)
class ToolProbe:
    """Result of resolving one external executable."""

    name: str
    executable: str | None

    @property
    def available(self) -> bool:
        return self.executable is not None


def probe_default_tools(configured: Mapping[str, str | None] | None = None) -> tuple[ToolProbe, ...]:
    """Locate common tools, honoring optional project-specific executable paths."""

    configured = configured or {}
    adapters = (
        BlenderAdapter(configured.get("blender") or None),
        ColmapAdapter(configured.get("colmap") or None),
        FFmpegAdapter(configured.get("ffmpeg") or None),
        PiperAdapter(configured.get("piper") or None),
    )
    return tuple(
        ToolProbe(adapter.name, str(path) if (path := adapter.resolve()) else None)
        for adapter in adapters
    )


def display_path(path: str | None) -> str:
    return str(Path(path)) if path else "not found in PATH"
