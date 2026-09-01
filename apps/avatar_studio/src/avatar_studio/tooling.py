"""Local external-tool discovery for Avatar Studio."""

from dataclasses import dataclass
from pathlib import Path

from avatar_studio.adapters import BlenderAdapter, ColmapAdapter, FFmpegAdapter, PiperAdapter


@dataclass(frozen=True, slots=True)
class ToolProbe:
    """Result of resolving one external executable."""

    name: str
    executable: str | None

    @property
    def available(self) -> bool:
        return self.executable is not None


def probe_default_tools() -> tuple[ToolProbe, ...]:
    """Locate common tools without executing or modifying them."""

    adapters = (BlenderAdapter(), ColmapAdapter(), FFmpegAdapter(), PiperAdapter())
    return tuple(
        ToolProbe(adapter.name, str(path) if (path := adapter.resolve()) else None)
        for adapter in adapters
    )


def display_path(path: str | None) -> str:
    """Return a stable display value for a discovered executable."""

    return str(Path(path)) if path else "not found in PATH"
