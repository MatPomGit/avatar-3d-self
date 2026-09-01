# Dokumentacja

## Dokumenty główne

- [Architektura](architecture.md): granice systemu, artefakty i standardy pracy.
- [Roadmapa](roadmap.md): kolejne etapy oraz kryteria ukończenia.
- [Dziennik zmian](../CHANGELOG.md): historia zmian.
- [ADR](adr/README.md): podjęte decyzje architektoniczne.

## Pipeline i narzędzia

- [Pipeline produkcyjny](complete-pipeline.md)
- [Integracja z silnikami](engine-integration.md)
- [Przewodnik realizmu](realistic_avatar_guide.md)
- [Konwerter formatów modeli](model_format_converter.md)
- [Przykłady konwersji](format_conversion_examples.md)
 - [Poradnik fotografii do fotogrametrii](photogrammetry-capture-guide.md)

## Środowiska

| Środowisko | Zastosowanie |
| --- | --- |
| Python 3.11 | narzędzia, testy i walidacja statyczna |
| Blender | konwersja i kontrola geometrii, materiałów oraz rigu |
| COLMAP | rekonstrukcja ze zweryfikowanych zdjęć |
| Unreal i MetaHuman | import, animacja i pomiar wydajności |
| GitHub Pages | publiczna strona i viewer |
