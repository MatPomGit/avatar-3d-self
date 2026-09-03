# Animacja twarzy

Animacja twarzy (facial animation) łączy zatwierdzony układ sterowania postacią
(rig), kształty deformacyjne (blend shapes), emocje, artykulację mowy i
mikroruchy. Najłatwiej myśleć o niej jak o rozmowie kilku animatorów, którzy w
tej samej chwili próbują poruszyć ustami, policzkami i powiekami. Każdy z nich ma
ważne zadanie, ale bez wspólnych zasad ich ruchy zaczną się wzajemnie wzmacniać
albo kasować. Celem opisanej niżej konfiguracji jest zachowanie podobieństwa
postaci, czytelności wypowiedzi i ciągłości ruchu także wtedy, gdy kilka źródeł
steruje tym samym regionem.

## Model warstwowy

**Pozycja neutralna (neutral pose)** jest punktem odniesienia, w którym wszystkie
wartości addytywne wynoszą `0`, a twarz nie zawiera przypadkowej emocji ani
artykulacji. Nie służy do „wyzerowania” anatomii: naturalne napięcie powiek, warg
i policzków należy zachować w bazowym rigu. Każdy test rozpoczynaj i kończ w tej
samej pozycji neutralnej, aby wykryć dryf kontrolek. W praktyce jest to odpowiednik
punktu „zero” na linijce: bez niego nie wiadomo, czy lekki uśmiech pochodzi z
warstwy emocji, czy został przypadkiem zapisany w bazie.

**Warstwa animacji (animation layer)** grupuje ruch o jednej funkcji. Warstwy
pozwalają osobno poprawiać mowę, emocję lub mrugnięcie, a potem składać je bez
niszczenia animacji źródłowej. Można je porównać do ścieżek w programie audio:
każdą da się wyciszyć, wzmocnić i sprawdzić osobno, a widz słyszy — tutaj: widzi —
ich wspólny wynik. W Avatar Studio stosuj kolejno:

1. pozycję neutralną;
2. emocję i afekt;
3. artykulację mowy;
4. mrugnięcie (blink) i śledzenie powiek za ruchem oka (eyelid follow);
5. korekty związane ze spojrzeniem;
6. mikroasymetrię.

**Maska animacji (animation mask)** określa w zakresie `0–1`, jak silnie warstwa
wpływa na kontrolkę lub region: `0` blokuje wpływ, `0,5` przepuszcza połowę, a
`1` cały sygnał. **Priorytet (priority)** rozstrzyga konflikt znaczeniowy; wyższa
warstwa może przejąć kontrolkę lub zachować wymagany zakres dla ważniejszego
sygnału. Dla ust priorytet ma zwykle artykulacja, dla brwi emocja, a dla powiek
mrugnięcie. Priorytet nie oznacza automatycznie pełnego wyciszenia niższej
warstwy — decyzję zapisuje maska i reguła konfliktu. Maska odpowiada więc na
pytanie „gdzie i jak mocno?”, a priorytet na pytanie „kto ma ostatnie słowo?”.

**Ograniczanie zakresu (clamping)** utrzymuje wynik w zatwierdzonym zakresie
kontrolki. Typowy znormalizowany zakres to `0–1`, ale kontrolki dwukierunkowe
mogą używać `-1–1`; zawsze stosuj zakres z listy kontrolek. Brak ograniczenia
powoduje przesterowanie, a zbyt wąski zakres spłaszcza ekspresję. Ograniczenie
działa jak mechaniczny ogranicznik: pozwala kontrolce dojść do bezpiecznego końca,
ale nie przepuszcza jej dalej, nawet jeśli suma warstw żąda większej wartości.

**Krzywa przejścia (transition curve)** steruje tempem narastania i wygaszania
wpływu. Krzywa liniowa daje stałe tempo; krzywa z łagodnym wejściem i wyjściem
(ease-in/ease-out) ogranicza szarpnięcia, lecz ustawiona zbyt miękko opóźnia
spółgłoski. Dla artykulacji zaczynaj od krótkich, asymetrycznych przejść, a dla
emocji od dłuższych krzywych S. Unikaj skoku wagi `0 → 1` w jednej klatce, chyba
że testujesz celowo reakcję impulsową. Warto patrzeć nie tylko na dwie pozy
końcowe, lecz przede wszystkim na drogę między nimi — widz częściej zauważy
szarpnięcie w przejściu niż niewielką różnicę w pozie docelowej.

## Wymagania wejściowe

Przed rozpoczęciem przygotuj:

- zatwierdzony układ sterowania twarzą (facial rig) w edytowalnej scenie
  źródłowej, z poprawną pozycją neutralną i bez błędów deformacji;
