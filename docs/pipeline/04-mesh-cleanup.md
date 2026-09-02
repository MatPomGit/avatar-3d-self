# 04. Cleanup high-poly

**Input:** niezmieniony mesh rekonstrukcji z etapu 03.  
**Editable output:** `avatar_body_clean_vNNN.blend`.  
**Derived output:** raport naprawionych regionów i inspekcja sceny Blender.

## Cel etapu

Cleanup ma usunąć artefakty rekonstrukcji bez zmiany tożsamości osoby. Nie jest to retopologia ani upiększanie modelu. Zadaniem jest doprowadzenie high-poly do stanu, w którym może być wiarygodnym źródłem do retopologii i bake'u.

## Przygotowanie

1. Zachowaj oryginalny mesh COLMAP jako plik tylko do odczytu lub osobną kopię.
2. Utwórz nową scenę Blender i zaimportuj kopię skanu.
3. Ustaw jednostki i skalę zgodnie z pomiarami z etapu 03.
4. Dodaj fotografie referencyjne przodu, profilu i tyłu jako osobne referencje, nie jako teksturę maskującą błędy.
5. Zapisz scenę jako `avatar_body_clean_v001.blend`.

## Procedura krok po kroku

### 1. Usuń geometrię tła

Usuń podłogę, fragmenty ścian, statywu i odłączone chmury powierzchni. Zanim usuniesz fragment, sprawdź w kilku widokach, czy nie jest częścią włosów, ubrania albo ciała.

### 2. Sprawdź normals

Włącz wizualizację orientacji ścian. Odwrócone normals napraw lokalnie. Jeżeli bardzo duży region ma niespójne normals, najpierw sprawdź, czy geometria nie ma samoprzecięć lub zduplikowanych powierzchni.

### 3. Usuń oczywiste duble i samoprzecięcia

Szukaj cienkich podwójnych warstw powstałych przez rekonstrukcję dwóch bliskich powierzchni. Nie używaj globalnego merge-by-distance z dużym progiem, ponieważ może połączyć palce, wargi lub powieki.

### 4. Napraw małe dziury

Małe otwory techniczne można zamknąć lokalnie. Duże braki anatomiczne wymagają porównania z referencjami. Jeżeli brak obejmuje charakterystyczny fragment twarzy, ucha lub dłoni, preferuj ponowny capture albo ręczną rekonstrukcję na podstawie wielu zdjęć zamiast automatycznego fill.

### 5. Usuń artefakty skanu

Typowe artefakty:

- cienkie kolce;
- pływające wyspy;
- błony pomiędzy palcami;
- powierzchnie łączące rękę z tułowiem;
- sztuczne zamknięcia pod brodą;
- błędna geometria soczewek i refleksów okularów;
- nadmiernie napompowana geometria włosów.

Naprawiaj je regionami i regularnie porównuj z fotografiami.

### 6. Ogranicz smoothing

Smoothing może być użyty wyłącznie do usunięcia wysokoczęstotliwościowego szumu, którego nie potwierdzają zdjęcia. Nie wygładzaj globalnie nosa, ust, powiek, bruzd, asymetrii policzków ani charakterystycznych zmian powierzchni skóry.

### 7. Zachowaj asymetrię

Nie stosuj automatycznej symetryzacji twarzy lub ciała. Symetria techniczna może ułatwić modelowanie, ale obniżyć podobieństwo. Jeżeli późniejszy rig wymaga częściowo symetrycznej topologii, należy rozdzielić symetrię topologii od symetrii kształtu.

## Kontrola twarzy

Sprawdź osobno:

1. szerokość i wysokość nosa;
2. profil nosa;
3. relację górnej i dolnej wargi;
4. kąciki ust;
5. kształt żuchwy;
6. objętość policzków;
7. pozycję i głębokość oczodołów;
8. kształt uszu;
9. asymetrię lewej i prawej strony.

Każdą korektę twarzy oceniaj na tle co najmniej dwóch fotografii z różnych kątów.

## Kontrola dłoni i stóp

Dłonie są częstym źródłem błędów fotogrametrii. Sprawdź, czy każdy palec jest oddzielony, czy paznokcie nie tworzą przypadkowych występów oraz czy przestrzenie między palcami są otwarte. Analogicznie sprawdź palce stóp, piętę i łuk stopy.

## Inspekcja w Avatar Studio

Po zapisaniu sceny:

1. otwórz etap 04 w Avatar Studio;
2. wybierz **Run supported operation**;
3. wskaż `.blend`;
4. sprawdź raport liczby obiektów, geometrii, materiałów i jednostek;
5. zarejestruj właściwą scenę `.blend` jako artefakt etapu.

Raport techniczny nie ocenia podobieństwa. Ocena wizualna nadal jest obowiązkowa.

## Typowe błędy

### Twarz wygląda „ładniej”, ale mniej podobnie

Cofnij smoothing lub symetryzację. W Avatar Studio podobieństwo ma wyższy priorytet niż estetyczne uśrednienie rysów.

### Po merge znikają szczeliny między palcami

Próg operacji był zbyt duży. Cofnij zmianę i napraw region lokalnie.

### Po wypełnieniu dziury powstaje płaska powierzchnia

Automatyczny fill nie zna anatomii. Odtwórz powierzchnię ręcznie na podstawie referencji albo wróć do lepszego capture.

## Validation

Przed zakończeniem etapu sprawdź:

- brak odłączonego tła;
- brak oczywistych self-intersections w krytycznych regionach;
- poprawne normals;
- zachowanie charakterystycznych cech i asymetrii;
- brak agresywnego smoothingu;
- kompletność twarzy, dłoni i stóp wystarczającą do retopologii;
- poprawną skalę sceny.

## DoD

High-poly jest technicznie oczyszczony, zachowuje podobieństwo, ma udokumentowane naprawy i stanowi stabilne źródło do retopologii oraz bake'u. Jeżeli cleanup wymaga zgadywania dużych fragmentów anatomii, etap nie powinien zostać zaliczony bez jawnego waivera i planu ponownego pozyskania danych.
