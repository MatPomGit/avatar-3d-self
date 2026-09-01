# Contributor guidance

## Project scope

`avatar-3d-self` is an editable, workstation-centred production pipeline for a
photorealistic digital self-avatar. It contains lightweight Python utilities,
documentation and a Three.js viewer. Reconstruction, DCC work, MetaHuman and
Unreal Engine integration require local specialist software and are not
reproducible on GitHub-hosted runners.

The quality order is: likeness to approved reference material, anatomical and
deformation quality, natural facial animation, and real-time performance. Do
not trade the first three for generic beautification or stylisation.

## Authoritative project facts

- Python 3.11+ is required; `pyproject.toml` is the dependency source of truth.
- CI runs `compileall`, Ruff's critical-error rules and pytest. It does not run
  COLMAP, Blender, MetaHuman or Unreal Engine.
- GitHub Pages is a static viewer only. It must never contain source scans,
  private reference photos, credentials or privileged processing logic.
- The canonical interchange package is documented in `docs/ARCHITECTURE.md`
  and decisions in `docs/adr/`.

## Asset and privacy rules

- Treat source photographs, body scans, audio recordings and biometric
  annotations as sensitive personal data. Keep them outside this public
  repository unless explicit publication approval is recorded.
- Large binary source and deliverable assets must use Git LFS when intentionally
  versioned. Do not commit generated caches, render outputs or workstation-only
  intermediate files.
- Preserve editable source, retopology, textures, rig and animation separately;
  an exported FBX or GLB must not be the only surviving asset.

## Change rules

- Read the relevant documentation and scripts before modifying a pipeline step.
- Keep changes small and reviewable. Do not push directly to `main`.
- Update the roadmap, changelog and an ADR when a change alters an architectural
  boundary, canonical format, privacy rule or runtime contract.
- Use type hints and `logging` in new or substantially changed Python code.
- Run the narrowest relevant checks, then `python -m pytest -q` and
  `ruff check scripts tests` for Python changes.

## Coordinate and export conventions

Source scans use a right-handed, Z-up convention. Exports for Unreal Engine are
converted deliberately at the exporter boundary and validated in the target
application. Exported meshes use centimetres. Never assume that a conversion
preserves materials, rigs, shape keys or animation: use its report and validate
in the target application.
