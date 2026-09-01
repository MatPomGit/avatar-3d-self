# Cele i wymagania

## Priorytety jakości

1. Podobieństwo do osoby referencyjnej.
2. Fotorealizm bez automatycznego upiększania lub odmładzania.
3. Poprawna anatomia i topologia deformacyjna.
4. Naturalna mimika, oczy i mikroruchy.
5. Pełny rig ciała, dłoni i twarzy.
6. Wiarygodna integracja mowy z Piper.
7. Stabilna praca w czasie rzeczywistym.
8. Edytowalność, reprodukowalność i interoperacyjność.

## Wymagania funkcjonalne

Awatar musi zawierać pełne ciało, dłonie i palce, stopy, oczy, jamę ustną, zęby i język, włosy, zarost, ubrania i okulary. System animacji musi łączyć ciało, gesty, gaze, blinking, emocje, lip-sync i ruch spoczynkowy.

Facial rig powinien zapewniać mapowanie do ARKit blend shapes oraz udokumentowane powiązania z FACS. Sterowanie lewą i prawą stroną twarzy musi być możliwe niezależnie tam, gdzie odpowiada temu anatomia i standard.

## Wymagania niefunkcjonalne

- formaty i jednostki są jawnie zdefiniowane;
- każdy eksport posiada raport potencjalnej utraty danych;
- prywatne dane są oddzielone od publicznego kodu;
- wszystkie istotne decyzje architektoniczne mają ADR;
- dokumentacja buduje się deterministycznie;
- narzędzia CLI mają równorzędne instrukcje Windows i Linux;
- walidacja obejmuje kryteria wizualne i mierzalne.
