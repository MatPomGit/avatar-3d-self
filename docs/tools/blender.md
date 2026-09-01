# Blender

Blender jest kanonicznym środowiskiem tworzenia treści cyfrowych (Digital Content Creation, DCC) projektu Avatar Studio. Oznacza to, że wersja wzorcowa geometrii, rigów, kształtów deformacyjnych, materiałów i animacji powinna pozostawać edytowalna w plikach `.blend`, nawet jeśli później powstaną artefakty FBX, GLB lub USD dla środowisk czasu rzeczywistego.

## Dlaczego wersja Blendera jest częścią artefaktu

Wersja programu wpływa na zachowanie importerów, eksporterów, modyfikatorów, węzłów materiałowych i interfejsu Python API. Ta sama scena zapisana i przetworzona w innej wersji może dać inny wynik eksportu. Dlatego raport każdego zatwierdzonego artefaktu zapisuje co najmniej:

- pełną wersję Blendera;
- system operacyjny;
- nazwę pliku `.blend` i jego SHA-256;
- wersję skryptu automatyzującego;
- użyty profil eksportu;
- ostrzeżenia i błędy ze standardowego wyjścia i standardowego wyjścia błędów.

Nie przyjmujemy zasady „zawsze najnowszy Blender”. Dla etapu produkcyjnego przypinamy wersję, a aktualizację wykonujemy świadomie po testach regresyjnych.

## Jednostki i skala

**Skala sceny (scene scale)** określa związek jednostek używanych przez Blender z rzeczywistymi wymiarami modelu. W Avatar Studio wartości geometryczne muszą odpowiadać rzeczywistym wymiarom człowieka, ponieważ błędna skala wpływa na rig, fizykę, rozpraszanie podpowierzchniowe (Subsurface Scattering, SSS), ruch wtórny i eksport do silników.

Praktyczna zasada:

- geometrię wzorcową utrzymuj w rzeczywistej skali;
- pomiary antropometryczne zapisuj w milimetrach lub centymetrach w dokumentacji;
- przed eksportem nie „naprawiaj” skali arbitralnym mnożnikiem;
- transformacja skali obiektu powinna być świadomie zatwierdzona przed skinningiem i eksportem.

Objawy złej skali to m.in. nieprawidłowa amplituda ruchu wtórnego, błędne promienie SSS, zbyt duże lub zbyt małe przesunięcia żuchwy oraz niewłaściwy rozmiar po imporcie do Unreal Engine lub Unity.

## Układ osi

**Układ współrzędnych (coordinate system)** definiuje kierunek osi X, Y i Z oraz to, która oś jest uznawana za pion i przód postaci. Blender i silniki czasu rzeczywistego mogą stosować inne konwencje, dlatego konwersja osi należy do profilu eksportu, a nie do ręcznego obracania wersji wzorcowej przed każdym eksportem.

Wymagania:

1. postać ma jeden kanoniczny kierunek przodu w scenie wzorcowej;
2. root i szkielet używają spójnego układu osi;
3. konwersję osi wykonuje eksporter lub adapter;
4. import testowy potwierdza, że postać nie jest obrócona, odbita ani pochylona.

## Transformacje

Przed rozpoczęciem wiązania skóry z kośćmi (skinning) sprawdź translację, obrót i skalę obiektów. Zastosowanie transformacji po utworzeniu rigu może zmienić zachowanie deformacji i macierze kości.

Nie stosuj automatycznie `Ctrl+A > All Transforms` na gotowym, zatwierdzonym rigu. Taka operacja jest dopuszczalna tylko wtedy, gdy wiadomo, które elementy są zależne od transformacji i wykonano test regresyjny.

## Nazewnictwo obiektów

Nazwy powinny być stabilne i możliwe do automatycznego przetwarzania. Zalecane grupy:

```text
GEO_body
GEO_eyes
GEO_teeth_upper
GEO_teeth_lower
GEO_tongue
GEO_glasses
GROOM_hair
GROOM_beard
RIG_body
RIG_face
```

Nie wpisuj do nazw obiektów numerów wersji takich jak `final2`, `new`, `fixed_final`. Wersję przechowuje system wersjonowania artefaktów, a nie nazwa obiektu.

