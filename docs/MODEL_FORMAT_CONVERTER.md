# Konwerter formatów modeli 3D

Repozytorium zawiera konwerter `scripts/model_format_converter.py` obsługujący pliki **FBX, glTF, GLB, USD, USDZ, OBJ, PLY i STL**. Konwersja jest wykonywana przez Blender w trybie bez interfejsu, dzięki czemu narzędzie może pracować nie tylko na samej siatce, ale również na UV, materiałach, teksturach, szkielecie, wagach kości, blendshapes i animacjach.

Przy każdej konwersji narzędzie najpierw analizuje zawartość sceny. Następnie sprawdza możliwości formatu docelowego i zapisuje raport JSON z informacją, które dane zostały zachowane, a które musiały zostać utracone lub uproszczone.

## Najprostsze użycie

```bash
python scripts/model_format_converter.py exports/avatar_final.fbx exports/avatar_final.glb
```

Dodatkowe przykłady:

```bash
# Kompletny asset do jednego pliku
python scripts/model_format_converter.py avatar.fbx avatar.usdz --textures embed

# Skan PLY do formatu nadającego się do dalszej pracy z materiałami
python scripts/model_format_converter.py scan.ply scan.glb

# Statyczny OBJ razem z MTL
python scripts/model_format_converter.py avatar.glb avatar.obj
```

Po konwersji obok pliku wynikowego powstaje raport, np. `avatar.glb.conversion.json`.

## Różnice między formatami

### GLB

GLB jest binarną odmianą glTF. Geometria, materiały PBR, tekstury, szkielet, skinning, blendshapes i animacje mogą znajdować się w jednym pliku. To wygodny format do viewerów WWW, wymiany assetów oraz przenoszenia kompletnej postaci między nowoczesnymi narzędziami.

### glTF

glTF przechowuje podobny zestaw danych jak GLB, ale zwykle jako plik `.gltf`, plik `.bin` oraz osobne tekstury. Jest wygodny wtedy, gdy użytkownik chce mieć dostęp do poszczególnych elementów assetu zamiast jednego pakietu.

### FBX

FBX jest rozbudowanym formatem wymiany używanym m.in. przez Blender, Maya, Unity i Unreal Engine. Dobrze nadaje się do animowanych postaci z rigami, morph targets i animacjami. Materiały oraz układ osi zawsze warto sprawdzić po imporcie do programu docelowego.

### USD

USD, czyli Universal Scene Description, jest formatem scenowym przeznaczonym do wymiany złożonych assetów i całych scen. Blender potrafi eksportować do USD siatki, UV, materiały, skeletony, skinned meshes, shape keys jako blend shapes oraz animacje. W praktyce USD jest dobrym wyborem, gdy model ma pozostać częścią większego pipeline scenowego, a nie tylko pojedynczym plikiem siatki.

### USDZ

USDZ jest pakietem USD zapisanym jako pojedyncze archiwum. Może zawierać scenę USD oraz jej zależności teksturowe, dlatego jest wygodny do przenoszenia kompletnego assetu jako jednego pliku. Blender tworzy USDZ przez eksport USD do pliku z rozszerzeniem `.usdz`.

### OBJ + MTL

OBJ przechowuje statyczną geometrię, normalne i UV. Materiały są zapisane w osobnym pliku `.mtl`, który może odwoływać się do plików tekstur. OBJ nie przechowuje armatur, skinningu, blendshapes ani animacji. Konwerter zawsze zapewnia plik MTL i wpis `mtllib` w pliku OBJ.

Przykład wyniku:

```text
avatar.obj
avatar.mtl
textures/
  skin_basecolor.png
  skin_normal.png
```

### PLY

PLY jest formatem używanym często dla skanów, chmur punktów i statycznych siatek. Blender może zapisywać w nim geometrię, UV, normalne oraz kolory wierzchołków, ale format nie jest przeznaczony do przenoszenia typowych materiałów PBR, tekstur, riga ani animacji postaci. Jest więc dobrym formatem wejściowym dla skanu, ale słabym formatem archiwalnym dla kompletnego awatara.

### STL

STL opisuje praktycznie wyłącznie powierzchnię zbudowaną z trójkątów. Nie przechowuje UV, materiałów, tekstur, skeletonu, blendshapes ani animacji. Nadaje się przede wszystkim do druku 3D i prostych zastosowań geometrycznych.

