# 01. Zbieranie referencji

**Input:** osoba referencyjna, aparat/telefon, miarka, kontrolowane światło.  
**Editable output:** prywatny zestaw zdjęć, pomiary, `capture_manifest.json`.  
**Derived output:** raport kompletności bez publikowania surowych danych.

## Kryteria techniczne

Zbierz osobno: geometrię neutralną, sylwetkę, dłonie, oczy, włosy i zarost, ubrania, okulary oraz ekspresje. Zachowaj stałą ogniskową i parametry w obrębie serii. Zapisz wzrost i wymiary pozwalające ustalić skalę.

Pełna procedura znajduje się w [Photography guide](../capture/photography-guide.md), [Expression capture](../capture/expression-capture.md) i [Measurements](../capture/measurements.md).

## Windows

1. Utwórz workspace poza repozytorium, np. `D:\Avatar3D\projects\self-avatar\capture`.
2. Skopiuj oryginały bez automatycznej kompresji.
3. Utwórz `face`, `body`, `hands`, `details`, `expressions`, `rejected`.
4. Wygeneruj i uzupełnij manifest.
5. Usuń z kopii publikacyjnych EXIF/GPS, jeżeli takie kopie mają powstać.

## Linux

1. Utwórz workspace poza repozytorium, np. `/home/<user>/Avatar3D/projects/self-avatar/capture`.
2. Skopiuj oryginały bez przetwarzania.
3. Utwórz `face`, `body`, `hands`, `details`, `expressions`, `rejected`.
4. Wygeneruj i uzupełnij manifest.
5. Usuń z kopii publikacyjnych EXIF/GPS, jeżeli takie kopie mają powstać.

## Failure conditions

Nieostrość, zmiana pozy w serii geometrycznej, zmienna ogniskowa, brak boków głowy/uszu, silne odbicia w okularach, automatyczne beauty filters albo nieznana skala blokują etap.

## Definition of Done

- kompletność zestawu potwierdzona;
- wszystkie serie mają manifest;
- istnieje co najmniej jeden znany wymiar skali;
- prywatne dane nie znajdują się w publicznym repozytorium.
