# 11. Okulary

**Dane wejściowe (input):** zdjęcia referencyjne i wymiary rzeczywistych oprawek.  
**Edytowalny wynik (editable output):** osobna geometria oprawek i soczewek, materiały oraz profil mocowania.  
**Wynik pochodny (derived output):** wersje zoptymalizowane dla środowiska docelowego.

Szczegółową specyfikację materiałową i geometryczną zawiera dokument [Okulary](../materials/glasses.md).

## Cel etapu

Okulary mają zachować charakterystyczny kontur widoczny na twarzy, prawidłowe położenie względem oczu i nosa oraz fizycznie wiarygodne zachowanie soczewek. Nie traktujemy ich jako elementu przyklejonego do powierzchni twarzy.

## Procedura wspólna

1. Zmierz szerokość frontu, mostek, soczewki, długość zauszników i grubości oprawki.
2. Zbuduj oprawki i soczewki jako osobne elementy.
3. Dopasuj model do frontalnych i bocznych referencji twarzy.
4. Zwiąż transform okularów z kością głowy.
5. Sprawdź kontakt z nosem i uszami.
6. Zweryfikuj pełny zestaw ekspresji twarzy oraz mrugnięcie.
7. Skonfiguruj materiał soczewki dla środowiska docelowego.
8. Przygotuj poziomy szczegółowości bez zmiany charakterystycznego konturu.

## Windows

W Blenderze wykonaj model wzorcowy i test eksportu do docelowego formatu. Jeżeli docelowy renderer używa własnego modelu refrakcji, materiał źródłowy pozostaw neutralny, a konwersję wykonuj przez profil eksportu.

## Linux

Stosuj tę samą geometrię wzorcową i parametry materiałowe. Automatyczna walidacja może sprawdzać skalę, nazwy obiektów, obecność osobnej soczewki oraz brak przypadkowo zastosowanych transformacji.

## Definition of Done

Etap jest zaliczony, gdy:

- podstawowe wymiary zgadzają się z pomiarem w granicach około 1 mm;
- oprawki i soczewki są osobnymi obiektami;
- okulary pozostają stabilne przy ruchu głowy;
- rzęsy, brwi i policzki nie przenikają przez geometrię w typowych ekspresjach;
- materiał soczewki nie generuje nienaturalnie silnych refleksów;
- artefakt źródłowy pozostaje edytowalny.