- wersjonowaną listę kontrolek z nazwą, regionem, zakresem, wartością neutralną,
  kierunkiem działania oraz informacją, czy kontrolka jest addytywna;
- zatwierdzony zestaw kształtów deformacyjnych, w tym kształty korekcyjne dla
  kombinacji wymaganych przez rig;
- klipy testowe: neutralność, pełny zakres każdej kontrolki, zestaw fonemów lub
  wizemów, emocje o niskiej i wysokiej intensywności, mrugnięcia, ruch oczu oraz
  klip łączący mowę z emocją.

Te materiały odpowiadają na cztery różne pytania: czym można poruszać, jak daleko,
jak powinien wyglądać poprawny ruch oraz na czym go sprawdzić. Jeżeli brakuje
któregokolwiek wejścia, nie buduj warstw „na pamięć”. Wróć do właściciela rigu,
uzupełnij artefakt i ponownie zatwierdź jego wersję.

## Procedura budowy i rozstrzygania konfliktów

### Dane wejściowe

Użyj kopii roboczej zatwierdzonej sceny, listy kontrolek, zestawu kształtów
deformacyjnych i klipów testowych. Zanotuj wersje wszystkich czterech artefaktów.

### Kroki

1. **Sprawdź bazę.** Odtwórz pozycję neutralną przez co najmniej dwie sekundy.
   Potwierdź brak dryfu, asymetrii nieobecnej w projekcie postaci i ruchu po
   powrocie wszystkich warstw do wagi `0`. Jeśli twarz nie jest poprawna już na
   tym etapie, kolejne warstwy tylko ukryją problem i utrudnią jego znalezienie.
2. **Utwórz osobne warstwy.** Załóż sześć warstw w kolejności z modelu powyżej;
   nie wypalaj ich razem. Każdej nadaj identyfikowalną nazwę i domyślną wagę.
3. **Przypisz regiony.** Dla każdej kontrolki wpisz wpływ maski na: szczękę,
   wargi, policzki, nos, brwi, powieki i oczy. Zacznij od `0` i włączaj tylko
   regiony niezbędne danej funkcji. Takie podejście jest bezpieczniejsze niż
   rozpoczęcie od pełnego wpływu i późniejsze szukanie, co należy wyłączyć.
4. **Ustal priorytety.** W macierzy konfliktów zapisz dla każdej wspólnej
   kontrolki warstwę nadrzędną, zakres zarezerwowany i sposób mieszania:
   zastąpienie, suma addytywna albo redukcja niższego sygnału.
5. **Rozstrzygnij mowę kontra emocję.** Zachowaj dla mowy szczękę oraz wewnętrzny
   kontur warg. Emocja może sterować kącikami i policzkami, ale jej maskę redukuj
   w klatkach wymagających zwarcia lub pełnego otwarcia ust. Nie wyciszaj całych
   policzków, ponieważ wspierają zarówno artykulację, jak i afekt. Innymi słowy:
   postać może mówić z uśmiechem, ale uśmiech nie może „zakleić” głosek takich jak
   „m”, „b” i „p”.
6. **Dodaj ograniczenia.** Dla każdej kontrolki ustaw zakres zgodny z listą oraz,
   jeśli rig tego wymaga, wspólny limit par antagonistycznych. Sprawdź także
   kształty korekcyjne przy wartościach bliskich limitowi.
7. **Zaprojektuj przejścia.** Ustaw krzywe wejścia i wyjścia oddzielnie. Dopasuj
   szybkie zmiany do artykulacji i mrugnięć, a wolniejsze do emocji i spojrzenia;
   następnie skontroluj prędkość i ciągłość na wykresie krzywych.
8. **Zapisz kontrakt.** Wyeksportuj tabelę masek, priorytetów, limitów i reguł
   konfliktu razem ze sceną, nie tylko wynikowy klip.

### Przykład obliczenia kontrolki

Załóż, że `mouthSmileLeft` ma zakres `0–1`. Emocja proponuje `0,70` przy masce
`0,80`, a mowa o wyższym priorytecie proponuje `0,50` przy masce `1,00` i
rezerwuje 70% zakresu. Wyobraź sobie, że kontrolka ma do dyspozycji ograniczony
budżet ruchu: mowa dostaje pierwszeństwo, a emocja może wykorzystać tylko część,
która po tej rezerwacji została. Obliczenie wygląda następująco:

```text
speech = 0.50 × 1.00 = 0.50
emotion = 0.70 × 0.80 × (1.00 - 0.70) = 0.168
raw = speech + emotion = 0.668
final = clamp(raw, 0.00, 0.60) = 0.60
```

