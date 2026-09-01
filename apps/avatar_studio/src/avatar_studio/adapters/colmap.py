"""COLMAP workstation adapter."""

from avatar_studio.adapters.base import ToolAdapter


class ColmapAdapter(ToolAdapter):
    name = "COLMAP"
    executable_names = ("colmap", "colmap.exe")
    version_args = ("-h",)
