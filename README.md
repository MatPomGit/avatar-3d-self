[![CI](https://github.com/MatPomGit/avatar-studio/actions/workflows/validate_and_export.yml/badge.svg)](https://github.com/MatPomGit/avatar-studio/actions/workflows/validate_and_export.yml)
[![Documentation](https://github.com/MatPomGit/avatar-studio/actions/workflows/pages.yml/badge.svg)](https://matpomgit.github.io/avatar-studio/)
[![Pipeline contract](https://github.com/MatPomGit/avatar-studio/actions/workflows/avatar_complete_pipeline.yml/badge.svg)](https://github.com/MatPomGit/avatar-studio/actions/workflows/avatar_complete_pipeline.yml)

# Avatar Studio

**Avatar Studio** to otwarte, reprodukowalne środowisko do budowy fotorealistycznego cyfrowego człowieka czasu rzeczywistego. Projekt łączy kompletny pipeline produkcyjny, dokumentację techniczną, walidatory oraz aplikację desktopową prowadzącą użytkownika od materiałów referencyjnych aż do animowanego awatara mówiącego indywidualnym głosem Piper TTS.

Docelowym rezultatem nie jest pojedynczy statyczny model 3D, lecz edytowalna postać obejmująca ciało, dłonie, twarz, oczy, włosy, zarost, ubrania i okulary, z pełnym układem sterowania postacią (rig), mimiką zgodną z ARKit/FACS, warstwową animacją, synchronizacją ruchu ust z mową oraz integracją z silnikami czasu rzeczywistego.

**Dokumentacja:** https://matpomgit.github.io/avatar-studio/

**Repozytorium:** https://github.com/MatPomGit/avatar-studio

## Założenia projektu

Avatar Studio jest rozwijany według kilku nadrzędnych zasad:

- podobieństwo do osoby referencyjnej ma pierwszeństwo przed stylizacją i automatycznym „upiększaniem”;
- geometria, tekstury, rig, animacje i dane źródłowe pozostają rozdzielone i edytowalne;
- pipeline ma być możliwie otwarty, reprodukowalny i automatyzowalny;
- wszystkie kluczowe etapy mają jawne kryteria odbioru i raporty walidacyjne;
- decyzje dotyczące topologii, materiałów i rigu uwzględniają docelowe działanie w czasie rzeczywistym;
- podobieństwo twarzy, oczy, naturalna mimika, koartykulacja i synchronizacja głosu są traktowane jako krytyczne kryteria jakości;
- problemy prowadzące do efektu doliny niesamowitości są wykrywane i klasyfikowane zamiast maskowane stylizacją.

## Pipeline

Kanoniczny proces produkcyjny składa się z 21 etapów:

```text
01  pozyskiwanie referencji
02  fotogrametria
03  rekonstrukcja
04  czyszczenie siatki
05  retopologia
06  UV
07  materiały PBR
08  oczy
09  włosy i zarost
10  ubrania
11  okulary
12  rig ciała
13  rig dłoni
14  rig twarzy
15  ruch wtórny
16  wiązanie skóry z kośćmi
17  animacja
18  synchronizacja ruchu ust z mową
19  integracja Piper
20  eksport
21  walidacja czasu rzeczywistego
```

Każdy etap ma osobny rozdział w dokumentacji, zależności, oczekiwane artefakty i kryteria Definition of Done.

## Główne obszary techniczne

### Rekonstrukcja i modelowanie

Projekt obejmuje pozyskiwanie materiału zdjęciowego, kalibrację kamery, fotogrametrię, wariant osoby obracającej się przed nieruchomą kamerą, rekonstrukcję obiektocentryczną, retopologię oraz walidację anatomii i podobieństwa.

### Materiały i wygląd

Dokumentacja obejmuje przepływ PBR, przestrzenie barw, głębię bitową, system kafli tekstur UDIM, gęstość tekseli, skórę z rozpraszaniem podpowierzchniowym, oczy, włosy, zarost, ubrania i okulary.

### Rig i deformacja

Awatar ma pełny szkielet ciała, palce, oczy i twarz. Warstwa mimiki jest projektowana pod ARKit Blend Shapes i FACS, z kształtami korekcyjnymi, kontrolą asymetrii oraz testami deformacji barków, dłoni, żuchwy, ust i powiek.

### Animacja i zachowanie

System zakłada warstwową animację ciała, gestów, głowy, spojrzenia, mrugania, emocji i mowy. Uwzględniane są sakkady, mikrosakkady, ruch wtórny, oddychanie i naturalne zachowanie w stanie bezczynności.

### Piper TTS i mowa

Docelowy przepływ mowy:

```text
tekst
  ↓
Piper TTS
  ↓
audio WAV
  ↓
fonemy i znaczniki czasu
  ↓
wizemy
  ↓
koartykulacja
  ↓
animacja twarzy
```

Piper jest źródłem dźwięku, nie kontrolerem twarzy. Zmiana tekstu, modelu głosu lub parametrów syntezy unieważnia wcześniejsze znaczniki czasowe i wymaga ponownego przeliczenia animacji mowy.

### Runtime

Projekt dokumentuje eksport i walidację dla Unreal Engine, Unity oraz Web. Uwzględnia poziomy szczegółowości (Level of Detail, LOD), budżety wydajności, morph targets, włosy, tekstury i testy importu.

## Avatar Studio Desktop

Publiczna strona GitHub Pages jest dokumentacją. Interaktywne prowadzenie użytkownika przez pipeline odbywa się w lokalnej aplikacji **Avatar Studio** zbudowanej w Pythonie 3.11 i PySide6.

Aplikacja odpowiada za:

- prezentowanie 21 etapów pipeline'u i ich zależności;
- lokalny stan projektu w SQLite;
- rejestrację i inspekcję artefaktów;
- SHA-256 artefaktów i raportów;
- uruchamianie adapterów Blendera, COLMAP, FFmpeg i Piper;
- logi i diagnostykę narzędzi;
- walidację wyników oraz blokowanie etapów niespełniających kryteriów.

Kod aplikacji znajduje się w `apps/avatar_studio/`.

## Adaptery narzędzi

Avatar Studio posiada wspólną warstwę adapterów dla narzędzi stacji roboczej:

| Adapter | Rola |
| --- | --- |
| Blender | inspekcja sceny, geometria, UV, materiały, szkielet, shape keys i animacje |
| COLMAP | ekstrakcja cech, dopasowanie, rekonstrukcja rzadka i analiza modelu |
| FFmpeg | analiza i normalizacja audio |
| Piper | synteza WAV, pochodzenie modelu i dane fonemów |

Każde uruchomienie może być zapisane jako deterministyczny raport zawierający argumenty, kod zakończenia, wyjście programu i dane właściwe dla operacji.

## Dokumentacja

Dokumentacja jest budowana przez MkDocs Material i publikowana automatycznie przez GitHub Pages.

Najważniejsze sekcje:

- `docs/project/` - architektura, konwencje, terminologia i wartości bazowe;
- `docs/pipeline/` - pełny 21-etapowy pipeline;
- `docs/capture/` - pozyskiwanie materiału referencyjnego;
- `docs/modeling/` - anatomia, topologia i jama ustna;
- `docs/materials/` - PBR, UV, skóra, oczy, włosy, ubrania i okulary;
- `docs/rigging/` - ciało, dłonie, ARKit/FACS i skinning;
- `docs/animation/` - ruch, mimika, spojrzenie i zachowanie;
- `docs/speech/` - Piper, fonemy, wizemy i koartykulacja;
- `docs/runtime/` - Unreal Engine, Unity, Web, LOD i wydajność;
- `docs/validation/` - podobieństwo, deformacja, animacja twarzy i efekt doliny niesamowitości;
- `docs/tools/` - Blender, COLMAP, FFmpeg, Piper i konwersja formatów;
- `docs/desktop/` - architektura i obsługa aplikacji Avatar Studio.

Każdy publikowalny plik Markdown musi znajdować się w nawigacji `mkdocs.yml`. CI sprawdza to automatycznie.

## Struktura repozytorium

```text
avatar-studio/
├── apps/avatar_studio/        aplikacja desktopowa
├── config/                    wartości bazowe i reguły terminologii
├── docs/                      dokumentacja MkDocs
├── scripts/                   walidatory i narzędzia pipeline'u
├── tests/                     testy automatyczne
├── source/                    edytowalne artefakty źródłowe
├── references/                publiczne, niepoufne manifesty referencji
├── animations/                konfiguracje i dane animacji
├── exports/                   artefakty pochodne i raporty eksportu
├── mkdocs.yml                 struktura dokumentacji
└── pyproject.toml             konfiguracja pakietu Python
```

Prywatne zdjęcia, nagrania głosu, modele Piper i osobiste workspace nie powinny trafiać do publicznego repozytorium.

## Instalacja środowiska deweloperskiego

### Windows

```powershell
git clone https://github.com/MatPomGit/avatar-studio.git
cd avatar-studio
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,docs,desktop,geometry,vision]"
```

### Linux

```bash
git clone https://github.com/MatPomGit/avatar-studio.git
cd avatar-studio
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,docs,desktop,geometry,vision]"
```

## Uruchomienie aplikacji

Po aktywacji środowiska:

```bash
avatar-studio
```

Aplikacja tworzy lokalny stan projektu w katalogu `.avatar-studio/` wewnątrz wybranego workspace.

## Dokumentacja lokalna

```bash
mkdocs serve
```

Pełna walidacja dokumentacji:

```bash
mkdocs build --strict
python scripts/check_mkdocs_coverage.py
python scripts/lint_docs_terminology.py
```

## Testy

```bash
pytest -q
ruff check scripts tests apps/avatar_studio/src
```

CI obejmuje testy Python, walidację kontraktów pipeline'u oraz budowę dokumentacji.

## Dane maszynowo czytelne

Kluczowe wartości bazowe nie powinny być kopiowane ręcznie pomiędzy dokumentami. Ich kanonicznym źródłem jest:

```text
config/technical_baselines.yaml
```

Reguły terminologiczne znajdują się w:

```text
config/terminology.yaml
```

Dzięki temu dokumentacja, aplikacja i testy mogą korzystać z tych samych kontraktów.

## Prywatność danych

Projekt dotyczy danych biometrycznych i osobistych, dlatego publiczne repozytorium zawiera kod, dokumentację, schematy, konfiguracje techniczne i niepoufne przykłady, ale nie powinno zawierać:

- surowych zdjęć osoby referencyjnej;
- prywatnych nagrań głosu;
- danych treningowych Piper;
- indywidualnych modeli głosu;
- sekretów i tokenów;
- prywatnych baz SQLite projektu.

Szczegółowe zasady znajdują się w dokumentacji prywatności i danych referencyjnych.

## Status projektu

Warstwa dokumentacji bazowej obejmuje cały planowany pipeline produkcyjny. Implementacja Avatar Studio jest nadal rozwijana, szczególnie w obszarach automatyzacji narzędzi, podglądu wyników, raportowania, pakowania aplikacji i integracji demonstratora czasu rzeczywistego.

Aktualny stan i kolejne etapy są opisane w `docs/roadmap/roadmap.md`.

## Licencja

Kod i materiały objęte repozytorium są udostępniane na warunkach **Apache License 2.0**, zgodnie z plikiem `LICENSE`.
