# Zasady dla współtwórców

## Zakres projektu

`avatar-3d-self` jest edytowalnym pipeline'em tworzenia fotorealistycznego awatara. Repozytorium zawiera lekkie narzędzia Python, dokumentację i statyczny viewer. Rekonstrukcja, Blender, MetaHuman, Unreal Engine oraz Piper działają lokalnie i nie są wykonywane w standardowym CI.

Priorytety jakości: podobieństwo do materiałów referencyjnych, anatomia i deformacje, naturalna mimika, wydajność czasu rzeczywistego.

## Zasady obowiązkowe

- Stosuj zasady nazewnictwa, PEP 8, PEP 257 i KISS opisane w `docs/architecture.md`.
- Kod, identyfikatory i docstringi zapisuj po angielsku. Dokumentację użytkową w Markdown zapisuj po polsku.
- Nie wprowadzaj frameworków, zależności ani warstw abstrakcji bez konkretnej potrzeby.
- Nowy lub zmieniony kod Python musi mieć czytelne nazwy, jawne importy i docstringi dla publicznych modułów, klas oraz funkcji.
- Dla zmian w Pythonie uruchom odpowiednie testy, `python -m pytest -q` oraz `ruff check scripts tests`.

## Dane i artefakty

- Zdjęcia, skany, nagrania głosu i adnotacje biometryczne są danymi wrażliwymi. Nie umieszczaj ich w publicznym repozytorium bez wyraźnej zgody.
- Duże, celowo wersjonowane zasoby używają Git LFS.
- Zachowuj osobno źródłową scenę DCC, retopologię, tekstury, rig i animacje. Eksport FBX lub GLB nie może być jedynym źródłem modelu.
- GitHub Pages zawiera wyłącznie publiczny, statyczny viewer i dokumentację.

## Zmiany

- Nie wypychaj zmian bezpośrednio do `main`.
- Zmiana granicy architektonicznej, formatu kanonicznego, zasad prywatności lub środowiska wykonawczego wymaga ADR.
- Formatów, nazw kości i plików wymaganych przez narzędzia nie zmieniaj bez migracji wszystkich referencji.
