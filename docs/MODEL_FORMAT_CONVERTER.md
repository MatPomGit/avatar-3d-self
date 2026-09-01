# Konwerter formatów modeli 3D

Repozytorium zawiera konwerter `scripts/model_format_converter.py` obsługujący pliki **FBX, glTF, GLB, OBJ i STL** w obu kierunkach, o ile Blender potrafi zaimportować format źródłowy i wyeksportować format docelowy.

Konwerter używa Blendera w trybie bez interfejsu. To ważne, ponieważ model 3D może zawierać znacznie więcej niż samą siatkę: mapy UV, materiały, tekstury, szkielet, wagi kości, blendshapes i animacje. Przy każdej konwersji narzędzie analizuje scenę i zapisuje raport JSON informujący, które dane zostały wykryte i których format docelowy nie potrafi zachować.

## Najprostsze użycie

```bash
python scripts/model_format_converter.py exports/avatar_final.fbx exports/avatar_final.glb
```

Jeżeli Blender nie znajduje się w `PATH`, podaj jego lokalizację:

```bash
python scripts/model_format_converter.py model.fbx model.glb \
  --blender "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
```

Można też uruchomić skrypt bezpośrednio przez Blender:

```bash
blender --background --python scripts/model_format_converter.py -- model.fbx model.glb
```

Po konwersji obok pliku wynikowego powstaje raport, np. `model.glb.conversion.json`.

## Różnice między formatami

### GLB

GLB jest binarną odmianą glTF. Geometria, materiały PBR, tekstury, szkielet, skinning, blendshapes i animacje mogą znajdować się w jednym pliku. To najwygodniejszy format do przenoszenia kompletnej postaci między nowoczesnymi narzędziami, viewerami WWW i silnikami obsługującymi glTF.

Praktycznie: jeżeli chcesz wysłać komuś jeden plik zawierający animowaną postać wraz z materiałami, **GLB jest zwykle najlepszym wyborem**.

### glTF

glTF przechowuje te same typy danych co GLB, ale najczęściej rozdziela je na plik `.gltf`, plik binarny `.bin` i osobne obrazy tekstur. Ułatwia to ręczne podmienianie tekstur i analizowanie struktury assetu, ale wymaga pilnowania kilku plików jednocześnie.

Praktycznie: wybierz **glTF**, gdy chcesz mieć tekstury jako osobne pliki. Wybierz **GLB**, gdy zależy Ci na jednym przenośnym pliku.

### FBX

FBX jest rozbudowanym formatem wymiany używanym m.in. przez Blender, Maya, Unity i Unreal Engine. Może przenosić geometrię, UV, materiały, szkielet, skinning, blendshapes i animacje. Poszczególne programy mogą jednak interpretować część materiałów, osi, skal i animacji nieco inaczej, dlatego po konwersji trzeba sprawdzić rezultat w programie docelowym.

Praktycznie: **FBX jest dobrym formatem roboczym dla animowanych postaci**, szczególnie w pipeline Unity/Unreal, ale materiały PBR często wymagają ponownego sprawdzenia po imporcie.

### OBJ

OBJ przechowuje geometrię i mapy UV. Materiały są zwykle opisane w dodatkowym pliku `.mtl`, który może wskazywać na osobne tekstury. OBJ nie przechowuje szkieletu, skinningu, blendshapes ani animacji.

Praktycznie: OBJ nadaje się do przeniesienia **statycznego modelu z UV i prostymi materiałami**. Jeżeli wyeksportujesz animowaną postać FBX do OBJ, otrzymasz jej geometrię, ale utracisz rig i animacje.

### STL

STL opisuje praktycznie wyłącznie powierzchnię zbudowaną z trójkątów. Nie przechowuje UV, tekstur, materiałów PBR, szkieletu, blendshapes ani animacji. Jest popularny przede wszystkim w druku 3D i prostych przepływach CAD.