Końcowa wartość wynosi `0,60`: priorytet mowy osłabił emocję, maski przeskalowały
oba sygnały, a zatwierdzony limit klipu zatrzymał sumę. Jest to przykład reguły
produkcyjnej, nie uniwersalny algorytm; sposób rezerwacji zakresu musi być zapisany
w macierzy konfliktów. Najważniejsza nie jest konkretna liczba `0,60`, lecz to,
że da się prześledzić, skąd się wzięła i dlaczego żadna warstwa nie może jej
samodzielnie przekroczyć.

### Oczekiwany wynik i odzyskiwanie

Wynikiem jest edytowalny stos warstw oraz wersjonowana tabela przypisań. Jeżeli
pojawia się konflikt, wyłącz kolejno warstwy od najniższego priorytetu, znajdź
parę kontrolek powodującą błąd, popraw jej maskę, limit lub krzywą i ponownie
wykonaj pełny zestaw testów. Nie naprawiaj konfliktu przez wypalenie warstw.

## Testy

Testuj jak widz, a diagnozuj jak technik: najpierw obejrzyj twarz w normalnym
tempie i zapytaj, czy wygląda wiarygodnie, a dopiero potem użyj wykresów i
odtwarzania klatka po klatce, aby znaleźć przyczynę zauważonego problemu.

1. **Pojedyncze warstwy:** odtwórz każdą od neutralności do wartości niskiej,
   typowej i maksymalnej, a następnie z powrotem. Kontroluj zakres, regiony poza
   maską, asymetrię, deformację i powrót do zera.
2. **Kombinacje:** przetestuj każdą parę współdzielącą kontrolki, następnie mowę
   z emocją, mrugnięciem, spojrzeniem i mikroasymetrią. Powtórz test dla skrajnych
   wartości oraz obu stron twarzy.
3. **Przejścia:** sprawdź wejście, fazę stałą i wyjście w normalnym tempie, klatka
   po klatce oraz w spowolnieniu. Szukaj skoków wartości, zmiany pochodnej,
   opóźnionej artykulacji i niepełnego powrotu do neutralności.
4. **Runtime:** odtwórz klip przy docelowej liczbie klatek na sekundę i z szybko
   zmieniającymi się wagami. Porównaj wynik ze sceną źródłową.

## Typowe błędy

| Błąd | Typowa przyczyna | Naprawa |
| --- | --- | --- |
| Przesterowanie | Sumowanie warstw bez limitu albo równoczesne pełne wartości antagonistów. | Ustaw zakres kontrolki i wspólny limit grupy, zmniejsz maskę niższego priorytetu, sprawdź kształt korekcyjny. |
| Popping | Skok wagi, nieciągła krzywa, zmiana priorytetu bez przejścia lub próg aktywacji kształtu. | Wygładź styczne krzywej, dodaj krótkie przenikanie (crossfade) i usuń nieciągłość progu. |
| Zamrożone policzki | Maska mowy lub emocji całkowicie blokuje policzki. | Rozdziel górny i dolny policzek, pozostaw częściowy wpływ obu warstw i przetestuj spółgłoski z uśmiechem. |
| Utrata artykulacji | Emocja przejmuje szczękę albo kontur warg i zasłania zwarcia fonemów. | Nadaj mowie wyższy priorytet w krytycznych klatkach, zarezerwuj zakres i lokalnie obniż maskę emocji. |
| Nienaturalna symetria | Lustrzane wartości, identyczne czasy obu stron albo brak mikroasymetrii. | Zróżnicuj amplitudę i czas w granicach projektu postaci; asymetrii nie dodawaj do wymaganych symetrycznych zwarć. |

## Kryteria ukończenia

Etap jest ukończony wyłącznie wtedy, gdy:

- wszystkie wymagane wejścia mają zatwierdzoną i zapisaną wersję;
- każda kontrolka ma region, maskę, priorytet, zakres i regułę konfliktu;
- żadna warstwa nie zmienia kontrolek poza własną maską ani nie przekracza
  zatwierdzonego zakresu;
- wszystkie testy pojedyncze, kombinacyjne, przejść i runtime przechodzą bez
  przesterowania, poppingów, utraty artykulacji i dryfu pozy neutralnej;
- mowa pozostaje czytelna w klipie mowa–emocja, a emocja jest rozpoznawalna bez
  zamrożenia policzków;
- wynik w runtime odpowiada scenie źródłowej, a stos warstw i tabela reguł
  pozostają edytowalne i dołączone do raportu walidacji.