## Co dzieje się z danymi podczas konwersji

| Dane modelu | FBX | glTF | GLB | USD | USDZ | OBJ + MTL | PLY | STL |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Geometria | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Mapy UV | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| Materiały | ✓ | ✓ | ✓ | ✓ | ✓ | ✓* | ✗ | ✗ |
| Tekstury | ✓ | ✓ | ✓ | ✓ | ✓ | ✓* | ✗ | ✗ |
| Szkielet | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| Wagi kości | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| Blendshapes / morph targets | ✓ | ✓ | ✓ | ✓** | ✓** | ✗ | ✗ | ✗ |
| Animacje | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |

`*` OBJ używa MTL i osobnych tekstur. Materiał PBR może wymagać uproszczenia do parametrów obsługiwanych przez MTL.

`**` Blender eksportuje shape keys jako USD blend shapes, ale absolute shape keys nie są obsługiwane.

Tabela opisuje możliwości formatów w tym pipeline, a nie gwarancję identycznej interpretacji danych przez każdy program 3D.

## Tekstury

Domyślnie konwerter stara się zachować tekstury:

```bash
python scripts/model_format_converter.py model.fbx model.glb --textures auto
```

Dostępne tryby:

```text
auto   dobierz naturalny sposób zapisu dla formatu
embed  osadź tekstury, jeżeli format i eksporter to umożliwia
copy   zachowaj tekstury jako pliki zewnętrzne
skip   usuń tekstury przed eksportem
```

Można dodatkowo zmniejszyć rozdzielczość i zmienić format obrazów:

```bash
python scripts/model_format_converter.py model.fbx model.usdz \
  --textures embed \
  --max-texture-size 2048 \
  --texture-format png
```

USDZ naturalnie nadaje się do pakowania zależności teksturowych razem ze sceną. Dla OBJ tekstury pozostają plikami zewnętrznymi wskazywanymi przez `.mtl`. Dla PLY i STL tekstury nie są częścią standardowego modelu konwersji i zostaną zgłoszone jako utrata danych.

## Animacje i blendshapes

Domyślny tryb `auto` zachowuje animacje, jeżeli format wyjściowy je obsługuje:

```bash
python scripts/model_format_converter.py character.fbx character.usd --animations keep
```

Aby świadomie usunąć animacje:

```bash
python scripts/model_format_converter.py character.fbx static.glb --animations strip
```

Eksport do OBJ, PLY lub STL powoduje utratę animacji. Konwerter wykrywa ten problem przed zapisem i umieszcza informację w raporcie.

## Tryb bezpieczny

Jeżeli nie chcesz dopuścić do konwersji powodującej utratę wykrytych danych, użyj `--strict`:

```bash
python scripts/model_format_converter.py animated_character.fbx character.ply --strict
```

Jeżeli wejściowy model zawiera szkielet, blendshapes, materiały lub animacje nieobsługiwane przez format docelowy, konwersja zostanie przerwana.

## Raport konwersji

Raport JSON zawiera m.in. liczbę obiektów, siatek, wierzchołków, warstw UV, atrybutów kolorów, materiałów, tekstur, armatur, shape keys i akcji animacji. Pole `losses` pokazuje dane, których nie da się zachować w wybranym formacie docelowym.

Dla OBJ raport zawiera również `companion_files`, dzięki czemu użytkownik widzi towarzyszący plik `.mtl`.

Przykład:

```json
{
  "input_format": ".glb",
  "output_format": ".obj",
  "companion_files": [
    "/path/to/avatar.mtl"
  ],
  "losses": [
    "szkielet",
    "wagi kości",
    "blendshapes / shape keys",
    "animacje"
  ],
  "lossless_for_detected_features": false
}
```

## Referencje techniczne

- Blender Manual: Universal Scene Description (USD), `https://docs.blender.org/manual/en/4.2/files/import_export/usd.html`
- Blender Manual: Wavefront OBJ, `https://docs.blender.org/manual/en/5.3/files/import_export/obj.html`
- Blender Manual: Stanford PLY, `https://docs.blender.org/manual/en/4.5/files/import_export/ply.html`
