# avatar-3d-self

Narzędzia i pipeline tworzenia fotorealistycznego, edytowalnego awatara 3D własnej osoby. Projekt obejmuje rekonstrukcję, przetwarzanie siatek, materiały, rig, animację oraz integrację z silnikiem i Piper TTS.

Strona projektu: **https://matpomgit.github.io/avatar-3d-self/**

## Stan

Projekt jest na wczesnym etapie. CI sprawdza kod i buduje stronę, ale nie uruchamia COLMAP, Blendera, MetaHuman ani Unreal Engine.

## Struktura

- `scripts/`: narzędzia pipeline'u;
- `source/`: opisy i źródła modelu;
- `references/`: metadane referencji;
- `animations/`: zasoby animacji;
- `exports/`: eksporty i raporty;
- `web/viewer/`: strona oraz viewer;
- `docs/`: dokumentacja.

## Środowisko Python

Wymagany jest Python 3.11.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Opcjonalne zależności:

```bash
python -m pip install -e ".[geometry]"
python -m pip install -e ".[vision]"
```

## Viewer WWW

```bash
cd web/viewer
npm install
npm run dev
```

## Konwerter formatów

Konwerter oparty na Blenderze obsługuje FBX, glTF, GLB, USD, USDZ, OBJ, PLY i STL oraz raportuje potencjalną utratę danych.

```bash
python scripts/model_format_converter.py exports/avatar_final.fbx exports/avatar_final.glb
```

Dalsze informacje: [dokumentacja](docs/index.md).
