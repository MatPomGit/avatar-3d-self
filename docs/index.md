# Project documentation

This directory contains maintained documentation for the current implementation of `avatar-3d-self`.

## Environment boundaries

The project uses three distinct execution environments:

1. **Python development and CI**
   - Python 3.11
   - source validation, utility code and tests
   - dependencies declared in `pyproject.toml`

2. **COLMAP reconstruction workstation**
   - COLMAP installed as a system application
   - reconstruction scripts call the `colmap` executable through `subprocess`
   - large scan data and generated reconstruction artifacts should not be treated as CI inputs

3. **Unreal Engine and MetaHuman workstation**
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

GitHub Actions should fail only for deterministic repository problems. Workflows requiring proprietary applications, GPU-heavy processing, large assets or workstation state remain manual until a dedicated runner exists.

Placeholder workflows are entry points for future automation, not claims that those pipelines are currently reproducible on GitHub-hosted runners.
