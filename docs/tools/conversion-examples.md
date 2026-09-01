# Przykłady konwersji formatów

Eksport jest artefaktem pochodnym. Każda konwersja powinna pozostawić raport zawierający format wejściowy i wyjściowy, jednostki, osie, liczbę obiektów, materiałów, kości, blend shapes i animacji oraz listę potencjalnych strat.

## Blender jako konwerter

### Windows

```powershell
blender.exe --background --python scripts/model_format_converter.py -- `
  source\avatar_master.blend exports\avatar_runtime.glb
```

### Linux

```bash
blender --background --python scripts/model_format_converter.py -- \
  source/avatar_master.blend exports/avatar_runtime.glb
```

## FBX → GLB

Po konwersji sprawdź skeleton, skinning, morph targets, animacje i materiały. Nie zakładaj, że poprawny import geometrii oznacza zachowanie całej semantyki FBX.

## OBJ / PLY

Formaty te są odpowiednie dla geometrii statycznej i skanów. Nie są formatem kanonicznym dla riggowanego avatara, ponieważ nie przenoszą pełnego skeletonu, blend shapes i animacji.

## USD / USDZ

Stosuj dopiero po walidacji konkretnego targetu. Raportuj, które materiały i deformery zostały odwzorowane, a które spłaszczone lub pominięte.

## Reguła akceptacji

Konwersja jest zatwierdzona dopiero po ponownym imporcie pliku wynikowego i wykonaniu testu kontrolnego obejmującego co najmniej rest pose, jedną animację ciała, ruch palców, jawOpen, mrugnięcie i wybrane blend shapes.