# Avatar Studio

**Avatar Studio** is a professional, reproducible environment for building a photorealistic, editable and real-time digital human. It combines a documented production pipeline with a local desktop application that guides the user through reference acquisition, reconstruction, retopology, PBR materials, hair, clothing, rigging, animation, Piper-based speech and runtime validation.

Documentation: **https://matpomgit.github.io/avatar-3d-self/**

The public website is documentation only. Interactive stage guidance, project state, artefact inspection and local tool orchestration belong to the **Avatar Studio** desktop application under `apps/avatar_studio/`.

## Naming

- product: `Avatar Studio`;
- Python package/import: `avatar_studio`;
- Python distribution: `avatar-studio`;
- CLI command: `avatar-studio`;
- Windows executable: `AvatarStudio.exe`;
- Linux executable: `AvatarStudio`.

The GitHub repository keeps its historical URL until it is renamed administratively. Internal code and documentation use the new canonical product name.

## Repository roles

- `docs/`: MkDocs documentation and technical specifications;
- `apps/avatar_studio/`: cross-platform desktop application;
- `scripts/`: deterministic pipeline utilities and validators;
- `source/`: approved editable source assets and manifests;
- `references/`: non-sensitive reference manifests;
- `animations/`: animation metadata and mappings;
- `exports/`: derived interchange artefacts and conversion reports;
- `tests/`: automated tests.

## Development environment

### Windows

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,docs,desktop,geometry,vision]"
```

### Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,docs,desktop,geometry,vision]"
```

## Documentation

### Windows

```powershell
mkdocs serve
```

### Linux

```bash
mkdocs serve
```

## Avatar Studio

### Windows

```powershell
avatar-studio
```

### Linux

```bash
avatar-studio
```

Application architecture and packaging are documented in `docs/desktop/architecture.md`.
