# Zasady dla współtwórców

## Zakres projektu

**Avatar Studio** jest profesjonalnym środowiskiem i edytowalnym pipeline'em tworzenia fotorealistycznego cyfrowego człowieka czasu rzeczywistego. Repozytorium zawiera narzędzia Python, dokumentację MkDocs i aplikację desktopową `avatar_studio`. Rekonstrukcja, Blender, COLMAP, Unreal Engine oraz Piper działają lokalnie i nie są wykonywane w standardowym CI.

Priorytety jakości: podobieństwo do materiałów referencyjnych, anatomia i deformacje, naturalna mimika, realistyczne oczy i skóra, wiarygodny lip-sync oraz wydajność czasu rzeczywistego.

## Zasady obowiązkowe

- Stosuj konwencje z `docs/project/conventions.md`, nazewnictwo z `docs/project/naming.md` oraz architekturę z `docs/project/architecture.md`.
- Kod, identyfikatory i docstringi zapisuj po angielsku. Dokumentację użytkową w Markdown zapisuj po polsku albo, dla stabilnych nazw standardów i API, zachowuj terminologię angielską.
- Procedury instalacyjne, polecenia CLI i ścieżki systemowe dokumentuj osobno dla Windows i Linux.
- Nie wprowadzaj frameworków ani warstw abstrakcji bez konkretnej potrzeby.
- Nowy lub zmieniony kod Python musi mieć czytelne nazwy, jawne importy i docstringi dla publicznych modułów, klas oraz funkcji.
- Dla zmian w Pythonie uruchom `python -m pytest -q` oraz `ruff check scripts apps tests`.
- Dla zmian dokumentacji uruchom `mkdocs build --strict`.

## Dane i artefakty

- Zdjęcia, skany, nagrania głosu i adnotacje biometryczne są danymi wrażliwymi. Nie umieszczaj ich w publicznym repozytorium bez wyraźnej zgody.
- Duże, celowo wersjonowane zasoby używają Git LFS. Prywatne źródła pozostają poza publicznym repozytorium.
- Zachowuj osobno źródłową scenę DCC, retopologię, tekstury, rig i animacje. Eksport FBX, GLB albo USD nie może być jedynym źródłem modelu.
- GitHub Pages zawiera wyłącznie publiczną dokumentację. Stan projektu i prywatne artefakty są obsługiwane lokalnie przez Avatar Studio.

## Zmiany

- Nie wypychaj zmian bezpośrednio do `main`.
- Zmiana granicy architektonicznej, formatu kanonicznego, zasad prywatności lub środowiska wykonawczego wymaga ADR.
- Formatów, nazw kości i plików wymaganych przez narzędzia nie zmieniaj bez migracji wszystkich referencji.