Praktycznie: STL wybierz wtedy, gdy potrzebujesz **samego kształtu do druku 3D**. Nie używaj go jako formatu archiwalnego dla cyfrowej postaci.

## Co dzieje się z danymi podczas konwersji

| Dane modelu | FBX | glTF | GLB | OBJ | STL |
| --- | :---: | :---: | :---: | :---: | :---: |
| Geometria | ✓ | ✓ | ✓ | ✓ | ✓ |
| Mapy UV | ✓ | ✓ | ✓ | ✓ | ✗ |
| Materiały | ✓ | ✓ | ✓ | ✓* | ✗ |
| Tekstury | ✓ | ✓ | ✓ | ✓* | ✗ |
| Szkielet | ✓ | ✓ | ✓ | ✗ | ✗ |
| Wagi kości | ✓ | ✓ | ✓ | ✗ | ✗ |
| Blendshapes / morph targets | ✓ | ✓ | ✓ | ✗ | ✗ |
| Animacje | ✓ | ✓ | ✓ | ✗ | ✗ |

`*` OBJ używa prostszego systemu materiałów MTL i osobnych plików tekstur. Materiał PBR z FBX lub glTF może wymagać uproszczenia.

Tabela opisuje możliwości formatów, a nie gwarancję idealnej konwersji pomiędzy każdym programem. Materiały, układ osi, skala i część ustawień animacji mogą wymagać kontroli po imporcie.

## Tekstury

Domyślnie konwerter stara się zachować tekstury:

```bash
python scripts/model_format_converter.py model.fbx model.glb --textures auto
```

Dostępne tryby:

```text
auto   dobierz naturalny sposób zapisu dla formatu
embed  osadź tekstury, jeżeli format i eksporter to umożliwia
copy   zapisz lub skopiuj tekstury obok modelu
skip   nie przenoś tekstur
```

GLB naturalnie nadaje się do umieszczenia tekstur wewnątrz jednego pliku. glTF i OBJ zwykle korzystają z plików zewnętrznych. Przy konwersji materiałów PBR zawsze należy sprawdzić Base Color, Normal, Roughness, Metallic i ewentualnie AO po imporcie do programu docelowego.

## Animacje i blendshapes

Domyślny tryb `auto` zachowuje animacje, jeżeli format wyjściowy je obsługuje:

```bash
python scripts/model_format_converter.py character.fbx character.glb --animations keep
```

Aby świadomie usunąć animacje:

```bash
python scripts/model_format_converter.py character.fbx static.glb --animations strip
```

Eksport do OBJ lub STL zawsze powoduje utratę animacji. Konwerter wykryje ten problem przed zapisem i umieści informację w raporcie.

## Tryb bezpieczny

Jeżeli nie chcesz dopuścić do konwersji powodującej utratę wykrytych danych, użyj `--strict`:

```bash
python scripts/model_format_converter.py animated_character.fbx character.obj --strict
```

Jeżeli wejściowy model zawiera np. szkielet, blendshapes albo animacje, konwersja zostanie przerwana zamiast utworzyć niepełny OBJ.

## Raport konwersji

Raport JSON zawiera m.in. liczbę obiektów, siatek, wierzchołków, materiałów, tekstur, armatur, shape keys i akcji animacji. Pole `losses` pokazuje dane, których nie da się zachować w wybranym formacie docelowym.

Przykład:

```json
{
  "input_format": ".fbx",
  "output_format": ".obj",
  "scene": {
    "meshes": 4,
    "materials": 7,
    "textures": 12,
    "armatures": 1,
    "shape_keys": 52,
    "actions": 3
  },
  "losses": [
    "szkielet",
    "wagi kości",
    "blendshapes / shape keys",
    "animacje"
  ],
  "lossless_for_detected_features": false
}
```

Dzięki temu użytkownik wie, że plik OBJ został utworzony poprawnie, ale nie jest już pełnym animowanym awatarem.
