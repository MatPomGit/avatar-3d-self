# Gesty

Gesty wspierają treść wypowiedzi, zamiast działać jako losowa dekoracja. Dobry
gest wygląda tak, jakby mówiący potrzebował go do przekazania myśli; zły sprawia
wrażenie ruchu uruchomionego tylko dlatego, że postać zbyt długo stała nieruchomo.
Znaczenie wynika zarówno z kształtu dłoni, jak i z czasu względem mowy.

## Kategorie i fazy

- gest deiktyczny (deictic gesture): wskazuje osobę, obiekt lub kierunek;
- gest ikoniczny (iconic gesture): odwzorowuje kształt, rozmiar lub ruch;
- gest rytmiczny (beat gesture): podkreśla rytm i akcent wypowiedzi;
- gest adaptacyjny (adaptive gesture): jest drobnym ruchem samoregulacyjnym lub
  spoczynkowym i nie powinien konkurować z przekazem.

Przed wyborem kategorii odpowiedz na proste pytanie: „Co odbiorca ma dzięki temu
ruchowi zrozumieć?”. Jeśli odpowiedź brzmi „gdzie?”, wybierz gest deiktyczny;
„jak to wygląda lub porusza się?” prowadzi do gestu ikonicznego, a „które słowo
jest najważniejsze?” — do rytmicznego. Jeśli ruch nie ma odpowiedzi na żadne z
tych pytań, prawdopodobnie nie jest potrzebny.

Każdy celowy gest dziel na **przygotowanie (preparation)**, które wyprowadza dłoń
z pozycji spoczynkowej; **uderzenie gestu (stroke)**, czyli czytelny moment
znaczeniowy; opcjonalne **zatrzymanie (hold)**; oraz **wycofanie (retraction)**,
które bezpiecznie przywraca dłoń lub prowadzi do następnego gestu. Te fazy można
porównać do wypowiadania zdania: preparation jest nabraniem oddechu, stroke —
ważnym słowem, hold — chwilą na jego zrozumienie, a retraction — spokojnym
domknięciem myśli. Pominięcie przygotowania daje nagły skok ręki, a pominięcie
wycofania pozostawia ją bez celu w powietrzu.

## Procedura projektowania gestu

### Wymagania wstępne i dane wejściowe

Przygotuj zatwierdzony szkielet (skeleton) i układ sterowania ciałem (body rig),
klip lokomocji lub bezczynności, nagranie wypowiedzi, transkrypcję z kodem
czasowym, oznaczone akcenty oraz obiekty i osoby, do których postać może się
odwołać. Ustal także docelową liczbę klatek na sekundę i przestrzeń dostępną dla
dłoni.

Nie zaczynaj od przeglądania biblioteki klipów. Najpierw ustal sens i czas gestu,
a dopiero później wybierz ruch, który je realizuje. W przeciwnym razie łatwo
dopasować wypowiedź do atrakcyjnej animacji zamiast animację do wypowiedzi.

### Kroki

1. **Przeanalizuj wypowiedź.** Przeczytaj całe zdanie, zaznacz nowe informacje,
   kontrasty, kierunki, wielkości i akcentowane sylaby. Usuń miejsca, w których
   ruch nie wnosi znaczenia albo koliduje z ważniejszym działaniem. Na pierwszym
   przejściu zaznaczaj intencję, nie konkretną pozę dłoni.
2. **Wybierz kategorię.** Dla konkretnego referenta wybierz gest deiktyczny, dla
   kształtu lub czynności — ikoniczny, a dla samego akcentu — rytmiczny. Gest
   adaptacyjny dodawaj oszczędnie wyłącznie w przerwach znaczeniowych.
3. **Wyznacz uderzenie.** Umieść najbardziej czytelną pozę lub zmianę kierunku
   uderzenia gestu na akcentowanej sylabie. Odsłuchaj nagranie, zamiast opierać
   synchronizację wyłącznie na początku wyrazu. Dłoń zwykle zaczyna podróż
   wcześniej, tak jak człowiek unosi rękę, zanim wypowie najważniejsze słowo.
4. **Wyznacz fazy.** Poprowadź przygotowanie przed akcentem, krótki hold tylko,
   gdy odbiorca musi odczytać kierunek lub kształt, i rozpocznij wycofanie po
   utracie znaczenia. Zapisz granice faz jako znaczniki na osi czasu.
5. **Skonfiguruj dłoń.** Ustaw nadgarstek i palce zgodnie z kategorią: przy
   wskazaniu wyprostuj właściwy palec, pozostałe ułóż naturalnie; w geście
   rytmicznym zachowaj luźną, stabilną konfigurację. Unikaj stale otwartej dłoni,
   przeprostów oraz identycznej konfiguracji obu rąk.
