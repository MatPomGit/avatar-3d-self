# Spojrzenie i sakkady

System gaze steruje osobno oczami, głową i górną częścią tułowia. Celem nie jest utrzymywanie gałek ocznych dokładnie na jednym punkcie, lecz odtwarzanie fiksacji, sakkad i naturalnego przenoszenia uwagi.

## Kinematyka sakkady

Dla amplitudy `A` do 20° stosujemy:

`T_ms = clamp(25 + 2.5*A, 30, 90)`.

Interpolacja pozycji oka musi mieć profil minimum-jerk lub równoważny, z jednym maksimum prędkości. Liniowy lerp jest zabroniony dla widocznych sakkad.

Dla ruchów >20° zwiększamy udział głowy. Powyżej około 30° domyślnie planujemy najpierw sakkadę oka, a następnie głowę z opóźnieniem 70-140 ms, po czym oczy częściowo wracają ku środkowi oczodołu.

## Fiksacja

Neutralna fiksacja na obiekcie trwa zwykle 220-650 ms. W rozmowie fiksacja na obszarze twarzy może trwać 0.7-2.5 s. Cel nie jest jednym pikselem: co 0.7-1.7 s generujemy mikrokorektę 0.1-0.6° w obrębie semantycznego targetu.

## Mikrosakkady

Widoczne mikrosakkady generujemy z częstością 0.4-1.2 Hz. Nie należy dodawać niezależnego szumu klatka po klatce. Każdy mikroruch ma własny cel, początek i koniec.

## Rozdział oczu i głowy

- do 8°: głównie oczy;
- 8-20°: oczy + niewielki udział głowy;
- 20-35°: oczy inicjują ruch, głowa przejmuje znaczną część;
- >35°: głowa i tułów stają się głównym mechanizmem orientacji.

Współczynniki są miękko interpolowane, nie przełączane progowo.

## Eyelid follow

Górna powieka podąża za pionowym ruchem oka. Baseline 0.35, dla spojrzenia w dół do 0.45. Funkcja jest ograniczona tak, aby nie powodowała sztucznego szerokiego otwarcia oka.

## Konwersacja

Podczas mówienia nie utrzymujemy ciągłego eye contact. Krótkie gaze aversion trwa typowo 0.2-1.1 s. Powrót spojrzenia często może poprzedzać koniec wypowiedzi lub sygnalizować przekazanie tury.

## Walidacja

Nagrywamy widok z bliska przez 60 s. Kryteria: brak stałego wpatrywania, brak jitteru, sakkady o realistycznym czasie, współpraca powiek i oczu, brak widocznej rozbieżności osi oczu przy bliskim celu.