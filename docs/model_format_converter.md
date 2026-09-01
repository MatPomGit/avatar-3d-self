# Konwerter formatów modeli 3D

`model_format_converter.py` jest narzędziem do kontrolowanej konwersji modeli i scen 3D pomiędzy formatami **FBX, glTF, GLB, USD, USDZ, OBJ, PLY i STL**. Konwerter został zaprojektowany przede wszystkim dla modeli postaci, dlatego nie ogranicza się do samej geometrii. Przed eksportem analizuje zawartość sceny i sprawdza obecność map UV, materiałów, tekstur, armatury, wag kości, blendshapes / shape keys oraz animacji.

Najważniejszą cechą narzędzia jest podejście **loss-aware**. Konwerter nie zakłada, że każda para formatów przenosi ten sam zestaw danych. Jeżeli format docelowy nie obsługuje części zawartości modelu, informacja trafia do konsoli i raportu JSON. Opcjonalny tryb `--strict` może przerwać taką operację przed utworzeniem niepełnego pliku.

> Konwerter automatyzuje import, analizę, przetwarzanie i eksport, ale nie może zagwarantować semantycznie identycznego wyniku w każdym programie 3D. Format pliku, importer i eksporter Blendera oraz aplikacja docelowa mają własne modele materiałów, osi, skal, animacji i cech sceny. Po konwersji zasobu produkcyjnego zawsze należy wykonać walidację w aplikacji docelowej.

## 1. Zakres funkcjonalny

Konwerter realizuje następujący przepływ:

1. rozpoznaje format wejściowy i wyjściowy na podstawie rozszerzenia pliku,
2. uruchamia Blender w trybie bez interfejsu, jeżeli skrypt został uruchomiony zwykłym Pythonem,
3. importuje model do pustej sceny Blendera,
4. wykonuje inwentaryzację danych obecnych w scenie,
5. porównuje wykryte dane z macierzą możliwości formatu docelowego,
6. opcjonalnie stosuje transformacje obiektów,
7. opcjonalnie usuwa animacje,
8. przetwarza obrazy tekstur,
9. eksportuje scenę do żądanego formatu,
10. dla OBJ zapewnia plik `.mtl` i deklarację `mtllib`,
11. zapisuje raport JSON opisujący wejście, wynik, ustawienia, przetworzone tekstury, pliki towarzyszące i wykryte straty.

Skrypt znajduje się w:

```text
scripts/model_format_converter.py
```

## 2. Wymagania

### Python

Do uruchomienia wrappera wymagany jest Python zgodny z projektem, obecnie **Python 3.11**.

Sam proces konwersji nie wykorzystuje zewnętrznego modułu `bpy` instalowanego przez `pip`. Skrypt uruchamia właściwy interpreter dostarczany z Blenderem.

### Blender

Blender jest wymaganym silnikiem importu i eksportu. Skrypt próbuje znaleźć go w następującej kolejności:

1. ścieżka podana parametrem `--blender`,
2. zmienna środowiskowa `BLENDER_BIN`,
3. polecenie `blender` dostępne w `PATH`,
4. typowe katalogi instalacyjne Blendera w systemie Windows.

Jeżeli Blender nie zostanie znaleziony, konwersja jest przerywana z czytelnym komunikatem.

Zalecana jest aktualna wersja **Blender 4.5 LTS** lub wersja nowsza, dla której używane w skrypcie operatory importu i eksportu pozostają zgodne.

### Sprawdzenie instalacji

Linux / macOS:

```bash
blender --version
python --version
```

Windows PowerShell:

```powershell
& "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" --version
python --version
```

## 3. Najprostsze użycie

Ogólna składnia:

```bash
python scripts/model_format_converter.py INPUT OUTPUT [OPCJE]
```

Przykład konwersji FBX do GLB:

```bash
python scripts/model_format_converter.py exports/avatar_final.fbx exports/avatar_final.glb
```

Przykład konwersji kompletnej postaci do USDZ:

```bash
python scripts/model_format_converter.py avatar.fbx avatar.usdz \
  --textures embed \
  --animations keep
```

Przykład konwersji skanu PLY do GLB:

```bash
python scripts/model_format_converter.py scan.ply scan.glb
```

Przykład eksportu statycznego modelu OBJ wraz z MTL:

```bash
python scripts/model_format_converter.py avatar.glb avatar.obj
```

