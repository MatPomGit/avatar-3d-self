# avatar-3d-self

Pipeline and tooling for building a realistic 3D self-avatar from scan data, through reconstruction and mesh processing, to MetaHuman and Unreal Engine integration.

## Status

The project is in early development. The repository intentionally separates lightweight Python tooling from workstation-specific 3D software. GitHub-hosted CI validates source quality but does not attempt to run COLMAP, Unreal Engine or MetaHuman workflows.

## Structure

- `scripts/` contains pipeline utilities.
- `source/` contains reconstruction and avatar source data.
- `exports/` is reserved for generated deliverables.
- `animations/` contains animation assets.
- `references/` contains source/reference material.
- `notebooks/` contains exploratory analysis.
- `docs/` contains maintained project documentation.
- `.github/workflows/` contains CI and manually triggered 3D workflow entry points.

## Development environment

Python 3.11 is the supported development version.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Optional dependency groups are installed only when needed:

```bash
python -m pip install -e ".[geometry]"
python -m pip install -e ".[vision]"
```

`pyproject.toml` is the single source of truth for Python dependencies. Unreal Engine's `unreal` module is provided by Unreal Engine itself and is therefore not declared as a PyPI dependency. COLMAP is an external executable and must also be installed separately.

## CI policy

Pull requests touching Python sources or project configuration run deterministic checks only:

- Python bytecode compilation,
- Ruff checks for syntax errors, undefined names and related critical failures.

Heavy 3D jobs stay manual until a reproducible dedicated runner or containerized toolchain is available.

## Documentation

See [`docs/index.md`](docs/index.md) for the maintained documentation index and environment boundaries.
