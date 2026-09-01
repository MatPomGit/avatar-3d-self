#!/usr/bin/env python3
"""Loss-aware converter for common 3D interchange formats used by Avatar Studio.

Supported formats: FBX, glTF, GLB, USD, USDZ, OBJ, PLY and STL.
The converter uses Blender in background mode because complete character assets can
contain geometry, UVs, materials, textures, armatures, skin weights, shape keys and
animation. Mesh-only conversion libraries cannot preserve all of those reliably.
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

SUPPORTED = {".fbx", ".gltf", ".glb", ".usd", ".usdz", ".obj", ".ply", ".stl"}

_RICH = {
    "geometry": True,
    "uv": True,
    "materials": True,
    "textures": True,
    "armature": True,
    "skinning": True,
    "shape_keys": True,
    "animation": True,
}

FORMAT_CAPABILITIES: dict[str, dict[str, bool]] = {
    ".fbx": dict(_RICH),
    ".gltf": dict(_RICH),
    ".glb": dict(_RICH),
    ".usd": dict(_RICH),
    ".usdz": dict(_RICH),
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
    ".ply": {
        "geometry": True,
        "uv": True,
        "materials": False,
        "textures": False,
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
        description="Konwersja FBX, glTF/GLB, USD/USDZ, OBJ, PLY i STL z kontrolą utraty danych."
    )
    parser.add_argument("input", type=Path, help="Plik wejściowy")
    parser.add_argument("output", type=Path, help="Plik wyjściowy")
    parser.add_argument(
        "--textures",
        choices=("auto", "embed", "copy", "skip"),
        default="auto",
        help="Sposób obsługi tekstur.",
    )
    parser.add_argument(
        "--texture-format",
        choices=("auto", "png", "jpeg"),
        default="auto",
        help="Opcjonalne przepisanie obrazów tekstur do PNG albo JPEG.",
    )
    parser.add_argument(
        "--max-texture-size",
        type=int,
        help="Zmniejsz większy bok każdej tekstury do podanej liczby pikseli.",
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
        help="Zastosuj obrót i skalę obiektów przed eksportem.",
    )
    parser.add_argument("--report", type=Path, help="Raport JSON. Domyślnie: <output>.conversion.json")
    parser.add_argument("--blender", help="Ścieżka do programu Blender, jeżeli nie znajduje się w PATH.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Przerwij konwersję, jeżeli wykryte dane zostaną utracone.",
    )
    return parser.parse_args(argv)


def extension(path: Path) -> str:
    ext = path.suffix.lower()
    if ext not in SUPPORTED:
        raise ValueError(
            f"Nieobsługiwany format {ext or '(brak)'}. Obsługiwane: {', '.join(sorted(SUPPORTED))}"
        )
    return ext


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


def loss_analysis(
    inventory: dict[str, Any], output_ext: str, animations: str, textures: str
) -> list[str]:
    present = present_features(inventory)
    supported = FORMAT_CAPABILITIES[output_ext]
    losses = [FEATURE_LABELS[key] for key, value in present.items() if value and not supported[key]]
    if animations == "strip" and present["animation"] and "animacje" not in losses:
        losses.append("animacje (wyłączone przez --animations strip)")
    if textures == "skip" and present["textures"] and "tekstury" not in losses:
        losses.append("tekstury (wyłączone przez --textures skip)")
    return losses


def find_blender(explicit: str | None) -> str:
    candidates: list[str | None] = []
    if explicit:
        candidates.extend([explicit, shutil.which(explicit)])
    env_blender = os.environ.get("BLENDER_BIN")
    if env_blender:
        candidates.extend([env_blender, shutil.which(env_blender)])
    candidates.append(shutil.which("blender"))
    if sys.platform == "win32":
        candidates.extend(
            [
                r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe",
                r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
            ]
        )
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate).resolve())
    raise RuntimeError(
        "Nie znaleziono Blendera. Dodaj blender do PATH, ustaw BLENDER_BIN albo użyj --blender."
    )


def rerun_in_blender(args: argparse.Namespace) -> int:
    command = [
        find_blender(args.blender),
        "--background",
        "--python",
        str(Path(__file__).resolve()),
        "--",
        str(args.input.resolve()),
        str(args.output.resolve()),
        "--textures",
        args.textures,
        "--texture-format",
        args.texture_format,
        "--animations",
        args.animations,
    ]
    if args.max_texture_size:
        command.extend(["--max-texture-size", str(args.max_texture_size)])
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
    raise RuntimeError(
        f"Brak działającego operatora Blendera: {[name for name, _ in candidates]}"
    ) from last_error


def reset_scene() -> None:
    import bpy  # type: ignore

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def import_model(path: Path) -> None:
    ext = extension(path)
    if ext == ".fbx":
        _call_first([("import_scene.fbx", {"filepath": str(path)})])
    elif ext in {".gltf", ".glb"}:
        _call_first([("import_scene.gltf", {"filepath": str(path)})])
    elif ext in {".usd", ".usdz"}:
        _call_first([("wm.usd_import", {"filepath": str(path)})])
    elif ext == ".obj":
        _call_first(
            [
                ("wm.obj_import", {"filepath": str(path)}),
                ("import_scene.obj", {"filepath": str(path)}),
            ]
        )
    elif ext == ".ply":
        _call_first(
            [
                ("wm.ply_import", {"filepath": str(path)}),
                ("import_mesh.ply", {"filepath": str(path)}),
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

    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
    materials = {mat.name for obj in meshes for mat in obj.data.materials if mat}
    images: set[str] = set()
    color_attributes = 0
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
    for obj in meshes:
        uv_layers += len(getattr(obj.data, "uv_layers", []))
        color_attributes += len(getattr(obj.data, "color_attributes", []))
        keys = getattr(obj.data, "shape_keys", None)
        if keys:
            shape_keys += max(0, len(keys.key_blocks) - 1)
        if any(mod.type == "ARMATURE" for mod in obj.modifiers) or obj.vertex_groups:
            skinned_meshes += 1

    return {
        "objects": len(bpy.context.scene.objects),
        "meshes": len(meshes),
        "vertices": sum(len(obj.data.vertices) for obj in meshes),
        "polygons": sum(len(obj.data.polygons) for obj in meshes),
        "uv_layers": uv_layers,
        "color_attributes": color_attributes,
        "materials": len(materials),
        "textures": len(images),
        "armatures": len(armatures),
        "skinned_meshes": skinned_meshes,
        "shape_keys": shape_keys,
        "actions": len(bpy.data.actions),
    }


def apply_transforms() -> None:
    import bpy  # type: ignore

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


def strip_animations() -> None:
    import bpy  # type: ignore

    for obj in bpy.context.scene.objects:
        if obj.animation_data:
            obj.animation_data_clear()
    for datablock in list(bpy.data.actions):
        bpy.data.actions.remove(datablock)


def strip_textures() -> None:
    import bpy  # type: ignore

    for material in bpy.data.materials:
        if material.use_nodes:
            for node in list(material.node_tree.nodes):
                if node.type == "TEX_IMAGE":
                    material.node_tree.nodes.remove(node)


def process_textures(mode: str, image_format: str, max_size: int | None) -> list[dict[str, Any]]:
    import bpy  # type: ignore

    processed: list[dict[str, Any]] = []
    if mode == "skip":
        strip_textures()
        return processed

    for image in bpy.data.images:
        if image.type != "IMAGE" or image.size[0] <= 0 or image.size[1] <= 0:
            continue
        before = [int(image.size[0]), int(image.size[1])]
        if max_size and max(before) > max_size:
            scale = max_size / max(before)
            image.scale(max(1, round(before[0] * scale)), max(1, round(before[1] * scale)))
        after = [int(image.size[0]), int(image.size[1])]

        if image_format != "auto" and image.packed_file is None and image.filepath:
            original = Path(bpy.path.abspath(image.filepath))
            if original.exists():
                suffix = ".png" if image_format == "png" else ".jpg"
                destination_dir = Path(bpy.path.abspath("//")) / "converted_textures"
                destination_dir.mkdir(parents=True, exist_ok=True)
                destination = destination_dir / f"{original.stem}{suffix}"
                image.filepath_raw = str(destination)
                image.file_format = "PNG" if image_format == "png" else "JPEG"
                image.save()
                image.filepath = str(destination)

        processed.append(
            {
                "name": image.name,
                "before": before,
                "after": after,
                "filepath": image.filepath,
            }
        )

    if mode == "embed":
        try:
            bpy.ops.file.pack_all()
        except RuntimeError:
            pass
    return processed


def _material_mtl_text() -> str:
    import bpy  # type: ignore

    lines = ["# Generated by Avatar Studio model_format_converter.py", ""]
    if not bpy.data.materials:
        lines.extend(["newmtl default", "Kd 0.8 0.8 0.8", "d 1.0", ""])
        return "\n".join(lines)

    for material in bpy.data.materials:
        color = material.diffuse_color
        lines.extend(
            [
                f"newmtl {material.name}",
                f"Kd {color[0]:.6f} {color[1]:.6f} {color[2]:.6f}",
                f"d {color[3]:.6f}",
                "illum 2",
            ]
        )
        if material.use_nodes:
            for node in material.node_tree.nodes:
                image = getattr(node, "image", None)
                if node.type == "TEX_IMAGE" and image and image.filepath:
                    lines.append(f"map_Kd {Path(image.filepath).name}")
                    break
        lines.append("")
    return "\n".join(lines)


def ensure_obj_mtl(obj_path: Path) -> Path:
    """Guarantee an OBJ companion MTL and a matching `mtllib` reference."""

    mtl_path = obj_path.with_suffix(".mtl")
    if not mtl_path.exists():
        mtl_path.write_text(_material_mtl_text(), encoding="utf-8")
    try:
        obj_text = obj_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        obj_text = obj_path.read_text(encoding="latin-1")
    expected = f"mtllib {mtl_path.name}"
    if expected not in obj_text:
        obj_path.write_text(expected + "\n" + obj_text, encoding="utf-8")
    return mtl_path


def export_model(path: Path, textures: str, animations: str) -> list[Path]:
    ext = extension(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    keep_animation = animations != "strip"
    companions: list[Path] = []

    if ext == ".fbx":
        _call_first(
            [(
                "export_scene.fbx",
                {
                    "filepath": str(path),
                    "use_selection": False,
                    "path_mode": "COPY" if textures in {"auto", "copy", "embed"} else "AUTO",
                    "embed_textures": textures == "embed",
                    "bake_anim": keep_animation,
                    "add_leaf_bones": False,
                },
            )]
        )
    elif ext in {".glb", ".gltf"}:
        _call_first(
            [(
                "export_scene.gltf",
                {
                    "filepath": str(path),
                    "export_format": "GLB" if ext == ".glb" else "GLTF_SEPARATE",
                    "export_animations": keep_animation,
                    "export_morph": True,
                    "export_skins": True,
                },
            )]
        )
    elif ext in {".usd", ".usdz"}:
        _call_first(
            [
                (
                    "wm.usd_export",
                    {
                        "filepath": str(path),
                        "export_animation": keep_animation,
                        "export_materials": textures != "skip",
                        "export_uvmaps": True,
                        "export_armatures": True,
                        "export_shapekeys": True,
                    },
                ),
                ("wm.usd_export", {"filepath": str(path)}),
            ]
        )
    elif ext == ".obj":
        _call_first(
            [
                ("wm.obj_export", {"filepath": str(path), "export_materials": True}),
                ("export_scene.obj", {"filepath": str(path), "use_materials": True}),
            ]
        )
        companions.append(ensure_obj_mtl(path))
    elif ext == ".ply":
        _call_first(
            [
                (
                    "wm.ply_export",
                    {
                        "filepath": str(path),
                        "export_uv": True,
                        "export_normals": True,
                        "export_colors": "SRGB",
                    },
                ),
                ("wm.ply_export", {"filepath": str(path)}),
                ("export_mesh.ply", {"filepath": str(path), "use_ascii": False}),
            ]
        )
    elif ext == ".stl":
        _call_first(
            [
                ("wm.stl_export", {"filepath": str(path)}),
                ("export_mesh.stl", {"filepath": str(path)}),
            ]
        )
    return companions


def conversion_report(
    args: argparse.Namespace,
    inventory: dict[str, Any],
    losses: list[str],
    processed_textures: list[dict[str, Any]],
    companion_files: list[Path],
) -> dict[str, Any]:
    output_ext = extension(args.output)
    return {
        "producer": "Avatar Studio",
        "input": str(args.input.resolve()),
        "output": str(args.output.resolve()),
        "input_format": extension(args.input),
        "output_format": output_ext,
        "scene": inventory,
        "output_capabilities": FORMAT_CAPABILITIES[output_ext],
        "requested": {
            "textures": args.textures,
            "texture_format": args.texture_format,
            "max_texture_size": args.max_texture_size,
            "animations": args.animations,
            "apply_transforms": args.apply_transforms,
        },
        "processed_textures": processed_textures,
        "companion_files": [str(path.resolve()) for path in companion_files],
        "losses": losses,
        "lossless_for_detected_features": not losses,
    }


def blender_main(args: argparse.Namespace) -> int:
    args.input = args.input.resolve()
    args.output = args.output.resolve()
    if not args.input.exists():
        raise FileNotFoundError(args.input)
    extension(args.input)
    output_ext = extension(args.output)
    if args.max_texture_size is not None and args.max_texture_size < 64:
        raise ValueError("--max-texture-size musi mieć co najmniej 64 piksele.")

    reset_scene()
    import_model(args.input)
    inventory = scene_inventory()
    losses = loss_analysis(inventory, output_ext, args.animations, args.textures)
    if losses:
        print("UWAGA: format docelowy nie zachowa: " + ", ".join(losses))
        if args.strict:
            raise RuntimeError(
                "Przerwano przez --strict, ponieważ konwersja powoduje utratę danych."
            )

    if args.apply_transforms:
        apply_transforms()
    if args.animations == "strip":
        strip_animations()
    processed_textures = process_textures(
        args.textures, args.texture_format, args.max_texture_size
    )
    companion_files = export_model(args.output, args.textures, args.animations)

    report_path = args.report or args.output.with_suffix(args.output.suffix + ".conversion.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(
            conversion_report(args, inventory, losses, processed_textures, companion_files),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Gotowe: {args.output}")
    for companion in companion_files:
        print(f"Plik towarzyszący: {companion}")
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
