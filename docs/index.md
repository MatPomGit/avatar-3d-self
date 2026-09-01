# Project documentation

This directory contains maintained documentation for the current implementation of `avatar-3d-self`.

## Main documentation

- [`COMPLETE_PIPELINE.md`](COMPLETE_PIPELINE.md) describes the end-to-end avatar production pipeline.
- [`REALISTIC_AVATAR_GUIDE.md`](REALISTIC_AVATAR_GUIDE.md) contains practical guidance for building the avatar.
- [`ENGINE_INTEGRATION.md`](ENGINE_INTEGRATION.md) covers integration with target 3D engines.
- [`MODEL_FORMAT_CONVERTER.md`](MODEL_FORMAT_CONVERTER.md) is the authoritative technical and user reference for the loss-aware 3D model converter.
- [`FORMAT_CONVERSION_EXAMPLES.md`](FORMAT_CONVERSION_EXAMPLES.md) contains validated conversion scenarios, expected losses and post-export checks.

## Environment boundaries

The project uses four distinct execution environments:

1. **Python development and CI**
   - Python 3.11
   - source validation, utility code and tests
   - dependencies declared in `pyproject.toml`

2. **Blender conversion and asset-processing workstation**
   - Blender installed as a system application
   - `scripts/model_format_converter.py` launches Blender in background mode
   - full conversion tests require representative 3D assets and are not suitable for lightweight GitHub-hosted CI

3. **COLMAP reconstruction workstation**
   - COLMAP installed as a system application
   - reconstruction scripts call the `colmap` executable through `subprocess`
   - large scan data and generated reconstruction artifacts should not be treated as CI inputs

4. **Unreal Engine and MetaHuman workstation**
   - Unreal Engine provides the `unreal` Python module
   - Unreal-specific scripts must run inside the Unreal Python environment
   - MetaHuman assets remain external to standard GitHub-hosted CI

## Dependency groups

`pyproject.toml` is the only Python dependency manifest.

- `dev` contains lightweight development and CI tools.
- `geometry` contains numerical and mesh-processing libraries.
- `vision` contains image-processing libraries.

Install only the group required for the task being performed.

## Automation policy

GitHub Actions should fail only for deterministic repository problems. Workflows requiring proprietary applications, GPU-heavy processing, large assets, Blender integration assets or workstation state remain manual until a dedicated runner exists.

Placeholder workflows are entry points for future automation, not claims that those pipelines are currently reproducible on GitHub-hosted runners.
