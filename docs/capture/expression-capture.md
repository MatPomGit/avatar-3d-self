# Capture ekspresji

Expression capture jest materiałem do budowy i kontroli facial rigu. Nie zastępuje neutralnej fotogrametrii.

## Zestaw bazowy

Zarejestruj neutral, jaw open, lips closed/pressed, pucker, funnel, smile left/right, frown left/right, cheek puff, nose sneer, brow inner up, brow down left/right, brow outer up left/right, blink left/right, eye wide left/right oraz pełny zakres gaze.

Dodatkowo wykonaj naturalne ekspresje: radość, smutek, złość, strach, zaskoczenie, obrzydzenie i ekspresje mieszane. Są one potrzebne do oceny kombinacji shapes i asymetrii, a nie tylko do odtworzenia pojedynczych AUs.

## Windows

1. Utwórz katalog `capture\expressions\<expression_id>`.
2. Ustaw kamerę na statywie i zablokuj parametry.
3. Nagraj neutral przed każdą grupą ekspresji.
4. Wykonaj frontalny widok i dodatkowe 45° dla ruchów policzków/jaw.
5. Nazwij pliki zgodnie z manifestem, nie opisem potocznym.

## Linux

1. Utwórz `capture/expressions/<expression_id>`.
2. Zachowaj tę samą kamerę, światło i odległość.
3. Rejestruj neutral reference między seriami.
4. Dodaj widoki 45° tam, gdzie ruch ma istotny komponent głębokości.
5. Uzupełnij intensywność i stronę ekspresji w manifeście.

## Intensywność

Dla ważnych ruchów rejestruj co najmniej trzy poziomy: subtle, medium, maximum voluntary. Rig nie może być kalibrowany wyłącznie na maksymalnych grymasach.
