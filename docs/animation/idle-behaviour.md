# Zachowanie w bezczynności

Idle jest złożeniem oddychania, postural sway, mikroruchów głowy, oczu, blinków i okazjonalnych korekt pozy. Żadna warstwa nie może być prostą pętlą odtwarzaną bez zmian.

## Oddychanie

Baseline: 14 oddechów/min, czyli 0.233 Hz. Zakres neutralny 10-20/min. Jeden cykl ma około 42% wdechu i 58% wydechu. Okres jest modulowany o ±8%, amplituda o ±10%.

Ruch klatki: około 4 mm, zakres 2-8 mm. Rotacja barków wynikająca z oddechu: około 0.35°, zakres 0.1-0.8°.

## Postural sway

Wolny składnik: baseline 0.18 Hz, zakres 0.08-0.35 Hz. Translacja środka tułowia 1-10 mm, domyślnie 4 mm. Rotacja tułowia 0.1-0.7°, domyślnie 0.25°.

Sway nie może jednocześnie osiągać maksimum we wszystkich osiach. Używamy 2-3 wolnych składowych o różnych fazach albo filtrujemy niskoczęstotliwościowy szum.

## Mikroruchy

Czytelna korekta głowy: 0.3-2.0° w czasie 250-900 ms. W neutralnym idle generujemy 2-5 takich korekt na 10 s, zależnie od gaze targetów. Proceduralny jitter poniżej 0.1° jest usuwany.

## Zmiana ciężaru

Większa korekta pozycji może pojawić się średnio co 15-45 s. Powinna angażować miednicę, kolano, stopę i kompensację tułowia, a nie tylko przesunięcie root bone.

## Warstwowanie

Idle ma niższy priorytet od locomotion, gestów i świadomej mimiki. Podczas chodu pozostają tylko te składniki, które mają sens, np. gaze, blinking i część oddychania.

## Walidacja

Test 2 min bez mowy nie może ujawniać punktu zapętlenia. Ruch ma pozostać subtelny również po przyspieszeniu nagrania 4×, co ułatwia wykrycie periodyczności.