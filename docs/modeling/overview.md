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