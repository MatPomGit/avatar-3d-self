# Architektura

## Granice systemu

Repozytorium wspiera tworzenie edytowalnego awatara czasu rzeczywistego. Nie jest usługą sieciową i nie ma backendu ani bazy danych. GitHub Pages udostępnia wyłącznie statyczny viewer oraz publiczną dokumentację.

Cykl zasobu:

`prywatne referencje -> rekonstrukcja -> edytowalna scena DCC -> retopologia, UV, materiały i rig -> eksport -> pakiet środowiska docelowego`

Źródłowa scena DCC jest artefaktem kanonicznym. Eksporty nie zastępują źródeł.

## Odpowiedzialność katalogów

| Katalog | Zawartość |
| --- | --- |
| `references/` | manifesty i niesensitive metadane referencji |
| `source/` | opisy źródeł oraz zaakceptowane zasoby LFS |
| `scripts/` | narzędzia Python |
| `animations/` | konfiguracja i metadane animacji |
| `exports/` | eksporty oraz raporty |
| `web/viewer/` | publiczny viewer |
| `docs/` | dokumentacja i ADR |

## Standardy kodu i nazw

To jest jedyne źródło zasad nazewnictwa i stylu.

- Pliki, pakiety, funkcje, zmienne, testy oraz metadane używane przez pipeline Python zapisuj małymi literami w `snake_case`.
- Klasy używają `PascalCase`, a stałe `UPPER_CASE`.
- Dokumenty Markdown, katalogi ogólnych zasobów i statyczne zasoby WWW zapisuj małymi literami w `kebab-case`.
- Wyjątki stanowią nazwy konwencjonalne lub wymagane przez narzędzia, np. `README.md`, `pyproject.toml`, `package.json` i `App.jsx`.
- Nie zmieniaj nazw formatu, kości, API ani plików zewnętrznych tylko dla zgodności stylistycznej.
- Nowy i modyfikowany Python stosuje PEP 8 oraz PEP 257. Kod i docstringi są po angielsku, z prostymi nazwami opisującymi intencję.
- Stosuj KISS. Preferuj bezpośrednie rozwiązanie; abstrakcję, zależność lub konfigurację dodaj tylko dla zweryfikowanej potrzeby.

Uzasadnienie tej decyzji znajduje się w [ADR-0004](adr/0004-naming-and-python-style.md).

## Format i eksport

Przechowuj scenę DCC jako źródło. FBX stosuj dla sprawdzonych ścieżek riggingu w silnikach, GLB/glTF dla WWW, a USD/USDZ dopiero po walidacji w docelowym środowisku. Raport konwersji jest wymagany, gdy format może utracić rig, shape keys, animacje, materiały lub tekstury.

Skany źródłowe używają prawoskrętnego układu Z-up. Eksporty do Unreal Engine mają jednostki w centymetrach i są sprawdzane po imporcie.

## Środowiska

Python i GitHub Actions wykonują deterministyczne kontrole. Blender, COLMAP, MetaHuman, Unreal Engine oraz Piper są środowiskami lokalnymi. Ich konfiguracja, binaria i prywatne dane nie należą do zależności pakietu Python ani do publicznego viewera.
