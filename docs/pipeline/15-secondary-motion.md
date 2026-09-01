# 15. Ruch wtórny

**Input:** zatwierdzony rig podstawowy, włosy, ubrania i anatomia postaci.  
**Editable output:** secondary rigs/simulation settings.

## Windows

1. Dodaj dynamikę tylko elementom, których bezwładność jest widoczna.
2. Dla długich włosów użyj chains/groom dynamics z collision proxies.
3. Dla postaci kobiecej z piersiami przygotuj oddzielne, ograniczone secondary controls lewej i prawej piersi.
4. Ustaw małą amplitudę, damping i lag względem klatki piersiowej.
5. Zweryfikuj chód, bieg, skręt i nagłe zatrzymanie.

## Linux

1. Zdefiniuj te same dynamiczne regiony i collision proxies.
2. Długie włosy podziel na logiczne pasma/guide groups.
3. Jeśli anatomia tego wymaga, dodaj wtórny rig piersi z ograniczeniami i tłumieniem.
4. Dodaj tylko subtelne soft-tissue motion w innych obszarach, jeśli poprawia realizm.
5. Sprawdź deterministyczność lub bake tam, gdzie wymaga tego eksport.

## DoD

Ruch wtórny jest opóźniony względem ruchu głównego, subtelny i wolny od eksplozji symulacji, tunelowania i stałych penetracji.
