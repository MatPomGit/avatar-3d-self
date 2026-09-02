from pathlib import Path

from avatar_studio.adapters.base import CommandResult
from avatar_studio.adapters.colmap import ColmapAdapter
from avatar_studio.store import ProjectStore


def test_stage_requires_artifact_before_pass(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    allowed, reasons = store.can_pass_stage("01-reference-acquisition")
    assert allowed is False
    assert any("artefact" in reason.lower() for reason in reasons)

    artifact = tmp_path / "capture_manifest.json"
    artifact.write_text('{"schema_version": 1}', encoding="utf-8")
    store.register_artifact("01-reference-acquisition", artifact)
    allowed, reasons = store.can_pass_stage("01-reference-acquisition")
    assert allowed is True
    assert reasons == ()


def test_failed_validation_requires_waiver(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    artifact = tmp_path / "capture_manifest.json"
    artifact.write_text("{}", encoding="utf-8")
    store.register_artifact("01-reference-acquisition", artifact)
    store.add_validation_result(
        "01-reference-acquisition",
        "coverage",
        "failed",
        message="Reference coverage is incomplete.",
    )
    allowed, _ = store.can_pass_stage("01-reference-acquisition")
    assert allowed is False
    store.add_waiver("01-reference-acquisition", "Known gap; a supplementary capture is scheduled.")
    allowed, reasons = store.can_pass_stage("01-reference-acquisition")
    assert allowed is True
    assert reasons == ()


def test_changed_approved_artifact_invalidates_downstream(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    first = tmp_path / "manifest-a.json"
    first.write_text('{"version": 1}', encoding="utf-8")
    store.register_artifact("01-reference-acquisition", first)
    store.set_stage_status("01-reference-acquisition", "passed")

    sparse_report = tmp_path / "sparse.json"
    sparse_report.write_text('{"models": ["0"]}', encoding="utf-8")
    store.register_artifact("02-photogrammetry", sparse_report)
    store.set_stage_status("02-photogrammetry", "passed")
    assert store.stage_statuses()["03-reconstruction"] == "ready"

    second = tmp_path / "manifest-b.json"
    second.write_text('{"version": 2}', encoding="utf-8")
    store.register_artifact("01-reference-acquisition", second)
    statuses = store.stage_statuses()
    assert statuses["02-photogrammetry"] == "ready"
    assert statuses["03-reconstruction"] == "pending"


def test_dense_colmap_builds_expected_command_chain(tmp_path: Path, monkeypatch) -> None:
    images = tmp_path / "images"
    images.mkdir()
    sparse = tmp_path / "sparse" / "0"
    sparse.mkdir(parents=True)
    workspace = tmp_path / "work"
    executable = tmp_path / "colmap"
    executable.write_text("fake", encoding="utf-8")
    adapter = ColmapAdapter(executable=executable)
    commands: list[tuple[str, ...]] = []

    def fake_run(args, **kwargs):
        command = tuple(str(value) for value in args)
        commands.append(command)
        if command[0] == "stereo_fusion":
            destination = Path(command[command.index("--output_path") + 1])
            destination.write_bytes(b"ply")
        if command[0] == "poisson_mesher":
            destination = Path(command[command.index("--output_path") + 1])
            destination.write_bytes(b"mesh")
        return CommandResult((str(executable), *command), 0, "", "")

    monkeypatch.setattr(adapter, "run", fake_run)
    report = adapter.reconstruct_dense(images, sparse, workspace, mesher="poisson")
    assert [command[0] for command in commands] == [
        "image_undistorter",
        "patch_match_stereo",
        "stereo_fusion",
        "poisson_mesher",
    ]
    assert Path(report["mesh"]).is_file()


def test_tool_path_is_project_local_metadata(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    store.set_tool_path("blender", "/opt/blender/blender")
    assert store.tool_path("blender") == "/opt/blender/blender"
