"""High-level, recorded workstation operations used by the desktop UI."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from avatar_studio.adapters import BlenderAdapter, ColmapAdapter, FFmpegAdapter, PiperAdapter
from avatar_studio.adapters.base import ToolAdapter
from avatar_studio.store import ProjectStore


ProgressCallback = Callable[[int, str], None]


class OperationService:
    """Execute supported tool operations with provenance reports and database records."""

    def __init__(self, store: ProjectStore) -> None:
        self.store = store
        self.active_adapter: ToolAdapter | None = None

    def cancel(self) -> None:
        if self.active_adapter is not None:
            self.active_adapter.cancel()

    def _adapter(self, cls: type[ToolAdapter], tool_name: str) -> ToolAdapter:
        configured = self.store.tool_path(tool_name)
        return cls(executable=configured or None)

    def _run_recorded(
        self,
        stage_id: str,
        adapter: ToolAdapter,
        operation_name: str,
        arguments: dict[str, Any],
        callback: Callable[[], dict[str, Any]],
        progress_callback: ProgressCallback | None = None,
    ) -> tuple[dict[str, Any], Path]:
        executable = adapter.resolve()
        if executable is None:
            raise FileNotFoundError(
                f"{adapter.name} executable was not found. Configure it in Tools > Settings."
            )
        run_id = self.store.start_tool_run(stage_id, str(executable), [operation_name, repr(arguments)])
        self.active_adapter = adapter
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        report_path = self.store.reports_dir / f"{stage_id}_{operation_name}_{timestamp}.json"
        if progress_callback:
            progress_callback(1, f"Starting {operation_name}")
        try:
            report = callback()
            report.update(
                {
                    "avatar_studio_operation": operation_name,
                    "stage_id": stage_id,
                    "parameters": arguments,
                    "tool_run_id": run_id,
                }
            )
            adapter.write_report(report, report_path)
            self.store.finish_tool_run(run_id, 0, report_path)
            if progress_callback:
                progress_callback(100, f"{operation_name} complete")
            return report, report_path
        except Exception:
            self.store.finish_tool_run(run_id, 1, report_path if report_path.exists() else None)
            raise
        finally:
            self.active_adapter = None

    def colmap_sparse(
        self,
        image_path: str | Path,
        *,
        camera_model: str = "OPENCV",
        matcher: str = "exhaustive",
        single_camera: bool = True,
        progress_callback: ProgressCallback | None = None,
    ) -> tuple[dict[str, Any], Path]:
        adapter = self._adapter(ColmapAdapter, "colmap")
        workspace = self.store.workspace / "work" / "colmap"
        args = {
            "image_path": str(Path(image_path).resolve()),
            "workspace": str(workspace),
            "camera_model": camera_model,
            "matcher": matcher,
            "single_camera": single_camera,
        }
        return self._run_recorded(
            "02-photogrammetry",
            adapter,
            "colmap_sparse",
            args,
            lambda: adapter.reconstruct_sparse(**args, progress_callback=progress_callback),  # type: ignore[attr-defined]
            progress_callback,
        )

    def colmap_dense(
        self,
        image_path: str | Path,
        sparse_model: str | Path,
        *,
        max_image_size: int = 3200,
        mesher: str = "poisson",
        progress_callback: ProgressCallback | None = None,
    ) -> tuple[dict[str, Any], Path]:
        adapter = self._adapter(ColmapAdapter, "colmap")
        workspace = self.store.workspace / "work" / "colmap"
        args = {
            "image_path": str(Path(image_path).resolve()),
            "sparse_model": str(Path(sparse_model).resolve()),
            "workspace": str(workspace),
            "max_image_size": max_image_size,
            "mesher": mesher,
        }
        return self._run_recorded(
            "03-reconstruction",
            adapter,
            "colmap_dense",
            args,
            lambda: adapter.reconstruct_dense(**args, progress_callback=progress_callback),  # type: ignore[attr-defined]
            progress_callback,
        )

    def inspect_blend(
        self,
        stage_id: str,
        blend_file: str | Path,
        *,
        progress_callback: ProgressCallback | None = None,
    ) -> tuple[dict[str, Any], Path]:
        adapter = self._adapter(BlenderAdapter, "blender")
        args = {"blend_file": str(Path(blend_file).resolve())}
        return self._run_recorded(
            stage_id,
            adapter,
            "blender_inspect",
            args,
            lambda: adapter.inspect_scene(**args),  # type: ignore[attr-defined]
            progress_callback,
        )

    def normalize_audio(
        self,
        input_file: str | Path,
        output_file: str | Path,
        *,
        sample_rate_hz: int = 22050,
        progress_callback: ProgressCallback | None = None,
    ) -> tuple[dict[str, Any], Path]:
        adapter = self._adapter(FFmpegAdapter, "ffmpeg")
        args = {
            "input_file": str(Path(input_file).resolve()),
            "output_file": str(Path(output_file).resolve()),
            "sample_rate_hz": sample_rate_hz,
            "overwrite": True,
        }
        return self._run_recorded(
            "19-piper-integration",
            adapter,
            "ffmpeg_normalize",
            args,
            lambda: adapter.normalize_wav(**args),  # type: ignore[attr-defined]
            progress_callback,
        )

    def synthesize_piper(
        self,
        text: str,
        model: str | Path,
        output_file: str | Path,
        *,
        length_scale: float = 1.0,
        progress_callback: ProgressCallback | None = None,
    ) -> tuple[dict[str, Any], Path]:
        adapter = self._adapter(PiperAdapter, "piper")
        call_args = {
            "text": text,
            "model": str(Path(model).resolve()),
            "output_wav": str(Path(output_file).resolve()),
            "length_scale": length_scale,
            "overwrite": True,
        }
        safe_report_args = {
            "text": f"<{len(text)} characters>",
            "model": call_args["model"],
            "output_wav": call_args["output_wav"],
            "length_scale": length_scale,
        }
        return self._run_recorded(
            "19-piper-integration",
            adapter,
            "piper_synthesize",
            safe_report_args,
            lambda: adapter.synthesize(**call_args),  # type: ignore[attr-defined]
            progress_callback,
        )
