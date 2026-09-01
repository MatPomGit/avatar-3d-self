# Praktyczne scenariusze konwersji

Ten dokument uzupełnia [`model_format_converter.md`](model_format_converter.md). Każdy scenariusz opisuje nie tylko polecenie, ale również oczekiwany zakres danych, typowe ryzyko oraz minimalną walidację po eksporcie.

## 1. FBX → GLB: kompletna postać do viewera WWW

```bash
python scripts/model_format_converter.py avatar.fbx avatar.glb \
  --textures embed \
  --animations keep
```

Oczekiwane do zachowania:

- geometria,
- UV,
- materiały PBR w zakresie możliwym do odwzorowania w glTF,
- tekstury,
- armatura,
- skinning,
- morph targets / shape keys,
- animacje.

GLB jest preferowany, gdy kompletny asset ma być jednym plikiem, np. dla Three.js albo innego viewera glTF.

Po konwersji sprawdź liczbę morph targets, animacji, poprawność orientacji modelu i wygląd materiału pod neutralnym oświetleniem.

## 2. FBX → GLB: wersja zoptymalizowana do WWW

```bash
python scripts/model_format_converter.py avatar.fbx avatar_web.glb \
  --textures embed \
  --max-texture-size 2048 \
  --animations keep
```

Ta wersja ogranicza największy wymiar tekstur do 2048 px. Jest rozsądnym wariantem dla podglądu WWW, jeżeli materiał źródłowy korzystał z map 4K lub 8K.

Nie dodawaj `--texture-format jpeg` globalnie, jeżeli asset zawiera normal map, roughness, metallic, AO albo maski. Dla tych map bezpieczniejszy jest PNG.

Walidacja: porównaj zbliżenie twarzy z wersją źródłową i sprawdź, czy redukcja tekstur nie usunęła istotnych detali skóry.

## 3. FBX → USD: asset do pipeline scenowego

```bash
python scripts/model_format_converter.py avatar.fbx avatar.usd \
  --textures copy \
  --animations keep
```

USD jest właściwy, gdy postać ma być częścią większej sceny lub pipeline DCC. Konwerter traktuje USD jako format bogaty, ale rzeczywista zgodność zależy od podzbioru USD obsługiwanego przez Blender i aplikację docelową.

Walidacja powinna objąć armaturę, skinned mesh, shape keys, materiały i zakres animacji. Dla krytycznych zasobów należy otworzyć plik również w niezależnym narzędziu obsługującym USD.

## 4. FBX → USDZ: pojedynczy pakiet USD

```bash
python scripts/model_format_converter.py avatar.fbx avatar.usdz \
  --textures embed \
  --animations keep
```

USDZ jest właściwy, gdy scena USD i zależności mają zostać przekazane jako jeden pakiet. Po eksporcie należy sprawdzić nie tylko samą geometrię, ale również obecność tekstur wewnątrz pakietu.

Dla materiałów korzystających z UDIM wykonaj osobny test zgodności, ponieważ obsługa pakowania UDIM do USDZ ma ograniczenia po stronie biblioteki USD używanej przez Blender.

## 5. GLB → glTF: rozdzielenie assetu na komponenty

```bash
python scripts/model_format_converter.py avatar.glb avatar.gltf --textures copy
```

Wynik jest wygodniejszy do inspekcji i ręcznego zarządzania teksturami. Zamiast jednego kontenera otrzymujesz plik opisowy glTF oraz powiązane bufory i obrazy.

Walidacja: przenieś cały zestaw plików do pustego katalogu i sprawdź, czy model nadal otwiera się bez brakujących zależności.

## 6. GLB → FBX: przejście do klasycznego pipeline DCC

```bash
python scripts/model_format_converter.py avatar.glb avatar.fbx --animations keep
```

Geometria, skinning, morph targets i animacje mogą zostać przeniesione, ale materiał glTF nie musi zostać odtworzony 1:1 jako materiał FBX.

Walidacja: sprawdź skalę, osie, hierarchię kości, bind pose, animacje i każdą mapę PBR w aplikacji docelowej.

## 7. USDZ → GLB: asset USD do nowoczesnego viewera

```bash
python scripts/model_format_converter.py avatar.usdz avatar.glb \
  --textures embed \
  --animations keep
```

Scena USDZ jest importowana do Blendera, a następnie eksportowana jako GLB. Konwersja jest przydatna do publikacji w WWW, ale może uprościć elementy sceny USD, które nie mają bezpośredniego odpowiednika w glTF.

Raport `losses` wykrywa straty na poziomie kategorii danych. Nie wykryje wszystkich różnic semantycznych pomiędzy systemem USD a glTF.

## 8. PLY → GLB: skan do dalszego opracowania

```bash
python scripts/model_format_converter.py scan.ply scan.glb
```

PLY może zawierać statyczną geometrię, UV, normalne i kolory wierzchołków. Konwersja do GLB daje wygodniejszy kontener do wizualizacji i dalszej pracy, ale nie tworzy automatycznie materiałów, tekstur, rigu ani animacji.

