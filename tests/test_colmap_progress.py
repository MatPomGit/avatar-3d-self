from pathlib import Path

from avatar_studio.adapters.base import CommandResult
from avatar_studio.adapters.colmap import ColmapAdapter


def test_sparse_reconstruction_reports_monotonic_phase_progress(tmp_path: Path, monkeypatch) -> None:
    images = tmp_path / "images"
    images.mkdir()
    workspace = tmp_path / "work"
    executable = tmp_path / "colmap"
    executable.write_text("stub", encoding="utf-8")
    adapter = ColmapAdapter(executable=executable)

    def fake_run(args, **_kwargs):
        if args[0] == "mapper":
            (workspace / "sparse" / "0").mkdir(parents=True, exist_ok=True)
        command = (str(executable), *(str(value) for value in args))
        return CommandResult(command, 0, "", "")

    monkeypatch.setattr(adapter, "run", fake_run)
    progress: list[tuple[int, str]] = []
    report = adapter.reconstruct_sparse(
        images,
        workspace,
        progress_callback=lambda value, message: progress.append((value, message)),
    )

    values = [value for value, _message in progress]
    assert values == sorted(values)
    assert values[0] == 5
    assert values[-1] == 100
    assert report["models"] == [str((workspace / "sparse" / "0").resolve())]
