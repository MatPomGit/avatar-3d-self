# Unreal Engine

Unreal jest jednym z docelowych środowisk, ale wersja silnika i profil importu muszą być przypięte w raporcie projektu.

## Windows

1. Utwórz czysty projekt walidacyjny dla konkretnej wersji Unreal.
2. Zaimportuj skeletal mesh i sprawdź skalę w centymetrach.
3. Zweryfikuj skeleton hierarchy, normals/tangents, morph targets i material slots.
4. Skonfiguruj materiały skóry, oczu i włosów w rendererze Unreal.
5. Odtwórz acceptance clips i wykonaj profiling.

## Linux

1. Jeżeli dana wersja projektu jest wspierana na Linux, utwórz równoważny projekt walidacyjny.
2. Zaimportuj ten sam artefakt.
3. Porównaj skeleton, morphs i materiały.
4. Zwróć uwagę na różnice backendu renderera i groom support.
5. Zapisz oddzielny raport wydajności.

Nie uznawaj MetaHuman compatibility za automatyczną. Jeżeli pipeline użyje MetaHuman, mapping i ograniczenia zostaną zapisane w osobnym ADR.
