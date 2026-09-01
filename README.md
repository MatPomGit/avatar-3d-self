# avatar-3d-self

Professional, reproducible pipeline for building a photorealistic, editable and real-time 3D self-avatar. The project covers reference acquisition, reconstruction, retopology, PBR materials, hair, clothing, body and facial rigging, animation, Piper-based speech and runtime validation.

Documentation: **https://matpomgit.github.io/avatar-3d-self/**

The public website is documentation only. Interactive stage guidance, project state, artefact inspection and local tool orchestration belong to the separate **Avatar Studio** desktop application under `apps/avatar_studio/`.

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
python -m pip install -e ".[dev,docs,desktop]"
```

### Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,docs,desktop]"
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

The application architecture and packaging strategy are documented in `docs/desktop/architecture.md`.
