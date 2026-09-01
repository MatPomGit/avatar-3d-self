from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "model_format_converter.py"
spec = spec_from_file_location("model_format_converter", MODULE_PATH)
assert spec and spec.loader
converter = module_from_spec(spec)
spec.loader.exec_module(converter)


def inventory(**overrides):
    base = {
        "objects": 1,
        "meshes": 1,
        "vertices": 100,
        "polygons": 50,
        "uv_layers": 1,
        "materials": 1,
        "textures": 1,
        "armatures": 1,
        "skinned_meshes": 1,
        "shape_keys": 10,
        "actions": 2,
    }
    base.update(overrides)
    return base


def test_glb_can_represent_detected_character_data():
    assert converter.loss_analysis(inventory(), ".glb", "keep", "auto") == []


def test_obj_reports_rig_morph_and_animation_loss():
    losses = converter.loss_analysis(inventory(), ".obj", "keep", "auto")
    assert "szkielet" in losses
    assert "wagi kości" in losses
    assert "blendshapes / shape keys" in losses
    assert "animacje" in losses
    assert "mapy UV" not in losses
    assert "tekstury" not in losses


def test_stl_reports_non_geometry_data_loss():
    losses = converter.loss_analysis(inventory(), ".stl", "keep", "auto")
    assert "mapy UV" in losses
    assert "materiały" in losses
    assert "tekstury" in losses
    assert "szkielet" in losses
    assert "animacje" in losses


def test_strip_animation_is_reported_even_for_glb():
    losses = converter.loss_analysis(inventory(), ".glb", "strip", "auto")
    assert losses == ["animacje (wyłączone przez --animations strip)"]


def test_skip_textures_is_reported():
    losses = converter.loss_analysis(inventory(), ".glb", "keep", "skip")
    assert losses == ["tekstury (wyłączone przez --textures skip)"]


def test_rejects_unknown_extension():
    try:
        converter.extension(Path("model.3ds"))
    except ValueError as exc:
        assert "Nieobsługiwany format" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
