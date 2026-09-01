from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import yaml

from avatar_studio.adapters import BlenderAdapter, ColmapAdapter, FFmpegAdapter, PiperAdapter
from avatar_studio.baselines import get_baseline, load_baselines


ROOT = Path(__file__).parents[1]


def test_machine_readable_baselines_have_expected_contract():
    path = ROOT / "config" / "technical_baselines.yaml"
    data = load_baselines(path)
    assert data["schema_version"] == 1
    assert get_baseline("behaviour.blink.duration_s", path=path)["baseline"] == 0.170
    assert get_baseline("runtime.target_fps", path=path) == 60
    assert get_baseline("speech.lip_seal.zero_at_jaw_open", path=path) == 0.22


def test_terminology_configuration_contains_canonical_coarticulation_rule():
    data = yaml.safe_load((ROOT / "config" / "terminology.yaml").read_text(encoding="utf-8"))
    rule = next(item for item in data["rules"] if item["english"] == "coarticulation")
    assert rule["preferred"] == "koartykulacja"
    assert rule["forbidden"]


def test_terminology_linter_passes_current_repository():
    module_path = ROOT / "scripts" / "lint_docs_terminology.py"
    spec = spec_from_file_location("lint_docs_terminology", module_path)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.lint() == []


def test_tool_adapters_accept_explicit_executable(tmp_path):
    executable = tmp_path / "tool"
    executable.write_text("placeholder", encoding="utf-8")
    for adapter_type in (BlenderAdapter, ColmapAdapter, FFmpegAdapter, PiperAdapter):
        adapter = adapter_type(executable=executable)
        assert adapter.available
        assert adapter.resolve() == executable
