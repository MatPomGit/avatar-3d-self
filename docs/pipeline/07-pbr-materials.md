# 07. Materiały PBR

**Input:** UV i high-poly/reference photography.  
**Editable output:** źródła tekstur oraz konfiguracja materiałów.  
**Derived output:** Base Color, Normal, Roughness, AO i opcjonalny Displacement/SSS masks.

## Windows

1. Bake'uj detale high-poly do zatwierdzonego low-poly.
2. Usuń oświetlenie z Base Color; cień nie jest albedo.
3. Odtwórz lokalny roughness skóry, ust, nosa i okolic oczu.
4. Skonfiguruj normal detail i SSS bez efektu wosku.
5. Testuj w neutralnym, frontalnym i bocznym świetle.

## Linux

1. Wygeneruj mapy z high-poly i referencji.
2. Oddziel kolor materiału od informacji o oświetleniu.
3. Zachowaj pory i mikrodetal bez przesadnego sharpeningu.
4. Dopasuj roughness i SSS do skali rzeczywistej.
5. Wykonaj render kontrolny w kilku warunkach oświetlenia.

## DoD

Skóra nie wygląda plastikowo ani woskowo, szwy UV nie dominują, normal map nie zawiera odwróconych kanałów, a wartości PBR są fizycznie sensowne.
