# Avatar Studio

Desktop companion for the Avatar 3D Self production pipeline.

The application is intentionally local-first. It stores project state in `.avatar-studio/project.sqlite3`, registers artefacts with hashes and metadata, exposes stage dependencies and acts as the future orchestration layer for Blender, COLMAP, Piper and validators.

## Windows

```powershell
python -m pip install -e ".[desktop]"
avatar-studio --workspace D:\Avatar3D\projects\self-avatar
```

A standalone `.exe` can be built with the `Desktop package` GitHub Actions workflow or locally with PyInstaller.

## Linux

```bash
python -m pip install -e ".[desktop]"
avatar-studio --workspace ~/Avatar3D/projects/self-avatar
```

The GUI is not required for deterministic validators; pipeline logic and project storage remain importable without PySide6.
