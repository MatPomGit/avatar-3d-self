# Architecture

## Purpose and boundary

The repository supports a photorealistic, real-time self-avatar while keeping
the production master editable. It is not a cloud service and has no backend or
shared database. GitHub Pages serves only a static viewer and public project
documentation.

## Asset lifecycle

`private reference material -> reconstruction -> editable DCC master ->
retopology/UV/materials/rig -> validated target export -> runtime package`

Each arrow is a controlled transformation. The inputs and high-value
intermediates remain outside the public repository or use approved Git LFS
storage. Generated runtime files never replace the editable master.

## Repository responsibilities

| Area | Contents | Boundary |
| --- | --- | --- |
| `references/` | non-sensitive manifests and capture metadata | no raw biometric media by default |
| `source/` | small descriptors and approved LFS assets | editable sources remain canonical |
| `scripts/` | deterministic Python utilities | no hidden workstation secrets |
| `animations/` | configuration and small metadata | large clips via approved LFS |
| `exports/` | target packages and reports | generated, reproducible where practical |
| `web/viewer/` | static Three.js viewer | public, client-side only |
| `docs/` | technical decisions and procedures | source of project process truth |

## Interchange contract

- Keep the DCC-native working file as the editable master.
- Use FBX for established engine rigging paths, GLB/glTF for web delivery, and
  USD/USDZ only when the target workflow is validated.
- A conversion report is required whenever a boundary may lose rigging, shape
  keys, animation, materials or textures.
- Coordinate conversion occurs at export. Source scans are right-handed Z-up;
  Unreal-target exports are centimetres and verified after import.

## Naming and code-style contract

- Use lowercase `snake_case` for Python filenames, packages, functions,
  variables, test modules and machine-oriented pipeline metadata.
- Use lowercase `kebab-case` for Markdown documentation, general asset folders
  and static web assets. The production-pipeline documents use
  `complete-pipeline.md` and `engine-integration.md`.
- Keep conventional or tool-mandated names unchanged, including repository root
  documents, `pyproject.toml`, `package.json` and exported React components such
  as `App.jsx`.
- Apply PEP 8 and PEP 257 to every new or modified Python module: readable
  layout, explicit imports, descriptive names, and concise English docstrings
  for public modules, classes and functions.
- Apply KISS: choose the smallest clear design, avoid speculative abstractions,
  and add dependencies only for a verified requirement.

See [ADR-0004](adr/0004-naming-and-python-style.md) for rationale and migration
rules.

## Runtime separation

Python and GitHub Actions handle deterministic checks. Blender, COLMAP,
MetaHuman, Unreal Engine and a local Piper deployment are external runtime
boundaries. Their configuration, binaries and private assets are not Python
package dependencies and must be documented per workstation when introduced.

See [ADR-0001](adr/0001-editable-master-and-interchange-formats.md) and
[ADR-0002](adr/0002-workstation-boundaries-and-public-viewer.md).
