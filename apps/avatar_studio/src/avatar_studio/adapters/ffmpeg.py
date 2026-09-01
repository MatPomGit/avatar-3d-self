"""FFmpeg workstation adapter."""

from avatar_studio.adapters.base import ToolAdapter


class FFmpegAdapter(ToolAdapter):
    name = "FFmpeg"
    executable_names = ("ffmpeg", "ffmpeg.exe")
    version_args = ("-version",)