## Modyfikatory

Modyfikatory mogą zmieniać geometrię proceduralnie. Przed eksportem należy rozstrzygnąć, które z nich pozostają edytowalne w wersji wzorcowej, a które muszą zostać zastosowane w artefakcie pochodnym.

Szczególnie kontroluj:

- Mirror;
- Subdivision Surface;
- Shrinkwrap;
- Surface Deform;
- Corrective Smooth;
- Armature;
- Geometry Nodes.

Nie stosuj modyfikatora tylko dlatego, że eksport go nie obsługuje. Najpierw utwórz kopię pochodną przeznaczoną do eksportu.

## Tryb bez interfejsu

**Tryb bez interfejsu (background mode)** uruchamia Blender bez okna graficznego. Jest używany do powtarzalnych walidacji, konwersji i eksportów. Nie zmniejsza wymagań jakościowych, ale pozwala uruchamiać te same operacje w sposób deterministyczny.

Przykład:

```text
blender scene.blend --background --python scripts/validate_scene.py
```

Kolejność argumentów ma znaczenie. Plik `.blend` powinien zostać wczytany przed wykonaniem skryptu, jeżeli skrypt ma pracować na tej scenie.

## Automatyczne wykonywanie skryptów

Pliki `.blend` mogą zawierać sterowniki i skrypty Python. Automatyczne wykonywanie skryptów powinno być traktowane jako decyzja bezpieczeństwa.

Dla plików zaufanych, utrzymywanych we własnym repozytorium lub prywatnym workspace, można jawnie użyć `--enable-autoexec`. Dla nieznanych plików zewnętrznych używaj `--disable-autoexec`, dopóki ich zawartość nie zostanie sprawdzona.

## Windows

Sprawdzenie wersji:

```powershell
& "C:\Program Files\Blender Foundation\Blender 4.x\blender.exe" --version
```

Przykładowa walidacja bez interfejsu:

```powershell
& "C:\Program Files\Blender Foundation\Blender 4.x\blender.exe" `
  source\avatar_master.blend `
  --background `
  --python scripts\validate_scene.py
```

W Avatar Studio zapisuj rzeczywistą ścieżkę `blender.exe`. Nie zakładaj konkretnej wersji w `C:\Program Files`.

## Linux

Sprawdzenie:

```bash
blender --version
which blender
```

Przykład:

```bash
blender source/avatar_master.blend \
  --background \
  --python scripts/validate_scene.py
```

Jeżeli używasz wersji przenośnej, zapisz pełną ścieżkę do pliku wykonywalnego w konfiguracji Avatar Studio.

## Walidacja sceny przed eksportem

Minimalna walidacja powinna sprawdzać:

- jednostki i skalę;
- liczbę obiektów i siatek;
- obiekty ukryte przeznaczone przypadkowo do eksportu;
- geometrię niebędącą rozmaitością (non-manifold geometry), jeśli jest niedozwolona dla danego zasobu;
- brakujących materiałów i tekstur;
- duplikaty nazw kości;
- obecność wszystkich wymaganych kształtów deformacyjnych;
- zakres wag wpływu kości;
- nieużywane lub osierocone dane;
- modyfikatory, których eksporter nie potrafi zachować.

## Zapis wersji wzorcowej

Plik wzorcowy nie powinien być nadpisywany wynikiem automatycznej konwersji. Zalecany podział:

```text
source/
  avatar_master.blend
exports/
  unreal/
  unity/
  web/
reports/
  blender/
```

Każdy eksport ma być odtwarzalny z wersji wzorcowej i profilu eksportu.

## Definition of Done

Konfiguracja Blender jest zaliczona, jeśli:

- wersja programu jest przypięta i zapisana w raporcie;
- scena używa zatwierdzonej skali i osi;
- skrypty można uruchomić w trybie bez interfejsu;
- żaden etap automatyzacji nie zależy od lokalnej nazwy katalogu repozytorium;
- walidator sceny przechodzi dla wersji wzorcowej;
- eksport i ponowny import zachowują skalę, szkielet, kształty deformacyjne i materiały zgodnie z profilem docelowym.
