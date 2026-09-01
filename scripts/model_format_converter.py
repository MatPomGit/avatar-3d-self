#!/usr/bin/env python3
"""Loss-aware model converter for FBX, glTF/GLB, OBJ and STL.

Run normally:
    python scripts/model_format_converter.py input.fbx output.glb

The wrapper locates Blender and re-runs itself in Blender background mode. You can
also invoke it directly through Blender:
    blender --background --python scripts/model_format_converter.py -- input.fbx output.glb

Blender is used intentionally: a mesh-only library cannot reliably preserve rigs,
shape keys, materials and animation across the richer formats supported here.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

SUPPORTED = {".fbx", ".gltf", ".glb", ".obj", ".stl"}

FORMAT_CAPABILITIES: dict[str, dict[str, bool]] = {
    ".fbx": {
        "geometry": True,
        "uv": True,
        "materials": True,
        "textures": True,
        "armature": True,
        "skinning": True,
        "shape_keys": True,
        "animation": True,
    },
    ".gltf": {
        "geometry": True,
        "uv": True,
        "materials": True,
        "textures": True,
        "armature": True,
        "skinning": True,
        "shape_keys": True,
        "animation": True,
    },
    ".glb": {
        "geometry": True,
        "uv": True,
        "materials": True,
        "textures": True,
        "armature": True,
        "skinning": True,
        "shape_keys": True,
        "animation": True,
    },
    ".obj": {
        "geometry": True,
        "uv": True,
        "materials": True,
        "textures": True,
        "armature": False,
        "skinning": False,
        "shape_keys": False,
        "animation": False,
    },
    ".stl": {
        "geometry": True,
        "uv": False,
        "materials": False,
        "textures": False,
        "armature": False,
        "skinning": False,
        "shape_keys": False,
        "animation": False,
    },
}

FEATURE_LABELS = {
    "geometry": "geometria",
    "uv": "mapy UV",
    "materials": "materiały",
    "textures": "tekstury",
    "armature": "szkielet",
    "skinning": "wagi kości",
    "shape_keys": "blendshapes / shape keys",
    "animation": "animacje",
}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Konwersja FBX, glTF/GLB, OBJ i STL z kontrolą utraty danych."
    )
    parser.add_argument("input", type=Path, help="Plik wejściowy")
    parser.add_argument("output", type=Path, help="Plik wyjściowy")
    parser.add_argument(
        "--textures",
        choices=("auto", "embed", "copy", "skip"),
        default="auto",
        help="Sposób obsługi tekstur. GLB naturalnie osadza tekstury w jednym pliku.",
    )
    parser.add_argument(
        "--animations",
        choices=("auto", "keep", "strip"),
        default="auto",
        help="Zachowanie animacji, jeżeli format docelowy je obsługuje.",
    )
    parser.add_argument(
        "--apply-transforms",
        action="store_true",
        help="Zastosuj transformacje obiektów przed eksportem.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Ścieżka raportu JSON. Domyślnie: <output>.conversion.json",
    )
    parser.add_argument(
        "--blender",
        help="Ścieżka do programu Blender, jeżeli nie znajduje się w PATH.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Przerwij konwersję, jeżeli format docelowy nie może zachować części danych.",
    )
    return parser.parse_args(argv)


def extension(path: Path) -> str:
    ext = path.suffix.lower()
    if ext not in SUPPORTED:
        names = ", ".join(sorted(SUPPORTED))
        raise ValueError(f"Nieobsługiwany format {ext or '(brak)'}. Obsługiwane: {names}")
    return ext


def find_blender(explicit: str | None) -> str:
    candidates = [explicit, os.environ.get("BLENDER_BIN"), shutil.which("blender")]
    if sys.platform == "win32":
        candidates.extend(
            [
                r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
            ]
        )
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise RuntimeError(
        "Nie znaleziono Blendera. Zainstaluj Blender i dodaj go do PATH albo użyj --blender."
    )


def rerun_in_blender(args: argparse.Namespace) -> int:
    blender = find_blender(args.blender)
    command = [
        blender,
        "--background",
        "--python",
        str(Path(__file__).resolve()),
        "--",
        str(args.input.resolve()),
        str(args.output.resolve()),
        "--textures",
        args.textures,
        "--animations",
        args.animations,
    ]
    if args.apply_transforms:
        command.append("--apply-transforms")
    if args.report:
        command.extend(["--report", str(args.report.resolve())])
    if args.strict:
        command.append("--strict")
    return subprocess.call(command)


def _operator(path: str):
    import bpy  # type: ignore

    target: Any = bpy.ops
    for part in path.split("."):
        target = getattr(target, part)
    return target


def _call_first(candidates: list[tuple[str, dict[str, Any]]]) -> None:
    last_error: Exception | None = None
    for name, kwargs in candidates:
        try:
            _operator(name)(**kwargs)
            return
        except (AttributeError, RuntimeError, TypeError) as exc:
            last_error = exc
    raise RuntimeError(f"Żaden operator Blendera nie zadziałał: {[x[0] for x in candidates]}") from last_error


def reset_scene() -> None:
    import bpy  # type: ignore

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.armatures, bpy.data.materials):
        # Only remove orphaned blocks. Imported blocks still used by scene objects remain intact.
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def import_model(path: Path) -> None:
    ext = extension(path)
    if ext == ".fbx":
        _call_first([("import_scene.fbx", {"filepath": str(path)})])
    elif ext in {".gltf", ".glb"}:
        _call_first([("import_scene.gltf", {"filepath": str(path)})])
    elif ext == ".obj":
        _call_first(
            [
                ("wm.obj_import", {"filepath": str(path)}),
                ("import_scene.obj", {"filepath": str(path)}),
            ]
        )
    elif ext == ".stl":
        _call_first(
            [
                ("wm.stl_import", {"filepath": str(path)}),
                ("import_mesh.stl", {"filepath": str(path)}),
            ]
        )


def scene_inventory() -> dict[str, Any]:
    import bpy  # type: ignore

    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
    materials = {mat.name for obj in mesh_objects for mat in obj.data.materials if mat}
    images = set()
    for material_name in materials:
        material = bpy.data.materials.get(material_name)
        if not material or not material.use_nodes:
            continue
        for node in material.node_tree.nodes:
            if node.type == "TEX_IMAGE" and getattr(node, "image", None):
                images.add(node.image.name)

    shape_keys = 0
    uv_layers = 0
    skinned_meshes = 0
    for obj in mesh_objects:
        uv_layers += len(getattr(obj.data, "uv_layers", []))
        keys = getattr(obj.data, "shape_keys", None)
        if keys:
            # Basis is not a morph target.
            shape_keys += max(0, len(keys.key_blocks) - 1)
        if any(mod.type == "ARMATURE" for mod in obj.modifiers) or obj.vertex_groups:
            skinned_meshes += 1

    actions = len(bpy.data.actions)
    return {
        "objects": len(bpy.context.scene.objects),
        "meshes": len(mesh_objects),
        "vertices": sum(len(obj.data.vertices) for obj in mesh_objects),
        "polygons": sum(len(obj.data.polygons) for obj in mesh_objects),
        "uv_layers": uv_layers,
        "materials": len(materials),
        "textures": len(images),
        "armatures": len(armatures),
        "skinned_meshes": skinned_meshes,
        "shape_keys": shape_keys,
        "actions": actions,
    }


def present_features(inventory: dict[str, Any]) -> dict[str, bool]:
    return {
        "geometry": inventory["meshes"] > 0,
        "uv": inventory["uv_layers"] > 0,
        "materials": inventory["materials"] > 0,
        "textures": inventory["textures"] > 0,
        "armature": inventory["armatures"] > 0,
        "skinning": inventory["skinned_meshes"] > 0,
        "shape_keys": inventory["shape_keys"] > 0,
        "animation": inventory["actions"] > 0,
    }


def loss_analysis(inventory: dict[str, Any], output_ext: str, animations: str, textures: str) -> list[str]:
    present = present_features(inventory)
    supported = FORMAT_CAPABILITIES[output_ext]
    losses = [FEATURE_LABELS[key] for key, value in present.items() if value and not supported[key]]
    if animations == "strip" and present["animation"] and "animacje" not in losses:
        losses.append("animacje (wyłączone przez --animations strip)")
    if textures == "skip" and present["textures"] and "tekstury" not in losses:
        losses.append("tekstury (wyłączone przez --textures skip)")
    return losses


def apply_transforms() -> None:
    import bpy  # type: ignore

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


def pack_or_copy_textures(mode: str) -> None:
    import bpy  # type: ignore

    if mode == "embed":
        try:
            bpy.ops.file.pack_all()
        except RuntimeError:
            pass


def export_model(path: Path, textures: str, animations: str) -> None:
    ext = extension(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    keep_animation = animations != "strip"

    if ext == ".fbx":
        embed = textures == "embed"
        path_mode = "COPY" if textures in {"copy", "embed", "auto"} else "AUTO"
        _call_first(
            [
                (
                    "export_scene.fbx",
                    {
                        "filepath": str(path),
                        "use_selection": False,
                        "path_mode": path_mode,
                        "embed_textures": embed,
                        "bake_anim": keep_animation,
                        "add_leaf_bones": False,
                    },
                )
            ]
        )
    elif ext == ".glb":
        _call_first(
            [
                (
                    "export_scene.gltf",
                    {
                        "filepath": str(path),
                        "export_format": "GLB",
                        "export_animations": keep_animation,
                        "export_morph": True,
                        "export_skins": True,
                    },
                )
            ]
        )
    elif ext == ".gltf":
        _call_first(
            [
                (
                    "export_scene.gltf",
                    {
                        "filepath": str(path),
                        "export_format": "GLTF_SEPARATE",
                        "export_animations": keep_animation,
                        "export_morph": True,
                        "export_skins": True,
                    },
                )
            ]
        )
    elif ext == ".obj":
        _call_first(
            [
                ("wm.obj_export", {"filepath": str(path), "export_materials": textures != "skip"}),
                ("export_scene.obj", {"filepath": str(path), "use_materials": textures != "skip"}),
            ]
        )
    elif ext == ".stl":
        _call_first(
            [
                ("wm.stl_export", {"filepath": str(path)}),
                ("export_mesh.stl", {"filepath": str(path)}),
            ]
        )


def conversion_report(
    args: argparse.Namespace,
    inventory: dict[str, Any],
    losses: list[str],
) -> dict[str, Any]:
    output_ext = extension(args.output)
    return {
        "input": str(args.input.resolve()),
        "output": str(args.output.resolve()),
        "input_format": extension(args.input),
        "output_format": output_ext,
        "scene": inventory,
        "output_capabilities": FORMAT_CAPABILITIES[output_ext],
        "requested": {
            "textures": args.textures,
            "animations": args.animations,
            "apply_transforms": args.apply_transforms,
        },
        "losses": losses,
        "lossless_for_detected_features": not losses,
    }


def blender_main(args: argparse.Namespace) -> int:
    args.input = args.input.resolve()
    args.output = args.output.resolve()
    if not args.input.exists():
        raise FileNotFoundError(args.input)
    extension(args.input)
    extension(args.output)

    reset_scene()
    import_model(args.input)
    inventory = scene_inventory()
    losses = loss_analysis(inventory, extension(args.output), args.animations, args.textures)

    if losses:
        print("UWAGA: format docelowy nie zachowa: " + ", ".join(losses))
        if args.strict:
            raise RuntimeError("Przerwano przez --strict, ponieważ konwersja powoduje utratę danych.")

    if args.apply_transforms:
        apply_transforms()
    if args.textures == "embed":
        pack_or_copy_textures(args.textures)

    export_model(args.output, args.textures, args.animations)
    report_path = args.report or args.output.with_suffix(args.output.suffix + ".conversion.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(conversion_report(args, inventory, losses), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Gotowe: {args.output}")
    print(f"Raport: {report_path}")
    return 0


def argv_after_blender_separator() -> list[str]:
    if "--" not in sys.argv:
        return []
    return sys.argv[sys.argv.index("--") + 1 :]


def main() -> int:
    blender_args = argv_after_blender_separator()
    args = parse_args(blender_args or sys.argv[1:])
    extension(args.input)
    extension(args.output)
    try:
        import bpy  # type: ignore  # noqa: F401
    except ImportError:
        return rerun_in_blender(args)
    return blender_main(args)


if __name__ == "__main__":
    raise SystemExit(main())
