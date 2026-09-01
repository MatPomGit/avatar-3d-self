# Emocje

System emocji opisuje stan jako zestaw wymiarów i ekspresji FACS/ARKit, a nie jako sześć sztywnych presetów. Presety radości, smutku, złości, strachu, zaskoczenia i obrzydzenia są punktami startowymi.

## Intensywność

Wagi 0-1:

- 0.00-0.10: praktycznie neutralna;
- 0.10-0.30: subtelna ekspresja konwersacyjna;
- 0.30-0.55: czytelna emocja;
- 0.55-0.80: silna emocja;
- 0.80-1.00: apex używany oszczędnie.

Nie ustawiamy wszystkich składowych presetu na tę samą wartość.

## Dynamika

Baseline onset 250 ms, apex hold 700 ms, offset 450 ms. Dopuszczalne zakresy: onset 180-450 ms, hold 0.4-2.5 s, offset 0.3-1.2 s. Surprise może mieć szybszy onset 100-220 ms.

## Asymetria

Dla naturalnych ekspresji stosujemy 5-12% różnicy amplitudy pomiędzy stronami, utrzymywanej na poziomie grup mięśniowych. Losowanie niezależnej asymetrii każdego shape key powoduje szum i jest zabronione.

## Przykładowe grupy

Radość: `mouthSmile`, cheek raise/squint, niewielka zmiana powiek i brwi. Smutek: inner brow raise, mouth frown, subtelne uniesienie środka brody. Złość: brow down, napięcie powiek, lips press/funnel zależnie od kontekstu. Zaskoczenie: brow up, eye wide, jaw open. Obrzydzenie: nose sneer, upper lip raise, cheek tension.

## Mieszanie

Stan może mieszać dwie emocje, ale suma intensywności wysokopoziomowych nie powinna automatycznie mapować się liniowo na shape keys. Resolver usuwa konflikty, np. pełne `mouthSmile` i pełne `mouthFrown`.

## Mowa

Lip-sync ma pierwszeństwo dla geometrycznej artykulacji warg i żuchwy, ale emocja zachowuje wpływ na kąciki ust, policzki, powieki, brwi i timing ruchu. Mowa nie może zamrażać reszty twarzy.

## Walidacja

Każda emocja jest testowana na intensywności 0.2, 0.5 i 0.8 oraz w dwóch mieszankach. Kryterium: czytelność bez przesadnej symetrii i bez nagłych zmian shape keys.