Po poprawnej konwersji powstaje również raport, np.:

```text
avatar.glb
avatar.glb.conversion.json
```

Dla OBJ typowy wynik ma postać:

```text
avatar.obj
avatar.mtl
avatar.obj.conversion.json
```

## 4. Pełna referencja interfejsu CLI

### `input`

Wymagany plik wejściowy. Format jest rozpoznawany na podstawie rozszerzenia.

Obsługiwane rozszerzenia:

```text
.fbx
.gltf
.glb
.usd
.usdz
.obj
.ply
.stl
```

### `output`

Wymagana ścieżka pliku wynikowego. Rozszerzenie określa format eksportu.

Przykład:

```bash
python scripts/model_format_converter.py model.fbx converted/model.glb
```

Katalog wyjściowy jest tworzony automatycznie, jeżeli jeszcze nie istnieje.

### `--textures {auto,embed,copy,skip}`

Steruje sposobem traktowania tekstur.

| Wartość | Znaczenie |
| --- | --- |
| `auto` | zachowuje tekstury i pozostawia naturalny sposób zapisu formatowi docelowemu |
| `embed` | przygotowuje obrazy do osadzenia / spakowania, jeżeli format i eksporter na to pozwalają |
| `copy` | zachowuje tekstury jako zależności zewnętrzne tam, gdzie format tego wymaga |
| `skip` | usuwa węzły obrazów tekstur z materiałów przed eksportem |

Przykład:

```bash
python scripts/model_format_converter.py avatar.fbx avatar.glb --textures embed
```

`skip` nie oznacza usunięcia samej geometrii ani materiałów. Usuwane są węzły obrazów tekstur. W formacie docelowym może więc pozostać materiał bez obrazów.

### `--texture-format {auto,png,jpeg}`

Pozwala przepisać obrazy tekstur do wybranego formatu przed eksportem.

```bash
python scripts/model_format_converter.py avatar.fbx avatar.glb \
  --texture-format png
```

`auto` nie wymusza zmiany typu pliku.

`png` jest bezpieczniejszym wyborem dla map technicznych i obrazów wymagających kanału alfa. `jpeg` może zmniejszyć rozmiar plików fotograficznych, ale kompresja stratna nie jest zalecana dla map normalnych, masek i innych map, w których niewielkie zmiany wartości pikseli mają znaczenie numeryczne.

Konwersja obrazu jest wykonywana tylko wtedy, gdy obraz ma prawidłową ścieżkę do istniejącego pliku i nie jest już spakowany wewnątrz danych Blendera.

### `--max-texture-size N`

Ogranicza większy wymiar obrazu do `N` pikseli z zachowaniem proporcji.

Przykład:

```bash
python scripts/model_format_converter.py avatar.fbx avatar_web.glb \
  --max-texture-size 2048
```

Dla tekstury 4096 × 2048 i wartości `2048` wynik będzie miał 2048 × 1024.

Minimalna dozwolona wartość wynosi **64 px**. Mniejsza wartość powoduje błąd i przerwanie konwersji.

### `--animations {auto,keep,strip}`

Steruje obecnością animacji.

| Wartość | Znaczenie |
| --- | --- |
| `auto` | zachowuje animacje, jeżeli eksporter formatu docelowego je obsługuje |
| `keep` | jawnie żąda zachowania animacji |
| `strip` | usuwa dane animacji przed eksportem |

Przykład świadomego utworzenia statycznego GLB:

```bash
python scripts/model_format_converter.py animated.fbx static.glb --animations strip
```

W trybie `strip` skrypt czyści `animation_data` obiektów i usuwa akcje z danych Blendera przed eksportem.

### `--apply-transforms`

Stosuje obrót i skalę obiektów przed eksportem. Lokalizacja nie jest aplikowana.

```bash
python scripts/model_format_converter.py bust.obj bust.stl --apply-transforms
```

Opcja jest przydatna przede wszystkim przy wymianie statycznej geometrii i przygotowaniu modeli do druku 3D. W przypadku zrigowanych postaci należy stosować ją świadomie, ponieważ aplikowanie transformacji może zmieniać relacje pomiędzy siatką, armaturą i aplikacją docelową.

### `--report PATH`

Pozwala wskazać własną lokalizację raportu JSON.

```bash
python scripts/model_format_converter.py model.fbx model.glb \
  --report reports/model_to_glb.json
```

Bez tej opcji raport ma nazwę:

