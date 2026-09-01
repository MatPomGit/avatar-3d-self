# Konfiguracja Linux

## Python i repozytorium

```bash
git clone https://github.com/MatPomGit/avatar-3d-self.git
cd avatar-3d-self
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,docs,desktop]"
```

Sprawdź:

```bash
python --version
python -m pytest -q
mkdocs build --strict
avatar-studio
```

## Narzędzia lokalne

Zainstaluj Blender, COLMAP, Git LFS i FFmpeg z repozytoriów dystrybucji albo oficjalnych wydań. W Avatar Studio wskaż rzeczywiste ścieżki binariów i nie zakładaj, że każde narzędzie znajduje się w `PATH`.

Przykładowy workspace:

```text
/home/<user>/Avatar3D/projects/self-avatar/
```

Prywatnego capture nie przechowuj w katalogu repozytorium.
