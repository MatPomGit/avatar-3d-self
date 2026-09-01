# Przegląd projektu

Avatar 3D Self rozwija kompletny cyfrowy odpowiednik człowieka, a nie pojedynczy statyczny model. Rezultatem ma być edytowalna postać czasu rzeczywistego ze spójną geometrią, PBR, włosami, ubraniami, pełnym riggingiem, mimiką, animacją i mową generowaną przez Piper.

## Granice produktu

Repozytorium ma trzy warstwy:

1. **Production assets and tooling**: skrypty, manifesty i edytowalne artefakty pipeline'u.
2. **Documentation**: statyczny portal MkDocs publikowany przez GitHub Pages.
3. **Avatar Studio**: lokalna aplikacja desktopowa prowadząca użytkownika przez pipeline i przechowująca jego stan.

Strona WWW nie odczytuje prywatnych zdjęć i nie jest panelem stanu projektu. Aplikacja desktopowa nie zastępuje DCC ani silnika, lecz orkiestruje proces, waliduje wyniki i dokumentuje postęp.

## Niezmienniki

- Kanonicznym źródłem modelu jest edytowalna scena DCC, nie FBX/GLB.
- Prywatne fotografie i nagrania nie trafiają do publicznego repozytorium.
- Każdy etap pozostawia jawny artefakt i raport walidacji.
- Zmiana topologii po rozpoczęciu riggingu jest zmianą łamiącą zależności i wymaga jawnej migracji.
- Wydajność runtime jest kryterium projektowym od początku, a nie końcową optymalizacją.
