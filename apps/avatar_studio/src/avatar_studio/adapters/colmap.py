"""COLMAP workstation adapter."""

from __future__ import annotations

from pathlib import Path
import re

from avatar_studio.adapters.base import CommandResult, ToolAdapter


class ColmapAdapter(ToolAdapter):
    name = "COLMAP"
    executable_names = ("colmap", "colmap.exe")
    version_args = ("-h",)

    def analyze_sparse_model(self, model_path: str | Path) -> dict:
        """Run COLMAP model_analyzer and normalize its principal quality metrics."""

        path = Path(model_path).resolve()
        if not path.exists():
            raise FileNotFoundError(path)
        result = self.run(("model_analyzer", "--path", str(path)))
        self._require_success(result, "COLMAP model analysis")
        metrics = self.parse_model_analyzer(result.stdout + "\n" + result.stderr)
        metrics.update(
            {
                "tool": "COLMAP",
                "model_path": str(path),
                "command": list(result.command),
            }
        )
        return metrics

    def reconstruct_sparse(
        self,
        image_path: str | Path,
        workspace: str | Path,
        *,
        camera_model: str = "OPENCV",
        single_camera: bool = True,
        matcher: str = "exhaustive",
        mask_path: str | Path | None = None,
        timeout_s: float = 3600.0,
    ) -> dict:
        """Execute feature extraction, matching and sparse mapping in a private workspace."""

        images = Path(image_path).resolve()
        if not images.is_dir():
            raise NotADirectoryError(images)
        root = Path(workspace).resolve()
        root.mkdir(parents=True, exist_ok=True)
        database = root / "database.db"
        sparse = root / "sparse"
        sparse.mkdir(parents=True, exist_ok=True)

        feature_args = [
            "feature_extractor",
            "--database_path",
            str(database),
            "--image_path",
            str(images),
            "--ImageReader.camera_model",
            camera_model,
            "--ImageReader.single_camera",
            "1" if single_camera else "0",
        ]
        if mask_path is not None:
            masks = Path(mask_path).resolve()
            if not masks.is_dir():
                raise NotADirectoryError(masks)
            feature_args.extend(("--ImageReader.mask_path", str(masks)))

        feature_result = self.run(feature_args, timeout_s=timeout_s)
        self._require_success(feature_result, "COLMAP feature extraction")

        matcher_command = {
            "exhaustive": "exhaustive_matcher",
            "sequential": "sequential_matcher",
            "spatial": "spatial_matcher",
        }.get(matcher)
        if matcher_command is None:
            raise ValueError("matcher must be exhaustive, sequential or spatial")
        match_result = self.run(
            (matcher_command, "--database_path", str(database)), timeout_s=timeout_s
        )
        self._require_success(match_result, "COLMAP feature matching")

        mapper_result = self.run(
            (
                "mapper",
                "--database_path",
                str(database),
                "--image_path",
                str(images),
                "--output_path",
                str(sparse),
            ),
            timeout_s=timeout_s,
        )
        self._require_success(mapper_result, "COLMAP sparse mapping")

        models = sorted(path for path in sparse.iterdir() if path.is_dir())
        return {
            "tool": "COLMAP",
            "database_path": str(database),
            "sparse_root": str(sparse),
            "models": [str(path) for path in models],
            "camera_model": camera_model,
            "single_camera": single_camera,
            "matcher": matcher,
            "commands": [
                list(feature_result.command),
                list(match_result.command),
                list(mapper_result.command),
            ],
        }

    @staticmethod
    def parse_model_analyzer(text: str) -> dict:
        """Parse stable numeric values from human-readable model_analyzer output."""

        patterns: dict[str, tuple[str, type]] = {
            "cameras": (r"(?im)^\s*Cameras\s*:\s*(\d+)", int),
            "images": (r"(?im)^\s*Images\s*:\s*(\d+)", int),
            "registered_images": (r"(?im)^\s*Registered images\s*:\s*(\d+)", int),
            "points3d": (r"(?im)^\s*(?:Points|Points3D)\s*:\s*(\d+)", int),
            "observations": (r"(?im)^\s*Observations\s*:\s*(\d+)", int),
            "mean_track_length": (r"(?im)^\s*Mean track length\s*:\s*([0-9.eE+-]+)", float),
            "mean_observations_per_image": (
                r"(?im)^\s*Mean observations per image\s*:\s*([0-9.eE+-]+)",
                float,
            ),
            "mean_reprojection_error_px": (
                r"(?im)^\s*Mean reprojection error\s*:\s*([0-9.eE+-]+)\s*(?:px)?",
                float,
            ),
        }
        metrics: dict[str, int | float | None] = {}
        for key, (pattern, cast) in patterns.items():
            match = re.search(pattern, text)
            metrics[key] = cast(match.group(1)) if match else None
        images = metrics.get("images")
        registered = metrics.get("registered_images")
        if isinstance(images, int) and images > 0 and isinstance(registered, int):
            metrics["registration_ratio"] = registered / images
        return metrics

    @staticmethod
    def _require_success(result: CommandResult, operation: str) -> None:
        if not result.ok:
            raise RuntimeError(
                f"{operation} failed with exit code {result.returncode}: {result.stderr.strip()}"
            )
