"""Piper TTS workstation adapter."""

from avatar_studio.adapters.base import ToolAdapter


class PiperAdapter(ToolAdapter):
    name = "Piper"
    executable_names = ("piper", "piper.exe")
    version_args = ("--help",)
