# Konwerter formatów modeli

`scripts/model_format_converter.py` służy do jawnej konwersji i raportowania ryzyka utraty danych. Konwersja nie może być używana jako sposób zastępowania kanonicznej sceny DCC.

## Windows

```powershell
python scripts\model_format_converter.py exports\avatar_final.fbx exports\avatar_final.glb
```

Przy integracji z Blenderem skonfiguruj pełną ścieżkę do `blender.exe`, jeśli skrypt jej wymaga. Po konwersji sprawdź raport: skeleton, skinning, morph targets, animation, materials, textures, units i axes.

## Linux

```bash
python scripts/model_format_converter.py exports/avatar_final.fbx exports/avatar_final.glb
```

Po konwersji wykonaj tę samą kontrolę raportu. Format wynikowy z mniejszą liczbą obsługiwanych cech nie jest automatycznie równoważny źródłu.