6. **Zsynchronizuj akcent.** Przesuwaj cały gest tak, aby stroke pokrywał się z
   akcentem, a nie dopiero po nim. Sprawdź synchronizację w normalnym tempie i na
   samej ścieżce audio; potem dopracuj krzywe bez przesuwania znacznika akcentu.
7. **Zmieszaj z lokomocją.** Zastosuj maskę animacji (animation mask) górnej
   części ciała i warstwę addytywną (additive layer), zachowując pracę miednicy,
   równowagę i przeciwfazę ramion. Stopniowo zwiększaj wpływ od kręgosłupa ku
   barkowi; podczas szybkiego ruchu zmniejsz amplitudę gestu zamiast blokować rękę.
8. **Skontroluj kolizje.** Sprawdź pełny tor łokcia, nadgarstka i palców względem
   tułowia, twarzy, drugiej ręki, ubrania i rekwizytów. Testuj skrajne klatki,
   przejścia oraz cały gest z lokomocją. Kolizję napraw przez zmianę łuku lub
   amplitudy, nie przez pojedyncze odsunięcie problematycznej klatki. Jedna
   poprawiona klatka może ukryć przecięcie w bezruchu, ale nie naprawi drogi,
   którą ręka pokonuje przed nią i po niej.
9. **Zróżnicuj i zatwierdź.** Unikaj idealnego powtarzania klipów i symetrycznych
   ruchów obu rąk. Obejrzyj wynik bez dźwięku dla czytelności oraz z dźwiękiem dla
   synchronizacji.

### Oczekiwany wynik, walidacja i odzyskiwanie

Wynikiem jest edytowalny klip z nazwanymi fazami, znacznikiem akcentu, warstwą
gestu i maską. Gest przechodzi walidację, gdy stroke jest czytelny i
zsynchronizowany, dłoń ma celową konfigurację, lokomocja zachowuje równowagę, a kończyny nie
przenikają geometrii. Gdy test nie przechodzi, wyłącz warstwę gestu, potwierdź
poprawność lokomocji, następnie włączaj kolejno tułów, ramię, przedramię i dłoń,
aby znaleźć błędną maskę lub fazę.

## Ćwiczenie: wskazanie i gest rytmiczny

Dla zdania „**Ten** panel pokazuje **trzy** wyniki” wykonaj dwa gesty:

1. Na słowie „Ten” zbuduj gest wskazujący: preparation rozpoczyna się przed
   słowem, stroke kieruje palec na panel, krótki hold potwierdza referent, a
   retraction prowadzi dłoń do neutralnej strefy przed tułowiem.
2. Na akcentowanej sylabie słowa „trzy” wykonaj jeden mały gest rytmiczny zmianą
   kierunku dłoni; zachowaj konfigurację palców zbliżoną do poprzedniej, ale nie
   sugeruj ponownego wskazania.
3. Połącz klipy nad cyklem chodu. Zamaskuj gest na górną część ciała, skoryguj
   amplitudę podczas podporu i sprawdź kolizje dłoni z tułowiem.
4. Obejrzyj całość z dźwiękiem, bez dźwięku i w widoku z boku. Zaliczenie wymaga
   jednoznacznego celu pierwszego gestu, zgodności drugiego z akcentem, pełnych
   czterech faz i braku kolizji.

## Redukcja zbyt częstych gestów

Jeżeli postać porusza rękami przy niemal każdym słowie, widz przestaje rozróżniać
ważne akcenty. Cisza ruchowa pełni tę samą funkcję co pauza w mowie: przygotowuje
miejsce dla następnego znaczącego gestu.

1. Oznacz każdy stroke na osi czasu i policz gesty w każdym zdaniu.
2. Nadaj im ważność: referent lub kontrast, akcent wspierający albo dekoracja.
3. Usuń dekoracje oraz gesty powtarzające tę samą informację.
4. Z sąsiednich gestów wybierz jeden silniejszy; połącz jego retraction z kolejnym
   preparation tylko wtedy, gdy oba gesty są znaczeniowo konieczne.
5. Wstaw okres neutralności po ważnym stroke i nie zastępuj usuniętego ruchu
   przypadkowym ruchem adaptacyjnym.
6. Ponownie odsłuchaj wypowiedź. Jeśli usunięcie gestu nie zmniejsza czytelności,
   pozostaw go usuniętym; jeśli zmniejsza, przywróć tylko stroke o mniejszej
   amplitudzie i ponownie sprawdź kolizje.
