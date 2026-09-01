# avatar-3d-self

Pipeline and tooling for building a realistic 3D self-avatar from scan data, through reconstruction and mesh processing, to MetaHuman and Unreal Engine integration.

## Project website

The public project website combines the project overview, the complete production procedure and the interactive 3D viewer:

**https://matpomgit.github.io/avatar-3d-self/**

The site is built from `web/viewer/` and deployed automatically to GitHub Pages after changes are merged into `main`.

## Status

The project is in early development. The repository intentionally separates lightweight Python tooling from workstation-specific 3D software. GitHub-hosted CI validates source quality but does not attempt to run COLMAP, Blender integration assets, Unreal Engine or MetaHuman workflows.

## Structure

- `scripts/` contains pipeline utilities.
- `source/` contains reconstruction and avatar source data.
- `exports/` is reserved for generated deliverables.
- `animations/` contains animation assets.
- `references/` contains source/reference material.
- `docs/` contains maintained project documentation.
- `web/viewer/` contains the GitHub Pages project site and interactive Three.js viewer.
- `.github/workflows/` contains CI, Pages deployment and manually triggered 3D workflow entry points.

## Model format converter

The repository includes a loss-aware Blender-backed converter for **FBX, glTF, GLB, USD, USDZ, OBJ, PLY and STL**. It inspects the imported scene before export and reports whether geometry, UVs, materials, textures, armatures, skin weights, shape keys and animations can be represented by the target format.

```bash
python scripts/model_format_converter.py exports/avatar_final.fbx exports/avatar_final.glb
python scripts/model_format_converter.py avatar.fbx avatar.usdz --textures embed
python scripts/model_format_converter.py scan.ply scan.glb
python scripts/model_format_converter.py avatar.glb avatar.obj --textures copy
```

OBJ export always includes a companion `.mtl` file named after the OBJ and an `mtllib` reference in the OBJ file. Texture processing can be included in the same operation:

```bash
python scripts/model_format_converter.py model.fbx model.usdz \
  --max-texture-size 2048 \
  --texture-format png \
  --textures embed \
  --animations keep
```

Use `--strict` when conversion should stop instead of silently creating a reduced asset. For example, converting an animated FBX to OBJ, PLY or STL would otherwise discard rigging and animation data.

Documentation:

- [`docs/model_format_converter.md`](docs/model_format_converter.md) — complete technical and user reference, CLI, architecture, capability matrix, validation and troubleshooting.
- [`docs/format_conversion_examples.md`](docs/format_conversion_examples.md) — practical conversion recipes with expected preserved data, losses and post-export checks.

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

`pyproject.toml` is the single source of truth for Python dependencies. Unreal Engine's `unreal` module is provided by Unreal Engine itself and is therefore not declared as a PyPI dependency. COLMAP and Blender are external executables and must also be installed separately.

## Web development

```bash
cd web/viewer
npm install
npm run dev
```

Production builds use the `/avatar-3d-self/` base path required by GitHub Pages.

## CI policy

Pull requests touching Python sources or project configuration run deterministic checks only:

- Python bytecode compilation,
- Ruff checks for syntax errors, undefined names and related critical failures.
- pytest tests.

The separate `GitHub Pages` workflow validates the web build on pull requests and deploys the site only from `main`. Heavy 3D jobs stay manual until a reproducible dedicated runner or containerized toolchain is available.

## Documentation

See [`docs/index.md`](docs/index.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/ROADMAP.md`](docs/ROADMAP.md), [`CHANGELOG.md`](CHANGELOG.md), [`docs/realistic_avatar_guide.md`](docs/realistic_avatar_guide.md), [`docs/COMPLETE_PIPELINE.md`](docs/COMPLETE_PIPELINE.md), [`docs/model_format_converter.md`](docs/model_format_converter.md) and [`docs/format_conversion_examples.md`](docs/format_conversion_examples.md) for detailed technical notes.
