# Konfiguracja Windows

## Python i repozytorium

```powershell
git clone https://github.com/MatPomGit/avatar-studio.git
cd avatar-studio
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,docs,desktop]"
```

Sprawdź:

```powershell
python --version
python -m pytest -q
mkdocs build --strict
avatar-studio
```

## Narzędzia lokalne

Zainstaluj Blender, COLMAP, Git LFS i FFmpeg z oficjalnych dystrybucji. Ścieżki do programów skonfiguruj w Avatar Studio zamiast wpisywać je na stałe w kodzie.

Przykładowa lokalizacja workspace:

```text
D:\AvatarStudio\projects\self-avatar\
```

Nie umieszczaj prywatnego materiału referencyjnego (reference capture) w katalogu sklonowanego repozytorium.