```text
<output>.<rozszerzenie>.conversion.json
```

Dla `avatar.glb` będzie to:

```text
avatar.glb.conversion.json
```

### `--blender PATH`

Jawnie wskazuje plik wykonywalny Blendera.

Windows:

```powershell
python scripts/model_format_converter.py model.fbx model.glb `
  --blender "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
```

Linux:

```bash
python scripts/model_format_converter.py model.fbx model.glb \
  --blender /opt/blender/blender
```

### `--strict`

Włącza tryb bezpieczny. Jeżeli model wejściowy zawiera dane, których format docelowy według macierzy konwertera nie może reprezentować, operacja jest przerywana przed eksportem.

Przykład:

```bash
python scripts/model_format_converter.py animated_character.fbx character.obj --strict
```

Jeżeli FBX zawiera rig, skinning, shape keys lub animacje, konwersja do OBJ zostanie zablokowana.

Tryb `--strict` jest zalecany w procesach automatycznych, CI i przetwarzaniu wsadowym, gdzie ciche utworzenie niepełnego zasobu byłoby gorsze niż przerwanie zadania.

## 5. Architektura działania

### 5.1. Uruchomienie poza Blenderem

Jeżeli skrypt zostanie uruchomiony zwykłym Pythonem, import `bpy` nie jest dostępny. Wrapper wyszukuje wtedy Blender i ponownie uruchamia ten sam skrypt w trybie:

```bash
blender --background --python scripts/model_format_converter.py -- INPUT OUTPUT ...
```

Dzięki temu użytkownik korzysta z prostego polecenia `python ...`, natomiast właściwa konwersja odbywa się w środowisku Blendera.

### 5.2. Reset sceny

Przed importem bieżące obiekty sceny są usuwane. Każda konwersja działa więc na czystej scenie, co ogranicza ryzyko przypadkowego dołączenia obiektów z domyślnego pliku `.blend`.

### 5.3. Import

Skrypt dobiera operator Blendera na podstawie rozszerzenia:

| Format | Operator / rodzina operatorów |
| --- | --- |
| FBX | `import_scene.fbx` |
| glTF / GLB | `import_scene.gltf` |
| USD / USDZ | `wm.usd_import` |
| OBJ | `wm.obj_import`, z fallbackiem do starszego `import_scene.obj` |
| PLY | `wm.ply_import`, z fallbackiem do starszego `import_mesh.ply` |
| STL | `wm.stl_import`, z fallbackiem do starszego `import_mesh.stl` |

Fallbacki zwiększają zgodność z różnymi wersjami Blendera.

### 5.4. Inwentaryzacja sceny

Po imporcie skrypt zbiera następujące dane:

```text
objects
meshes
vertices
polygons
uv_layers
color_attributes
materials
textures
armatures
skinned_meshes
shape_keys
actions
```

Inwentaryzacja nie jest tylko statystyką. Na jej podstawie wykonywana jest analiza potencjalnych strat.

Przykład interpretacji:

```text
armatures > 0       -> scena zawiera szkielet
skinned_meshes > 0  -> wykryto siatkę związaną z armaturą lub grupami wierzchołków
shape_keys > 0      -> wykryto blendshapes / morph targets
actions > 0         -> wykryto akcje animacji
```

W przypadku shape keys blok `Basis` nie jest liczony jako właściwy morph target.

### 5.5. Analiza strat

Konwerter posiada wewnętrzną macierz `FORMAT_CAPABILITIES`. Dla każdej wykrytej cechy porównuje jej obecność z możliwościami formatu docelowego.

Jeżeli np. źródłowy FBX zawiera:

```text
geometrię
UV
materiały
tekstury
szkielet
skinning
52 shape keys
3 akcje animacji
```

oraz zostanie wybrany OBJ, raport strat powinien zawierać co najmniej:

```text
szkielet
wagi kości
blendshapes / shape keys
animacje
```

Jeżeli wybrano `--textures skip`, tekstury są również raportowane jako świadomie usunięte.

Jeżeli wybrano `--animations strip`, analogicznie raportowane jest świadome usunięcie animacji.

### 5.6. Eksport

Eksporter dobierany jest na podstawie rozszerzenia docelowego. Dla formatów, które pozwalają na przenoszenie animowanej postaci, skrypt aktywuje odpowiednie opcje eksportu skinningu, morph targets i animacji.

## 6. Macierz możliwości formatów

Poniższa tabela przedstawia **model możliwości używany przez konwerter**. Nie jest to gwarancja, że każdy program docelowy odtworzy wszystkie dane identycznie.

| Dane | FBX | glTF | GLB | USD | USDZ | OBJ + MTL | PLY | STL |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Geometria | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Mapy UV | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| Materiały | ✓ | ✓ | ✓ | ✓ | ✓ | ✓* | ✗ | ✗ |
| Tekstury | ✓ | ✓ | ✓ | ✓ | ✓ | ✓* | ✗ | ✗ |
| Szkielet | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| Skinning / wagi kości | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| Blendshapes / morph targets | ✓ | ✓ | ✓ | ✓** | ✓** | ✗ | ✗ | ✗ |
| Animacje | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |

`*` OBJ korzysta z osobnego pliku MTL i zewnętrznych tekstur. Materiał jest znacznie prostszy niż pełny graf shaderów Blendera lub nowoczesny materiał PBR.

`**` Blender potrafi eksportować shape keys jako USD blend shapes, ale wsparcie zależy od rodzaju shape keys oraz implementacji importera w aplikacji docelowej.

## 7. Charakterystyka formatów i wybór właściwego celu

### 7.1. GLB

GLB jest binarnym kontenerem glTF. Jest dobrym wyborem dla kompletnego zasobu publikowanego w sieci, viewerze Three.js albo aplikacji obsługującej glTF. Geometria, bufory, materiały, tekstury, skóra szkieletowa, morph targets i animacje mogą znajdować się w jednym pliku.

Wybierz GLB, gdy priorytetem jest:

- jeden przenośny plik,
- publikacja w WWW,
- zachowanie materiałów PBR,
- przeniesienie animowanego modelu bez pakietu dodatkowych plików.

### 7.2. glTF

glTF opisuje ten sam typ nowoczesnego assetu co GLB, ale w wariancie `GLTF_SEPARATE` używanym przez skrypt dane są rozdzielane na plik `.gltf`, bufory binarne oraz obrazy.

Wybierz glTF, gdy priorytetem jest:

- możliwość ręcznego podmieniania tekstur,
- łatwa inspekcja struktury JSON,
- jawne rozdzielenie zasobu na komponenty.

### 7.3. FBX

FBX pozostaje praktycznym formatem wymiany animowanych postaci pomiędzy aplikacjami DCC oraz silnikami czasu rzeczywistego. Może przenosić geometrię, UV, armaturę, skinning, shape keys / morph targets i animacje.

Największym ryzykiem nie jest zwykle utrata samej geometrii, lecz różnice w:

- orientacji osi,
- skali,
- strukturze kości,
- interpretacji animacji,
- materiale i przypisaniu tekstur.

Po konwersji FBX należy zawsze sprawdzić zasób w docelowej wersji Unity, Unreal Engine lub innego programu.

### 7.4. USD

USD jest formatem opisu sceny, a nie tylko pojedynczej siatki. Nadaje się do wymiany bardziej złożonych assetów i scen, w których istotne są hierarchie, transformacje, materiały, animacja i dalsze przetwarzanie w pipeline DCC.

Blender 4.5 eksportuje m.in. siatki, armatury i deformujące się siatki oraz obsługuje animację. Należy jednak pamiętać, że importer i eksporter Blendera obsługują podzbiór całego ekosystemu USD. Zaawansowane mechanizmy kompozycji USD, warstwy, warianty i referencje nie są równoważne pełnej implementacji produkcyjnego systemu USD.

Wybierz USD, gdy zasób ma być częścią większego pipeline scenowego.

### 7.5. USDZ

USDZ jest pakietem USD przeznaczonym do przenoszenia sceny i jej zależności jako jednego pliku. Blender tworzy pakiet USDZ po wybraniu rozszerzenia `.usdz`; zależności teksturowe mogą zostać dołączone do archiwum.

USDZ jest dobrym wyborem, gdy potrzebny jest pojedynczy pakiet USD, szczególnie do dystrybucji i zastosowań korzystających z ekosystemu Apple / AR.

Istotne ograniczenie Blendera 4.5: pakowanie tekstur UDIM do USDZ ma ograniczenia wynikające z biblioteki USD. Dla assetów korzystających z UDIM konieczna jest osobna walidacja.

### 7.6. OBJ + MTL

OBJ jest formatem statycznej geometrii. Przechowuje pozycje wierzchołków, normalne, UV i przypisanie materiałów. Sam OBJ nie jest kompletnym kontenerem materiałowym. Biblioteka materiałów jest zapisywana w osobnym pliku `.mtl`.

Konwerter **zawsze** zapewnia obecność pliku MTL po eksporcie OBJ. Jeżeli eksporter Blendera nie utworzy MTL, skrypt generuje minimalny plik z materiałami i dodaje do OBJ odpowiednią deklarację:

```text
mtllib avatar.mtl
```

Typowy zestaw:

```text
avatar.obj
avatar.mtl
skin_basecolor.png
skin_normal.png
```

OBJ nie obsługuje armatury, skinningu, blendshapes ani animacji. Jest więc właściwy dla statycznej siatki, ale nie jako format archiwalny pełnej cyfrowej postaci.

Współczesny eksporter OBJ Blendera może zapisywać rozszerzenia PBR w MTL, jednak ich interpretacja nie jest jednakowa we wszystkich importerach OBJ. Dla maksymalnej interoperacyjności należy traktować MTL jako materiał uproszczony.

### 7.7. PLY

PLY jest szczególnie przydatny dla danych pochodzących ze skanowania 3D i fotogrametrii. Blender może eksportować aktywne UV, normalne i kolory wierzchołków. W tym konwerterze PLY jest traktowany jako format **statycznej geometrii / skanu**.

PLY nie jest traktowany jako format przenoszący:

- materiały PBR,
- pliki tekstur,
- armaturę,
- skinning,
- shape keys,
- animacje.

Przy eksporcie skrypt próbuje włączyć:

```text
UV
normals
vertex colors w sRGB
```

Wybierz PLY, gdy istotna jest geometria skanu i ewentualne dane per-vertex, a nie pełna animowana postać.

### 7.8. STL

STL przechowuje przede wszystkim powierzchnię trójkątową. W kontekście tego projektu jest formatem docelowym dla druku 3D lub prostego przekazania kształtu.

Konwersja do STL traci:

- UV,
- materiały,
- tekstury,
- rig,
- skinning,
- shape keys,
- animacje.

Jeżeli model ma być używany ponownie w pipeline cyfrowej postaci, STL nie powinien być formatem archiwalnym.

## 8. Tekstury i materiały

### 8.1. Inwentaryzacja obrazów

Konwerter identyfikuje obrazy używane przez węzły `TEX_IMAGE` w materiałach przypisanych do obiektów typu `MESH`.

Raport zawiera liczbę wykrytych tekstur oraz informacje o każdym przetworzonym obrazie:

```json
{
  "name": "skin_basecolor",
  "before": [4096, 4096],
  "after": [2048, 2048],
  "filepath": ".../skin_basecolor.png"
}
```

### 8.2. Skalowanie

Skalowanie zmienia rozmiar obrazu w pamięci Blendera przed eksportem. Proporcje są zachowane.

Zalecane wartości zależą od przeznaczenia:

| Zastosowanie | Typowy limit |
| --- | ---: |
| lekki podgląd WWW | 1024–2048 px |
| wysokiej jakości viewer | 2048–4096 px |
| materiał produkcyjny offline | bez wymuszania limitu lub zgodnie z pipeline |

Nie należy bezrefleksyjnie zmniejszać map normalnych i masek, jeżeli model będzie oglądany z bardzo małej odległości.

### 8.3. PNG kontra JPEG

PNG jest formatem bezstratnym i nadaje się do:

- normal map,
- roughness,
- metallic,
- AO,
- masek,
- obrazów z kanałem alfa.

JPEG ma sens głównie dla danych fotograficznych bez kanału alfa, np. niektórych map Base Color. Nie należy używać JPEG do map, których wartość piksela jest parametrem materiału.

### 8.4. Materiały nie są gwarantowanie identyczne

Konwersja obrazu tekstury nie jest tym samym co konwersja całego materiału. Blender, glTF, FBX, USD i MTL mają różne modele materiałowe. Nawet jeżeli pliki tekstur zostaną zachowane, po imporcie należy sprawdzić co najmniej:

- Base Color,
- Normal,
- Roughness / Smoothness,
- Metallic,
- AO,
- Alpha / Opacity,
- kierunek kanału Y mapy normalnej, jeżeli aplikacja docelowa tego wymaga.

## 9. Rig, skinning, blendshapes i animacja

### 9.1. Armatura

Konwerter wykrywa obiekty typu `ARMATURE`. Sama obecność armatury nie oznacza jeszcze, że każda siatka jest prawidłowo zrigowana.

### 9.2. Skinning

Siatka jest traktowana jako skinned, jeżeli ma modyfikator `ARMATURE` albo grupy wierzchołków. Jest to praktyczny heurystyczny test używany do raportu, a nie pełny audyt jakości wag kości.

### 9.3. Blendshapes / shape keys

Skrypt liczy shape keys z pominięciem `Basis`. Dla postaci twarzowych liczba może odpowiadać zestawowi ekspresji, visemes albo standardowi ARKit, ale konwerter nie interpretuje znaczenia nazw. Sprawdza jedynie obecność i możliwość reprezentacji w formacie docelowym.

### 9.4. Animacje

Liczba animacji w raporcie odpowiada liczbie `bpy.data.actions` po imporcie. Jest to wskaźnik obecności danych animacyjnych, a nie gwarancja, że wszystkie NLA tracks, constraints i niestandardowe zależności zostaną identycznie odtworzone po eksporcie.

Po konwersji animowanej postaci należy sprawdzić:

1. pozycję w klatce zerowej,
2. bind pose,
3. deformację barków, szyi i twarzy,
4. nazwy i hierarchię kości,
5. zakres klatek,
6. wszystkie eksportowane klipy,
7. shape keys / morph targets,
8. lip sync i mruganie, jeżeli występują.

## 10. Raport konwersji

Raport jest obowiązkowym artefaktem każdej udanej konwersji.

Przykładowa struktura:

```json
{
  "input": "/data/avatar.fbx",
  "output": "/data/avatar.obj",
  "input_format": ".fbx",
  "output_format": ".obj",
  "scene": {
    "objects": 6,
    "meshes": 4,
    "vertices": 82314,
    "polygons": 80102,
    "uv_layers": 4,
    "color_attributes": 0,
    "materials": 7,
    "textures": 12,
    "armatures": 1,
    "skinned_meshes": 4,
    "shape_keys": 52,
    "actions": 3
  },
  "output_capabilities": {
    "geometry": true,
    "uv": true,
    "materials": true,
    "textures": true,
    "armature": false,
    "skinning": false,
    "shape_keys": false,
    "animation": false
  },
  "requested": {
    "textures": "auto",
    "texture_format": "auto",
    "max_texture_size": null,
    "animations": "auto",
    "apply_transforms": false
  },
  "processed_textures": [],
  "companion_files": [
    "/data/avatar.mtl"
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

### Interpretacja pól

`scene` opisuje dane wykryte **po imporcie do Blendera i przed celowym usuwaniem animacji lub tekstur**.

`output_capabilities` pokazuje macierz możliwości używaną przez konwerter dla wybranego rozszerzenia docelowego.

`requested` zapisuje parametry przekazane przez użytkownika.

`processed_textures` dokumentuje operacje na obrazach.

`companion_files` zawiera pliki towarzyszące wygenerowane poza głównym plikiem docelowym. Obecnie szczególnie istotny jest plik MTL dla OBJ.

`losses` opisuje wykryte dane, które nie są reprezentowane przez format docelowy lub zostały świadomie usunięte opcją CLI.

`lossless_for_detected_features: true` oznacza wyłącznie, że według macierzy konwertera nie wykryto oczywistej utraty typów danych. Nie oznacza numerycznej ani wizualnej identyczności assetu.

## 11. Zalecane scenariusze użycia

### Kompletna animowana postać do WWW

```bash
python scripts/model_format_converter.py avatar.fbx avatar.glb \
  --textures embed \
  --animations keep \
  --max-texture-size 2048
```

Po konwersji sprawdź materiały, morph targets i wszystkie klipy w viewerze glTF.

### Kompletna postać do pipeline USD

```bash
python scripts/model_format_converter.py avatar.fbx avatar.usd \
  --animations keep
```

Sprawdź rig i materiał w aplikacji korzystającej z USD. Nie zakładaj, że wszystkie niestandardowe węzły materiału Blendera zostały odtworzone.

### Pojedynczy pakiet USDZ

```bash
python scripts/model_format_converter.py avatar.glb avatar.usdz \
  --textures embed \
  --animations keep
```

Zweryfikuj obecność tekstur w docelowym viewerze USDZ.

### Statyczny OBJ z MTL

```bash
python scripts/model_format_converter.py avatar.glb avatar.obj
```

Wynik powinien zawierać `avatar.obj`, `avatar.mtl` oraz raport. Jeżeli źródło było animowane, raport poinformuje o utracie rigu, skinningu, shape keys i animacji.

### Skan PLY do GLB

```bash
python scripts/model_format_converter.py scan.ply scan.glb
```

GLB nie odzyska materiałów, tekstur, rigu ani animacji, których nie było w PLY. Konwersja zmienia kontener danych, ale nie rekonstruuje brakujących cech.

### Model do druku 3D

```bash
python scripts/model_format_converter.py bust.obj bust.stl --apply-transforms
```

Przed drukiem należy dodatkowo sprawdzić szczelność siatki, skalę fizyczną, normalne i brak samoprzecięć. Konwerter formatów nie wykonuje automatycznej naprawy siatki do druku.

## 12. Procedura walidacji po konwersji

Dla zasobu produkcyjnego rekomendowana jest walidacja w czterech warstwach.

### Geometria

Sprawdź:

- liczbę obiektów,
- proporcje i skalę,
- orientację osi,
- położenie modelu względem początku układu,
- normalne,
- topologię i brak nieoczekiwanej triangulacji,
- UV.

### Materiały

Sprawdź:

- przypisanie materiałów do właściwych siatek,
- obecność wszystkich tekstur,
- Base Color,
- Normal,
- Roughness / Smoothness,
- Metallic,
- Alpha,
- zachowanie materiału pod kilkoma kierunkami oświetlenia.

### Animacja

Sprawdź:

- hierarchię kości,
- orientację kości,
- bind pose,
- wagi wierzchołków,
- zakres klatek,
- wszystkie klipy,
- shape keys / morph targets,
- brak przesunięcia skali lub osi po imporcie.

### Artefakty plikowe

Sprawdź:

- istnienie głównego pliku wyjściowego,
- raport `.conversion.json`,
- `companion_files`,
- dla OBJ obecność `.mtl`,
- dla glTF osobne bufory i tekstury,
- dla USDZ możliwość otwarcia pakietu bez brakujących zależności.

## 13. Typowe problemy

### „Nie znaleziono Blendera”

Użyj:

```bash
python scripts/model_format_converter.py model.fbx model.glb \
  --blender /pełna/ścieżka/do/blender
```

albo ustaw:

```bash
export BLENDER_BIN=/pełna/ścieżka/do/blender
```

PowerShell:

```powershell
$env:BLENDER_BIN = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
```

### Format nieobsługiwany

Skrypt akceptuje tylko rozszerzenia wymienione w `SUPPORTED`. Zmiana nazwy pliku nie konwertuje jego zawartości. Plik musi rzeczywiście być zapisany w poprawnym formacie odpowiadającym rozszerzeniu.

### `--strict` przerywa eksport

To zachowanie jest zamierzone. Odczytaj listę `losses` w komunikacie i wybierz format bogatszy, np. GLB, glTF, FBX lub USD/USDZ, albo świadomie usuń niepotrzebne dane.

### Po eksporcie OBJ brakuje animacji

To nie jest błąd konwertera. OBJ nie obsługuje animacji, armatury ani skinningu. Użyj GLB, glTF, FBX, USD albo USDZ.

### Materiał po konwersji wygląda inaczej

Najczęstsza przyczyna to różnica modeli shaderów pomiędzy formatami lub aplikacjami. Sprawdź mapowanie kanałów, Roughness / Smoothness, mapę normalną, przestrzeń kolorów i kanał alfa.

### Tekstura JPEG wygląda gorzej

JPEG jest kompresją stratną. Dla map normalnych, masek, roughness i innych map technicznych użyj PNG.

### USDZ nie zawiera oczekiwanej tekstury

Zweryfikuj, czy obraz jest prawidłowo przypisany do materiału, ma poprawną ścieżkę oraz czy nie korzysta z nieobsługiwanego wariantu, np. problematycznego pakowania UDIM. Otwórz USDZ w niezależnym viewerze, aby odróżnić problem eksportu od problemu importera aplikacji docelowej.

## 14. Ograniczenia konwertera

Konwerter nie wykonuje automatycznie:

- retopologii,
- naprawy niepoprawnej siatki,
- generowania UV,
- rekonstrukcji brakujących materiałów,
- bake materiałów proceduralnych do PBR,
- konwersji wszystkich niestandardowych shaderów Blendera,
- retargetingu szkieletu,
- zmiany standardu nazewnictwa kości,
- generowania nowych blendshapes,
- naprawy błędnych wag skinningu,
- optymalizacji liczby polygonów,
- pełnego audytu poprawności animacji,
- automatycznej naprawy modelu do druku 3D.

Jego zadaniem jest **kontrolowana konwersja istniejącego assetu i jawne raportowanie potencjalnej utraty klas danych**.

## 15. Ważne zastrzeżenia dotyczące macierzy „lossless”

Macierz konwertera działa na poziomie kategorii danych. Przykładowo `materials: true` oznacza, że format docelowy posiada mechanizm reprezentacji materiałów, a nie że dowolny node graph Blendera zostanie przeniesiony 1:1.

Analogicznie:

- `animation: true` nie gwarantuje identycznego zachowania constraints i sterowników,
- `shape_keys: true` nie gwarantuje obsługi każdego wariantu morph targets przez każdą aplikację,
- `textures: true` nie gwarantuje identycznej interpretacji przestrzeni kolorów,
- `armature: true` nie gwarantuje identycznych osi kości i retargetingu,
- `uv: true` nie gwarantuje zachowania wielu zestawów UV w każdym importerze.

Dlatego `lossless_for_detected_features` należy interpretować jako **brak oczywistej straty kategorii danych**, a nie dowód bitowej lub wizualnej równoważności plików.

## 16. Testowanie i rozwój

Logika niezależna od Blendera jest objęta testami w:

```text
tests/test_model_format_converter.py
```

Testy sprawdzają m.in.:

- obsługiwane rozszerzenia,
- macierz możliwości formatów,
- wykrywanie strat dla OBJ, PLY i STL,
- zachowanie bogatych formatów,
- raportowanie świadomego usuwania tekstur i animacji,
- generowanie MTL dla OBJ.

Uruchomienie testów:

```bash
python -m pytest tests/test_model_format_converter.py
```

Do pełnego testu integracyjnego potrzebny jest Blender oraz zestaw kontrolnych plików zawierających geometrię, materiały, tekstury, rig, morph targets i animacje.

## 17. Rekomendowany zestaw testów integracyjnych

Dla rozwoju konwertera warto utrzymywać mały zestaw referencyjnych assetów:

| Asset | Zawartość | Cel |
| --- | --- | --- |
| `static_mesh` | geometria + UV | podstawowa konwersja |
| `pbr_mesh` | geometria + UV + materiał + tekstury | walidacja materiałów |
| `rigged_character` | mesh + armature + skinning | walidacja rigu |
| `morph_character` | rig + shape keys | walidacja blendshapes |
| `animated_character` | rig + kilka actions | walidacja animacji |
| `scan_vertex_color` | PLY + vertex colors | walidacja danych skanera |

Dla każdego assetu należy wykonywać konwersję do wszystkich sensownych formatów i porównywać raport z oczekiwanym zestawem strat.

## 18. Referencje techniczne

Dokumentacja konwertera opisuje zachowanie implementacji projektu. Szczegółowe możliwości operatorów importu i eksportu wynikają z Blendera.

Oficjalne źródła:

- Blender 4.5 LTS, Universal Scene Description: https://docs.blender.org/manual/en/4.5/files/import_export/usd.html
- Blender 4.5 LTS, Wavefront OBJ: https://docs.blender.org/manual/en/4.5/files/import_export/obj.html
- Blender 4.5 LTS, Stanford PLY: https://docs.blender.org/manual/en/4.5/files/import_export/ply.html
- Blender 4.5 LTS, FBX: https://docs.blender.org/manual/en/4.5/files/import_export/fbx.html
- Khronos glTF: https://www.khronos.org/gltf/
- OpenUSD: https://openusd.org/

## 19. Powiązane pliki

- implementacja: [`../scripts/model_format_converter.py`](../scripts/model_format_converter.py)
- praktyczne przykłady: [`FORMAT_CONVERSION_EXAMPLES.md`](FORMAT_CONVERSION_EXAMPLES.md)
- testy: [`../tests/test_model_format_converter.py`](../tests/test_model_format_converter.py)
- dokumentacja integracji z silnikami: [`ENGINE_INTEGRATION.md`](ENGINE_INTEGRATION.md)
