# Modeling

Modeling obejmuje rekonstrukcję, korektę anatomii, retopologię i przygotowanie geometrii do rigu. Celem nie jest wyłącznie poprawny wygląd w pozie neutralnej, lecz siatka, która zachowuje podobieństwo i deformuje się przewidywalnie.

## Zasady

- high-poly ze skanu jest źródłem informacji o kształcie, nie siatką produkcyjną;
- topologia produkcyjna musi być edytowalna i stabilna;
- po zatwierdzeniu retopologii obowiązuje topology freeze;
- oczy, zęby, język, włosy, zarost, ubrania i okulary pozostają osobnymi zasobami;
- zmiana proporcji po rozpoczęciu rigu wymaga ponownej walidacji deformacji.

## Kolejność

1. [Anatomia i proporcje](anatomy-and-proportions.md)
2. [Topologia](topology.md)
3. [Topologia twarzy](face-topology.md)
4. [Dłonie i stopy](hands-and-feet.md)
5. [Jama ustna](mouth-cavity.md)

Powiązane etapy wykonawcze znajdują się w sekcji [Production pipeline](../pipeline/overview.md).

## Mapa decyzyjna

| Decyzja | Odpowiedź |
| --- | --- |
| Wymagane wejście | Zatwierdzona rekonstrukcja lub skan, pomiary i referencje oraz jawna skala. |
| Kolejność lektury | [Anatomia i proporcje](anatomy-and-proportions.md) → [topologia](topology.md) → [twarz](face-topology.md) → [dłonie i stopy](hands-and-feet.md) → [jama ustna](mouth-cavity.md). |
| Rezultat | Edytowalny, retopologizowany bazowy mesh z osobnymi elementami pomocniczymi, gotowy do topology freeze. |
| Przejście dalej | Podobieństwo, skala, anatomia, przepływ pętli i podstawowe testy deformacji są zatwierdzone; topologia otrzymała status `approved`. |
| Gdy warunek nie jest spełniony | Nie rozpoczynaj UV ani rigu. Wróć do właściwego etapu 04–05 i użyj [diagnostyki geometrii](../validation/geometry.md). |
