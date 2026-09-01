# Animacja podczas mowy

Mówiący awatar nie może animować wyłącznie ust. Warstwa speech behavior łączy artykulację, twarz, gaze, blink, głowę, tułów i gesty.

## Warstwy

1. phoneme/viseme curves;
2. jaw and tongue;
3. emotional facial state;
4. gaze and conversational gaze aversion;
5. blinking;
6. head accents;
7. upper-body gestures;
8. breathing and remaining idle motion.

## Head accents

Dla zaakcentowanej frazy można dodać ruch głowy 0.5-2.5°, typowo 250-700 ms. Nie generujemy akcentu dla każdego słowa. Baseline to 0-3 czytelne head accents na 10 s ciągłej wypowiedzi.

## Gesty

Gesture stroke powinien przypadać w pobliżu akcentowanego semantycznie fragmentu, zwykle z tolerancją ±250 ms. Przy braku analizy semantycznej preferujemy rzadsze gesty zamiast losowych ruchów rąk.

## Gaze

Podczas mówienia postać może odwracać wzrok na 0.2-1.1 s, zwłaszcza przy planowaniu wypowiedzi. Powrót spojrzenia do rozmówcy może sygnalizować końcówkę frazy lub zmianę tury.

## Blink

Blink nie jest blokowany przez mowę. Generator może preferować granice fraz i sakkady, ale zachowuje losowość. Nie ustawiamy blinku na każdej pauzie.

## Oddychanie

Długi speech segment może modulować podstawowy cykl oddechowy. W uproszczonym runtime ograniczamy widoczny wdech w środku długiej frazy i pozwalamy na większy wdech w pauzie >350 ms.

## Priorytety

Artykulacja wygrywa konflikt w obrębie warg i żuchwy. Emocja zachowuje kąciki ust, policzki, brwi i powieki. Gesture layer nie może nadpisywać locomotion ani stabilizacji stóp.

## Walidacja

Test: co najmniej 60 s ciągłej mowy. Oceniane są synchronizacja, różnorodność spojrzenia, brak periodycznego blinku, brak mechanicznych head bobów i brak gestów niezwiązanych z rytmem wypowiedzi.