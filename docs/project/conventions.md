# Konwencje

## Nazewnictwo

- Python: `snake_case`, klasy `PascalCase`, stałe `UPPER_CASE`.
- Markdown i katalogi zasobów: `kebab-case`.
- Kości, blend shapes i nazwy wymagane przez zewnętrzne standardy zachowują ich kanoniczną pisownię.
- Pliki kolejnych wersji artefaktów używają jawnego numeru `vNNN`.

## Kod

Python 3.11, PEP 8 i PEP 257. Preferowane są małe moduły, jawne zależności i KISS. Adapter do zewnętrznego programu nie może mieszać logiki domenowej z parsowaniem UI.

## Dokumentacja procedur

Każda procedura zależna od systemu operacyjnego musi mieć osobne sekcje **Windows** i **Linux**. Nie używaj jednego bloku poleceń z komentarzem „na Windows zmień ścieżkę”.

Procedura techniczna powinna podawać kolejno: prerequisites, input, kroki, expected output, validation i recovery. Nie zastępuj polecenia ogólnym stwierdzeniem typu „skonfiguruj poprawnie”.
