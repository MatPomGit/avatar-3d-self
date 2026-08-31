# avatar-3d-self

Pipeline for building a realistic 3D self-avatar from scan data, with tooling for COLMAP reconstruction, mesh processing, MetaHuman preparation and Unreal Engine export.

## Project status

The repository is currently at an early development stage. GitHub CI intentionally performs only lightweight, deterministic checks. Operations that require COLMAP, Unreal Engine, MetaHuman assets or other workstation-specific 3D software are not executed on standard GitHub-hosted runners.

## Repository layout

- `scripts/` contains pipeline utilities.
- `source/` contains source avatar and MetaHuman-related data.
- `exports/` is reserved for generated exports.
- `animations/` contains animation-related assets.
- `references/` contains reference material.
- `docs/` contains project documentation.
- `.github/workflows/` contains CI and manually triggered pipeline placeholders.

## Python environment

Use Python 3.11 for development and CI compatibility.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Tools tied to Unreal Engine or COLMAP should be installed in their native environments rather than forced into the lightweight CI environment.

## CI policy

Pull requests touching Python sources, dependency metadata or workflow files run a short CI job that checks:

- Python bytecode compilation,
- critical Ruff errors such as syntax problems and undefined names.

Heavy 3D processing remains manual until a dedicated runner or reproducible containerized toolchain is available.

## Dependency updates

Dependabot groups Python dependency updates and GitHub Actions updates to reduce unnecessary pull-request noise.