Walidacja: sprawdź położenie skanu, skalę, normalne oraz kolory wierzchołków, jeżeli były obecne w źródle.

## 9. GLB → PLY: statyczny eksport geometrii

```bash
python scripts/model_format_converter.py avatar.glb avatar.ply
```

Oczekiwane straty dla typowej animowanej postaci:

```text
materiały
tekstury
szkielet
wagi kości
blendshapes / shape keys
animacje
```

PLY ma sens jako format pośredni do analizy geometrii, skanowania, obliczeń naukowych albo narzędzi pracujących na siatce i atrybutach wierzchołków.

Jeżeli nie chcesz dopuścić do takiej redukcji danych:

```bash
python scripts/model_format_converter.py avatar.glb avatar.ply --strict
```

## 10. GLB → OBJ + MTL: statyczna geometria z materiałem

```bash
python scripts/model_format_converter.py avatar.glb avatar.obj --textures copy
```

Konwerter zapewnia:

```text
avatar.obj
avatar.mtl
avatar.obj.conversion.json
```

OBJ zachowuje geometrię i UV. MTL opisuje materiały i może wskazywać tekstury. Rig, skinning, shape keys i animacje są tracone.

Sprawdź, czy pierwsza część OBJ zawiera deklarację:

```text
mtllib avatar.mtl
```

Następnie otwórz model w niezależnym importerze OBJ i sprawdź, czy materiał został przypisany do właściwych części siatki.

## 11. FBX → OBJ + MTL w trybie bezpiecznym

```bash
python scripts/model_format_converter.py avatar.fbx avatar.obj --strict
```

Dla animowanej postaci to polecenie powinno zakończyć się błędem przed eksportem, ponieważ OBJ nie może przechować armatury, skinningu, shape keys i animacji.

To jest oczekiwane zachowanie i przykład właściwego użycia `--strict`.

## 12. OBJ → STL: przygotowanie samej geometrii

```bash
python scripts/model_format_converter.py bust.obj bust.stl --apply-transforms
```

STL zachowuje kształt powierzchni, ale nie UV, materiały ani tekstury. Opcja `--apply-transforms` aplikuje obrót i skalę przed eksportem.

Przed drukiem 3D wykonaj dodatkowo kontrolę manifold, jednostek, grubości ścian i samoprzecięć. Konwerter nie naprawia geometrii do druku.

## 13. STL → GLB: zmiana kontenera bez rekonstrukcji danych

```bash
python scripts/model_format_converter.py scan.stl scan.glb
```

GLB jest bogatszym formatem, ale konwersja nie rekonstruuje danych, których nie było w STL. Wynik nadal będzie zasadniczo statyczną geometrią bez UV, tekstur, rigu i animacji.

To ważna zasada: **konwersja do bogatszego formatu nie tworzy brakujących danych**.

## 14. Świadome usunięcie animacji

```bash
python scripts/model_format_converter.py animated.fbx static.glb \
  --animations strip
```

Skrypt usuwa dane animacji przed eksportem. Raport powinien zawierać informację, że animacje zostały usunięte na żądanie użytkownika.

Używaj tego wariantu, jeżeli potrzebujesz statycznej wersji postaci, ale chcesz zachować rig i morph targets.

## 15. Świadome usunięcie tekstur

```bash
python scripts/model_format_converter.py avatar.fbx geometry_only.glb \
  --textures skip
```

Węzły obrazów tekstur zostaną usunięte przed eksportem. Materiały mogą pozostać, ale bez powiązanych obrazów. Raport oznaczy tekstury jako świadomie utracone.

## 16. Własna lokalizacja raportu

```bash
python scripts/model_format_converter.py avatar.fbx avatar.glb \
  --report reports/avatar_fbx_to_glb.json
```

To rozwiązanie jest przydatne w automatyzacji, gdy raporty mają być archiwizowane oddzielnie od plików wynikowych.

## 17. Wskazanie konkretnej instalacji Blendera

Windows PowerShell:

```powershell
python scripts/model_format_converter.py avatar.fbx avatar.glb `
  --blender "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
```

Linux:

```bash
python scripts/model_format_converter.py avatar.fbx avatar.glb \
  --blender /opt/blender/blender
```

## 18. Minimalny zestaw kontroli po każdej konwersji

Po każdej konwersji produkcyjnej:

1. sprawdź, czy główny plik wynikowy istnieje i otwiera się w aplikacji docelowej,
2. przeczytaj `*.conversion.json`, szczególnie `losses`,
3. sprawdź `companion_files`,
4. porównaj skalę i orientację modelu,
5. sprawdź UV i normalne,
6. sprawdź przypisanie materiałów i tekstur,
7. dla postaci zrigowanej sprawdź bind pose i deformację,
8. dla twarzy sprawdź morph targets / blendshapes,
9. odtwórz wszystkie wymagane klipy animacji,
10. wykonaj wizualne porównanie ze źródłem.

Pełna referencja działania i ograniczeń znajduje się w [`model_format_converter.md`](model_format_converter.md).
