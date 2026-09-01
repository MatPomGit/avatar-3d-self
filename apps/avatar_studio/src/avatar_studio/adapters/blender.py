"""Blender workstation adapter."""

from avatar_studio.adapters.base import ToolAdapter


class BlenderAdapter(ToolAdapter):
    name = "Blender"
    executable_names = ("blender", "blender.exe")
    version_args = ("--version",)
