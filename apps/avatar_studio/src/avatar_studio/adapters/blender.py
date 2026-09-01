"""Blender workstation adapter."""

from __future__ import annotations

import json
from pathlib import Path

from avatar_studio.adapters.base import CommandResult, ToolAdapter


_REPORT_MARKER = "AVATAR_STUDIO_SCENE_REPORT="


class BlenderAdapter(ToolAdapter):
    name = "Blender"
    executable_names = ("blender", "blender.exe")
    version_args = ("--version",)

    def inspect_scene(self, blend_file: str | Path, *, timeout_s: float = 120.0) -> dict:
        """Inspect a .blend file in background mode and return a JSON-safe scene inventory."""

        blend_path = Path(blend_file).resolve()
        if blend_path.suffix.lower() != ".blend":
            raise ValueError("Blender scene inspection requires a .blend file")
        if not blend_path.exists():
            raise FileNotFoundError(blend_path)

        script = (
            "import bpy,json;"
            "meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];"
            "arms=[o for o in bpy.context.scene.objects if o.type=='ARMATURE'];"
            "r={"
            "'file':bpy.data.filepath,"
            "'objects':len(bpy.context.scene.objects),"
            "'meshes':len(meshes),"
            "'vertices':sum(len(o.data.vertices) for o in meshes),"
            "'polygons':sum(len(o.data.polygons) for o in meshes),"
            "'uv_layers':sum(len(o.data.uv_layers) for o in meshes),"
            "'materials':len(bpy.data.materials),"
            "'images':len(bpy.data.images),"
            "'armatures':len(arms),"
            "'bones':sum(len(o.data.bones) for o in arms),"
            "'shape_keys':sum(max(0,len(o.data.shape_keys.key_blocks)-1) if o.data.shape_keys else 0 for o in meshes),"
            "'actions':len(bpy.data.actions),"
            "'unit_system':bpy.context.scene.unit_settings.system,"
            "'scale_length':bpy.context.scene.unit_settings.scale_length,"
            "'fps':bpy.context.scene.render.fps/bpy.context.scene.render.fps_base"
            "};"
            f"print('{_REPORT_MARKER}'+json.dumps(r,sort_keys=True))"
        )
        result = self.run(
            ("--background", str(blend_path), "--python-expr", script),
            timeout_s=timeout_s,
        )
        self._require_success(result, "Blender scene inspection")
        report = self._parse_report(result)
        report["tool"] = "Blender"
        report["command"] = list(result.command)
        return report

    @staticmethod
    def _require_success(result: CommandResult, operation: str) -> None:
        if not result.ok:
            raise RuntimeError(
                f"{operation} failed with exit code {result.returncode}: {result.stderr.strip()}"
            )

    @staticmethod
    def _parse_report(result: CommandResult) -> dict:
        for line in reversed(result.stdout.splitlines()):
            if line.startswith(_REPORT_MARKER):
                return json.loads(line[len(_REPORT_MARKER) :])
        raise RuntimeError("Blender did not emit an Avatar Studio scene report")
