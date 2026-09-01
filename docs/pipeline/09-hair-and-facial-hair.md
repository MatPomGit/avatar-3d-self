# 09. Włosy i zarost

**Input:** zdjęcia linii włosów, kierunku wzrostu, brody i wąsów.  
**Editable output:** groom, hair cards lub rozwiązanie hybrydowe.

## Windows

1. Odtwórz hairline przed zagęszczaniem fryzury.
2. Podziel włosy na guide regions zgodne z kierunkiem wzrostu.
3. Brodę i wąsy traktuj jako osobne groomy/warstwy.
4. Przygotuj runtime representation i LOD.
5. Dodaj dynamikę tylko tam, gdzie długość włosów ją uzasadnia.

## Linux

1. Zbuduj scalp/guides i sprawdź sylwetkę fryzury.
2. Dodaj density, clumping i variation w kontrolowany sposób.
3. Odtwórz zarost geometrycznie zamiast wyłącznie teksturą.
4. Wygeneruj cards lub zoptymalizowany groom dla target engine.
5. Przetestuj kolizje i ruch wtórny.

## DoD

Linia włosów i zarost zgadzają się z referencją, skóra nie prześwituje przypadkowo, LOD nie zmienia gwałtownie sylwetki i brak widocznego clippingu.
